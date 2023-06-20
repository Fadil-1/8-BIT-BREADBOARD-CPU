'''
  Inputs {From MSB(A17) to LSB(A0)}:

  Opcode (Data bus bit 7 --> A17 ... Bit _0 --> A10) 

  II(Interrupt inhibit) --> A9

  IR(Interrupt request) --> A8

  Step counter (Bit _3 --> A7 ... Bit _0 --> A4) 

  Zero      (Z)    flag --> A3
  Overflow  (O/V)  flag --> A2
  Negative  (N)    flag --> A1
  Carry     (C)    flag --> A0

   _______________     _______________     _______________  
  |               |   |               |   |               |
  |     ROM 0     |   |     ROM 1     |   |     ROM 2     |
  |               |   |               |   |               | 
   ‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾     ‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾     ‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾  
     15  -->  0          31 --> 16             47 --> 32
'''


from copy import deepcopy
import array

INTPUT_WORD_SIZE = 18 # From 0 to 17 --> 18-bit word
ROM_SIZE = 2**INTPUT_WORD_SIZE

# ROM 0
_CLKW  = 1 <<  15  #  Clock speed select
_DW    = 1 <<  14  #  D Register(General purpose register 4) Write
_BW    = 1 <<  13  #  B Register(General purpose register 2) Write
H_cin  = 1 <<  12  #  Shift register carry in 
#_SdE  = 1 <<  11  #  Segmented display enable
_HC    = 1 <<  10  #  Shift register clear/reset
ZS     = 1 <<  9   #  ALU select(0: 382 ALU; 1: 194-shift register)
Z2     = 1 <<  8   #  ALU control_2
Z1     = 1 <<  7   #  ALU control_1
_FW    = 1 <<  6   #  Flag register write/in
IR_in  = 1 <<  5   #  Instruction register in
TI     = 1 <<  4   #  Toggle interrupt(Sets interrupt to the opposite of its current state)
_OS    = 1 <<  3   #  OLED select(D/C# Data by default, command when asserted)
OR     = 1 <<  2   #  OLED data(Read/_Write Write by default, and read when asserted)
OE     = 1 <<  1   #  OLED enable(Read/write is enabled when pulled high)
_OC    = 1         #  OLED clear

# ROM 1
EX     = 1 <<  31 #  Extra (Extra/Unused control line)
SdM    = 1 <<  30 #  Segmented display mode(Signed/_Unsigned)
Z0     = 1 <<  29 #  ALU control_0
_ScR   = 1 <<  28 #  Step counter reset to 0
BRlW   = 1 <<  27 #  Transfer Register lower byte write
_PChE  = 1 <<  26 #  Program counter upper byte enable
_PClE  = 1 <<  25 #  Program counter lower byte enable
_GE    = 1 <<  24 #  G Register(General purpose register 6) enable  
GW     = 1 <<  23 #  G Register(General purpose register 6) Write
_OO    = 1 <<  22 #  OLED transceiver enable
_PSE   = 1 <<  21 #  Port selector enable
_PSW   = 1 <<  20 #  Port selector write
HLT    = 1 <<  19 #  Clock halt/stop
SPW    = 1 <<  18 #  Stack pointer load
SPD    = 1 <<  17 #  Stack pointer count direction(_up/down)
_SPC   = 1 <<  16 #  Stack pointer count enable

# ROM 2
_SPE   = 1 <<  47 #  Stack pointer word(16-bits) enable
BRhW   = 1 <<  46 #  Transfer Register upper byte write
_MW    = 1 <<  45 #  Memory write
ZW     = 1 <<  44 #  Accumulator write
_BRE   = 1 <<  43 #  Transfer Register word(16-bits) enable
_PCE   = 1 <<  42 #  Program counter word(16-bits) enable
PCC    = 1 <<  41 #  Program counter count up
_PCW   = 1 <<  40 #  Program counter write/in (Jump)
_PS    = 1 <<  39 #  Port select in
# 74HCT238 3-to-8 non inverting decoder
WR_2   = 1 <<  38 #  Write decoder A2
WR_1   = 1 <<  37 #  Write decoder A1
WR_0   = 1 <<  36 #  Write decoder A0
# 74HCT154 4-to-16 inverting decoder
RD_3   = 1 <<  35 #  Read decoder A3
RD_2   = 1 <<  34 #  Read decoder A2
RD_1   = 1 <<  33 #  Read decoder A1
RD_0   = 1 <<  32 #  Read decoder A0

# The decoders are arranged so that every lines they control are considered active high
# For example the 74HCT254 is an inverting decoder; and all it's output lines are connected
# To active-low inputs; making its outputs controllable as active high outputs

## 74HCT238
SdW = WR_2 | WR_1 | WR_0 #  Segmented display write
EW  = WR_2 | WR_1        #  E Register(General purpose register 5) write
SdT = WR_2 |        WR_0 #  Segmented display's temporary register(lower byte) write
CW  =        WR_1 | WR_0 #  C Register(General purpose register 3) write (Decoder's output goes through an inverter first)
AW  =        WR_1        #  A Register(General purpose register 1) write (Decoder's output goes through an inverter first)

