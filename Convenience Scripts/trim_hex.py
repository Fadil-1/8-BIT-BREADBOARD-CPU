def remove_up_to_element(file_path, index):
    with open(file_path, 'r') as file:
        content = file.read()
    # Split the content by commas
    content = content.split(',')
    
    try:
        # Remove elements up to and including the specified element
        # Strip any leading/trailing spaces or newlines from the modified content
        modified_content = ','.join(content[index:]).strip()

    except ValueError:
        print(f"Element {index} not found in the file.")
        return

    # Write the modified content back to the file
    with open(file_path, 'w') as file:
        file.write(modified_content)

file_path = '...'
remove_up_to_element(file_path, 0xC000)
