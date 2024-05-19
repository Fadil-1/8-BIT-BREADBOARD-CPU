'''
Fadil Isamotu 
May 2024 (v1.0)
'''
from copy import deepcopy
import array
import traceback

INTPUT_WORD_SIZE = 18 # From 0 to 17 --> 18-bit word
ROM_SIZE = 2**INTPUT_WORD_SIZE

# ROM 0
_CLKW  = 1 <<  15  #  Clock speed select
_DW    = 1 <<  14  #  D Register(General purpose register 4) Write
_BW    = 1 <<  13  #  B Register(General purpose register 2) Write
H_cin  = 1 <<  12  #  Shift register carry in 
_SdE   = 1 <<  11  #  Segmented display enable
_HC    = 1 <<  10  #  Shift register clear/reset
ZS     = 1 <<  9   #  ALU select(0: 382 ALU; 1: 194-shift register)
Z2     = 1 <<  8   #  ALU control_2
Z1     = 1 <<  7   #  ALU control_1
_FW    = 1 <<  6   #  Flag register write/in
IR_in  = 1 <<  5   #  Instruction register in
TI     = 1 <<  4   #  Toggle interrupt(Sets interrupt to the opposite of its current state)
_OS    = 1 <<  3   #  OLED select(D/C# Data by default, command when asserted)
OR     = 1 <<  2   #  OLED data(Read/_Write Write by default, and read when asserted)
_OE     = 1 <<  1  #  OLED enable(Read/write: read when pulled high; write by default)
_OC    = 1         #  OLED clear

# ROM 1
EX     = 1 <<  31 #  Extra (Extra/Unused control line)
SdM    = 1 <<  30 #  Segmented display mode(Signed/_Unsigned)
Z0     = 1 <<  29 #  ALU control_0
_ScR   = 1 <<  28 #  Step counter reset to 0
BRlW   = 1 <<  27 #  Transfer Register lower byte write
_PChE  = 1 <<  26 #  Program counter upper byte enable
_PClE  = 1 <<  25 #  Program counter lower byte enable
_EE    = 1 <<  24 #  E Register(General purpose register 5) enable  
EW     = 1 <<  23 #  E Register(General purpose register 5) Write
Ex2    = 1 <<  22 #  Extra 2 (Extra/Unused control line 2)
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

## 74HCT238
SdW = WR_2 | WR_1 | WR_0 #  Segmented display write
IW  = WR_2 | WR_1        #  I Register(Interrupt Register) write
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
IE    =        RD_2 |        RD_0 #  I Register(Interrupt register) enable 
ME    =        RD_2               #  Memory enable to 8-bit bus 

active_low_lines = _CLKW | _DW | _BW | _HC  | _FW | _OE | _OS | _OC | _ScR | \
_PChE | _PClE | _EE | _PSE | _PSW | _SPC | _SPE | _MW | \
_BRE | _PCE | _PCW | _PS
 
ALU_ZERO           =                0
ALU_ACC_minus_BUS  =                Z0
ALU_BUS_minus_ACC  =           Z1
ALU_ADD            =           Z1 | Z0
ALU_XOR            =      Z2       
ALU_OR             =      Z2 |      Z0
ALU_AND            =      Z2 | Z1
ALU_FF             =      Z2 | Z1 | Z0
SHIFT_REG          = ZS 
SHIFT_REG_SL       = ZS |           Z0    
SHIFT_REG_SR       = ZS |      Z1

ALU_MIRROR_BUS     =    FLG_MIRROR_BUS   = ZS |      Z1 | Z0 # Writes bus content in the shift register.

FLG_CLC            = ZS | Z2
FLG_STC            = ZS | Z2  | Z0

II_Flag  = 0b100000 # Interrupt Inhibit Flag(Keep interrupt from taking effect)
IRQ_Flag =  0b10000 # Interrupt Request Flag(Pending interrupt)
Z_Flag   =   0b1000
O_Flag   =    0b100
N_Flag   =     0b10
C_Flag   =      0b1


"""
Each instruction is 8-bit(1-byte) long, and can make up instructions with up to 16 steps.
The EPROMs are input as follows: 

A_17  A_16  A_15  A_14  A_13  A_12  A_11  A_10  A_9  A_8     A_7  A_6  A_5  A_4  A_3  A_2  A_1  A_0
|     |     |     |     |     |     |     |      |    |       |    |    |    |    |    |    |    |
|                                         |      |    |       |              |    Z    O    N    C
|                                         |      | Pending    |              |    
|-----------------------------------------|      | Interrupt  |--------------|    
These are the instruction bits(2^8 = up to            |            These are the         
256 different instructions)                   Interrupt       steps bits(2^4             
                                              Inhibit         = 16 steps max)      
"""