## 74HCT154
ZE    = RD_3 | RD_2 | RD_1 | RD_0 #  Accumulator enable
DE    = RD_3 | RD_2 | RD_1        #  D Register(General purpose register 4) enable 
CE    = RD_3 | RD_2 |        RD_0 #  C Register(General purpose register 3) enable 
AE    = RD_3 | RD_2               #  A Register(General purpose register 1) enable 
BE    = RD_3 |        RD_1 | RD_0 #  B Register(General purpose register 2) enable 
FE    = RD_3 |        RD_1        #  Flags Register enable 
BRhE  = RD_3 |               RD_0 #  Transfer Register Upper byte Enable
BRlE  = RD_3                      #  Transfer Register Lower byte Enable
SPhE  =        RD_2 | RD_1 | RD_0 #  Stack Pointer Upper byte Enable 
SPlE  =        RD_2 | RD_1        #  Stack Pointer lower byte Enable
EE    =        RD_2 |        RD_0 #  E Register(General purpose register 5) enable 
ME    =        RD_2               #  Memory enable to 8-bit bus 

active_low_lines = _CLKW | _DW | _BW | _HC  | _FW |_OS | _OC | _ScR | \
_PChE | _PClE | _GE | _OO | _PSE | _PSW | _SPC | _SPE | _MW | \
_BRE | _PCE | _PCW | _PS
 
ALU_ZERO           =                0
ALU_ACC_minus_BUS  =                Z0
ALU_BUS_minus_ACC  =           Z1
ALU_ADD            =           Z1 | Z0
ALU_XOR            =      Z2       
ALU_OR             =      Z2 |      Z0
ALU_AND            =      Z2 | Z1
ALU_FF             =      Z2 | Z1 | Z0
ALU_SL             = ZS |           Z0    
ALU_SR             = ZS |      Z1
ALU_MIRROR_BUS     =    FLG_MIRROR_BUS   = ZS |      Z1 | Z0  
FLG_RSC            = ZS | Z2
FLG_STC            = ZS | Z2  |Z0

II_Flag  = 0b100000
IRQ_Flag =  0b10000 
Z_Flag   =   0b1000
O_Flag   =    0b100
N_Flag   =     0b10
C_Flag   =      0b1



"""
Each opcode is 8-bit(1-byte) long, and can make up instructions with up to 16 steps.
The EPROMs are input as follows: 

A_17  A_16  A_15  A_14  A_13  A_12  A_11  A_10  A_9  A_8  A_7  A_6  A_5  A_4  A_3  A_2  A_1  A_0
|     |     |     |     |     |     |     |     |    |    |    |    |    |    |    |    |    |
|                                         |     |              |    |    |    Z    O    N    C
|                                         |     |              |    |   Pending 
|-----------------------------------------|     |--------------|    |   Interrupt
These are the opcode bits(2^8 = up to           These are the       |   
256 different instructions)                     steps bits(2^4   Interrupt  
                                              = 16 steps max)   Inhibit
"""


def build_address(opcode=0b0, step=0b0, II=0b0, IR=0b0, Z=0b0, O=0b0, N=0b0, C=0b0):
   '''
   Organizes bit position of every element in the microcode input.
   If a an element of the input word is not input it will default to 0.
   '''
   return opcode << 10 | step << 6 | II << 5 | IR << 4 | Z << 3 | O << 2 | N << 1 | C

def al_norm(microcode):
    '''
    al_norm(Active_low normalization):
    Ensures that active low lines stay high and active high lines stay low
    when not needed in a microcode by "XORing" the current control word with the bits
    position of all active-low control lines. 
    '''
    return microcode ^ active_low_lines

def trim_word(EPROM_number, microcode):
  '''
  Trims a part of the microcode for it's corresponding EPROM.
  Refer to docstring to see how EPROMS are layed out.
  '''
  shifted_microcode = microcode >> (16*EPROM_number)
  mask = 0xFFFF # 16 1s
  return shifted_microcode & mask # AND the 16 output bits of the selected EPROM 

adr = -1 # Start at -1 because the function assigning addresses increments before assigning
#FETCH = [_PCE | ME | IR_in, PCC] # Fetch code 
FETCH = [_PCE | ME | IR_in | PCC] # Fetch code 


def full_microcode(t_1 = 0, t_2 = 0, t_3 = 0, t_4 = 0, t_5 = 0, t_6 = 0,
                    t_7 = 0, t_8 = 0, t_9 = 0, t_10 = 0, t_11 = 0,
                      t_12 = 0, t_13 = 0, t_14 = 0, t_15 = 0):
    """
    Creates microcode and ends it by resetting the step counter
    """
    global adr
    end = False


    steps = [t_1, t_2, t_3, t_4, t_5, t_6, t_7, t_8, 
             t_9, t_10, t_11, t_12, t_13, t_14, t_15]
    
    for i, step in enumerate(steps):
        if step == 0 and not end:
            steps[i] = _ScR
            end = True

    steps = FETCH + steps
    adr += 1

    return steps

########################################
instructions_without_flags = dict()
instructions_without_flags = dict()
instructions_without_flags = dict()
recycling_address = []

def add_microcode(micro_instruction, name):
    '''
    Updates the unconditional instructions with correct dictionary key.
    '''
    global adr
    if recycling_address:
        instructions_without_flags[recycling_address[0]] = micro_instruction, name
        recycling_address.pop(0)
        adr -= 1
    else:
        instructions_without_flags[adr] = micro_instruction, name

