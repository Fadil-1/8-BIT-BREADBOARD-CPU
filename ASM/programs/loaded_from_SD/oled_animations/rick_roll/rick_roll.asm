#addr 0x0200
#include "../../../../ruledef.asm"
#include "../../../../drivers/oled/oled_constants.asm"

JMP START

#include "../../../../drivers/oled/oled_lowlevel.asm"
#include "../../../../drivers/oled/oled_text_4x6.asm"
#include "../../../../drivers/oled/oled_graphics.asm"
#include "../../../../drivers/spi_sd/SPI_routines.asm"
#include "../../../../drivers/spi_sd/SPI_init.asm"
#include "../../../../drivers/spi_sd/sd_block_io.asm"

; ---------- SD delta video state ----------
VID_FRAME_LEFT    = 0x7340
VID_SECTORS_LEFT  = 0x7341
VID_RUNS_LEFT     = 0x7342
VID_RUN_COL       = 0x7343
VID_RUN_ROW       = 0x7344
VID_RUN_COUNT     = 0x7345
VID_PTR_LO        = 0x7346
VID_PTR_HI        = 0x7347

VID_BUFFER_LO     = 0x00
VID_BUFFER_HI     = 0x60
VID_FRAME_COUNT   = 0x0E
VID_SLOT_SECTORS  = 0x01

START:
    MOV $CLK, 0x07
    JSR OLED_INIT
    JSR OLED4_SET_DEFAULT_ORIGIN
    JSR OLED4_HOME
    JSR OLEDG_CLEAR_SAFE_AREA
    JSR VID_PRINT_START_TEXT
    JSR SD_INIT_RELIABLE

VID_LOOP:
    JSR OLEDG_CLEAR_SAFE_AREA
    JSR VID_SET_START_BLOCK
    MOV $A, VID_FRAME_COUNT
    MOV VID_FRAME_LEFT, $A

VID_FRAME_LOOP:
    JSR VID_LOAD_SLOT_TO_BUFFER
    JC VID_READ_FAIL

    JSR VID_DRAW_DELTA_SLOT

    MOV $A, VID_FRAME_LEFT
    STC
    NOP
    SUB $A, 0x01
    PSF
    MOV VID_FRAME_LEFT, $A
    PLF
    JNZ VID_FRAME_LOOP

    JMP VID_LOOP

VID_SET_START_BLOCK:
    MOV $A, 0x00
    MOV SD_BLOCK_ADDR_MSB, $A
    MOV $A, 0x00
    MOV SD_BLOCK_ADDR_B2, $A
    MOV $A, 0x08
    MOV SD_BLOCK_ADDR_B1, $A
    MOV $A, 0x98
    MOV SD_BLOCK_ADDR_LSB, $A
    RTS

VID_INC_SD_BLOCK:
    MOV $A, SD_BLOCK_ADDR_LSB
    CLC
    NOP
    ADD $A, 0x01
    PSF
    MOV SD_BLOCK_ADDR_LSB, $A
    PLF
    JNC .VID_INC_DONE

    MOV $A, SD_BLOCK_ADDR_B1
    CLC
    NOP
    ADD $A, 0x01
    PSF
    MOV SD_BLOCK_ADDR_B1, $A
    PLF
    JNC .VID_INC_DONE

    MOV $A, SD_BLOCK_ADDR_B2
    CLC
    NOP
    ADD $A, 0x01
    PSF
    MOV SD_BLOCK_ADDR_B2, $A
    PLF
    JNC .VID_INC_DONE

    MOV $A, SD_BLOCK_ADDR_MSB
    CLC
    NOP
    ADD $A, 0x01
    MOV SD_BLOCK_ADDR_MSB, $A

.VID_INC_DONE:
    RTS

VID_LOAD_SLOT_TO_BUFFER:
    MOV $C, VID_BUFFER_LO
    MOV $D, VID_BUFFER_HI
    MOV $A, VID_SLOT_SECTORS
    MOV VID_SECTORS_LEFT, $A

.VID_LOAD_SECTOR:
    JSR SD_READ_BLOCK_TO_RAM_512
    JC .VID_LOAD_FAIL
    JSR VID_INC_SD_BLOCK

    MOV $A, VID_SECTORS_LEFT
    STC
    NOP
    SUB $A, 0x01
    PSF
    MOV VID_SECTORS_LEFT, $A
    PLF
    JNZ .VID_LOAD_SECTOR

    CLC
    RTS

.VID_LOAD_FAIL:
    STC
    RTS

VID_INC_CD:
    CLC
    NOP
    ADD $C, 0x01
    JNC .VID_INC_CD_DONE
    CLC
    NOP
    ADD $D, 0x01

.VID_INC_CD_DONE:
    RTS

VID_SAVE_PTR:
    MOV VID_PTR_LO, $C
    MOV VID_PTR_HI, $D
    RTS

VID_RESTORE_PTR:
    MOV $C, VID_PTR_LO
    MOV $D, VID_PTR_HI
    RTS

VID_DRAW_DELTA_SLOT:
    MOV $C, VID_BUFFER_LO
    MOV $D, VID_BUFFER_HI
    MOV $A, [$CD]
    MOV VID_RUNS_LEFT, $A
    JSR VID_INC_CD
    JSR VID_INC_CD

.VID_RUN_LOOP:
    MOV $A, VID_RUNS_LEFT
    STC
    NOP
    CMP $A, 0x00
    JZ .VID_RUNS_DONE

    MOV $A, [$CD]
    MOV VID_RUN_COL, $A
    JSR VID_INC_CD

    MOV $A, [$CD]
    MOV VID_RUN_ROW, $A
    JSR VID_INC_CD

    MOV $A, [$CD]
    MOV VID_RUN_COUNT, $A
    JSR VID_INC_CD

    JSR VID_SAVE_PTR
    JSR VID_BEGIN_RUN_WINDOW
    JSR VID_RESTORE_PTR

    MOV $B, VID_RUN_COUNT

