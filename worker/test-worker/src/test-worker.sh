echo "###############################################################################################"
echo "Testing-worker is running!"
echo "###############################################################################################"

###################################################################################################
#                                                                                                 #
# Parameter description:                                                                          #
#   $1 == redis                                                                                   #
#   $2 == ${REDIS_PASSWORD}                                                                       #
#   $3 == minio                                                                                   #
#   $4 == ${MINIO_ACCESS_KEY}                                                                     #
#   $5 == ${MINIO_SECRET_KEY}                                                                     #
#                                                                                                 #
###################################################################################################

# Step 1: Create all necessary buckets and upload all needed files into their corresponding buckets
echo ""
echo "Starting to create all needed buckets and upload all needed files."
python3 -u buckets_and_uploads.py $1 $2 $3 $4 $5

bucket_and_upload_result=$?
if [ $bucket_and_upload_result -eq 200 ]
then
    echo "All needed buckets were created successfully."
    echo "All needed files were uploaded successfully."
    echo "###############################################################################################"
elif [ $bucket_and_upload_result -eq 400 ]
then
    echo "No bucket was created and no file was uploaded, because it was not possible to establish a connection with the MinIO-server."
else
    echo "During the setup of all buckets and their uploads, at least one file upload failed."
    echo "######################################################################"

    category=$((bucket_and_upload_result / 100))
    upload=$((bucket_and_upload_result % 100))

    if [ $category -eq 0 ]
    then
        echo "The error occured within the following function: upload_all_text_prep_files"
        echo "The following upload failed: $upload"
    elif [ $category -eq 1 ]
    then
        echo "The error occured within the following function: upload_all_remaining_files"
        echo "The following upload failed: $upload"
    fi
fi

# Step 2: Setup all test cases for the text-preparation-worker and execute these test cases
echo "Test 1 is now executed! It is tested whether the text-prep-worker recogizes an unsupported file type"
python3 -u text-preparation-tests/test_not_supported_file_types.py $1 $2 $3 $4 $5
not_supported_files_result=$?

if [ $not_supported_files_result -eq 0 ]
then
    echo "The test case was successfully executed. The text-prep-worker recognized that the file type of the task was not supported!"
else
    echo "The text-prep-worker did not recognize that the received file type is not supported!"
fi
echo "###############################################################################################"

echo "Test 2 is now executed! It is tested whether all supported file types are correctly processed!"
python3 -u text-preparation-tests/test_supported_file_types.py $1 $2 $3 $4 $5
supported_files_result=$?

if [ $supported_files_result -eq 0 ]
then
    echo "Tests for all supported file types were executed successfully!"
else
    echo "At least one of the executed test cases failed. Therefore, the text-prep-worker does not process all supported file types correctly!"
fi
echo "###############################################################################################"

echo "Test 3 is now executed! It is tested whether the text-prep-worker recogizes a correct task"
python3 -u text-preparation-tests/test_correct_json.py $1 $2 $3 $4 $5
correct_json_result=$?

if [ $correct_json_result -eq 0 ]
then
    echo "The test case was successfully executed. The text-prep-worker recognized that the structure of the received task was correct!"
else
    echo "The text-prep-worker falsely recognized the structure of the received task as wrong!"
fi
echo "###############################################################################################"

# Step 3: Copying all files from the RESOURCE-bucket to the TRAINING_RESOURCE-bucket
echo ""
python3 -u copy_text_preparation_results.py $3 $4 $5
echo "###############################################################################################"

# Step 4: Setup all test cases for the data-preparation-worker and execute these test cases
echo "Test 4 is now executed: It is tested whether the data-prep-worker processes a valid task correctly"
python3 -u data-preparation-tests/test_data_preparation.py $1 $2 $3 $4 $5
data_preparation_result=$?

if [ $data_preparation_result -eq 0 ]
then
    echo "The test case was successfully executed. The data-preparation-worker correctly processed a valid task!"
else
    echo "The test case failed. The data-preparation-worker failed at processing a valid task!"
fi
echo "###############################################################################################"

# Step 5: Setup all test cases for the kaldi-worker and execute these test cases
echo "Test 5 is now executed: It is tested whether the kaldi-worker processes a valid task correctly"
python3 -u kaldi-tests/test_kaldi_worker.py $1 $2 $3 $4 $5
kaldi_test_result=$?

if [ $kaldi_test_result -eq 0 ]
then
    echo "The test case was successfully executed. The kaldi-worker correctly processed a valid task!"
else
    echo "The test case failed. The kaldi-worker failed at processing a valid task!"
fi
echo "###############################################################################################"

# Step 6: Setup all test cases for the decode-worker and execute these test cases
echo "Test 6 is now executed: It is tested whether the decode-worker processes a valid task correctly"
python3 -u decode-tests/test_decode_worker.py $1 $2 $3 $4 $5
decode_test_result=$?

if [ $decode_test_result -eq 0 ]
then
    echo "The test case was successfully executed. The decode-worker correctly processed a valid task!"
else
    echo "The test case failed. The decode-worker failed at processing a valid task!"
fi

# Step 7: Evaluate all results. 
echo "###############################################################################################"
echo "Summary of all executed test cases:"
echo "###############################################################################################"

echo "Test case 1: Does the text-prep-worker recogizes an unsupported file type?"
echo "Expected exit code for success:          0"
echo "Exit code after executing the test case: $not_supported_files_result"

echo "Test case 2: Does the text-prep-worker recognize all supported file types?"
echo "Expected exit code for success:          0"
echo "Exit code after executing the test case: $supported_files_result"

echo "Test case 3: Does the text-prep-worker recogizes a correct task?"
echo "Expected exit code for success:          0"
echo "Exit code after executing the test case: $correct_json_result"

echo "Test case 4: Does the data-prep-worker process a valid task correctly?"
echo "Expected exit code for success:          0"
echo "Exit code after executing the test case: $data_preparation_result"

echo "Test case 5: Does the kaldi-worker process a valid task correctly?"
echo "Expected exit code for success:          0"
echo "Exit code after executing the test case: $kaldi_test_result"

echo "Test case 6: Does the decode-worker process a valid task correctly?"
echo "Expected exit code for success:          0"
echo "Exit code after executing the test case: $decode_test_result"

echo "###############################################################################################"
exit_code=0
if [[ $not_supported_files_result -eq 0 && \
     $supported_files_result -eq 0 && \
     $correct_json_result -eq 0 && \
     $data_preparation_result -eq 0 && \
     $kaldi_test_result -eq 0 && \
     $decode_test_result -eq 0 ]]
then
    echo "All test cases were executed successfully! Test-worker terminates with exit code 0!"
else
    echo "At least one test case failed. Test-Worker terminated with exit code -1!"
    $exit_code=-1
fi
echo "###############################################################################################"
exit $exit_code