def build_address(instruction=0b0, step=0b0, II=0b0, IR=0b0, Z=0b0, O=0b0, N=0b0, C=0b0):
   '''
   Organizes bit position of every element in the microcode input.
   If an element of the input word is not input it will default to 0.
   '''
   return instruction << 10 | step << 6 | II << 5 | IR << 4 | Z << 3 | O << 2 | N << 1 | C

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

# Keeps track of the current instruction's address.
adr = 0

FETCH = [_PCE | ME | IR_in | PCC] # Fetch micro code 

def full_microcode(t_1 = 0, t_2 = 0, t_3 = 0, t_4 = 0, t_5 = 0, t_6 = 0,
                    t_7 = 0, t_8 = 0, t_9 = 0, t_10 = 0, t_11 = 0,
                      t_12 = 0, t_13 = 0, t_14 = 0, t_15 = 0):
    """
    Creates full microcode for a single instruction and ends it by resetting the step counter.
    Note that, the maximum number of micro steps allowed when using this function is 15, as 
    t_0 is automatically prepended with the fetch cycle. 
    """
    global adr

    steps = [t_1, t_2, t_3, t_4, t_5, t_6, t_7, t_8, 
             t_9, t_10, t_11, t_12, t_13, t_14, t_15]
    
    for i, step in enumerate(steps):
        if step == 0:
            steps[i] = _ScR
            break

    steps = FETCH + steps
    adr += 1

    return steps


instructions_without_flags = dict()
recycling_address = []

def add_microcode(micro_operations, name):
    '''
    Updates the instructions_without_flags dictionary 
    with the current address as the key, and (micro_operations, name) as the value.
    '''
    instructions_without_flags[adr] = micro_operations, name

'''
$   Register
#   Number
@   Address
[]  Memory location
[@] Address at a memory location
[#] Number at a memory location
'''

ABCD = ['A' ,'B' ,'C' ,'D']

# All registers' write lines
write_to_reg = {'A': AW, 
                'B': _BW, 
                'C':CW, 
                'D':_DW,
                'E': EW,
                'I': IW}

# All registers enable lines
enable_reg = {'A': AE, 
              'B': BE, 
              'C': CE, 
              'D': DE,
              'E': _EE,
              'I': IE}


####################
### RESET VECTOR ###
####################
INACTIVE = al_norm(active_low_lines)
instructions_without_flags[adr] =([ ALU_ZERO | ZW | _OC,                                    
                                    ALU_ZERO | ZW | _OC,                                
                                    ZE | AW  | BRlW | BRhW | IR_in | _OC,                    
                                    ZE | CW  | _BRE | SPW  | FLG_MIRROR_BUS | _FW | _OC,     
                                    ZE | SdT | _SPC | SPD,                             
                                    ZE | SdW | _BW | _DW | EW | SHIFT_REG_SR | H_cin,  
                                    SHIFT_REG | ZW,                                    
                                    ZE | SHIFT_REG_SR | H_cin,                         
                                    SHIFT_REG | ZW,                                    
                                    ZE | BRhW,                                         
                                    _BRE | _PCW,                                       
                                    TI,                           
                                    INACTIVE, INACTIVE, INACTIVE, 
    
    
                                    _PCE | ME | IR_in],                       
                                    f'RST')
#################
### Set carry ### 
#################
add_microcode(full_microcode(FLG_STC | _FW), f'STC')

########################
## Reset/Clear carry ### 
########################
add_microcode(full_microcode(FLG_CLC | _FW), f'CLC')

