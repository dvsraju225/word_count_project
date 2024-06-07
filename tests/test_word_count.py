import unittest
from unittest.mock import patch, mock_open
import pandas as pd
import json
from src.word_count import process_json, save_to_csv

# Sample JSON data for testing
sample_json = json.dumps([
    {"abstract__value": "This is a test. This test is only a test."},
    {"abstract__value": "Another test text with some test words and some longer words."}
])

class TestWordCount(unittest.TestCase):

    @patch("builtins.open", new_callable=mock_open, read_data=sample_json)
    def test_process_json(self, mock_file):
        # Mock the file path
        file_path = 'dummy_path.json'

        # Process the JSON data
        df = process_json(file_path)

        # Check if the DataFrame is not empty
        self.assertFalse(df.empty, "The DataFrame should not be empty.")

        # Check if the DataFrame has the expected columns
        expected_columns = ['unique_id', 'another', 'words', 'longer']
        self.assertTrue(all(col in df.columns for col in expected_columns), "Missing expected columns.")

        # Check the word frequencies
        expected_freq = {'another': 1, 'words': 2, 'longer': 1}
        actual_freq = df.set_index('unique_id').to_dict(orient='index')
        actual_combined_freq = {k: sum(d[k] for d in actual_freq.values()) for k in expected_freq}
        self.assertDictEqual(actual_combined_freq, expected_freq, "The word frequencies do not match the expected values.")

    @patch("pandas.DataFrame.to_csv")
    def test_save_to_csv(self, mock_to_csv):
        # Create a sample DataFrame
        data = {'unique_id': [1, 2], 'another': [1, 0], 'words': [1, 1], 'longer': [0, 1]}
        df = pd.DataFrame(data)

        # Mock the output file path
        output_path = 'dummy_output.csv'

        # Save the DataFrame to CSV
        save_to_csv(df, output_path)

        # Assert that to_csv was called with the correct parameters
        mock_to_csv.assert_called_once_with(output_path, index=False)

if __name__ == "__main__":
    unittest.main()
