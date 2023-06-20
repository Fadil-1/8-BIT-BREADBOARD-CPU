'''
STATUS: WORKING!

TO DO:
GIVE BETTER NAME TO VARIABLES, AND REORGANIZE FOR LEGIBILITY. EXPLAIN WHY EEPROM IMAGE(BIN FILE) SIZE
MUST BE THE SAME AS EEPROM SIZE. The EEPROM programmer software displays my values as follow
Real values:         c3f    406   db   ...
EEPROM programmer :  3f0c   0604  db00 ... 
Outputs are correct on the displays when I just write from the EEPROM programmer without modifying the bytes order.
Is it just displaying this way? Is it writing this way? Go over that.

THIS PROGRAM GENERATES BINARY DECODER EEPROMS FOR FOUR PARALLEL 7 SEGMENT DISPLAYS.
THE CORRESPONDING FALSTAD CIRCUIT CAN BE FOUND AT https


     _____                 _____                 _____                 _____                _____               _____  
    |_\|/_|               |_\|/_|               |_\|/_|               |_\|/_|              |_\|/_|             |_\|/_| 
    | /|\ |.              | /|\ |.              | /|\ |.              | /|\ |.             | /|\ |.            | /|\ |.
     ‾‾‾‾‾                 ‾‾‾‾‾                 ‾‾‾‾‾                 ‾‾‾‾‾                ‾‾‾‾‾               ‾‾‾‾‾  
393216 <-- 327680     327680 <-- 262144     262144 <-- 196608     196608 <-- 131072    131072 <-- 65536      65536 <-- 0    

            UNUSED__FILLED_WITH_ZEROS------->    524,288 <-- 327680    <-------UNUSED__FILLED_WITH_ZEROS

     _____                 _____                 _____                 _____                _____               _____  
    |_\|/_|               |_\|/_|               |_\|/_|               |_\|/_|              |_\|/_|             |_\|/_| 
    | /|\ |.              | /|\ |.              | /|\ |.              | /|\ |.             | /|\ |.            | /|\ |.
     ‾‾‾‾‾                 ‾‾‾‾‾                 ‾‾‾‾‾                 ‾‾‾‾‾                ‾‾‾‾‾               ‾‾‾‾‾  
393216 <-- 327680     327680 <-- 655360     655360 <-- 589824     589824 <-- 524288    524288 <-- 458752    458752 <-- 393216       

            UNUSED__FILLED_WITH_ZEROS------->    1,048,576 <-- 917,504   <-------UNUSED__FILLED_WITH_ZEROS                                                                    
'''


import array


#digits = [0xc3f, 0x406, 0xdb, 0x8f, 0xe6, 0x2069, 0xfd, 0x7, 0xff, 0xef]# 14-segment display.
#digits = [0x3F, 0x06, 0x5B, 0x4F, 0x66, 0x6D, 0x7D, 0x07, 0x7F, 0x6F] # 7-segment display.

digits = [0x3f, 0x6, 0xdb, 0x8f, 0xe6, 0xed, 0xfd, 0x7, 0xff, 0xef]# 14-segment display with modified 0, 1 and 5.

'''
The M27C160 UVEPROM has 2^20 = 1_048_576 address lines, and 16 output lines(16-bit word size, therefore,
it is a 1_048_576 bit EPROM, however, when considering output word size in terms of bytes,
then it can be seen as 2_097_152 bit EPROM.
M27C160_SIZE = 1_048_576 # If 8-bit word
M27C160_SIZE = 2_097_152 # If 16-bit word
'''

doc = open('rom.bin', 'wb') # Opening the output file in binary mode

OUTPUT_WORD_SIZE = 16 
ROM_SIZE = 2**OUTPUT_WORD_SIZE

# Number of digits used, excluding sign digit.
DISPLAY_DIGITS = 5 # My setup has 6 segment displays: Leftmost for sign nd rightmost for digits.

# Finding the number of pins which satisfies the display's requirements.
COUNTER_PINS = i = 0
while 2**COUNTER_PINS <6:
   COUNTER_PINS = 2^i
   i += 1

"""
I am using the three first bits of my 74HCT161 counter(8 states max).
I only need 6 states, therefore I feed the 7-th output of the decoder to the reset pin of the counter.


The unsigned digits span address 0 to address 393,216(pin A0 to A18) of the EPROM as follows:
1's place, from 0 to 65535
10's place, from 65536 to 131071
100's place, from 131072 to 196607
1000's place, from 196608 to 262143
10000's place, from 262144 to 327679
signs place, from 327680 to 393215, which is the 6'th tick of the counter(6 * 65,536 = 393,216). 

The two next states are never used(Address 393216 to 458,752 to 524,288).
The two complements digits should be activated when a switch is set; and the only remaining address line is pin 
A19(which spans the full EPROM size: 1,048,576) 524,288 - 524,288 = 524,288 of usable memory to program the two complements. 
"""


UNUSED_STATES = 2**COUNTER_PINS - (DISPLAY_DIGITS + 1)

UNSIGNED_START = 0
UNSIGNED_0_START = UNSIGNED_END = ROM_SIZE*DISPLAY_DIGITS
UNSIGNED_0_END = UNSIGNED_0_START + ROM_SIZE

FILL = ROM_SIZE*UNUSED_STATES
COMPLEMENT_START = UNSIGNED_0_END + FILL
COMPLEMENTS_SIGN_START = COMPLEMENT_END = COMPLEMENT_START + (ROM_SIZE*DISPLAY_DIGITS)
COMPLEMENTS_SIGN_END = COMPLEMENTS_SIGN_START + ROM_SIZE


print(f'\nEEPROM SIZE {ROM_SIZE}\n')

for i, index in enumerate(range(UNSIGNED_START, UNSIGNED_END, ROM_SIZE)):
  print(f"{10**i}'s place, from {index:,} to {index+ROM_SIZE:,}")
  for x in range(ROM_SIZE):
    doc.write(array.array("H", [ (digits[x % 10] if i==0 else digits[int(x / (10**i))% 10])] ))

print(f"signs place, from {UNSIGNED_0_START:,} to {UNSIGNED_0_END:,}\n")
for x in range(ROM_SIZE):
  doc.write(array.array("H", [0x0]))


print(f"Filling {UNSIGNED_0_END:,} to {UNSIGNED_0_END + FILL:,}(unused addresses) with zeros\n")
for x in range(FILL):
  doc.write(array.array("H", [0x0]))


for i, index in enumerate(range(COMPLEMENT_START, COMPLEMENT_END, ROM_SIZE)):
  print(f"Complements {10**i}'s place, from {index:,} to {index+ROM_SIZE:,}")
  for x in range(-(int(ROM_SIZE/2)), (int(ROM_SIZE/2))):
    doc.write(array.array("H", [ (digits[abs(int(x/(10**i))) % 10]) ]))


print(f"Complements signs place, from {COMPLEMENTS_SIGN_START:,} to {COMPLEMENTS_SIGN_END:,}")
for x in range(-(int(ROM_SIZE/2)), (int(ROM_SIZE/2))):
    if x < 0:
        doc.write(array.array("H", [0xc0]))
    else:
        doc.write(array.array("H", [0x0]))

print(f"Filling {COMPLEMENTS_SIGN_END:,} to {COMPLEMENTS_SIGN_END + FILL:,}(unused addresses) with zeros\n")
for x in range(FILL):
  doc.write(array.array("H", [0x0]))

doc.close()