#################
### IMMEDIATE ###
#################
for dest in ABCD:
    add_microcode(full_microcode(_PCE | ME | write_to_reg[dest] | PCC), 
                                 f'MOV ${dest}, #') 
    add_microcode(full_microcode(enable_reg[dest] | ALU_MIRROR_BUS,
                                 SHIFT_REG | ZW,
                                _PCE | ME | ALU_ADD | ZW | _FW,  
                                write_to_reg[dest] | ZE | PCC),
                                f'ADD ${dest}, #') 
    add_microcode(full_microcode(enable_reg[dest] | ALU_MIRROR_BUS,
                                 SHIFT_REG | ZW,
                                 _PCE | ME | ALU_ACC_minus_BUS | ZW | _FW,
                                 write_to_reg[dest] | ZE | PCC), 
                                 f'SUB ${dest}, #')
    add_microcode(full_microcode(enable_reg[dest] | ALU_MIRROR_BUS,
                                 SHIFT_REG | ZW,
                                 _PCE | ME | ALU_AND | ZW | _FW,  
                                 write_to_reg[dest] | ZE | PCC), 
                                 f'AND ${dest}, #')
    add_microcode(full_microcode(enable_reg[dest] | ALU_MIRROR_BUS,
                                 SHIFT_REG | ZW,
                                 _PCE | ME | ALU_OR | ZW | _FW,  
                                 write_to_reg[dest] | ZE | PCC), 
                                 f'OR ${dest}, #')
    add_microcode(full_microcode(enable_reg[dest] | ALU_MIRROR_BUS,
                                 SHIFT_REG | ZW,
                                 _PCE | ME | ALU_XOR | ZW | _FW,  
                                 write_to_reg[dest] | ZE | PCC), 
                                 f'XOR ${dest}, #')
    add_microcode(full_microcode(enable_reg[dest] | ALU_MIRROR_BUS,
                                 SHIFT_REG | ZW,
                                 _PCE | ME | ALU_ACC_minus_BUS | _FW | PCC), 
                                 f'CMP ${dest}, #')

## IMMEDIATE WITH E
add_microcode(full_microcode(_PCE | ME | write_to_reg[dest] | PCC),
                             f'MOV $E, #')

add_microcode(full_microcode(enable_reg['E'] | ALU_MIRROR_BUS,
                             SHIFT_REG | ZW,
                             _PCE | ME | ALU_ADD | ZW | _FW,  
                             write_to_reg['E'] | ZE | PCC),
                             f'ADD $E, #') 

add_microcode(full_microcode(enable_reg['E'] | ALU_MIRROR_BUS,
                             SHIFT_REG | ZW,
                             _PCE | ME | ALU_ACC_minus_BUS | ZW | _FW,
                             write_to_reg['E'] | ZE | PCC), 
                             f'SUB $E, #')

add_microcode(full_microcode(enable_reg['E'] | ALU_MIRROR_BUS,
                             SHIFT_REG | ZW,
                             _PCE | ME | ALU_ACC_minus_BUS | _FW | PCC), 
                             f'CMP $E, #') 

                                                 

## DIRECT REGISTER WITH E
for reg in ABCD:
    add_microcode(full_microcode(write_to_reg[reg] | enable_reg['E']), 
                                 f'MOV ${reg}, $E')   
    
    add_microcode(full_microcode(write_to_reg['E'] | enable_reg[reg]), 
                                 f'MOV $E, ${reg}')
    
    add_microcode(full_microcode(enable_reg['E'] | ALU_MIRROR_BUS,
                                 SHIFT_REG | ZW,
                                 enable_reg[reg] | ALU_ACC_minus_BUS | _FW), 
                                 f'CMP $E, {reg}')


#####################
### CLOCK CONTROL ###
#####################

# CLK IMMEDIATE
add_microcode(full_microcode(_PCE | ME | _CLKW, PCC), # Select I/O from RAM content.
                            f'MOV $CLK, #') 

# CLK DIRECT REGISTER
add_microcode(full_microcode(_CLKW | enable_reg['E']), 
                                 f'MOV $CLK, $E')