.VID_DATA_LOOP:
    MOV $A, [$CD]
    OLD $A
    JSR VID_INC_CD
    STC
    NOP
    SUB $B, 0x01
    JNZ .VID_DATA_LOOP

    MOV $A, VID_RUNS_LEFT
    STC
    NOP
    SUB $A, 0x01
    MOV VID_RUNS_LEFT, $A
    JMP .VID_RUN_LOOP

.VID_RUNS_DONE:
    RTS

VID_BEGIN_RUN_WINDOW:
    MOV $A, 0x15
    OLC $A
    MOV $A, VID_RUN_COL
    OLC $A
    MOV $A, VID_RUN_COUNT
    STC
    NOP
    SUB $A, 0x01
    CLC
    NOP
    ADD $A, VID_RUN_COL
    OLC $A

    MOV $A, 0x75
    OLC $A
    MOV $A, VID_RUN_ROW
    OLC $A
    MOV $A, VID_RUN_ROW
    OLC $A

    MOV $A, 0x5C
    OLC $A
    RTS

VID_READ_FAIL:
    JSR OLEDG_CLEAR_SAFE_AREA
    JSR OLED4_HOME
    JSR VID_PRINT_READ_FAIL

.VID_FAIL_HOLD:
    JSR OLEDG_DELAY_HOLD
    JMP .VID_FAIL_HOLD

VID_PRINT_START_TEXT:
    MOV $A, 0x53 ; S
    JSR OLED4_PUTC
    MOV $A, 0x44 ; D
    JSR OLED4_PUTC
    MOV $A, 0x20 ; space
    JSR OLED4_PUTC
    MOV $A, 0x44 ; D
    JSR OLED4_PUTC
    MOV $A, 0x45 ; E
    JSR OLED4_PUTC
    MOV $A, 0x4C ; L
    JSR OLED4_PUTC
    MOV $A, 0x54 ; T
    JSR OLED4_PUTC
    MOV $A, 0x41 ; A
    JSR OLED4_PUTC
    MOV $A, 0x20 ; space
    JSR OLED4_PUTC
    MOV $A, 0x56 ; V
    JSR OLED4_PUTC
    MOV $A, 0x49 ; I
    JSR OLED4_PUTC
    MOV $A, 0x44 ; D
    JSR OLED4_PUTC
    MOV $A, 0x45 ; E
    JSR OLED4_PUTC
    MOV $A, 0x4F ; O
    JSR OLED4_PUTC
    MOV $A, 0x0A
    JSR OLED4_PUTC
    MOV $A, 0x42 ; B
    JSR OLED4_PUTC
    MOV $A, 0x4C ; L
    JSR OLED4_PUTC
    MOV $A, 0x4F ; O
    JSR OLED4_PUTC
    MOV $A, 0x43 ; C
    JSR OLED4_PUTC
    MOV $A, 0x4B ; K
    JSR OLED4_PUTC
    MOV $A, 0x20 ; space
    JSR OLED4_PUTC
    MOV $A, 0x32 ; 2
    JSR OLED4_PUTC
    MOV $A, 0x32 ; 2
    JSR OLED4_PUTC
    MOV $A, 0x30 ; 0
    JSR OLED4_PUTC
    MOV $A, 0x30 ; 0
    JSR OLED4_PUTC
    MOV $A, 0x0A
    JSR OLED4_PUTC
    MOV $A, 0x46 ; F
    JSR OLED4_PUTC
    MOV $A, 0x52 ; R
    JSR OLED4_PUTC
    MOV $A, 0x41 ; A
    JSR OLED4_PUTC
    MOV $A, 0x4D ; M
    JSR OLED4_PUTC
    MOV $A, 0x45 ; E
    JSR OLED4_PUTC
    MOV $A, 0x53 ; S
    JSR OLED4_PUTC
    MOV $A, 0x20 ; space
    JSR OLED4_PUTC
    MOV $A, 0x31 ; 1
    JSR OLED4_PUTC
    MOV $A, 0x34 ; 4
    JSR OLED4_PUTC
    MOV $A, 0x0A
    JSR OLED4_PUTC
    MOV $A, 0x53 ; S
    JSR OLED4_PUTC
    MOV $A, 0x4C ; L
    JSR OLED4_PUTC
    MOV $A, 0x4F ; O
    JSR OLED4_PUTC
    MOV $A, 0x54 ; T
    JSR OLED4_PUTC
    MOV $A, 0x20 ; space
    JSR OLED4_PUTC
    MOV $A, 0x31 ; 1
    JSR OLED4_PUTC
    MOV $A, 0x0A
    JSR OLED4_PUTC
    RTS

VID_PRINT_READ_FAIL:
    MOV $A, 0x53 ; S
    JSR OLED4_PUTC
    MOV $A, 0x44 ; D
    JSR OLED4_PUTC
    MOV $A, 0x20 ; space
    JSR OLED4_PUTC
    MOV $A, 0x52 ; R
    JSR OLED4_PUTC
    MOV $A, 0x45 ; E
    JSR OLED4_PUTC
    MOV $A, 0x41 ; A
    JSR OLED4_PUTC
    MOV $A, 0x44 ; D
    JSR OLED4_PUTC
    MOV $A, 0x20 ; space
    JSR OLED4_PUTC
    MOV $A, 0x46 ; F
    JSR OLED4_PUTC
    MOV $A, 0x41 ; A
    JSR OLED4_PUTC
    MOV $A, 0x49 ; I
    JSR OLED4_PUTC
    MOV $A, 0x4C ; L
    JSR OLED4_PUTC
    RTS
