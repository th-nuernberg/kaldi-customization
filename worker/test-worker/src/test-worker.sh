echo "----------------------------------------------------------------------"
echo "Testing-worker is running!"
echo "----------------------------------------------------------------------"


# Step 1: Create all necessary buckets and upload all needed files into their corresponding buckets
echo "----------------------------------------------------------------------"
echo "Starting to create all needed buckets and upload all needed files."
python3 buckets_and_uploads.py $1 $2 $3 $4 $5
echo "Creation of all needed buckets and uploading finished successfully."
echo "----------------------------------------------------------------------"

# Step 2: Setup all test cases for the text-preparation-worker and execute these test cases
echo ""
python3 test_text_preparation.py $1 $2 $3 $4 $5
echo "----------------------------------------------------------------------"

# Step 3: Evaluate the test results
echo ""
echo "Test evaluation not implemented yet"
echo ""
echo "----------------------------------------------------------------------"

# Step 4: Setup all test cases for the data-preparation-worker and execute these test cases
echo ""
python3 test_data_preparation.py $1 $2 $3 $4 $5
echo ""
echo "----------------------------------------------------------------------"

# Step 5: Evaluate the test results
echo ""
echo "Test evaluation not implemented yet"
echo ""
echo "----------------------------------------------------------------------"

# Step 6: Setup all test cases for the kaldi-worker and execute these test cases
echo ""
echo "Python call not implemented yet"
echo ""
echo "----------------------------------------------------------------------"

# Step 7: Evaluate the test results
echo ""
echo "Test evaluation not implemented yet"
echo ""
echo "----------------------------------------------------------------------"

# Step 8: Setup all test cases for the decode-worker and execute these test cases
echo ""
echo "Python call not implemented yet"
echo ""
echo "----------------------------------------------------------------------"

# Step 9: Evaluate the test results
echo ""
echo "Test evaluation not implemented yet"
echo ""
echo "----------------------------------------------------------------------"

# Step 10: Evaluate all results. 
#          If all tests were successfully executed --> exit 0
#          Else --> print which test cases failed
echo ""
echo "General evaluation not implemented yet"
echo ""
echo "----------------------------------------------------------------------"