#######################
### DIRECT REGISTER ###
#######################
for dest in ABCD:
    for src in ABCD:
        if dest == src:
            continue

        add_microcode(full_microcode(write_to_reg[dest] | enable_reg[src]), 
                                    f'MOV ${dest}, ${src}')

        add_microcode(full_microcode(enable_reg[dest] | ALU_MIRROR_BUS,
                                     SHIFT_REG | ZW,
                                     enable_reg[src] | ALU_ADD |_FW | ZW,  
                                     write_to_reg[dest] | ZE), 
                                    f'ADD ${dest}, ${src}')
        add_microcode(full_microcode(enable_reg[dest] | ALU_MIRROR_BUS,
                                     SHIFT_REG | ZW,
                                     enable_reg[src] | ALU_ACC_minus_BUS | _FW | ZW,  
                                     write_to_reg[dest] | ZE), 
                                    f'SUB ${dest}, ${src}')
        add_microcode(full_microcode(enable_reg[dest] | ALU_MIRROR_BUS,
                                     SHIFT_REG | ZW,
                                     enable_reg[src] | ALU_AND |_FW | ZW,  
                                     write_to_reg[dest] | ZE), 
                                    f'AND ${dest}, ${src}')
        add_microcode(full_microcode(enable_reg[dest] | ALU_MIRROR_BUS,
                                     SHIFT_REG | ZW,
                                     enable_reg[src] | ALU_OR |_FW | ZW,  
                                     write_to_reg[dest] | ZE), 
                                    f'OR ${dest}, ${src}')
        add_microcode(full_microcode(enable_reg[dest] | ALU_MIRROR_BUS,
                                     SHIFT_REG | ZW,
                                     enable_reg[src] | ALU_XOR |_FW | ZW,  
                                     write_to_reg[dest] | ZE), 
                                    f'XOR ${dest}, ${src}')      
        add_microcode(full_microcode(enable_reg[dest] | ALU_MIRROR_BUS,
                                     SHIFT_REG | ZW,
                                     enable_reg[src] | ALU_ACC_minus_BUS |_FW), 
                                    f'CMP ${dest}, ${src}')

#########################
### INDIRECT REGISTER ###
#########################

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

        add_microcode(full_microcode(CE | BRlW,
                                     DE | BRhW,
                                     enable_reg[dest] | ALU_MIRROR_BUS,
                                     SHIFT_REG | ZW,
                                     _BRE | ME | ALU_ADD | ZW | _FW,
                                     write_to_reg[dest] | ZE ),
                                    f'ADD ${dest}, [$CD]')
        
        add_microcode(full_microcode(CE | BRlW,
                                     DE | BRhW,
                                     enable_reg[dest] | ALU_MIRROR_BUS,
                                     SHIFT_REG | ZW,
                                     _BRE | ME | ALU_ACC_minus_BUS | ZW | _FW,
                                     write_to_reg[dest] | ZE ),
                                    f'SUB ${dest}, [$CD]')
        
        add_microcode(full_microcode(CE | BRlW,
                                     DE | BRhW,
                                     enable_reg[dest] | ALU_MIRROR_BUS,
                                     SHIFT_REG | ZW,
                                     _BRE | ME | ALU_AND | ZW | _FW,
                                     write_to_reg[dest] | ZE ),
                                    f'AND ${dest}, [$CD]')
        
        add_microcode(full_microcode(CE | BRlW,
                                     DE | BRhW,
                                     enable_reg[dest] | ALU_MIRROR_BUS,
                                     SHIFT_REG | ZW,
                                     _BRE | ME | ALU_OR | ZW | _FW,
                                     write_to_reg[dest] | ZE ),
                                    f'OR ${dest}, [$CD]')
        
        add_microcode(full_microcode(CE | BRlW,
                                     DE | BRhW,
                                     enable_reg[dest] | ALU_MIRROR_BUS,
                                     SHIFT_REG | ZW,
                                     _BRE | ME | ALU_XOR | ZW | _FW,
                                     write_to_reg[dest] | ZE ),
                                    f'XOR ${dest}, [$CD]')
        
        add_microcode(full_microcode(CE | BRlW,
                                     DE | BRhW,
                                     enable_reg[dest] | ALU_MIRROR_BUS,
                                     SHIFT_REG | ZW,
                                     _BRE | ME | ALU_ACC_minus_BUS | _FW),
                                    f'CMP ${dest}, [$CD]')

