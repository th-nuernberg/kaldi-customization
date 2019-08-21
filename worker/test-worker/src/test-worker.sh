echo "----------------------------------------------------------------------"
echo "Testing-worker is running!"
echo "----------------------------------------------------------------------"


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
echo "----------------------------------------------------------------------"
echo "Starting to create all needed buckets and upload all needed files."
python3 -u buckets_and_uploads.py $1 $2 $3 $4 $5
echo "Creation of all needed buckets and uploading finished successfully."
echo "----------------------------------------------------------------------"

# Step 2.1: Setup all test cases for the text-preparation-worker and execute these test cases
echo ""
python3 -u test_text_preparation.py $1 $2 $3 $4 $5
echo "----------------------------------------------------------------------"

# Step 2.2: Copying all files from the RESOURCE-bucket to the TRAINING_RESOURCE-bucket
echo ""
python3 -u copy_text_preparation_results.py $3 $4 $5
echo "----------------------------------------------------------------------"

# Step 3: Evaluate the test results
echo ""
echo "Text-Preparation-Worker test evaluation not implemented yet."
echo ""
echo "----------------------------------------------------------------------"

# Step 4: Setup all test cases for the data-preparation-worker and execute these test cases
echo ""
python3 -u test_data_preparation.py $1 $2 $3 $4 $5
echo ""
echo "----------------------------------------------------------------------"

# Step 5: Evaluate the test results
echo ""
echo "Data-Preparation-Worker test evaluation not implemented yet"
echo ""
echo "----------------------------------------------------------------------"

# Step 6: Setup all test cases for the kaldi-worker and execute these test cases
echo ""
python3 -u test_kaldi_worker.py $1 $2 $3 $4 $5
echo ""
echo "----------------------------------------------------------------------"

# Step 7: Evaluate the test results
echo ""
echo "Kaldi-Worker test evaluation not implemented yet"
echo ""
echo "----------------------------------------------------------------------"

# Step 8: Setup all test cases for the decode-worker and execute these test cases
echo ""
python3 -u test_decode_worker.py $1 $2 $3 $4 $5
echo ""
echo "----------------------------------------------------------------------"

# Step 9: Evaluate the test results
echo ""
echo "Decode-Worker test evaluation not implemented yet"
echo ""
echo "----------------------------------------------------------------------"

# Step 10: Evaluate all results. 
#          If all tests were successfully executed --> exit 0
#          Else --> print which test cases failed
echo ""
echo "General evaluation not implemented yet"
echo ""
echo "----------------------------------------------------------------------"

echo "All tests finished successfully. Exiting with code 0"
exit 0