ABCD = ['A' ,'B' ,'C' ,'D']
EG = ['E', 'G']
# All registers' write lines
write_to_reg = {'A': AW, 
                'B': _BW, 
                'C':CW, 
                'D':_DW,
                'E': EW,
                'G': GW}

# All registers enable lines(OO = OLED display's transceiver)
enable_reg = {'A': AE, 
              'B': BE, 
              'C': CE, 
              'D': DE,
              'E': EE,
              'G': _GE}



# $   Register
# #   Number
# @   Address
# []  Memory location
# [@] Address at a memory location
# [#] Number at a memory location

### AT OPCODE 0b00000000 no matter what the flags are 
# RST Soft Reset Instruction (From 0 to 15)
# Jumps to address BB80 of memory(which is the start address of the memory EPROM)
# At that address, there is code that first jumps PC to BB81, and
# copies itself to address 0x000 of RAM.
adr += 1
instructions_without_flags[adr] =([ ALU_ZERO | ZW,                                            # s = 0  Write zero in accumulator.
                                    ZE | BRhW | BRlW | AW | IR_in,                            # s = 1  Write 0 in bridge, A register, and instruction register.(Placing 0 in IR will keep it at the reset opcode even when the "forced" zeros are is removed).
                                    ZE | _BRE | SPW | SPD | CW | FLG_MIRROR_BUS | _FW | _PCW, # s = 2  Write 0 in stack pointer, flags, and C register(Also write zero into PC in case the fetch counter reset button is release before "unforcing" zero from the instruction register).
                                    ZE | _SPC | SPD | SdW,                                    # s = 3  SPD(Down from 0 goes to 0xFFFF) and write zero in segmented display register. 
                                    ZE | _BW | _DW | GW | SdT,                                # s = 4  Write 0 in registers B, D, G, and temporary segmented display register.
                                    ZE | ALU_SR | H_cin | ZW,  BRlW,                          # s = 5  Write 0b10000000(0x80) in accumulator and 0b10000000(0x80) in lower byte o bridge.
                                    ZE | ALU_SR | H_cin | ZW,                                 # s = 6  (Z= 0b10000000) Write 0b11000000 in accumulator.
                                    ZE | ALU_SR | ZW,                                         # s = 7  (Z= 0b11000000) Write 0b01100000 in accumulator
                                    ZE | ALU_SR | H_cin | ZW,                                 # s = 8  (Z= 0b01100000) Write 0b10110000 in accumulator
                                    ZE | ALU_SR | H_cin | ZW,                                 # s = 9  (Z= 0b10110000) Write 0b11011000 in accumulator                
                                    ZE | ALU_SR | H_cin | ZW,                                 # s = 10 (Z= 0b11011000) Write 0b11101100 in accumulator
                                    ZE | ALU_SR | ZW,                                         # s = 11 (Z= 0b11101100) Write 0b01110110 in accumulator 
                                    ZE | ALU_SR | H_cin | ZW,                                 # s = 12 (Z= 0b01110110) Write 0b10111011(BB) in accumulator
                                    ZE | BRhW,                                                # s = 13 (Z= 0b10111011)Write 0b10111011(BB) in high byte of bridge,
                                    _BRE | _PCW,                                              # s = 14  0xBB80 IN PROGRAM COUNTER
                                    _PCE | ME | IR_in],                                       # s = 15
                             f'RST')



## INTERRUPT (From 16 to 31)
add_microcode(full_microcode(  FE | _SPE | _MW | SPD | TI,                # Write flag to stack memory and toggle interrupt.
                              _SPC | SPD             | ALU_FF | ZW,       # Decrement stack pointer by one and write 255 to accumulator.
                              _PClE | _SPE | _MW | SPD | FLG_RSC | _FW,   # Write lower byte of Program counter to stack memory, and clear carry flag. 
                              _SPC | SPD             | ZE | BRhW,        # Write 255 into high byte of bridge and decrement stack pointer by one.
                              _PChE | _SPE | _MW | SPD,                   # Write Higher byte of program counter to stack memory.
                              _SPC | SPD             | ZE | ALU_SL | ZW,  # Decrement stack pointer by one and write 0xFE to accumulator(By shifting 0xFF left once). 
                              ZE | BRlW,                                 # Write 0xFE to lower byte of bridge.
                              _BRE | ME | ALU_MIRROR_BUS | ZW,            # Write content at RAM address 0xFFFE to accumulator.
                              _SPE | ZE | _MW,                            # Write content of accumulator(RAM address 0xFFFE) to stack memory.
                              ALU_FF | ZW,                                # Write 0xFF to accumulator.
                              ZE | BRlW,                                 # Write 0xFF to lower byte of bridge.
                              _BRE | ME | ALU_MIRROR_BUS | ZW,            # Write content of RAM at 0xFFFF into accumulator.
                              ZE | BRhW,                                 # Write content of accumulator(RAM address 0xFFFF) into lower byte of bridge.
                              _SPE | ME | BRlW,                          # Write content of current stack address in lower byte of bridge. 
                              _BRE | _PCW ),                              # Enable content of bridge to 16-bit bus and write it to the program counter. 
                              "ITR")