#########################
### ABSOLUTE REGISTER ###
#########################
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
                                enable_reg[dest] | ALU_MIRROR_BUS | PCC,
                                SHIFT_REG | ZW,
                                _BRE | ME | ALU_ADD | ZW | _FW,
                                write_to_reg[dest] | ZE ),
                                f'ADD ${dest}, [@]')
    add_microcode(full_microcode(_PCE | ME | BRlW | PCC,
                                _PCE | ME | BRhW, 
                                enable_reg[dest] | ALU_MIRROR_BUS | PCC,
                                SHIFT_REG | ZW,
                                _BRE | ME | ALU_ACC_minus_BUS | ZW | _FW,
                                write_to_reg[dest] | ZE ), 
                                f'SUB ${dest}, [@]')
    add_microcode(full_microcode(_PCE | ME | BRlW | PCC,
                                _PCE | ME | BRhW, 
                                enable_reg[dest] | ALU_MIRROR_BUS | PCC,
                                SHIFT_REG | ZW,
                                _BRE | ME | ALU_AND | ZW | _FW,
                                write_to_reg[dest] | ZE ), 
                                f'AND ${dest}, [@]')
    add_microcode(full_microcode(_PCE | ME | BRlW | PCC,
                                _PCE | ME | BRhW, 
                                enable_reg[dest] | ALU_MIRROR_BUS | PCC,
                                SHIFT_REG | ZW,
                                _BRE | ME | ALU_OR | ZW | _FW,
                                write_to_reg[dest] | ZE ), 
                                f'OR ${dest}, [@]')
    add_microcode(full_microcode(_PCE | ME | BRlW | PCC,
                                _PCE | ME | BRhW, 
                                enable_reg[dest] | ALU_MIRROR_BUS | PCC,
                                SHIFT_REG | ZW,
                                _BRE | ME | ALU_XOR | ZW | _FW,
                                write_to_reg[dest] | ZE ), 
                                f'XOR ${dest}, [@]')
    add_microcode(full_microcode(_PCE | ME | BRlW | PCC,
                                _PCE | ME | BRhW, 
                                enable_reg[dest] | ALU_MIRROR_BUS | PCC,
                                SHIFT_REG | ZW,
                                _BRE | ME | ALU_ACC_minus_BUS | _FW),
                                f'CMP ${dest}, [@]') 
###########
### I/O ###
###########

## SEGMENTED DISPLAY

# Lower byte of a number
add_microcode(full_microcode(enable_reg['A'] | SdT), 
                                f'SDL $A')
add_microcode(full_microcode(enable_reg['B'] | SdT), 
                                f'SDL $B')

# Higher byte of a number
add_microcode(full_microcode(enable_reg['A'] | SdW), 
                                f'SDH $A')
add_microcode(full_microcode(enable_reg['B'] | SdW), 
                                f'SDH $B')

## Port Selector
# Output: Write content in RA to port selected from memory content.  
add_microcode(full_microcode(_PCE | ME | _PS | PCC, 
                             AE | _PSW),            
                            f'OUT #, RA')

# Input: Write content in port from memory content to RA.  
add_microcode(full_microcode(_PCE | ME | _PS | PCC, 
                             AW | _PSE),            
                            f'INP RA, #')

# Output: Write content of RA to port in RB.
add_microcode(full_microcode(BE | _PS,         
                             AE | _PSW),       
                            f'OUT RB, RA')

# INPUT: Write content from port in RB to RA.
add_microcode(full_microcode(BE | _PS,         
                             AW | _PSE),       
                            f'INP RA, RB')

## OLED DISPLAY
# Reset
add_microcode(full_microcode(_OC,_OC,_OC,_OC,_OC,_OC), f'OLR')

# Data immediate
add_microcode(full_microcode(_PCE | ME, 
                             _OE | _PCE | ME | PCC),
                            f'OLD #')

add_microcode(full_microcode(_OS | _PCE | ME,
                             _OE |  _OS | _PCE | ME | PCC),
                            f'OLC #')

# Data direct register
add_microcode(full_microcode(enable_reg['A'],
                            _OE | enable_reg['A']),
                            f'OLD $A')

add_microcode(full_microcode(enable_reg['B'],
                            _OE | enable_reg['B']),
                            f'OLD $B')

# Command direct register
add_microcode(full_microcode(_OS | enable_reg['A'],
                             _OS | _OE | enable_reg['A']),
                            f'OLC $A')

add_microcode(full_microcode(_OS | enable_reg['B'],
                             _OS | _OE | enable_reg['B']),
                            f'OLC $B')

#############
### SHIFT ###
#############

## Left Shift

# Register
for src in ABCD:
    add_microcode(full_microcode(enable_reg[src] | SHIFT_REG_SL | _FW, 
                                 SHIFT_REG | ZW,                       
                                 write_to_reg[src] | ZE),              
                                 f'LSL ${src}')
# Address
add_microcode(full_microcode(_PCE | ME | BRlW | PCC, 
                             _PCE | ME | BRhW,       
                             _BRE | ME | SHIFT_REG_SL | _FW, 
                             SHIFT_REG | ZW | PCC,     
                             _BRE | ZE | _MW ),        
                            'LSL [@]')
