import brotlicffi as brotli  # Use brotlicffi instead of brotli
import os
from collections import defaultdict
from tabulate import tabulate  # Import tabulate for table formatting

def compress_with_brotli(data):
    """
    Compresses the given data using LZMA and returns the size of the compressed data.
    """
    compressed_data = brotli.compress(data.encode('utf-8'))
    return len(compressed_data)

def calculate_compression_difference(training_data, test_slice):
    """
    Calculates the compression difference for a test slice with a given training dataset.
    """
    combined_data = training_data + test_slice
    combined_size = compress_with_brotli(combined_data)
    training_size = compress_with_brotli(training_data)
    return combined_size - training_size

def classify_slices(training_data_map, test_slices):
    """
    Classifies each test slice to the best matching training dataset.
    """
    result_table = defaultdict(lambda: defaultdict(int))

    for test_author, slices in test_slices.items():
        for test_slice in slices:
            best_match = None
            smallest_difference = float('inf')

            for train_author, training_data in training_data_map.items():
                difference = calculate_compression_difference(training_data, test_slice)

                if difference < smallest_difference:
                    smallest_difference = difference
                    best_match = train_author

            result_table[test_author][best_match] += 1

    return result_table

def display_result_table(result_table):
    """
    Display the classification results in a tabular format using tabulate.
    """
    authors = list(result_table.keys())
    headers = [""] + authors  # First column is empty for row labels
    rows = []

    for test_author in authors:
        row = [test_author] + [result_table[test_author].get(train_author, 0) for train_author in authors]
        rows.append(row)

    print(tabulate(rows, headers=headers, tablefmt="grid"))

def load_text(file_path, size_in_kb):
    """
    Load a specific amount of text (in kilobytes) from a file.
    """
    if not os.path.exists(file_path):
        print(f"Error: File not found -> {file_path}")
        return ""

    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read(size_in_kb * 1024)  # Read size_in_kb KB
    except Exception as e:
        print(f"Error reading file {file_path}: {e}")
        return ""

def load_test_slices(file_path, num_slices=32, slice_size_kb=4):
    """
    Loads test slices from a file, splitting it into multiple parts.
    """
    text = load_text(file_path, num_slices * slice_size_kb)  # Load the full required text
    slice_size = slice_size_kb * 1024  # Convert KB to bytes
    return [text[i * slice_size:(i + 1) * slice_size] for i in range(num_slices) if i * slice_size < len(text)]

if __name__ == "__main__":
    # Paths to training and test files
    training_files = {
        "shotlay-Mamo-wednhe": r"C:\Users\USER\Documents\professor\second-year-second-semester-report\Amharic Novel\Test\shotelay-Mamo-wednhe.txt",
        "TSegaye-gebremden": r"C:\Users\USER\Documents\professor\second-year-second-semester-report\Amharic Novel\traning\TSegaye-gebremden.txt",
        "Romeoandjulit-michel-kebde": r"C:\Users\USER\Documents\professor\second-year-second-semester-report\Amharic Novel\traning\Romeoandjulit-michel-kebde.txt",
        "papiyo": r"C:\Users\USER\Documents\professor\second-year-second-semester-report\Amharic Novel\traning\papiyo-by natenail-getachew.txt",
        "book5": r"C:\Users\USER\Documents\professor\second-year-second-semester-report\Amharic Novel\traning\book5.txt",
        "book6": r"C:\Users\USER\Documents\professor\second-year-second-semester-report\Amharic Novel\traning\book6.txt",
        "book7": r"C:\Users\USER\Documents\professor\second-year-second-semester-report\Amharic Novel\traning\book7.txt"

    }
    test_files = {
        "shotlay-Mamo-wednhe": r"C:\Users\USER\Documents\professor\second-year-second-semester-report\Amharic Novel\Test\shotelay-Mamo-wednhe.txt",
        "Romeoandjulit-michel-kebde": r"C:\Users\USER\Documents\professor\second-year-second-semester-report\Amharic Novel\Test\Romeoandjulit-michel-kebde.txt",
        "TSegaye-gebremden": r"C:\Users\USER\Documents\professor\second-year-second-semester-report\Amharic Novel\Test\TSegaye-gebremden.txt",
        "papiyo": r"C:\Users\USER\Documents\professor\second-year-second-semester-report\Amharic Novel\Test\papiyo-by natenail-getachew.txt",
        "book5": r"C:\Users\USER\Documents\professor\second-year-second-semester-report\Amharic Novel\Test\book5.txt",
        "book6": r"C:\Users\USER\Documents\professor\second-year-second-semester-report\Amharic Novel\Test\book6.txt",
        "book7": r"C:\Users\USER\Documents\professor\second-year-second-semester-report\Amharic Novel\Test\book7.txt"
    }

    # Load training data (64 kB per author)
    training_data_map = {
        author: load_text(file_path, 128) for author, file_path in training_files.items()
    }

    # Load test slices (16 slices per file, 4 kB each)
    test_slices = {
        author: load_test_slices(file_path, num_slices=32, slice_size_kb=4) for author, file_path in test_files.items()
    }

    # Classify the test slices
    result_table = classify_slices(training_data_map, test_slices)

    # Display results as a table
    print("\nClassification Results:")
    display_result_table(result_table)
