def remove_up_to_element(file_path, index):
    with open(file_path, "r") as file:
        content = file.read()

    # Splits the content by commas and find the position of the element
    content = content.split(",")
    try:
        # Removes elements up to and including the specified element
        modified_content = ",".join(content[index :])

    except ValueError:
        print(f"Element {index} not found in the file.")
        return

    # Writes the modified content back to the file
    with open(file_path, "w") as file:
        file.write(modified_content)

file_path = "./ASM/16-bit_bounce/16-bit_bounce_copy.txt"
remove_up_to_element(file_path, 0xC000)
