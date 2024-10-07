1- trim_hex.py: When using comma-separated-hex format to generate machine code, Customasm writes 
   49152 (0xC000) zeros (0x00) to fill the boot loader ROM's offset space, "#addr 0xC000".
   trim_hex.py removes these zeros so that the actual byte code can be easily copied and pasted
   in Arduino IDE and used for other tasks.

2- hexacomma_to_bin.py: Converts a comma-separated hex value file into a binary (.bin) file. 
   Used to generate real .bin images for ROM programmer.

3- files_comparator.py: Compares two files to check if they are identical. Used for sanity checks such as 
   whether image on EPROM has changed from original .bin over time. 

4- convert_instructions_to_markdown.py: Writes all the CPU instructions and corresponding microsteps in a markdown file.
