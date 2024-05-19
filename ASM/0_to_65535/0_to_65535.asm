;----------------------------------------------------------------------
; Displays all numbers within 16-bit range[0 : 65535] on 6-digit 
; 14-segment display (Works on microcode V1)
;----------------------------------------------------------------------

#include "ruledef.asm"

; Offsets the starting address to the boot loader ROM's location (0xC000) to align jump operations.
#addr 0xC000 

; Initializes registers
MOV $B, 0x00 ; Initialize lower byte to 0
MOV $A, 0x00 ; Initialize upper byte to 0

main_loop:
    ; Displays the current value
    SDL $B       ; Loads lower byte (B) to ST
    SDH $A       ; Loads upper byte (A) to SD (with ST)

    ; Increments the lower byte
    CLC          ; Clears the Carry flag before adding
    ADD $B, 0x01 

    ; Checks for Carry, and if there is, increment the upper byte
    JC increment_upper 

    ; If no Carry, jump to the start of the loop
    JMP main_loop

increment_upper:
    CLC          ; Clears the Carry flag before adding
    ADD $A, 0x01 

    ; Continues the loop
    JMP main_loop

; Wraps around from 65535 to 0 automatically due to overflow