## NO OP (From 32 to 47 )
add_microcode(full_microcode(), f'NOP')

## Reset/Clear carry (From 48 to 63)
add_microcode(full_microcode(FLG_RSC | _FW), f'CLC')

## Set carry (From 64 to 79)
add_microcode(full_microcode(FLG_STC | _FW), f'STC')


## RETURN FROM SUBROUTINE (From 80 to 95)
add_microcode(full_microcode(_SPC,
                            BRhW | _SPE | ME,
                            _SPC,
                            BRlW | _SPE | ME,
                            _BRE | _PCW ), 
                            f'RTS')

## RETURN FROM INTERRUPT (From 96 to 111)
add_microcode(full_microcode(_SPC,
                            BRhW | _SPE | ME,
                            _SPC,
                            BRlW | _SPE | ME,
                            _BRE | _PCW | _SPC,
                            _SPE | ME | FLG_MIRROR_BUS | _FW | TI), 
                            f'RTI')

## (From 112 to 127)

### IMMEDIATE
for dest in ABCD:
    add_microcode(full_microcode(_PCE | ME | write_to_reg[dest] | PCC),
                                 f'MOV ${dest}, #')
    add_microcode(full_microcode(enable_reg[dest] | ALU_MIRROR_BUS | ZW, 
                                _PCE | ME | ALU_ADD | ZW | _FW,  
                                write_to_reg[dest] | ZE | PCC),
                                f'ADD ${dest}, #') 
    add_microcode(full_microcode(enable_reg[dest] | ALU_MIRROR_BUS | ZW, 
                                 _PCE | ME | ALU_ACC_minus_BUS | ZW | _FW,
                                 write_to_reg[dest] | ZE | PCC), 
                                 f'SUB ${dest}, #') 
    add_microcode(full_microcode(enable_reg[dest] | ALU_MIRROR_BUS | ZW, 
                                 _PCE | ME | ALU_AND | ZW | _FW,  
                                 write_to_reg[dest] | ZE | PCC), 
                                 f'AND ${dest}, #') 
    add_microcode(full_microcode(enable_reg[dest] | ALU_MIRROR_BUS | ZW, 
                                 _PCE | ME | ALU_OR | ZW | _FW,  
                                 write_to_reg[dest] | ZE | PCC), 
                                 f'OR ${dest}, #') 
    add_microcode(full_microcode(enable_reg[dest] | ALU_MIRROR_BUS | ZW, 
                                 _PCE | ME | ALU_XOR | ZW | _FW,  
                                 write_to_reg[dest] | ZE | PCC), 
                                 f'XOR ${dest}, #') 
    add_microcode(full_microcode(enable_reg[dest] | ALU_MIRROR_BUS | ZW, 
                                 _PCE | ME | ALU_ACC_minus_BUS | _FW | PCC), 
                                 f'CMP ${dest}, #')
# Clock Control
# CLK IMMEDIATE: Write content in RAM to CLK/DISPLAY register from memory content.  
add_microcode(full_microcode(_PCE | ME | _CLKW, PCC), # Select I/O from RAM content.
                            f'MOV $CLK, #')


## DIRECT REGISTER MODE
for dest in ABCD:
    for src in ABCD:
        if dest == src:
            #recycling_address.append(adr +1) # Recycle address for later use
            continue

        add_microcode(full_microcode(write_to_reg[dest] | enable_reg[src]), 
                                    f'MOV ${dest}, ${src}')

        add_microcode(full_microcode(enable_reg[dest] | ALU_MIRROR_BUS | ZW,
                                     enable_reg[src] | ALU_ADD |_FW | ZW,  
                                     write_to_reg[dest] | ZE), 
                                    f'ADD ${dest}, ${src}')
        add_microcode(full_microcode(enable_reg[dest] | ALU_MIRROR_BUS | ZW,
                                     enable_reg[src] | ALU_ACC_minus_BUS |_FW | ZW,  
                                     write_to_reg[dest] | ZE), 
                                    f'SUB ${dest}, ${src}')
        add_microcode(full_microcode(enable_reg[dest] | ALU_MIRROR_BUS | ZW,
                                     enable_reg[src] | ALU_AND |_FW | ZW,  
                                     write_to_reg[dest] | ZE), 
                                    f'AND ${dest}, ${src}')
        add_microcode(full_microcode(enable_reg[dest] | ALU_MIRROR_BUS | ZW,
                                     enable_reg[src] | ALU_OR |_FW | ZW,  
                                     write_to_reg[dest] | ZE), 
                                    f'OR ${dest}, ${src}')
        add_microcode(full_microcode(enable_reg[dest] | ALU_MIRROR_BUS | ZW,
                                     enable_reg[src] | ALU_XOR |_FW | ZW,  
                                     write_to_reg[dest] | ZE), 
                                    f'XOR ${dest}, ${src}')      
        add_microcode(full_microcode(enable_reg[dest] | ALU_MIRROR_BUS | ZW,
                                     enable_reg[src] | ALU_ACC_minus_BUS |_FW), 
                                    f'CMP ${dest}, ${src}')


    
