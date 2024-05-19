;----------------------------------------------------------------------
; Fibonacci sequence up to max number within 16 bits.
; range[1 : 46368] on 6-digit 14-segment display (Works on microcode V1)
;----------------------------------------------------------------------

#include "ruledef.asm"

; Offsets the starting address to the boot loader ROM's location (0xC000) to align jump operations.
#addr 0xC000 

; Initializes the first two Fibonacci numbers F0 = 0 (in $A:$B) and F1 = 1 (in $C:$D)
fib_init:
    MOV $A, 0x00   ; High byte of F0
    MOV $B, 0x00   ; Low  byte of F0
    MOV $C, 0x00   ; High byte of F1
    MOV $D, 0x01   ; Low  byte of F1

; Main loop for calculating Fibonacci numbers
main_loop_fib:
    ; Saves current state of F1 (which will become the new F0) onto the stack
    PSH $C   ; Saves current F1 high byte (future F0 high) 
    PSH $D   ; Saves current F1 low byte (future F0 low)

    ; Calculates new Fibonacci number (F0 + F1), starting with the low byte
    CLC          ; Clears Carry flag before addition
    ADD $B, $D   ; Adds the low bytes of F0 and F1 (result stored in $B, intended for new F1 low)
    MOV $E, $B   ; Stores new F1 low byte temporarily in $E (since $B will be overwritten with old F1 low)
    
    ; Now, adds the high bytes for the new Fibonacci number
    ADD $C, $A   ; Adds (with Carry) the high bytes of old F0 ($A) and old F1 (originally in $C, now in $A) for new F1 high

    MOV $D, $E   ; Else, moves stored new F1 low byte (from $E) into $D and continues execution.

    ; At this stage $C and $D contain the new/current F1

    PUL $B       ; Pulls old F1 low byte back into $B, now as part of new F0
    PUL $A       ; Pulls old F1 high byte into $A, now as part of new F0 (since $C will be used for new F1 high)

    JC fib_init ; Resets the sequence if the high byte generates an overflow.
    
    ; Displays the new Fibonacci number (currently in $A:$D for high:low bytes)
    PSH $A       ; Saves new F1 high byte before display
    MOV $A, $D
    SDL $A       ; Loads new F1 low byte of display reg
    MOV $A, $C
    SDH $A       ; Displays new F1
    PUL $A       ; Restores new F1 high byte for display

    JMP main_loop_fib ; Continues loop for next Fibonacci number if no no overflow occurs
    