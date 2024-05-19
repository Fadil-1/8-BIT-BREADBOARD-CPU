;----------------------------------------------------------------------
; Bounces between start and end of numbers within 16 bits.
; range[0 : 65535] on 6-digit 14-segment display (Works on microcode V1)
;----------------------------------------------------------------------

#include "ruledef.asm"

; Offsets the starting address to the boot loader ROM's location (0xC000) to align jump operations.
#addr 0xC000 

; Initializes registers
MOV $B, 0x00   ; Initializes lower byte to 0
MOV $A, 0x00   ; Initializes upper byte to 0
MOV $D, 0x00   ; Direction flag, 0 for incrementing, 1 for decrementing

main_loop:
    ; Displays the current value
    SDL $B       ; Loads lower byte (B) to ST
    SDH $A       ; Loads upper byte (A) to SD (with ST)

    ; Checks direction
    STC          ; Sets the Carry flag before comparing
    CMP $D, 0x00 ; Compares direction flag with 0
    JZ increment ; Jumps to increment if Z flag is set (direction is 0)
    JMP decrement ; Otherwise, go to decrement

increment:
    ; Increments the lower byte
    CLC          ; Clears the Carry flag before adding
    ADD $B, 0x01 

    ; Checks for Carry, and if there is, increments the upper byte
    JC increment_upper

    ; Checks if value reached 65535 (0xFFFF)
    STC          ; Sets the Carry flag before comparing
    CMP $B, 0xFF ; Compares lower byte with 0xFF
    JNZ main_loop ; If not equal, continues main loop
    
    STC          ; Sets the Carry flag before comparing
    CMP $A, 0xFF ; Compares upper byte with 0xFF
    JNZ main_loop ; If not equal, continues main loop

    ; If 65535 is reached, switches direction
    MOV $D, 0x01 ; Sets direction flag to decrementing
    JMP main_loop

increment_upper:
    CLC          ; Clears the Carry flag before adding
    ADD $A, 0x01 
    JMP main_loop

decrement:
    ; Decrements the lower byte
    STC          ; Sets the Carry flag before subtracting
    SUB $B, 0x01 

    ; Checks for borrow, and if there is, decrements the upper byte
    JNC decrement_upper

    ; Checks if lower byte reached 0
    STC          ; Sets the Carry flag before comparing
    CMP $B, 0x00 ; Compares lower byte with 0
    JNZ main_loop ; If not 0, continues main loop

    ; Checks if upper byte reached 0
    STC          ; Sets the Carry flag before comparing
    CMP $A, 0x00 ; Compares upper byte with 0
    JNZ main_loop ; If not 0, continues main loop

    ; If both are 0, switches direction
    MOV $D, 0x00 ; Sets direction flag to incrementing
    JMP main_loop

decrement_upper:
    STC          ; Sets the Carry flag before subtracting
    SUB $A, 0x01 
    JMP main_loop