# INDIRECT REGISTER MODE
# Read
for dest in ABCD:
        add_microcode(full_microcode( CE | BRlW,
                                      DE | BRhW,
                                     _BRE | ME | write_to_reg[dest]), 
                                    f'MOV ${dest}, [$CD]')
        # Write
        add_microcode(full_microcode( CE | BRlW,
                                      DE | BRhW,
                                     _BRE | _MW | enable_reg[dest]), 
                                    f'MOV [$CD], ${dest}')

        add_microcode(full_microcode( CE | BRlW,
                                      DE | BRhW,
                                     enable_reg[dest] | ALU_MIRROR_BUS | ZW,
                                     _BRE | ME | ALU_ADD | ZW | _FW,
                                     write_to_reg[dest] | ZE ),
                                    f'ADD ${dest}, [$CD]')
        
        add_microcode(full_microcode( CE | BRlW,
                                      DE | BRhW,
                                     enable_reg[dest] | ALU_MIRROR_BUS | ZW,
                                     _BRE | ME | ALU_ACC_minus_BUS | ZW | _FW,
                                     write_to_reg[dest] | ZE ),
                                    f'SUB ${dest}, [$CD]')
        
        add_microcode(full_microcode( CE | BRlW,
                                      DE | BRhW,
                                     enable_reg[dest] | ALU_MIRROR_BUS | ZW,
                                     _BRE | ME | ALU_AND | ZW | _FW,
                                     write_to_reg[dest] | ZE ),
                                    f'AND ${dest}, [$CD]')
        
        add_microcode(full_microcode( CE | BRlW,
                                      DE | BRhW,
                                     enable_reg[dest] | ALU_MIRROR_BUS | ZW,
                                     _BRE | ME | ALU_OR | ZW | _FW,
                                     write_to_reg[dest] | ZE ),
                                    f'OR ${dest}, [$CD]')
        
        add_microcode(full_microcode( CE | BRlW,
                                      DE | BRhW,
                                     enable_reg[dest] | ALU_MIRROR_BUS | ZW,
                                     _BRE | ME | ALU_XOR | ZW | _FW,
                                     write_to_reg[dest] | ZE ),
                                    f'XOR ${dest}, [$CD]')
        
        add_microcode(full_microcode( CE | BRlW,
                                      DE | BRhW,
                                     enable_reg[dest] | ALU_MIRROR_BUS | ZW,
                                     _BRE | ME | ALU_ACC_minus_BUS | _FW),
                                    f'CMP ${dest}, [$CD]')


# ABSOLUTE REGISTER MODE
for dest in ABCD:
    add_microcode(full_microcode(_PCE| ME | BRlW | PCC,
                                 _PCE | ME | BRhW, 
                                 _BRE | ME | write_to_reg[dest] | PCC), 
                                f'MOV ${dest}, [@]')
    add_microcode(full_microcode(_PCE | ME | BRlW | PCC,
                                _PCE | ME | BRhW, 
                                _BRE | _MW | enable_reg[dest] | PCC),
                                f'MOV [@], ${dest}')
    add_microcode(full_microcode(_PCE | ME | BRlW | PCC,
                                _PCE | ME | BRhW, 
                                enable_reg[dest] | ALU_MIRROR_BUS | ZW | PCC,
                                _BRE | ME | ALU_ADD | ZW | _FW,
                                write_to_reg[dest] | ZE ),
                                f'ADD ${dest}, [@]')
    add_microcode(full_microcode(_PCE | ME | BRlW | PCC,
                                _PCE | ME | BRhW, 
                                enable_reg[dest] | ALU_MIRROR_BUS | ZW | PCC,
                                _BRE | ME | ALU_ACC_minus_BUS | ZW | _FW,
                                write_to_reg[dest] | ZE ), 
                                f'SUB ${dest}, [@]')
    add_microcode(full_microcode(_PCE | ME | BRlW | PCC,
                                _PCE | ME | BRhW, 
                                enable_reg[dest] | ALU_MIRROR_BUS | ZW | PCC,
                                _BRE | ME | ALU_AND | ZW | _FW,
                                write_to_reg[dest] | ZE ), 
                                f'AND ${dest}, [@]')
    add_microcode(full_microcode(_PCE | ME | BRlW | PCC,
                                _PCE | ME | BRhW, 
                                enable_reg[dest] | ALU_MIRROR_BUS | ZW | PCC,
                                _BRE | ME | ALU_OR | ZW | _FW,
                                write_to_reg[dest] | ZE ), 
                                f'OR ${dest}, [@]')
    add_microcode(full_microcode(_PCE | ME | BRlW | PCC,
                                _PCE | ME | BRhW, 
                                enable_reg[dest] | ALU_MIRROR_BUS | ZW | PCC,
                                _BRE | ME | ALU_XOR | ZW | _FW,
                                write_to_reg[dest] | ZE ), 
                                f'XOR ${dest}, [@]')
    add_microcode(full_microcode(_PCE | ME | BRlW | PCC,
                                _PCE | ME | BRhW, 
                                enable_reg[dest] | ALU_MIRROR_BUS | ZW | PCC,
                                _BRE | ME | ALU_ACC_minus_BUS | _FW),
                                f'CMP ${dest}, [@]') 

## OUT
# 8-bit with trailing zeros
for src in ABCD:
    add_microcode(full_microcode(enable_reg[src] | SdT,  
                                 ALU_ZERO | ZW, 
                                 ZE | SdW  ), 
                                 f'SDT ${src}')

