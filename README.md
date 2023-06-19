# 8-BIT-BREADBOARD-CPU
This project is a detailed overview and repository for my 8-bit breadboard computer. Like most breadboard computers on te internet today, the design is inspired by Ben Eater's's 8-bit CPU series. My build is expanded to include various additional features such as an OLED display, SPI BUS, and 48-K-byte of RAM.


![](https://drive.google.com/uc?export=view&id=1J6w5AhHXn8bqoUTQK_zxlKinYP8Q_5Fw)




## Acknowledgment

A HUGE thank you to [ULF_Casper](https://github.com/DerULF1) for his 8-bit CPU series. His design, especially the interrupt handling design and the PS2 module, served as a foundation for the I/O in my build. The PS2 module is so well-implemented that I integrated it into my build with no changes.

## Features

- Programmable clock speed(Chosen from 8 different clockspeeds)
- 16-bit program Counter
- 16-bit stack Pointer
- Transfer register between data and address bus (termed as the Bridge Register (BR) in codes)
- 16-bit Output register
- PS2 keyboard decoder
- 16-bit 14-segment display(signed and unsigned 16-bit intergers for now)
- SPI BUS connected to an Adafruit Bluetooth receiver and an SD card slot.
- 128 x 64 monochrome OLED display
- 48-K-byte of RAM(Remaining 16-k-byte address space is used for an operating system and stack memory)
- ALU with Shift (LSR LSR) AND, ADD, SUB, OR, XOR
- 7 flags:: Four ALU flags: (Z-O-N-C) in writable 4-bit register; and two interrupt flags
- 6 general purpose registers: A, B, C, D, E, G
- 4-bit microcode step counter(With dynamic microsteps reset)


![Breadboard Layout](https://drive.google.com/uc?export=view&id=1zukj_0ZykpeB-WHHXUYvnjysiwniDT3_)


## Current Control Words

| Control Word  |                               Description                              |
| ------------- | -----------------------------------------------------------------------|
| CLKW          |  Clock speed select                                                    |
| DW            |  D Register(General purpose register 4) Write                          |
| BW            |  B Register(General purpose register 2) Write                          |
| Hcin          |  Shift register carry in                                               |
| HC            |  Shift register clear/reset                                            |
| ZS            |  ALU select(0: 382 ALU; 1: 194-shift register)                         |
| Z2            |  ALU control2                                                          |
| Z1            |  ALU control1                                                          |
| FW            |  Flag register write/in                                                |
| IRin          |  Instruction register in                                               |
| TI            |  Toggle interrupt(Sets interrupt to the opposite of its current state) |
| OS            |  OLED select(D/C# Data by default, command when asserted)              |
| OR            |  OLED data(Read/Write Write by default, and read when asserted)        |
| OE            |  OLED enable(Read/write is enabled when pulled high)                   |
| OC            |  OLED clear                                                            |
| EX            |  Extra (Extra/Unused control line)                                     |
| SdM           |  Segmented display mode(Signed/Unsigned)                               |
| Z0            |  ALU control0                                                          |
| ScR           |  Step counter reset to 0                                               |
| BRlW          |  Transfer Register lower byte write                                    |
| PChE          |  Program counter upper byte enable                                     |
| PClE          |  Program counter lower byte enable                                     |
| GE            |  G Register(General purpose register 6) enable                         |
| GW            |  G Register(General purpose register 6) Write                          |
| OO            |  OLED transceiver enable                                               |
| PSE           |  Port selector enable                                                  |
| PSW           |  Port selector write                                                   |
| HLT           |  Clock halt/stop                                                       |
| SPW           |  Stack pointer load                                                    |
| SPD           |  Stack pointer count direction(up/down)                                |
| SPC           |  Stack pointer count enable                                            |
| SPE           |  Stack pointer word(16-bits) enable                                    |
| BRhW          |  Transfer Register upper byte write                                    |
| MW            |  Memory write                                                          |
| ZW            |  Accumulator write                                                     |
| BRE           |  Transfer Register word(16-bits) enable                                |
| PCE           |  Program counter word(16-bits) enable                                  |
| PCC           |  Program counter count up                                              |
| PCW           |  Program counter write/in (Jump)                                       |
| PS            |  Port select in                                                        |
| WR2           |  Write decoder A2                                                      |
| WR1           |  Write decoder A1                                                      |
| WR0           |  Write decoder A0                                                      |
| RD3           |  Read decoder A3                                                       |
| RD2           |  Read decoder A2                                                       |
| RD1           |  Read decoder A1                                                       |
| RD0           |  Read decoder A0                                                       |
| SdW           |  Segmented display write                                               |
| EW            |  E Register(General purpose register 5) write                          |
| SdT           |  Segmented display's temporary register(lower byte) write              |
| CW            |  C Register(General purpose register 3) write                          |
| AW            |  A Register(General purpose register 1) write                          |
| ZE            |  Accumulator enable                                                    |
| DE            |  D Register(General purpose register 4) enable                         |
| CE            |  C Register(General purpose register 3) enable                         |
| AE            |  A Register(General purpose register 1) enable                         |
| BE            |  B Register(General purpose register 2) enable                         |
| FE            |  Flags Register enable                                                 |
| BRhE          |  Transfer Register Upper byte Enable                                   |
| BRlE          |  Transfer Register Lower byte Enable                                   |
| SPhE          |  Stack Pointer Upper byte Enable                                       |
| SPlE          |  Stack Pointer lower byte Enable                                       |
| EE            |  E Register(General purpose register 5) enable                         |
| ME            |  Memory enable to 8-bit bus                                            |

More detailed descriptions and schematics for each module can be found in the respective folders.

