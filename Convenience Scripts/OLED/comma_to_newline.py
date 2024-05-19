def process_and_write_data(input_file_path, output_file_path, start="", end=""):
    # Read the input data from the file
    with open(input_file_path, 'r') as file:
        input_data = file.read().strip()  # Read and strip trailing newlines
    
    # Splits the input data by commas and writes each item on a new line in the output file
    with open(output_file_path, 'w') as file:
        for item in input_data.split(','):
            file.write(f"{start}{item}{end}\n")  # Write each item on a new line

# Define file paths
input_file_path = "./cropped_images/cropped_550_KHz_binary_hex.txt"
output_file_path = "./550_KHz.txt"  # Output file path

# Process and write the data
process_and_write_data(input_file_path, output_file_path, start="\tOLD ")