# Output address content with trailing zeros
add_microcode(full_microcode(_PCE | ME | BRlW | PCC,
                             _PCE | ME | BRhW,
                             _BRE | ME | SdT | PCC, 
                              ALU_ZERO | ZW, 
                              ZE | SdW ),
                             f'SDT [@]')

# Output indirect address with trailing zeros
add_microcode(full_microcode( CE | BRlW,
                              DE | BRhW,
                             _BRE | ME | SdT,
                              ALU_ZERO | ZW, 
                              ZE | SdW ),
                             'SDT [$CD]')


# Lower byte of number
add_microcode(full_microcode(enable_reg['A'] | SdT), 
                                f'SDL $A')
add_microcode(full_microcode(enable_reg['B'] | SdT), 
                                f'SDL $B')
add_microcode(full_microcode(_GE | SdT), 
                                f'SDL $G')
add_microcode(full_microcode(_PCE | ME | BRlW | PCC,
                             _PCE | ME | BRhW,
                             _BRE | ME | SdT | PCC),
                             f'SDL [@]')
add_microcode(full_microcode( CE | BRlW,
                              DE | BRhW,
                             _BRE | ME | SdT),
                             'SDL [$CD]')

# Higher byte of number
add_microcode(full_microcode(enable_reg['A'] | SdW), 
                                f'SDH $A')
add_microcode(full_microcode(enable_reg['B'] | SdW), 
                                f'SDH $B')
add_microcode(full_microcode(_GE | SdW), 
                                f'SDH $G')
add_microcode(full_microcode(_PCE | ME | BRlW | PCC,
                             _PCE | ME | BRhW,
                             _BRE | ME | SdW | PCC),
                             f'SDH [@]')
add_microcode(full_microcode( CE | BRlW,
                              DE | BRhW,
                             _BRE | ME | SdW),
                             'SDH [$CD]')




## SL
# Register
for src in ABCD:
    add_microcode(full_microcode(enable_reg[dest] | ALU_SL | ZW | _FW,
                                 write_to_reg[dest] | ZE),
                                 f'LSL ${src}')
# Address
add_microcode(full_microcode(_PCE | ME | BRlW | PCC,
                             _PCE | ME | BRhW,
                             _BRE | ME | ALU_SL | ZW | _FW | PCC,
                             _BRE | ZE | _MW ),
                            'LSL @')
# Indirect
add_microcode(full_microcode( CE | BRlW,
                              DE | BRhW,
                             _BRE | ME | ALU_SL | ZW | _FW,
                             _BRE | ZE | _MW ),
                            'LSL [$CD]')

## SR
# Register
for src in ABCD:
    add_microcode(full_microcode(enable_reg[dest] | ALU_SR | ZW | _FW,
                                 write_to_reg[dest] | ZE),
                                 f'LSR ${src}')
# Address
add_microcode(full_microcode(_PCE | ME | BRlW | PCC,
                             _PCE | ME | BRhW,
                             _BRE | ME | ALU_SR | ZW | _FW | PCC,
                             _BRE | ZE | _MW ),
                            'LSR @')
# Indirect
add_microcode(full_microcode( CE | BRlW,
                              DE | BRhW,
                             _BRE | ME | ALU_SR | ZW | _FW,
                             _BRE | ZE | _MW ),
                            'LSR [$CD]')

## PUSH PULL
# Register
for src in ABCD:
    add_microcode(full_microcode(enable_reg[src] | _SPE | _MW | SPD,
                                 _SPC | SPD ),
                                 f'PSH ${src}')
    add_microcode(full_microcode(_SPC,
                                 write_to_reg[dest] | _SPE | ME),
                                 f'PUL ${src}')
    
add_microcode(full_microcode(FE | _SPE | _MW | SPD,
                             _SPC | SPD),
                             f'PSF ${src}')


add_microcode(full_microcode(_SPC | ALU_ZERO | ZW,       
                             _SPE | ME | ALU_OR | _FW),  
                             f'PLF ${src}')              


## Stack Pointer
add_microcode(full_microcode( CE | BRlW,
                              DE | BRhW,
                             _BRE | SPW ),
                             f'MOV $SP, $CD')

add_microcode(full_microcode(SPlE | EW,
                             SPhE | GW),
                             f'MOV $CD, $SP')

## Jump
add_microcode(full_microcode(_PCE | ME | BRlW | PCC,
                             _PCE | ME | BRhW ,
                             _BRE | _PCW ,),
                             f'JMP @')


add_microcode(full_microcode(_PCE | ME | BRlW | PCC,
                             _PCE | ME | BRhW | PCC,
                             _PClE | _SPE | _MW | SPD,
                             _SPC | SPD,
                             _PChE | _SPE | _MW | SPD,
                             _BRE | _PCW | _SPC | SPD),
                             f'JSR @')

add_microcode(full_microcode( CE | BRlW,
                              DE | BRhW,
                             _BRE | _PCW),
                             f'JMP [$CD]')

add_microcode(full_microcode(CE | BRlW,
                              DE | BRhW,
                             _PClE | _SPE | _MW | SPD,
                             _SPC | SPD,
                             _PChE | _SPE | _MW | SPD,
                             _BRE | _PCW | _SPC | SPD),
                             f'JSR [$CD]')