# Indirect
add_microcode(full_microcode( CE | BRlW, 
                              DE | BRhW, 
                             _BRE | ME | SHIFT_REG_SL | _FW,
                              SHIFT_REG | ZW,                
                             _BRE | ZE | _MW ),              
                            'LSL [$CD]')
###################
### Right Shift ###
###################

## Register
for src in ABCD:
    add_microcode(full_microcode(enable_reg[src] | SHIFT_REG_SR | _FW, 
                                 SHIFT_REG | ZW,                       
                                 write_to_reg[src] | ZE),              
                                 f'LSR ${src}')
## Address
add_microcode(full_microcode(_PCE | ME | BRlW | PCC, 
                             _PCE | ME | BRhW,       
                             _BRE | ME | SHIFT_REG_SR | _FW,
                             SHIFT_REG | ZW | PCC,       
                             _BRE | ZE | _MW ),          
                            'LSR [@]')
## Indirect
add_microcode(full_microcode( CE | BRlW, 
                              DE | BRhW, 
                             _BRE | ME | SHIFT_REG_SR | _FW, 
                              SHIFT_REG | ZW,                
                             _BRE | ZE | _MW ),              
                            'LSR [$CD]')

#################
### PUSH/PULL ###
#################

# Register
for reg in ABCD:
    add_microcode(full_microcode(enable_reg[reg] | _SPE | _MW | SPD,
                                 _SPC | SPD ),
                                 f'PSH ${reg}')
    add_microcode(full_microcode(_SPC,
                                 write_to_reg[reg] | _SPE | ME),
                                 f'PUL ${reg}')
# Flags   
add_microcode(full_microcode(FE | _SPE | _MW | SPD,
                             _SPC | SPD),
                             f'PSF')


add_microcode(full_microcode(_SPC | ALU_ZERO | ZW,       
                             _SPE | ME | ALU_OR | _FW),  
                             f'PLF')              

#####################
### STACK POINTER ###
#####################
add_microcode(full_microcode( CE | BRlW,
                              DE | BRhW,
                             _BRE | SPW ),
                             f'MOV $SP, $CD')

add_microcode(full_microcode(SPlE | CW,
                             SPhE | _DW),
                             f'MOV $CD, $SP')

#############
### JUMPS ###
#############
add_microcode(full_microcode(_PCE | ME | BRlW | PCC,
                             _PCE | ME | BRhW ,
                             _BRE | _PCW),
                             f'JMP [@]')

add_microcode(full_microcode(_PCE | ME | BRlW | PCC,
                             _PCE | ME | BRhW | PCC,
                             _PClE | _SPE | _MW | SPD,
                             _SPC | SPD,
                             _PChE | _SPE | _MW | SPD,
                             _BRE | _PCW | _SPC | SPD),
                             f'JSR [@]')

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

##############################
### RETURN FROM SUBROUTINE ### 
##############################
add_microcode(full_microcode(_SPC,
                            BRhW | _SPE | ME,
                            _SPC,
                            BRlW | _SPE | ME,
                            _BRE | _PCW ), 
                            f'RTS')

#########################
### CONDITIONAL JUMPS ###
#########################

# Jump if zero
add_microcode(full_microcode(PCC,
                             PCC),
                             f'JZ [@]')
# Jump if overflow
add_microcode(full_microcode(PCC,
                             PCC),
                             f'JO [@]')
# Jump if lower than zero
add_microcode(full_microcode(PCC,
                             PCC),
                             f'JN [@]')
# Jump if carry
add_microcode(full_microcode(PCC,
                             PCC),
                             f'JC [@]')
# Jump if not zero
add_microcode(full_microcode(PCC,
                             PCC),
                             f'JNZ [@]')
# Jump if not overflow
add_microcode(full_microcode(PCC,
                             PCC),
                             f'JNO [@]')

# Jump if positive (JGZ including Z)
add_microcode(full_microcode(PCC,
                             PCC),
                             f'JP [@]')
# Jump if not carry
add_microcode(full_microcode(PCC,
                             PCC),
                             f'JNC [@]')
# Jump if greater than zero
add_microcode(full_microcode(PCC,
                             PCC),
                             f'JGZ [@]')

#################
### INTERRUPT ###
#################

