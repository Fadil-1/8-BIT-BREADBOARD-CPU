# 8-BIT-BREADBOARD-CPU
This project is a detailed overview and repository for my 8-bit breadboard computer. Like most breadboard computers on the internet today, the design is inspired by ![Ben Eater](https://github.com/beneater)'s ![8-bit CPU series](https://www.youtube.com/playlist?list=PLowKtXNTBypGqImE405J2565dvjafglHU). My build is expanded to include various additional features such as an OLED display, SPI BUS, and 48 KB of RAM.

![Full](https://github.com/Fadil-1/8-BIT-BREADBOARD-CPU/blob/main/images/full.jpg?raw=true)

## Acknowledgment

A HUGE thank you to [ULF_Casper](https://github.com/DerULF1) for his 8-bit CPU ![series](https://www.youtube.com/playlist?list=PL5-Ar_CvItgaP27eT_C7MnCiubkyaEqF0). His design, especially the interrupt handling design and the PS2 module, served as a foundation for the I/O in my build. The PS2 module is so well-implemented that I integrated it into my build with no changes.

## Features

- Programmable clock speed(Chosen from 8 different clockspeeds)
- 16-bit program Counter
- 16-bit stack Pointer
- Transfer register between data and address bus (termed as the Bridge Register (BR) in codes)
- 16-bit Output register
- PS2 keyboard decoder
- 16-bit 14-segment display (signed and unsigned 16-bit intergers for now)
- SPI BUS connected to an Adafruit Bluetooth receiver and an SD card slot.
- 128 x 64 monochrome OLED display
- 48-K-byte of RAM(Remaining 16-k-byte address space is used for a bootloader and stack memory)
- ALU with Shift (LSR LSR) AND, ADD, SUB, OR, XOR
- 7 flags:: Four ALU flags: (Z-O-N-C) in writable 4-bit register; and two interrupt flags
- 6 general purpose registers: A, B, C, D, E, G
- 4-bit microcode step counter(With dynamic microsteps reset)

![Breadboard Layout](https://github.com/Fadil-1/8-BIT-BREADBOARD-CPU/blob/main/images/Layout.png?raw=true)

## Architecture

![Modules Block Diagram](https://github.com/Fadil-1/8-BIT-BREADBOARD-CPU/blob/main/images/architecture.png?raw=true)

More detailed descriptions and schematics for each module can be found in the respective folders.