## Conditional Jumps
# Jump if zero
add_microcode(full_microcode(PCC),
                             f'JZ [@]')
# Jump is overflow
add_microcode(full_microcode(PCC),
                             f'JO [@]')
# Jump if lower than zero
add_microcode(full_microcode(PCC),
                             f'JN [@]')
# Jump if carry
add_microcode(full_microcode(PCC),
                             f'JC [@]')
# Jump if not zero
add_microcode(full_microcode(PCC),
                             f'JNZ [@]')
# Jump if not overflow
add_microcode(full_microcode(PCC),
                             f'JNO [@]')
# Jump if positive (JGZ including Z)
add_microcode(full_microcode(PCC),
                             f'JP [@]')
# Jump if not carry
add_microcode(full_microcode(PCC),
                             f'JNC [@]')
# Jump if greater than zero
add_microcode(full_microcode(PCC),
                             f'JGZ [@]')


## IMMEDIATE MODE WITH EG
add_microcode(full_microcode(_PCE | ME | write_to_reg[dest] | PCC),
                                f'MOV ${"E"}, #')
add_microcode(full_microcode(_PCE | ME | write_to_reg[dest] | PCC),
                                f'MOV ${"G"}, #')

## DIRECT REGISTER MODE WITH EG
add_microcode(full_microcode(write_to_reg['A'] | enable_reg['E']), 
                             f'MOV ${"A"}, ${"E"}')
add_microcode(full_microcode(write_to_reg['B'] | enable_reg['E']), 
                             f'MOV ${"B"}, ${"E"}')
add_microcode(full_microcode(write_to_reg['C'] | enable_reg['E']), 
                             f'MOV ${"C"}, ${"E"}')
add_microcode(full_microcode(write_to_reg['D'] | enable_reg['E']), 
                             f'MOV ${"D"}, ${"E"}')

add_microcode(full_microcode(write_to_reg['A'] | enable_reg['G']), 
                             f'MOV ${"A"}, ${"G"}')
add_microcode(full_microcode(write_to_reg['B'] | enable_reg['G']), 
                             f'MOV ${"B"}, ${"G"}')
add_microcode(full_microcode(write_to_reg['C'] | enable_reg['G']), 
                             f'MOV ${"C"}, ${"G"}')
add_microcode(full_microcode(write_to_reg['D'] | enable_reg['G']), 
                             f'MOV ${"D"}, ${"G"}')

add_microcode(full_microcode(write_to_reg['E'] | enable_reg['A']), 
                             f'MOV ${"E"}, ${"A"}')
add_microcode(full_microcode(write_to_reg['E'] | enable_reg['B']), 
                             f'MOV ${"E"}, ${"B"}')
add_microcode(full_microcode(write_to_reg['E'] | enable_reg['C']), 
                             f'MOV ${"E"}, ${"C"}')
add_microcode(full_microcode(write_to_reg['E'] | enable_reg['D']), 
                             f'MOV ${"E"}, ${"D"}')

add_microcode(full_microcode(write_to_reg['G'] | enable_reg['A']), 
                             f'MOV ${"G"}, ${"A"}')
add_microcode(full_microcode(write_to_reg['G'] | enable_reg['B']), 
                             f'MOV ${"G"}, ${"B"}')
add_microcode(full_microcode(write_to_reg['G'] | enable_reg['C']), 
                             f'MOV ${"G"}, ${"C"}')
add_microcode(full_microcode(write_to_reg['G'] | enable_reg['D']), 
                             f'MOV ${"G"}, ${"D"}')

# HALT
add_microcode(full_microcode(HLT), f'HLT')
print(instructions_without_flags[35])

# Fill Unused opcodes with NO OPS:
op_num = 0 # Give different name to every filler opcode to be able to construct a dictionary with no duplicate keys 
while len(instructions_without_flags) < 256:
    op_num += 1
    add_microcode(full_microcode(), f'FILLER_{op_num}')

# Key = The instruction string; Value = opcode 
opcodes_dict = {y[1]: x for x, y in instructions_without_flags.items()}
# Key = The opcode; Value = control word 
microcode_dict = {x : y[0] for x, y in instructions_without_flags.items()}
# Return opcode for each of these conditional instructions.
JZ   = opcodes_dict['JZ [@]']
JO   = opcodes_dict['JO [@]']
JN   = opcodes_dict['JN [@]']
JC   = opcodes_dict['JC [@]']
JNZ  = opcodes_dict['JNZ [@]']
JNO  = opcodes_dict['JNO [@]']
JP   = opcodes_dict['JP [@]'] # 0 to infinity
JGZ  = opcodes_dict['JGZ [@]']
JNC  = opcodes_dict['JNC [@]']



# Create a copy of the instructions for every flag combination
microcode = [deepcopy(microcode_dict) for x in range ((C_Flag  | Z_Flag | N_Flag  | O_Flag  | II_Flag | IRQ_Flag) + 1)]
# The interrupt code starts at address 16(10000). For now the microcode EPROM has 16 in general purpose register E. 
jump_to_interrupt_code = [ALU_ZERO | ZW, ZE | BRhW, EE | BRlW, _BRE | _PCW]
conditional_jump = [_PCE | ME | BRlW | PCC, _PCE | ME | BRhW, _BRE | _PCW]

