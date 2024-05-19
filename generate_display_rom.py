import array

def generate_display_rom():
    """
    This function generates a binary decoder ROM image for 6 parallel 14-segment displays, with each
    display activated sequentially. The ROM is structured to hold data for both unsigned numbers and 
    their complements, including the sign representation.
    """
    # Defines the segment patterns for the digits on a 14-segment display.
    # I modified the the pattern for digits 0, 1, and 5 from the way they are typically represented. 
    digits = [0x3f, 0x6, 0xdb, 0x8f, 0xe6, 0xed, 0xfd, 0x7, 0xff, 0xef]# 14-segment display with modified 0, 1 and 5.


    # Opening/Creating the output file in binary mode to save ROM's image.
    doc = open('segmented_display_rom.bin', 'wb') 

    # Constants for the ROM's output mode and the ROM size.
    OUTPUT_WORD_SIZE = 16 
    ROM_SIZE = 2**OUTPUT_WORD_SIZE

    # Number of digits used, excluding sign digit.
    DISPLAY_DIGITS = 5

    # Deducting the number of unused states.
    DECODER_SELECTS = 3
    UNUSED_STATES = 2**DECODER_SELECTS - (DISPLAY_DIGITS + 1)

    # Start address for unsigned numbers.
    UNSIGNED_START = 0

    # Start and end addresses for the sign of unsigned numbers.
    UNSIGNED_0_START = UNSIGNED_END = ROM_SIZE*DISPLAY_DIGITS
    UNSIGNED_0_END = UNSIGNED_0_START + ROM_SIZE

    # Calculates the size to fill unused addresses with zeros.
    FILL = ROM_SIZE*UNUSED_STATES

    # Start and end addresses for the complements of numbers.
    COMPLEMENT_START = UNSIGNED_0_END + FILL
    COMPLEMENTS_SIGN_START = COMPLEMENT_END = COMPLEMENT_START + (ROM_SIZE*DISPLAY_DIGITS)
    COMPLEMENTS_SIGN_END = COMPLEMENTS_SIGN_START + ROM_SIZE

    # Writes data for unsigned numbers.
    for i, index in enumerate(range(UNSIGNED_START, UNSIGNED_END, ROM_SIZE)):
      print(f"{10**i}'s place, from {index:,} to {index+ROM_SIZE:,}")
      for x in range(ROM_SIZE):
        doc.write(array.array("H", [ (digits[x % 10] if i==0 else digits[int(x / (10**i))% 10])] ))

    # Writes data for the sign place of unsigned numbers.
    print(f"signs place, from {UNSIGNED_0_START:,} to {UNSIGNED_0_END:,}\n")
    for x in range(ROM_SIZE):
      doc.write(array.array("H", [0x0]))

    # Fills unused addresses with zeros.
    print(f"Filling {UNSIGNED_0_END:,} to {UNSIGNED_0_END + FILL:,}(unused addresses) with zeros\n")
    for x in range(FILL):
      doc.write(array.array("H", [0x0]))

    # Writes data for the complements.
    for i, index in enumerate(range(COMPLEMENT_START, COMPLEMENT_END, ROM_SIZE)):
      print(f"Complements {10**i}'s place, from {index:,} to {index+ROM_SIZE:,}")
      for x in range(-(int(ROM_SIZE/2)), (int(ROM_SIZE/2))):
        doc.write(array.array("H", [ (digits[abs(int(x/(10**i))) % 10]) ]))

    # Writes data for the complements' sign place.
    print(f"Complements signs place, from {COMPLEMENTS_SIGN_START:,} to {COMPLEMENTS_SIGN_END:,}")
    for x in range(-(int(ROM_SIZE/2)), (int(ROM_SIZE/2))):
        if x < 0:
            doc.write(array.array("H", [0xc0]))
        else:
            doc.write(array.array("H", [0x0]))
    # Fills remaining unused addresses with zeros.
    print(f"Filling {COMPLEMENTS_SIGN_END:,} to {COMPLEMENTS_SIGN_END + FILL:,}(unused addresses) with zeros\n")
    for x in range(FILL):
      doc.write(array.array("H", [0x0]))

    # Closes the file after writing the ROM.
    doc.close()

# Calling the function to generate the ROM.
generate_display_rom()