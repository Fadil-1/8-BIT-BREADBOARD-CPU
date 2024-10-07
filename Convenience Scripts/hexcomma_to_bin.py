import argparse

def hex_to_bin_file(input_filename, output_filename):
    with open(input_filename, 'r') as input_file:
        hex_data = input_file.read()
    
    # Remove spaces and newline
    hex_data = hex_data.replace(" ", "").replace("\n", "")
    
    # Then split hexs into a list of values
    hex_values = hex_data.split(',')
    
    # Convert hex values to bytes and write to a binary file
    with open(output_filename, 'wb') as output_file:
        for hex_value in hex_values:
            # Convert hex strings (ex "0x00") to bytes and writing to the binary file
            byte = int(hex_value, 16)
            output_file.write(byte.to_bytes(1, 'big'))

def main():
    parser = argparse.ArgumentParser(description="Convert a hex comma-separated file to a binary (.bin) file.")
    parser.add_argument("input", help="Input ASCII file with hex values.")
    parser.add_argument("output", help="Output binary file.")
    
    args = parser.parse_args()
    hex_to_bin_file(args.input, args.output)
    
    print(f"Conversion complete. Binary file saved as {args.output}.")

if __name__ == "__main__":
    main()
