def format_instructions_from_file(input_file_path, output_file_path):
    # Reads the text file
    with open(input_file_path, 'r') as file:
        instructions = file.read().strip().split("\n\n")

    # Initializes formatted output
    formatted_output = ""

    # Processes each instruction set
    for instruction in instructions:
        lines = instruction.split("\n")
        identifier = lines[0].strip()
        formatted_output += f"{identifier}\n\n"
        formatted_output += "| Microsteps | Control Word |\n|------------|--------------|\n"
        for line in lines[1:]:
            microstep, control_word = line.split(": ")
            formatted_output += f"| {microstep}| {control_word} |\n"
        formatted_output += "\n"

    # Write the formatted output to the new file
    with open(output_file_path, 'w') as file:
        file.write(formatted_output.strip())

    return "Output written to file successfully."

input_file_path = 'instructionss.txt'
output_file_path = 'output.txt'

# Calls the function and stores the result
result = format_instructions_from_file(input_file_path, output_file_path)

#print(result)