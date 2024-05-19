1- trim_hex.py: When using comma-separated-hex format to generate machine code, Customasm writes 
   49152 (0xC000) zeros (0x00) to fill the boot loader ROM's offset space, "#addr 0xC000".
   trim_hex.py removes these zeros so that the actual byte code can be easily copied and pasted
   in Arduino IDE.
2- binary_files_comparator.py compares two binary files to check if they are identical.
3- convert_instructions_to_markdown.py writes all of the CPU's instructions and corresponding microsteps in a markdown file.
