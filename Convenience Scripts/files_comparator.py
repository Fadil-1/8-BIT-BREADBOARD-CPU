def are_files_identical(file1_path, file2_path):
    try:
        with open(file1_path, "rb") as file1, open(file2_path, "rb") as file2:
            file1_contents = file1.read()
            file2_contents = file2.read()

            return True if file1_contents == file2_contents else print("The files are not identical")
    
    except IOError as e:
        print(f"An I/O error occurred: {e.strerror}")
        return False


file1 = r"./1_compar.bin"
file2 = r"./microcode_rom_1.bin"

if are_files_identical(file1, file2):
    print("The files are identical.")