# SET II
add_microcode(full_microcode(),    # Write content of RA to selected I/O
                            f'SII')

# CLEAR II
add_microcode(full_microcode(),    # Write content of RA to selected I/O
                            f'CII')

# INTERRUPT HANDLER
add_microcode(full_microcode(TI | FE | _SPE | _MW | ALU_FF | ZW | SPD,                             
                              ZE | SHIFT_REG_SL | BRhW | _SPC | SPD,                             
                              _PClE | _SPE | _MW | SHIFT_REG | ZW | SPD,                            
                              ZE | BRlW | _SPC | SPD,  
                              _PChE | _SPE | _MW | ALU_FF | ZW | SPD, 
                              _BRE | ME | ALU_AND | ZW | _SPC | SPD,   
                              ZE | _SPE | _MW | SPD,                                  
                              ALU_FF | ZW,                   
                              ZE | BRlW,                     
                              _BRE | ME | ALU_AND | ZW,      
                              ZE | BRhW,                     
                              _SPE | ME | BRlW,              
                              _BRE | _PCW | FLG_CLC | _FW),                  
                              "ITR")
interrupt_handler_address = adr

# RETURN FROM INTERRUPT  
add_microcode(full_microcode( _SPC,
                              BRhW | _SPE | ME,
                              _SPC,
                              BRlW | _SPE | ME,
                              _BRE | _PCW | _SPC,
                              _SPE | ME | FLG_MIRROR_BUS | _FW | TI), 
                              f'RTI')

#############
### NO OP ### 
#############
add_microcode(full_microcode(), f'NOP')

############
### HALT ###
############
add_microcode(full_microcode(HLT), f'HLT')



# Fill Unused instructions with NO OPS:
number_of_fillers = 0 
while len(instructions_without_flags) < 256:
    number_of_fillers += 1
    add_microcode(full_microcode(), f'FILLER_{number_of_fillers}')


# Key = The instruction string/name; Value = instruction 
instructions_dict = {y[1]: x for x, y in instructions_without_flags.items()}
# Key = The instruction; Value = control word 
microcode_dict = {x : y[0] for x, y in instructions_without_flags.items()}

if len(instructions_without_flags) > 256: 
    print("Instructions exceed 256")
    exit()

# Returns instruction for each of these conditional instructions.
JZ   = instructions_dict['JZ [@]']
JO   = instructions_dict['JO [@]']
JN   = instructions_dict['JN [@]']
JC   = instructions_dict['JC [@]']
JNZ  = instructions_dict['JNZ [@]']
JNO  = instructions_dict['JNO [@]']
JP   = instructions_dict['JP [@]']
JGZ  = instructions_dict['JGZ [@]']
JNC  = instructions_dict['JNC [@]']
SII  = instructions_dict['SII']
CII  = instructions_dict['CII']

# Creates a copy of the micro-code dictionary for every flags combination.
microcode = [deepcopy(microcode_dict) for x in range ((C_Flag  | Z_Flag | N_Flag  | O_Flag  | II_Flag | IRQ_Flag) + 1)]


# CONDITIONAL JUMPS MICRO-OPERATIONS
# The interrupt code starts at address 16(10000). Register I is hardwired to 16. 
jump_to_interrupt_handler = [ALU_ZERO | ZW | IW, # Writes 0 into the accumulator, and makes sure the hard wired value on the interrupt register is written.
                          ZE | BRhW,          # Writes 0 into upper byte of bridge.
                          IE | BRlW,          # Writes interrupt address into lower byte of bridge.
                          _BRE | _PCW,        # Writes location of interrupt code in PC. 
                          _ScR]               # End the microcode by resetting the step counter.


# JMP @ instruction 
conditional_jump = FETCH + [_PCE | ME | BRlW | PCC, # Writes RAM content at PC address to lower byte of bridge, increment PC by 1.
                    _PCE | ME | BRhW,       # Writes RAM content at PC address + 1 to upper byte of bridge.
                    _BRE | _PCW,            # Writes content of bridge into PC. # End the microcode by resetting the step counter.
                    _ScR]                   # End the microcode by resetting the step counter.

# Interrupt Inhibit
set_II = clear_II = FETCH + [TI, 
                            _ScR]