def cond_jmp(instruction, jp = conditional_jump.copy()):
    '''
    Dynamically converts an unconditional instruction to a conditional instruction; moving the 
    position position of the step counter clear signal and using the jump argument as the specific jump code  
    '''
    
    jump = jp.copy()
    jump.append(_ScR)

    start = instruction.index(_ScR)
    end = start + len(jump)

    if (start + len(jump)) < len(instruction):
        instruction[start : end] = jump

    elif (start + len(jump)) == len(instruction):
        instruction[start: ] = jump

    else:
        print(f'ERROR!! NOT ENOUGH STEPS REMAINING TO FOR JUMP')
        exit()


def generate_microcode():
    global kk, xx
    # For every possible combination of flags
    for flags in range((II_Flag | IRQ_Flag | Z_Flag | O_Flag | N_Flag | C_Flag ) + 1):
        
        II  = flags & II_Flag 
        IRQ = flags & IRQ_Flag
        Z   = flags & Z_Flag  
        O   = flags & O_Flag  
        N   = flags & N_Flag  
        C   = flags & C_Flag  
        
        
        # If an interrupt service is requested while the interrupt 
        # inhibit signal is asserted; ignore the request.
        if IRQ & II:
           if Z:
               cond_jmp(microcode[flags][JZ]) 
           else:
               cond_jmp(microcode[flags][JNZ]) 
           
           if O:
               cond_jmp(microcode[flags][JO]) 
           else:
               cond_jmp(microcode[flags][JNO]) 
           
           if N: 
               cond_jmp(microcode[flags][JN]) 
           else:
               cond_jmp(microcode[flags][JP]) 
           
           if C:
              cond_jmp(microcode[flags][JC]) 
           else:
               cond_jmp(microcode[flags][JNC]) 
        
           if (not N and not Z):
               cond_jmp(microcode[flags][JGZ])

        # If an interrupt is requested, jump to interrupt 
        # code right after the current instruction has ended.
        elif IRQ:
            for opcode, control_word in microcode[flags].items():
                # Ignore reset and interrupt codes 
                if(opcode == 0 or opcode == 1): 
                    continue
                # Ignore filler instructions if any.
                if op_num:
                    if opcode in range((256 - op_num), 256):
                        continue
                #print(opcode, ':', instructions_without_flags[opcode][0])
                cond_jmp(control_word, jp = jump_to_interrupt_code)

        # When only the II flag is asserted; things should take their normal course

        else: # For all other flags

           if Z:
               cond_jmp(microcode[flags][JZ]) 
           else:
               cond_jmp(microcode[flags][JNZ]) 
           
           if O:
               cond_jmp(microcode[flags][JO]) 
           else:
               cond_jmp(microcode[flags][JNO]) 
           
           if N: 
               cond_jmp(microcode[flags][JN]) 
           else:
               cond_jmp(microcode[flags][JP]) 
           
           if C:
              cond_jmp(microcode[flags][JC]) 
           else:
               cond_jmp(microcode[flags][JNC]) 
        
           if (not N and not Z):
               cond_jmp(microcode[flags][JGZ])
 

generate_microcode()

def assign_rom(microcode_list, rom_number):
    """
    Normalizes control line activation and shift bits to their appropriate ROM.
    Takes a microcode list of dictionaries. 
    """
    # List of dictionaries
    EPROM = deepcopy(microcode_list)
    # For every dictionary in the list dict{}
    for microcode_dict in EPROM:
        # For every key/opcode in the dictionary 0b0..:
        for opcode in microcode_dict:
            # For every micro instruction steps at this opcode [a, b, c,...]
            for i, control_word in enumerate(microcode_dict[opcode]):
                # Normalize and trim word unless it is 0
                if microcode_dict[opcode][i] != 0:
                    microcode_dict[opcode][i] = trim_word(rom_number, al_norm(control_word))

    return EPROM

roms = [assign_rom(microcode, 0), assign_rom(microcode, 1), assign_rom(microcode, 2)]


def write_to_address(file, data):
    data = array.array('H', [data])
    file.write(data)


def generate_microcode_rom():
    for i, rom in enumerate(roms):
        print(f'\nWriting Microcode for rom_{i}', end ='')
        with open(f"microcode_rom_{i}.bin", 'wb') as file:
            for address in range(ROM_SIZE):
                
                if address% 5000 == 0:
                    print(f'.', end = ' ')

                opcode = (address & 0b111111110000000000) >> 10 
                flags_h = (address & 0b000000001100000000) >> 4 
                flags_l = address & 0b1111
                flags   = flags_h | flags_l
                step  = (address & 0b000000000011110000) >> 4

                write_to_address(file, rom[flags][opcode][step])

    print('\nDone!')

generate_microcode_rom()

#for instruction, details in instructions_without_flags.items():
#    print(f'    {details[1]} => {hex(instruction)}')

for instruction, details in instructions_without_flags.items():
    if ('MOV' in details[1] or 'ADD' in details[1] or 'SD' in details[1] or 'ALU' in details[1]) or details[1][0] == 'J':
        print(f'{details[1]}')