def cond_jmp(micro_operations, jp = conditional_jump.copy()):
    """
    Dynamically converts an unconditional instruction to a conditional instruction; moving the 
    position of the step counter clear signal and using the jump argument as the specific jump code. 
    """
    
    jump = jp.copy()
 
    if jump != jump_to_interrupt_handler:
        micro_operations [:] = jump  + (16-len(jump))*[0] # Fill the rest of the list with zeros till it reaches length 16

    else:

        start = micro_operations.index(_ScR) 
        new_instruction_length = end = start + len(jump)

        if new_instruction_length < 16:
            micro_operations[start : end] = jump

        elif new_instruction_length == 16:
            micro_operations[start: ] = jump

        # Safeguard in case of lengths greater than 16.
        else:
            raise ValueError()
    



def generate_microcode():
    global kk, xx
    # For every possible combination of flags
    for flags in range((II_Flag | IRQ_Flag | Z_Flag | O_Flag | N_Flag | C_Flag ) + 1):
        '''
        ANDing with the current flag combination basically defines 
        which flag is active in this value/iteration of the loop.
        EX: If loop is at 010010, IRQ and N would be HIGH, from teh set of ANDs below.
        '''
    
        II  = flags & II_Flag 
        IRQ = flags & IRQ_Flag
        Z   = flags & Z_Flag  
        O   = flags & O_Flag  
        N   = flags & N_Flag  
        C   = flags & C_Flag  
        
        try:
        
            # If an interrupt service is requested while the interrupt 
            # inhibit signal is asserted; ignore the request.
            if IRQ and II:

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


            elif IRQ:
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

                # Loop into all of the ocpodes for the current flags combination
                for instruction, micro_operations in microcode[flags].items():
                    # Ignore reset and interrupt codes 
                    if(instruction == 0 or instruction == interrupt_handler_address): 
                        continue
                    # Ignore filler instructions if any.
                    if number_of_fillers:
                        if instruction in range((256 - number_of_fillers), 256):
                            continue
                    # Add the micro-operations to jump to the interrupt code.
                    cond_jmp(micro_operations, jp = jump_to_interrupt_handler)
            

            elif II:

                cond_jmp(microcode[flags][CII], clear_II) 

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

            else:

                cond_jmp(microcode[flags][SII], set_II) 

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

        except Exception as e:
            trace = traceback.format_exc()
            print(f"ERROR!! NOT ENOUGH STEPS REMAINING FOR JUMP\n{trace}")
            exit()

generate_microcode()


def assign_rom(microcode_list, rom_number):
    """
    Normalizes control line activation and shift bits to their appropriate ROM.
    Takes a microcode list of dictionaries. 
    """
    # List of dictionaries
    EPROM = deepcopy(microcode_list)
    # For every dictionary in the list of dictionaries
    for microcode_dict in EPROM:
        # For every key/instruction in every dictionary:
        for instruction in microcode_dict:
            # For every micro-operation at this instruction [a, b, c,...]
            for i, control_word in enumerate(microcode_dict[instruction]):
                microcode_dict[instruction][i] = trim_word(rom_number, al_norm(control_word))
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
                if address % 5000 == 0:
                    print(f'.', end = ' ')

                instruction = (address & 0b111111110000000000) >> 10 
                flags_h = (address & 0b00000001100000000) >> 4 # Shifts only by four because it is ORed with the 4-bit ZONC
                flags_l = address & 0b1111
                flags   = flags_h | flags_l
                step  = (address & 0b000000000011110000) >> 4
                write_to_address(file, rom[flags][instruction][step])
    print('\nDone!')

generate_microcode_rom()

def generate_ruledef():
    '''
    Generates a ruledef.asm directive file for Customasm in Little Endian.
    '''
    with open('ruledef.asm', 'w') as ruledef:

        ruledef.writelines('#ruledef\n{\n')

        for i, (instruction, _) in enumerate(instructions_dict.items()):

            instruction = instruction.split()

            end =''

            ruledef.writelines('    ')

            for z in instruction:
            
                if '@' in z:
                    end += '@ le(address)'
                    ruledef.writelines(z.replace('@', 'address: u16').replace('[', '{').replace(']', '}').ljust(5))

                elif '#' in instruction:
                    end = '@ im'
                    #end = ''
                    ruledef.writelines(z.replace('#', '{im: i8}').ljust(5))
                else:
                    end += ''
                    ruledef.writelines(z.ljust(5))
 
            ruledef.writelines(f" => 0x{i:02x} {end}\n") 
        ruledef.writelines('}')

#generate_ruledef()