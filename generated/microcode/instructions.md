## `RST` (0x00)

| Microstep | Control Signals |
| :---: | :---: |
| t_0 | _OC, ZW |
| t_1 | _OC, IR_in, BRlW, RD_0, RD_1, RD_2, RD_3, WR_1, BRhW |
| t_2 | _OC, _FW, Z1, ZS, Z0, RD_0, RD_1, RD_2, RD_3, WR_0, WR_1 |
| t_3 | RD_0, RD_1, RD_2, RD_3, WR_0, WR_2 |
| t_4 | Z1, ZS, H_cin, _BW, _DW, EW, RD_0, RD_1, RD_2, RD_3, WR_0, WR_1, WR_2 |
| t_5 | ZS, ZW |
| t_6 | Z1, ZS, H_cin, RD_0, RD_1, RD_2, RD_3 |
| t_7 | ZS, ZW |
| t_8 | RD_0, RD_1, RD_2, RD_3, BRhW |
| t_9 | SPW, _BRE |
| t_10 | _SPC, SPD |
| t_11 | _PCW, _BRE |
| t_12 | TI |
| t_13 |  |
| t_14 |  |
| t_15 | IR_in, RD_2, _PCE |


## `STC` (0x01)

| Microstep | Control Signals |
| :---: | :---: |
| t_0 | IR_in, RD_2, PCC, _PCE |
| t_1 | _FW, Z2, ZS, Z0 |
| t_2 | _ScR |


## `CLC` (0x02)

| Microstep | Control Signals |
| :---: | :---: |
| t_0 | IR_in, RD_2, PCC, _PCE |
| t_1 | _FW, Z2, ZS |
| t_2 | _ScR |


## `MOV $A, #` (0x03)

| Microstep | Control Signals |
| :---: | :---: |
| t_0 | IR_in, RD_2, PCC, _PCE |
| t_1 | RD_2, WR_1, PCC, _PCE |
| t_2 | _ScR |


## `ADD $A, #` (0x04)

| Microstep | Control Signals |
| :---: | :---: |
| t_0 | IR_in, RD_2, PCC, _PCE |
| t_1 | Z1, ZS, Z0, RD_2, RD_3 |
| t_2 | ZS, ZW |
| t_3 | _FW, Z1, Z0, RD_2, _PCE, ZW |
| t_4 | RD_0, RD_1, RD_2, RD_3, WR_1, PCC |
| t_5 | _ScR |


## `SUB $A, #` (0x05)

| Microstep | Control Signals |
| :---: | :---: |
| t_0 | IR_in, RD_2, PCC, _PCE |
| t_1 | Z1, ZS, Z0, RD_2, RD_3 |
| t_2 | ZS, ZW |
| t_3 | _FW, Z0, RD_2, _PCE, ZW |
| t_4 | RD_0, RD_1, RD_2, RD_3, WR_1, PCC |
| t_5 | _ScR |


## `AND $A, #` (0x06)

| Microstep | Control Signals |
| :---: | :---: |
| t_0 | IR_in, RD_2, PCC, _PCE |
| t_1 | Z1, ZS, Z0, RD_2, RD_3 |
| t_2 | ZS, ZW |
| t_3 | _FW, Z1, Z2, RD_2, _PCE, ZW |
| t_4 | RD_0, RD_1, RD_2, RD_3, WR_1, PCC |
| t_5 | _ScR |


## `OR $A, #` (0x07)

| Microstep | Control Signals |
| :---: | :---: |
| t_0 | IR_in, RD_2, PCC, _PCE |
| t_1 | Z1, ZS, Z0, RD_2, RD_3 |
| t_2 | ZS, ZW |
| t_3 | _FW, Z2, Z0, RD_2, _PCE, ZW |
| t_4 | RD_0, RD_1, RD_2, RD_3, WR_1, PCC |
| t_5 | _ScR |


## `XOR $A, #` (0x08)

| Microstep | Control Signals |
| :---: | :---: |
| t_0 | IR_in, RD_2, PCC, _PCE |
| t_1 | Z1, ZS, Z0, RD_2, RD_3 |
| t_2 | ZS, ZW |
| t_3 | _FW, Z2, RD_2, _PCE, ZW |
| t_4 | RD_0, RD_1, RD_2, RD_3, WR_1, PCC |
| t_5 | _ScR |


## `CMP $A, #` (0x09)

| Microstep | Control Signals |
| :---: | :---: |
| t_0 | IR_in, RD_2, PCC, _PCE |
| t_1 | Z1, ZS, Z0, RD_2, RD_3 |
| t_2 | ZS, ZW |
| t_3 | _FW, Z0, RD_2, PCC, _PCE |
| t_4 | _ScR |


## `MOV $B, #` (0x0A)

| Microstep | Control Signals |
| :---: | :---: |
| t_0 | IR_in, RD_2, PCC, _PCE |
| t_1 | _BW, RD_2, PCC, _PCE |
| t_2 | _ScR |


## `ADD $B, #` (0x0B)

| Microstep | Control Signals |
| :---: | :---: |
| t_0 | IR_in, RD_2, PCC, _PCE |
| t_1 | Z1, ZS, Z0, RD_0, RD_1, RD_3 |
| t_2 | ZS, ZW |
| t_3 | _FW, Z1, Z0, RD_2, _PCE, ZW |
| t_4 | _BW, RD_0, RD_1, RD_2, RD_3, PCC |
| t_5 | _ScR |


## `SUB $B, #` (0x0C)

| Microstep | Control Signals |
| :---: | :---: |
| t_0 | IR_in, RD_2, PCC, _PCE |
| t_1 | Z1, ZS, Z0, RD_0, RD_1, RD_3 |
| t_2 | ZS, ZW |
| t_3 | _FW, Z0, RD_2, _PCE, ZW |
| t_4 | _BW, RD_0, RD_1, RD_2, RD_3, PCC |
| t_5 | _ScR |


## `AND $B, #` (0x0D)

| Microstep | Control Signals |
| :---: | :---: |
| t_0 | IR_in, RD_2, PCC, _PCE |
| t_1 | Z1, ZS, Z0, RD_0, RD_1, RD_3 |
| t_2 | ZS, ZW |
| t_3 | _FW, Z1, Z2, RD_2, _PCE, ZW |
| t_4 | _BW, RD_0, RD_1, RD_2, RD_3, PCC |
| t_5 | _ScR |


## `OR $B, #` (0x0E)

| Microstep | Control Signals |
| :---: | :---: |
| t_0 | IR_in, RD_2, PCC, _PCE |
| t_1 | Z1, ZS, Z0, RD_0, RD_1, RD_3 |
| t_2 | ZS, ZW |
| t_3 | _FW, Z2, Z0, RD_2, _PCE, ZW |
| t_4 | _BW, RD_0, RD_1, RD_2, RD_3, PCC |
| t_5 | _ScR |


## `XOR $B, #` (0x0F)

| Microstep | Control Signals |
| :---: | :---: |
| t_0 | IR_in, RD_2, PCC, _PCE |
| t_1 | Z1, ZS, Z0, RD_0, RD_1, RD_3 |
| t_2 | ZS, ZW |
| t_3 | _FW, Z2, RD_2, _PCE, ZW |
| t_4 | _BW, RD_0, RD_1, RD_2, RD_3, PCC |
| t_5 | _ScR |


## `CMP $B, #` (0x10)

| Microstep | Control Signals |
| :---: | :---: |
| t_0 | IR_in, RD_2, PCC, _PCE |
| t_1 | Z1, ZS, Z0, RD_0, RD_1, RD_3 |
| t_2 | ZS, ZW |
| t_3 | _FW, Z0, RD_2, PCC, _PCE |
| t_4 | _ScR |


## `MOV $C, #` (0x11)

| Microstep | Control Signals |
| :---: | :---: |
| t_0 | IR_in, RD_2, PCC, _PCE |
| t_1 | RD_2, WR_0, WR_1, PCC, _PCE |
| t_2 | _ScR |


## `ADD $C, #` (0x12)

| Microstep | Control Signals |
| :---: | :---: |
| t_0 | IR_in, RD_2, PCC, _PCE |
| t_1 | Z1, ZS, Z0, RD_0, RD_2, RD_3 |
| t_2 | ZS, ZW |
| t_3 | _FW, Z1, Z0, RD_2, _PCE, ZW |
| t_4 | RD_0, RD_1, RD_2, RD_3, WR_0, WR_1, PCC |
| t_5 | _ScR |


## `SUB $C, #` (0x13)

| Microstep | Control Signals |
| :---: | :---: |
| t_0 | IR_in, RD_2, PCC, _PCE |
| t_1 | Z1, ZS, Z0, RD_0, RD_2, RD_3 |
| t_2 | ZS, ZW |
| t_3 | _FW, Z0, RD_2, _PCE, ZW |
| t_4 | RD_0, RD_1, RD_2, RD_3, WR_0, WR_1, PCC |
| t_5 | _ScR |


## `AND $C, #` (0x14)

| Microstep | Control Signals |
| :---: | :---: |
| t_0 | IR_in, RD_2, PCC, _PCE |
| t_1 | Z1, ZS, Z0, RD_0, RD_2, RD_3 |
| t_2 | ZS, ZW |
| t_3 | _FW, Z1, Z2, RD_2, _PCE, ZW |
| t_4 | RD_0, RD_1, RD_2, RD_3, WR_0, WR_1, PCC |
| t_5 | _ScR |


## `OR $C, #` (0x15)

| Microstep | Control Signals |
| :---: | :---: |
| t_0 | IR_in, RD_2, PCC, _PCE |
| t_1 | Z1, ZS, Z0, RD_0, RD_2, RD_3 |
| t_2 | ZS, ZW |
| t_3 | _FW, Z2, Z0, RD_2, _PCE, ZW |
| t_4 | RD_0, RD_1, RD_2, RD_3, WR_0, WR_1, PCC |
| t_5 | _ScR |


## `XOR $C, #` (0x16)

| Microstep | Control Signals |
| :---: | :---: |
| t_0 | IR_in, RD_2, PCC, _PCE |
| t_1 | Z1, ZS, Z0, RD_0, RD_2, RD_3 |
| t_2 | ZS, ZW |
| t_3 | _FW, Z2, RD_2, _PCE, ZW |
| t_4 | RD_0, RD_1, RD_2, RD_3, WR_0, WR_1, PCC |
| t_5 | _ScR |


## `CMP $C, #` (0x17)

| Microstep | Control Signals |
| :---: | :---: |
| t_0 | IR_in, RD_2, PCC, _PCE |
| t_1 | Z1, ZS, Z0, RD_0, RD_2, RD_3 |
| t_2 | ZS, ZW |
| t_3 | _FW, Z0, RD_2, PCC, _PCE |
| t_4 | _ScR |


## `MOV $D, #` (0x18)

| Microstep | Control Signals |
| :---: | :---: |
| t_0 | IR_in, RD_2, PCC, _PCE |
| t_1 | _DW, RD_2, PCC, _PCE |
| t_2 | _ScR |


## `ADD $D, #` (0x19)

| Microstep | Control Signals |
| :---: | :---: |
| t_0 | IR_in, RD_2, PCC, _PCE |
| t_1 | Z1, ZS, Z0, RD_1, RD_2, RD_3 |
| t_2 | ZS, ZW |
| t_3 | _FW, Z1, Z0, RD_2, _PCE, ZW |
| t_4 | _DW, RD_0, RD_1, RD_2, RD_3, PCC |
| t_5 | _ScR |


## `SUB $D, #` (0x1A)

| Microstep | Control Signals |
| :---: | :---: |
| t_0 | IR_in, RD_2, PCC, _PCE |
| t_1 | Z1, ZS, Z0, RD_1, RD_2, RD_3 |
| t_2 | ZS, ZW |
| t_3 | _FW, Z0, RD_2, _PCE, ZW |
| t_4 | _DW, RD_0, RD_1, RD_2, RD_3, PCC |
| t_5 | _ScR |


## `AND $D, #` (0x1B)

| Microstep | Control Signals |
| :---: | :---: |
| t_0 | IR_in, RD_2, PCC, _PCE |
| t_1 | Z1, ZS, Z0, RD_1, RD_2, RD_3 |
| t_2 | ZS, ZW |
| t_3 | _FW, Z1, Z2, RD_2, _PCE, ZW |
| t_4 | _DW, RD_0, RD_1, RD_2, RD_3, PCC |
| t_5 | _ScR |


## `OR $D, #` (0x1C)

| Microstep | Control Signals |
| :---: | :---: |
| t_0 | IR_in, RD_2, PCC, _PCE |
| t_1 | Z1, ZS, Z0, RD_1, RD_2, RD_3 |
| t_2 | ZS, ZW |
| t_3 | _FW, Z2, Z0, RD_2, _PCE, ZW |
| t_4 | _DW, RD_0, RD_1, RD_2, RD_3, PCC |
| t_5 | _ScR |


## `XOR $D, #` (0x1D)

| Microstep | Control Signals |
| :---: | :---: |
| t_0 | IR_in, RD_2, PCC, _PCE |
| t_1 | Z1, ZS, Z0, RD_1, RD_2, RD_3 |
| t_2 | ZS, ZW |
| t_3 | _FW, Z2, RD_2, _PCE, ZW |
| t_4 | _DW, RD_0, RD_1, RD_2, RD_3, PCC |
| t_5 | _ScR |


## `CMP $D, #` (0x1E)

| Microstep | Control Signals |
| :---: | :---: |
| t_0 | IR_in, RD_2, PCC, _PCE |
| t_1 | Z1, ZS, Z0, RD_1, RD_2, RD_3 |
| t_2 | ZS, ZW |
| t_3 | _FW, Z0, RD_2, PCC, _PCE |
| t_4 | _ScR |


## `MOV $E, #` (0x1F)

| Microstep | Control Signals |
| :---: | :---: |
| t_0 | IR_in, RD_2, PCC, _PCE |
| t_1 | _DW, RD_2, PCC, _PCE |
| t_2 | _ScR |


## `ADD $E, #` (0x20)

| Microstep | Control Signals |
| :---: | :---: |
| t_0 | IR_in, RD_2, PCC, _PCE |
| t_1 | Z1, ZS, _EE, Z0 |
| t_2 | ZS, ZW |
| t_3 | _FW, Z1, Z0, RD_2, _PCE, ZW |
| t_4 | EW, RD_0, RD_1, RD_2, RD_3, PCC |
| t_5 | _ScR |


## `SUB $E, #` (0x21)

| Microstep | Control Signals |
| :---: | :---: |
| t_0 | IR_in, RD_2, PCC, _PCE |
| t_1 | Z1, ZS, _EE, Z0 |
| t_2 | ZS, ZW |
| t_3 | _FW, Z0, RD_2, _PCE, ZW |
| t_4 | EW, RD_0, RD_1, RD_2, RD_3, PCC |
| t_5 | _ScR |


## `CMP $E, #` (0x22)

| Microstep | Control Signals |
| :---: | :---: |
| t_0 | IR_in, RD_2, PCC, _PCE |
| t_1 | Z1, ZS, _EE, Z0 |
| t_2 | ZS, ZW |
| t_3 | _FW, Z0, RD_2, PCC, _PCE |
| t_4 | _ScR |


## `MOV $A, $E` (0x23)

| Microstep | Control Signals |
| :---: | :---: |
| t_0 | IR_in, RD_2, PCC, _PCE |
| t_1 | _EE, WR_1 |
| t_2 | _ScR |


## `MOV $E, $A` (0x24)

| Microstep | Control Signals |
| :---: | :---: |
| t_0 | IR_in, RD_2, PCC, _PCE |
| t_1 | EW, RD_2, RD_3 |
| t_2 | _ScR |


## `CMP $E, A` (0x25)

| Microstep | Control Signals |
| :---: | :---: |
| t_0 | IR_in, RD_2, PCC, _PCE |
| t_1 | Z1, ZS, _EE, Z0 |
| t_2 | ZS, ZW |
| t_3 | _FW, Z0, RD_2, RD_3 |
| t_4 | _ScR |


## `MOV $B, $E` (0x26)

| Microstep | Control Signals |
| :---: | :---: |
| t_0 | IR_in, RD_2, PCC, _PCE |
| t_1 | _BW, _EE |
| t_2 | _ScR |


## `MOV $E, $B` (0x27)

| Microstep | Control Signals |
| :---: | :---: |
| t_0 | IR_in, RD_2, PCC, _PCE |
| t_1 | EW, RD_0, RD_1, RD_3 |
| t_2 | _ScR |


## `CMP $E, B` (0x28)

| Microstep | Control Signals |
| :---: | :---: |
| t_0 | IR_in, RD_2, PCC, _PCE |
| t_1 | Z1, ZS, _EE, Z0 |
| t_2 | ZS, ZW |
| t_3 | _FW, Z0, RD_0, RD_1, RD_3 |
| t_4 | _ScR |


## `MOV $C, $E` (0x29)

| Microstep | Control Signals |
| :---: | :---: |
| t_0 | IR_in, RD_2, PCC, _PCE |
| t_1 | _EE, WR_0, WR_1 |
| t_2 | _ScR |


## `MOV $E, $C` (0x2A)

| Microstep | Control Signals |
| :---: | :---: |
| t_0 | IR_in, RD_2, PCC, _PCE |
| t_1 | EW, RD_0, RD_2, RD_3 |
| t_2 | _ScR |


## `CMP $E, C` (0x2B)

| Microstep | Control Signals |
| :---: | :---: |
| t_0 | IR_in, RD_2, PCC, _PCE |
| t_1 | Z1, ZS, _EE, Z0 |
| t_2 | ZS, ZW |
| t_3 | _FW, Z0, RD_0, RD_2, RD_3 |
| t_4 | _ScR |


## `MOV $D, $E` (0x2C)

| Microstep | Control Signals |
| :---: | :---: |
| t_0 | IR_in, RD_2, PCC, _PCE |
| t_1 | _DW, _EE |
| t_2 | _ScR |


## `MOV $E, $D` (0x2D)

| Microstep | Control Signals |
| :---: | :---: |
| t_0 | IR_in, RD_2, PCC, _PCE |
| t_1 | EW, RD_1, RD_2, RD_3 |
| t_2 | _ScR |


## `CMP $E, D` (0x2E)

| Microstep | Control Signals |
| :---: | :---: |
| t_0 | IR_in, RD_2, PCC, _PCE |
| t_1 | Z1, ZS, _EE, Z0 |
| t_2 | ZS, ZW |
| t_3 | _FW, Z0, RD_1, RD_2, RD_3 |
| t_4 | _ScR |


## `MOV $CLK, #` (0x2F)

| Microstep | Control Signals |
| :---: | :---: |
| t_0 | IR_in, RD_2, PCC, _PCE |
| t_1 | _CLKW, RD_2, _PCE |
| t_2 | PCC |
| t_3 | _ScR |


## `MOV $CLK, $E` (0x30)

| Microstep | Control Signals |
| :---: | :---: |
| t_0 | IR_in, RD_2, PCC, _PCE |
| t_1 | _CLKW, _EE |
| t_2 | _ScR |


## `MOV $A, $B` (0x31)

| Microstep | Control Signals |
| :---: | :---: |
| t_0 | IR_in, RD_2, PCC, _PCE |
| t_1 | RD_0, RD_1, RD_3, WR_1 |
| t_2 | _ScR |


## `ADD $A, $B` (0x32)

| Microstep | Control Signals |
| :---: | :---: |
| t_0 | IR_in, RD_2, PCC, _PCE |
| t_1 | Z1, ZS, Z0, RD_2, RD_3 |
| t_2 | ZS, ZW |
| t_3 | _FW, Z1, Z0, RD_0, RD_1, RD_3, ZW |
| t_4 | RD_0, RD_1, RD_2, RD_3, WR_1 |
| t_5 | _ScR |


## `SUB $A, $B` (0x33)

| Microstep | Control Signals |
| :---: | :---: |
| t_0 | IR_in, RD_2, PCC, _PCE |
| t_1 | Z1, ZS, Z0, RD_2, RD_3 |
| t_2 | ZS, ZW |
| t_3 | _FW, Z0, RD_0, RD_1, RD_3, ZW |
| t_4 | RD_0, RD_1, RD_2, RD_3, WR_1 |
| t_5 | _ScR |


## `AND $A, $B` (0x34)

| Microstep | Control Signals |
| :---: | :---: |
| t_0 | IR_in, RD_2, PCC, _PCE |
| t_1 | Z1, ZS, Z0, RD_2, RD_3 |
| t_2 | ZS, ZW |
| t_3 | _FW, Z1, Z2, RD_0, RD_1, RD_3, ZW |
| t_4 | RD_0, RD_1, RD_2, RD_3, WR_1 |
| t_5 | _ScR |


## `OR $A, $B` (0x35)

| Microstep | Control Signals |
| :---: | :---: |
| t_0 | IR_in, RD_2, PCC, _PCE |
| t_1 | Z1, ZS, Z0, RD_2, RD_3 |
| t_2 | ZS, ZW |
| t_3 | _FW, Z2, Z0, RD_0, RD_1, RD_3, ZW |
| t_4 | RD_0, RD_1, RD_2, RD_3, WR_1 |
| t_5 | _ScR |


## `XOR $A, $B` (0x36)

| Microstep | Control Signals |
| :---: | :---: |
| t_0 | IR_in, RD_2, PCC, _PCE |
| t_1 | Z1, ZS, Z0, RD_2, RD_3 |
| t_2 | ZS, ZW |
| t_3 | _FW, Z2, RD_0, RD_1, RD_3, ZW |
| t_4 | RD_0, RD_1, RD_2, RD_3, WR_1 |
| t_5 | _ScR |


## `CMP $A, $B` (0x37)

| Microstep | Control Signals |
| :---: | :---: |
| t_0 | IR_in, RD_2, PCC, _PCE |
| t_1 | Z1, ZS, Z0, RD_2, RD_3 |
| t_2 | ZS, ZW |
| t_3 | _FW, Z0, RD_0, RD_1, RD_3 |
| t_4 | _ScR |


## `MOV $A, $C` (0x38)

| Microstep | Control Signals |
| :---: | :---: |
| t_0 | IR_in, RD_2, PCC, _PCE |
| t_1 | RD_0, RD_2, RD_3, WR_1 |
| t_2 | _ScR |


## `ADD $A, $C` (0x39)

| Microstep | Control Signals |
| :---: | :---: |
| t_0 | IR_in, RD_2, PCC, _PCE |
| t_1 | Z1, ZS, Z0, RD_2, RD_3 |
| t_2 | ZS, ZW |
| t_3 | _FW, Z1, Z0, RD_0, RD_2, RD_3, ZW |
| t_4 | RD_0, RD_1, RD_2, RD_3, WR_1 |
| t_5 | _ScR |


## `SUB $A, $C` (0x3A)

| Microstep | Control Signals |
| :---: | :---: |
| t_0 | IR_in, RD_2, PCC, _PCE |
| t_1 | Z1, ZS, Z0, RD_2, RD_3 |
| t_2 | ZS, ZW |
| t_3 | _FW, Z0, RD_0, RD_2, RD_3, ZW |
| t_4 | RD_0, RD_1, RD_2, RD_3, WR_1 |
| t_5 | _ScR |


## `AND $A, $C` (0x3B)

| Microstep | Control Signals |
| :---: | :---: |
| t_0 | IR_in, RD_2, PCC, _PCE |
| t_1 | Z1, ZS, Z0, RD_2, RD_3 |
| t_2 | ZS, ZW |
| t_3 | _FW, Z1, Z2, RD_0, RD_2, RD_3, ZW |
| t_4 | RD_0, RD_1, RD_2, RD_3, WR_1 |
| t_5 | _ScR |


## `OR $A, $C` (0x3C)

| Microstep | Control Signals |
| :---: | :---: |
| t_0 | IR_in, RD_2, PCC, _PCE |
| t_1 | Z1, ZS, Z0, RD_2, RD_3 |
| t_2 | ZS, ZW |
| t_3 | _FW, Z2, Z0, RD_0, RD_2, RD_3, ZW |
| t_4 | RD_0, RD_1, RD_2, RD_3, WR_1 |
| t_5 | _ScR |


## `XOR $A, $C` (0x3D)

| Microstep | Control Signals |
| :---: | :---: |
| t_0 | IR_in, RD_2, PCC, _PCE |
| t_1 | Z1, ZS, Z0, RD_2, RD_3 |
| t_2 | ZS, ZW |
| t_3 | _FW, Z2, RD_0, RD_2, RD_3, ZW |
| t_4 | RD_0, RD_1, RD_2, RD_3, WR_1 |
| t_5 | _ScR |


## `CMP $A, $C` (0x3E)

| Microstep | Control Signals |
| :---: | :---: |
| t_0 | IR_in, RD_2, PCC, _PCE |
| t_1 | Z1, ZS, Z0, RD_2, RD_3 |
| t_2 | ZS, ZW |
| t_3 | _FW, Z0, RD_0, RD_2, RD_3 |
| t_4 | _ScR |


## `MOV $A, $D` (0x3F)

| Microstep | Control Signals |
| :---: | :---: |
| t_0 | IR_in, RD_2, PCC, _PCE |
| t_1 | RD_1, RD_2, RD_3, WR_1 |
| t_2 | _ScR |


## `ADD $A, $D` (0x40)

| Microstep | Control Signals |
| :---: | :---: |
| t_0 | IR_in, RD_2, PCC, _PCE |
| t_1 | Z1, ZS, Z0, RD_2, RD_3 |
| t_2 | ZS, ZW |
| t_3 | _FW, Z1, Z0, RD_1, RD_2, RD_3, ZW |
| t_4 | RD_0, RD_1, RD_2, RD_3, WR_1 |
| t_5 | _ScR |


## `SUB $A, $D` (0x41)

| Microstep | Control Signals |
| :---: | :---: |
| t_0 | IR_in, RD_2, PCC, _PCE |
| t_1 | Z1, ZS, Z0, RD_2, RD_3 |
| t_2 | ZS, ZW |
| t_3 | _FW, Z0, RD_1, RD_2, RD_3, ZW |
| t_4 | RD_0, RD_1, RD_2, RD_3, WR_1 |
| t_5 | _ScR |


## `AND $A, $D` (0x42)

| Microstep | Control Signals |
| :---: | :---: |
| t_0 | IR_in, RD_2, PCC, _PCE |
| t_1 | Z1, ZS, Z0, RD_2, RD_3 |
| t_2 | ZS, ZW |
| t_3 | _FW, Z1, Z2, RD_1, RD_2, RD_3, ZW |
| t_4 | RD_0, RD_1, RD_2, RD_3, WR_1 |
| t_5 | _ScR |


## `OR $A, $D` (0x43)

| Microstep | Control Signals |
| :---: | :---: |
| t_0 | IR_in, RD_2, PCC, _PCE |
| t_1 | Z1, ZS, Z0, RD_2, RD_3 |
| t_2 | ZS, ZW |
| t_3 | _FW, Z2, Z0, RD_1, RD_2, RD_3, ZW |
| t_4 | RD_0, RD_1, RD_2, RD_3, WR_1 |
| t_5 | _ScR |


## `XOR $A, $D` (0x44)

| Microstep | Control Signals |
| :---: | :---: |
| t_0 | IR_in, RD_2, PCC, _PCE |
| t_1 | Z1, ZS, Z0, RD_2, RD_3 |
| t_2 | ZS, ZW |
| t_3 | _FW, Z2, RD_1, RD_2, RD_3, ZW |
| t_4 | RD_0, RD_1, RD_2, RD_3, WR_1 |
| t_5 | _ScR |


## `CMP $A, $D` (0x45)

| Microstep | Control Signals |
| :---: | :---: |
| t_0 | IR_in, RD_2, PCC, _PCE |
| t_1 | Z1, ZS, Z0, RD_2, RD_3 |
| t_2 | ZS, ZW |
| t_3 | _FW, Z0, RD_1, RD_2, RD_3 |
| t_4 | _ScR |


## `MOV $B, $A` (0x46)

| Microstep | Control Signals |
| :---: | :---: |
| t_0 | IR_in, RD_2, PCC, _PCE |
| t_1 | _BW, RD_2, RD_3 |
| t_2 | _ScR |


## `ADD $B, $A` (0x47)

| Microstep | Control Signals |
| :---: | :---: |
| t_0 | IR_in, RD_2, PCC, _PCE |
| t_1 | Z1, ZS, Z0, RD_0, RD_1, RD_3 |
| t_2 | ZS, ZW |
| t_3 | _FW, Z1, Z0, RD_2, RD_3, ZW |
| t_4 | _BW, RD_0, RD_1, RD_2, RD_3 |
| t_5 | _ScR |


## `SUB $B, $A` (0x48)

| Microstep | Control Signals |
| :---: | :---: |
| t_0 | IR_in, RD_2, PCC, _PCE |
| t_1 | Z1, ZS, Z0, RD_0, RD_1, RD_3 |
| t_2 | ZS, ZW |
| t_3 | _FW, Z0, RD_2, RD_3, ZW |
| t_4 | _BW, RD_0, RD_1, RD_2, RD_3 |
| t_5 | _ScR |


## `AND $B, $A` (0x49)

| Microstep | Control Signals |
| :---: | :---: |
| t_0 | IR_in, RD_2, PCC, _PCE |
| t_1 | Z1, ZS, Z0, RD_0, RD_1, RD_3 |
| t_2 | ZS, ZW |
| t_3 | _FW, Z1, Z2, RD_2, RD_3, ZW |
| t_4 | _BW, RD_0, RD_1, RD_2, RD_3 |
| t_5 | _ScR |


## `OR $B, $A` (0x4A)

| Microstep | Control Signals |
| :---: | :---: |
| t_0 | IR_in, RD_2, PCC, _PCE |
| t_1 | Z1, ZS, Z0, RD_0, RD_1, RD_3 |
| t_2 | ZS, ZW |
| t_3 | _FW, Z2, Z0, RD_2, RD_3, ZW |
| t_4 | _BW, RD_0, RD_1, RD_2, RD_3 |
| t_5 | _ScR |


## `XOR $B, $A` (0x4B)

| Microstep | Control Signals |
| :---: | :---: |
| t_0 | IR_in, RD_2, PCC, _PCE |
| t_1 | Z1, ZS, Z0, RD_0, RD_1, RD_3 |
| t_2 | ZS, ZW |
| t_3 | _FW, Z2, RD_2, RD_3, ZW |
| t_4 | _BW, RD_0, RD_1, RD_2, RD_3 |
| t_5 | _ScR |


## `CMP $B, $A` (0x4C)

| Microstep | Control Signals |
| :---: | :---: |
| t_0 | IR_in, RD_2, PCC, _PCE |
| t_1 | Z1, ZS, Z0, RD_0, RD_1, RD_3 |
| t_2 | ZS, ZW |
| t_3 | _FW, Z0, RD_2, RD_3 |
| t_4 | _ScR |


## `MOV $B, $C` (0x4D)

| Microstep | Control Signals |
| :---: | :---: |
| t_0 | IR_in, RD_2, PCC, _PCE |
| t_1 | _BW, RD_0, RD_2, RD_3 |
| t_2 | _ScR |


## `ADD $B, $C` (0x4E)

| Microstep | Control Signals |
| :---: | :---: |
| t_0 | IR_in, RD_2, PCC, _PCE |
| t_1 | Z1, ZS, Z0, RD_0, RD_1, RD_3 |
| t_2 | ZS, ZW |
| t_3 | _FW, Z1, Z0, RD_0, RD_2, RD_3, ZW |
| t_4 | _BW, RD_0, RD_1, RD_2, RD_3 |
| t_5 | _ScR |


## `SUB $B, $C` (0x4F)

| Microstep | Control Signals |
| :---: | :---: |
| t_0 | IR_in, RD_2, PCC, _PCE |
| t_1 | Z1, ZS, Z0, RD_0, RD_1, RD_3 |
| t_2 | ZS, ZW |
| t_3 | _FW, Z0, RD_0, RD_2, RD_3, ZW |
| t_4 | _BW, RD_0, RD_1, RD_2, RD_3 |
| t_5 | _ScR |


## `AND $B, $C` (0x50)

| Microstep | Control Signals |
| :---: | :---: |
| t_0 | IR_in, RD_2, PCC, _PCE |
| t_1 | Z1, ZS, Z0, RD_0, RD_1, RD_3 |
| t_2 | ZS, ZW |
| t_3 | _FW, Z1, Z2, RD_0, RD_2, RD_3, ZW |
| t_4 | _BW, RD_0, RD_1, RD_2, RD_3 |
| t_5 | _ScR |


## `OR $B, $C` (0x51)

| Microstep | Control Signals |
| :---: | :---: |
| t_0 | IR_in, RD_2, PCC, _PCE |
| t_1 | Z1, ZS, Z0, RD_0, RD_1, RD_3 |
| t_2 | ZS, ZW |
| t_3 | _FW, Z2, Z0, RD_0, RD_2, RD_3, ZW |
| t_4 | _BW, RD_0, RD_1, RD_2, RD_3 |
| t_5 | _ScR |


## `XOR $B, $C` (0x52)

| Microstep | Control Signals |
| :---: | :---: |
| t_0 | IR_in, RD_2, PCC, _PCE |
| t_1 | Z1, ZS, Z0, RD_0, RD_1, RD_3 |
| t_2 | ZS, ZW |
| t_3 | _FW, Z2, RD_0, RD_2, RD_3, ZW |
| t_4 | _BW, RD_0, RD_1, RD_2, RD_3 |
| t_5 | _ScR |


## `CMP $B, $C` (0x53)

| Microstep | Control Signals |
| :---: | :---: |
| t_0 | IR_in, RD_2, PCC, _PCE |
| t_1 | Z1, ZS, Z0, RD_0, RD_1, RD_3 |
| t_2 | ZS, ZW |
| t_3 | _FW, Z0, RD_0, RD_2, RD_3 |
| t_4 | _ScR |


## `MOV $B, $D` (0x54)

| Microstep | Control Signals |
| :---: | :---: |
| t_0 | IR_in, RD_2, PCC, _PCE |
| t_1 | _BW, RD_1, RD_2, RD_3 |
| t_2 | _ScR |


## `ADD $B, $D` (0x55)

| Microstep | Control Signals |
| :---: | :---: |
| t_0 | IR_in, RD_2, PCC, _PCE |
| t_1 | Z1, ZS, Z0, RD_0, RD_1, RD_3 |
| t_2 | ZS, ZW |
| t_3 | _FW, Z1, Z0, RD_1, RD_2, RD_3, ZW |
| t_4 | _BW, RD_0, RD_1, RD_2, RD_3 |
| t_5 | _ScR |


## `SUB $B, $D` (0x56)

| Microstep | Control Signals |
| :---: | :---: |
| t_0 | IR_in, RD_2, PCC, _PCE |
| t_1 | Z1, ZS, Z0, RD_0, RD_1, RD_3 |
| t_2 | ZS, ZW |
| t_3 | _FW, Z0, RD_1, RD_2, RD_3, ZW |
| t_4 | _BW, RD_0, RD_1, RD_2, RD_3 |
| t_5 | _ScR |


## `AND $B, $D` (0x57)

| Microstep | Control Signals |
| :---: | :---: |
| t_0 | IR_in, RD_2, PCC, _PCE |
| t_1 | Z1, ZS, Z0, RD_0, RD_1, RD_3 |
| t_2 | ZS, ZW |
| t_3 | _FW, Z1, Z2, RD_1, RD_2, RD_3, ZW |
| t_4 | _BW, RD_0, RD_1, RD_2, RD_3 |
| t_5 | _ScR |


## `OR $B, $D` (0x58)

| Microstep | Control Signals |
| :---: | :---: |
| t_0 | IR_in, RD_2, PCC, _PCE |
| t_1 | Z1, ZS, Z0, RD_0, RD_1, RD_3 |
| t_2 | ZS, ZW |
| t_3 | _FW, Z2, Z0, RD_1, RD_2, RD_3, ZW |
| t_4 | _BW, RD_0, RD_1, RD_2, RD_3 |
| t_5 | _ScR |


## `XOR $B, $D` (0x59)

| Microstep | Control Signals |
| :---: | :---: |
| t_0 | IR_in, RD_2, PCC, _PCE |
| t_1 | Z1, ZS, Z0, RD_0, RD_1, RD_3 |
| t_2 | ZS, ZW |
| t_3 | _FW, Z2, RD_1, RD_2, RD_3, ZW |
| t_4 | _BW, RD_0, RD_1, RD_2, RD_3 |
| t_5 | _ScR |


## `CMP $B, $D` (0x5A)

| Microstep | Control Signals |
| :---: | :---: |
| t_0 | IR_in, RD_2, PCC, _PCE |
| t_1 | Z1, ZS, Z0, RD_0, RD_1, RD_3 |
| t_2 | ZS, ZW |
| t_3 | _FW, Z0, RD_1, RD_2, RD_3 |
| t_4 | _ScR |


## `MOV $C, $A` (0x5B)

| Microstep | Control Signals |
| :---: | :---: |
| t_0 | IR_in, RD_2, PCC, _PCE |
| t_1 | RD_2, RD_3, WR_0, WR_1 |
| t_2 | _ScR |


## `ADD $C, $A` (0x5C)

| Microstep | Control Signals |
| :---: | :---: |
| t_0 | IR_in, RD_2, PCC, _PCE |
| t_1 | Z1, ZS, Z0, RD_0, RD_2, RD_3 |
| t_2 | ZS, ZW |
| t_3 | _FW, Z1, Z0, RD_2, RD_3, ZW |
| t_4 | RD_0, RD_1, RD_2, RD_3, WR_0, WR_1 |
| t_5 | _ScR |


## `SUB $C, $A` (0x5D)

| Microstep | Control Signals |
| :---: | :---: |
| t_0 | IR_in, RD_2, PCC, _PCE |
| t_1 | Z1, ZS, Z0, RD_0, RD_2, RD_3 |
| t_2 | ZS, ZW |
| t_3 | _FW, Z0, RD_2, RD_3, ZW |
| t_4 | RD_0, RD_1, RD_2, RD_3, WR_0, WR_1 |
| t_5 | _ScR |


## `AND $C, $A` (0x5E)

| Microstep | Control Signals |
| :---: | :---: |
| t_0 | IR_in, RD_2, PCC, _PCE |
| t_1 | Z1, ZS, Z0, RD_0, RD_2, RD_3 |
| t_2 | ZS, ZW |
| t_3 | _FW, Z1, Z2, RD_2, RD_3, ZW |
| t_4 | RD_0, RD_1, RD_2, RD_3, WR_0, WR_1 |
| t_5 | _ScR |


## `OR $C, $A` (0x5F)

| Microstep | Control Signals |
| :---: | :---: |
| t_0 | IR_in, RD_2, PCC, _PCE |
| t_1 | Z1, ZS, Z0, RD_0, RD_2, RD_3 |
| t_2 | ZS, ZW |
| t_3 | _FW, Z2, Z0, RD_2, RD_3, ZW |
| t_4 | RD_0, RD_1, RD_2, RD_3, WR_0, WR_1 |
| t_5 | _ScR |


## `XOR $C, $A` (0x60)

| Microstep | Control Signals |
| :---: | :---: |
| t_0 | IR_in, RD_2, PCC, _PCE |
| t_1 | Z1, ZS, Z0, RD_0, RD_2, RD_3 |
| t_2 | ZS, ZW |
| t_3 | _FW, Z2, RD_2, RD_3, ZW |
| t_4 | RD_0, RD_1, RD_2, RD_3, WR_0, WR_1 |
| t_5 | _ScR |


## `CMP $C, $A` (0x61)

| Microstep | Control Signals |
| :---: | :---: |
| t_0 | IR_in, RD_2, PCC, _PCE |
| t_1 | Z1, ZS, Z0, RD_0, RD_2, RD_3 |
| t_2 | ZS, ZW |
| t_3 | _FW, Z0, RD_2, RD_3 |
| t_4 | _ScR |


## `MOV $C, $B` (0x62)

| Microstep | Control Signals |
| :---: | :---: |
| t_0 | IR_in, RD_2, PCC, _PCE |
| t_1 | RD_0, RD_1, RD_3, WR_0, WR_1 |
| t_2 | _ScR |


## `ADD $C, $B` (0x63)

| Microstep | Control Signals |
| :---: | :---: |
| t_0 | IR_in, RD_2, PCC, _PCE |
| t_1 | Z1, ZS, Z0, RD_0, RD_2, RD_3 |
| t_2 | ZS, ZW |
| t_3 | _FW, Z1, Z0, RD_0, RD_1, RD_3, ZW |
| t_4 | RD_0, RD_1, RD_2, RD_3, WR_0, WR_1 |
| t_5 | _ScR |


## `SUB $C, $B` (0x64)

| Microstep | Control Signals |
| :---: | :---: |
| t_0 | IR_in, RD_2, PCC, _PCE |
| t_1 | Z1, ZS, Z0, RD_0, RD_2, RD_3 |
| t_2 | ZS, ZW |
| t_3 | _FW, Z0, RD_0, RD_1, RD_3, ZW |
| t_4 | RD_0, RD_1, RD_2, RD_3, WR_0, WR_1 |
| t_5 | _ScR |


## `AND $C, $B` (0x65)

| Microstep | Control Signals |
| :---: | :---: |
| t_0 | IR_in, RD_2, PCC, _PCE |
| t_1 | Z1, ZS, Z0, RD_0, RD_2, RD_3 |
| t_2 | ZS, ZW |
| t_3 | _FW, Z1, Z2, RD_0, RD_1, RD_3, ZW |
| t_4 | RD_0, RD_1, RD_2, RD_3, WR_0, WR_1 |
| t_5 | _ScR |


## `OR $C, $B` (0x66)

| Microstep | Control Signals |
| :---: | :---: |
| t_0 | IR_in, RD_2, PCC, _PCE |
| t_1 | Z1, ZS, Z0, RD_0, RD_2, RD_3 |
| t_2 | ZS, ZW |
| t_3 | _FW, Z2, Z0, RD_0, RD_1, RD_3, ZW |
| t_4 | RD_0, RD_1, RD_2, RD_3, WR_0, WR_1 |
| t_5 | _ScR |


## `XOR $C, $B` (0x67)

| Microstep | Control Signals |
| :---: | :---: |
| t_0 | IR_in, RD_2, PCC, _PCE |
| t_1 | Z1, ZS, Z0, RD_0, RD_2, RD_3 |
| t_2 | ZS, ZW |
| t_3 | _FW, Z2, RD_0, RD_1, RD_3, ZW |
| t_4 | RD_0, RD_1, RD_2, RD_3, WR_0, WR_1 |
| t_5 | _ScR |


## `CMP $C, $B` (0x68)

| Microstep | Control Signals |
| :---: | :---: |
| t_0 | IR_in, RD_2, PCC, _PCE |
| t_1 | Z1, ZS, Z0, RD_0, RD_2, RD_3 |
| t_2 | ZS, ZW |
| t_3 | _FW, Z0, RD_0, RD_1, RD_3 |
| t_4 | _ScR |


## `MOV $C, $D` (0x69)

| Microstep | Control Signals |
| :---: | :---: |
| t_0 | IR_in, RD_2, PCC, _PCE |
| t_1 | RD_1, RD_2, RD_3, WR_0, WR_1 |
| t_2 | _ScR |


## `ADD $C, $D` (0x6A)

| Microstep | Control Signals |
| :---: | :---: |
| t_0 | IR_in, RD_2, PCC, _PCE |
| t_1 | Z1, ZS, Z0, RD_0, RD_2, RD_3 |
| t_2 | ZS, ZW |
| t_3 | _FW, Z1, Z0, RD_1, RD_2, RD_3, ZW |
| t_4 | RD_0, RD_1, RD_2, RD_3, WR_0, WR_1 |
| t_5 | _ScR |


## `SUB $C, $D` (0x6B)

| Microstep | Control Signals |
| :---: | :---: |
| t_0 | IR_in, RD_2, PCC, _PCE |
| t_1 | Z1, ZS, Z0, RD_0, RD_2, RD_3 |
| t_2 | ZS, ZW |
| t_3 | _FW, Z0, RD_1, RD_2, RD_3, ZW |
| t_4 | RD_0, RD_1, RD_2, RD_3, WR_0, WR_1 |
| t_5 | _ScR |


## `AND $C, $D` (0x6C)

| Microstep | Control Signals |
| :---: | :---: |
| t_0 | IR_in, RD_2, PCC, _PCE |
| t_1 | Z1, ZS, Z0, RD_0, RD_2, RD_3 |
| t_2 | ZS, ZW |
| t_3 | _FW, Z1, Z2, RD_1, RD_2, RD_3, ZW |
| t_4 | RD_0, RD_1, RD_2, RD_3, WR_0, WR_1 |
| t_5 | _ScR |


## `OR $C, $D` (0x6D)

| Microstep | Control Signals |
| :---: | :---: |
| t_0 | IR_in, RD_2, PCC, _PCE |
| t_1 | Z1, ZS, Z0, RD_0, RD_2, RD_3 |
| t_2 | ZS, ZW |
| t_3 | _FW, Z2, Z0, RD_1, RD_2, RD_3, ZW |
| t_4 | RD_0, RD_1, RD_2, RD_3, WR_0, WR_1 |
| t_5 | _ScR |


## `XOR $C, $D` (0x6E)

| Microstep | Control Signals |
| :---: | :---: |
| t_0 | IR_in, RD_2, PCC, _PCE |
| t_1 | Z1, ZS, Z0, RD_0, RD_2, RD_3 |
| t_2 | ZS, ZW |
| t_3 | _FW, Z2, RD_1, RD_2, RD_3, ZW |
| t_4 | RD_0, RD_1, RD_2, RD_3, WR_0, WR_1 |
| t_5 | _ScR |


## `CMP $C, $D` (0x6F)

| Microstep | Control Signals |
| :---: | :---: |
| t_0 | IR_in, RD_2, PCC, _PCE |
| t_1 | Z1, ZS, Z0, RD_0, RD_2, RD_3 |
| t_2 | ZS, ZW |
| t_3 | _FW, Z0, RD_1, RD_2, RD_3 |
| t_4 | _ScR |


## `MOV $D, $A` (0x70)

| Microstep | Control Signals |
| :---: | :---: |
| t_0 | IR_in, RD_2, PCC, _PCE |
| t_1 | _DW, RD_2, RD_3 |
| t_2 | _ScR |


## `ADD $D, $A` (0x71)

| Microstep | Control Signals |
| :---: | :---: |
| t_0 | IR_in, RD_2, PCC, _PCE |
| t_1 | Z1, ZS, Z0, RD_1, RD_2, RD_3 |
| t_2 | ZS, ZW |
| t_3 | _FW, Z1, Z0, RD_2, RD_3, ZW |
| t_4 | _DW, RD_0, RD_1, RD_2, RD_3 |
| t_5 | _ScR |


## `SUB $D, $A` (0x72)

| Microstep | Control Signals |
| :---: | :---: |
| t_0 | IR_in, RD_2, PCC, _PCE |
| t_1 | Z1, ZS, Z0, RD_1, RD_2, RD_3 |
| t_2 | ZS, ZW |
| t_3 | _FW, Z0, RD_2, RD_3, ZW |
| t_4 | _DW, RD_0, RD_1, RD_2, RD_3 |
| t_5 | _ScR |


## `AND $D, $A` (0x73)

| Microstep | Control Signals |
| :---: | :---: |
| t_0 | IR_in, RD_2, PCC, _PCE |
| t_1 | Z1, ZS, Z0, RD_1, RD_2, RD_3 |
| t_2 | ZS, ZW |
| t_3 | _FW, Z1, Z2, RD_2, RD_3, ZW |
| t_4 | _DW, RD_0, RD_1, RD_2, RD_3 |
| t_5 | _ScR |


## `OR $D, $A` (0x74)

| Microstep | Control Signals |
| :---: | :---: |
| t_0 | IR_in, RD_2, PCC, _PCE |
| t_1 | Z1, ZS, Z0, RD_1, RD_2, RD_3 |
| t_2 | ZS, ZW |
| t_3 | _FW, Z2, Z0, RD_2, RD_3, ZW |
| t_4 | _DW, RD_0, RD_1, RD_2, RD_3 |
| t_5 | _ScR |


## `XOR $D, $A` (0x75)

| Microstep | Control Signals |
| :---: | :---: |
| t_0 | IR_in, RD_2, PCC, _PCE |
| t_1 | Z1, ZS, Z0, RD_1, RD_2, RD_3 |
| t_2 | ZS, ZW |
| t_3 | _FW, Z2, RD_2, RD_3, ZW |
| t_4 | _DW, RD_0, RD_1, RD_2, RD_3 |
| t_5 | _ScR |


## `CMP $D, $A` (0x76)

| Microstep | Control Signals |
| :---: | :---: |
| t_0 | IR_in, RD_2, PCC, _PCE |
| t_1 | Z1, ZS, Z0, RD_1, RD_2, RD_3 |
| t_2 | ZS, ZW |
| t_3 | _FW, Z0, RD_2, RD_3 |
| t_4 | _ScR |


## `MOV $D, $B` (0x77)

| Microstep | Control Signals |
| :---: | :---: |
| t_0 | IR_in, RD_2, PCC, _PCE |
| t_1 | _DW, RD_0, RD_1, RD_3 |
| t_2 | _ScR |


## `ADD $D, $B` (0x78)

| Microstep | Control Signals |
| :---: | :---: |
| t_0 | IR_in, RD_2, PCC, _PCE |
| t_1 | Z1, ZS, Z0, RD_1, RD_2, RD_3 |
| t_2 | ZS, ZW |
| t_3 | _FW, Z1, Z0, RD_0, RD_1, RD_3, ZW |
| t_4 | _DW, RD_0, RD_1, RD_2, RD_3 |
| t_5 | _ScR |


## `SUB $D, $B` (0x79)

| Microstep | Control Signals |
| :---: | :---: |
| t_0 | IR_in, RD_2, PCC, _PCE |
| t_1 | Z1, ZS, Z0, RD_1, RD_2, RD_3 |
| t_2 | ZS, ZW |
| t_3 | _FW, Z0, RD_0, RD_1, RD_3, ZW |
| t_4 | _DW, RD_0, RD_1, RD_2, RD_3 |
| t_5 | _ScR |


## `AND $D, $B` (0x7A)

| Microstep | Control Signals |
| :---: | :---: |
| t_0 | IR_in, RD_2, PCC, _PCE |
| t_1 | Z1, ZS, Z0, RD_1, RD_2, RD_3 |
| t_2 | ZS, ZW |
| t_3 | _FW, Z1, Z2, RD_0, RD_1, RD_3, ZW |
| t_4 | _DW, RD_0, RD_1, RD_2, RD_3 |
| t_5 | _ScR |


## `OR $D, $B` (0x7B)

| Microstep | Control Signals |
| :---: | :---: |
| t_0 | IR_in, RD_2, PCC, _PCE |
| t_1 | Z1, ZS, Z0, RD_1, RD_2, RD_3 |
| t_2 | ZS, ZW |
| t_3 | _FW, Z2, Z0, RD_0, RD_1, RD_3, ZW |
| t_4 | _DW, RD_0, RD_1, RD_2, RD_3 |
| t_5 | _ScR |


## `XOR $D, $B` (0x7C)

| Microstep | Control Signals |
| :---: | :---: |
| t_0 | IR_in, RD_2, PCC, _PCE |
| t_1 | Z1, ZS, Z0, RD_1, RD_2, RD_3 |
| t_2 | ZS, ZW |
| t_3 | _FW, Z2, RD_0, RD_1, RD_3, ZW |
| t_4 | _DW, RD_0, RD_1, RD_2, RD_3 |
| t_5 | _ScR |


## `CMP $D, $B` (0x7D)

| Microstep | Control Signals |
| :---: | :---: |
| t_0 | IR_in, RD_2, PCC, _PCE |
| t_1 | Z1, ZS, Z0, RD_1, RD_2, RD_3 |
| t_2 | ZS, ZW |
| t_3 | _FW, Z0, RD_0, RD_1, RD_3 |
| t_4 | _ScR |


## `MOV $D, $C` (0x7E)

| Microstep | Control Signals |
| :---: | :---: |
| t_0 | IR_in, RD_2, PCC, _PCE |
| t_1 | _DW, RD_0, RD_2, RD_3 |
| t_2 | _ScR |


## `ADD $D, $C` (0x7F)

| Microstep | Control Signals |
| :---: | :---: |
| t_0 | IR_in, RD_2, PCC, _PCE |
| t_1 | Z1, ZS, Z0, RD_1, RD_2, RD_3 |
| t_2 | ZS, ZW |
| t_3 | _FW, Z1, Z0, RD_0, RD_2, RD_3, ZW |
| t_4 | _DW, RD_0, RD_1, RD_2, RD_3 |
| t_5 | _ScR |


## `SUB $D, $C` (0x80)

| Microstep | Control Signals |
| :---: | :---: |
| t_0 | IR_in, RD_2, PCC, _PCE |
| t_1 | Z1, ZS, Z0, RD_1, RD_2, RD_3 |
| t_2 | ZS, ZW |
| t_3 | _FW, Z0, RD_0, RD_2, RD_3, ZW |
| t_4 | _DW, RD_0, RD_1, RD_2, RD_3 |
| t_5 | _ScR |


## `AND $D, $C` (0x81)

| Microstep | Control Signals |
| :---: | :---: |
| t_0 | IR_in, RD_2, PCC, _PCE |
| t_1 | Z1, ZS, Z0, RD_1, RD_2, RD_3 |
| t_2 | ZS, ZW |
| t_3 | _FW, Z1, Z2, RD_0, RD_2, RD_3, ZW |
| t_4 | _DW, RD_0, RD_1, RD_2, RD_3 |
| t_5 | _ScR |


## `OR $D, $C` (0x82)

| Microstep | Control Signals |
| :---: | :---: |
| t_0 | IR_in, RD_2, PCC, _PCE |
| t_1 | Z1, ZS, Z0, RD_1, RD_2, RD_3 |
| t_2 | ZS, ZW |
| t_3 | _FW, Z2, Z0, RD_0, RD_2, RD_3, ZW |
| t_4 | _DW, RD_0, RD_1, RD_2, RD_3 |
| t_5 | _ScR |


## `XOR $D, $C` (0x83)

| Microstep | Control Signals |
| :---: | :---: |
| t_0 | IR_in, RD_2, PCC, _PCE |
| t_1 | Z1, ZS, Z0, RD_1, RD_2, RD_3 |
| t_2 | ZS, ZW |
| t_3 | _FW, Z2, RD_0, RD_2, RD_3, ZW |
| t_4 | _DW, RD_0, RD_1, RD_2, RD_3 |
| t_5 | _ScR |


## `CMP $D, $C` (0x84)

| Microstep | Control Signals |
| :---: | :---: |
| t_0 | IR_in, RD_2, PCC, _PCE |
| t_1 | Z1, ZS, Z0, RD_1, RD_2, RD_3 |
| t_2 | ZS, ZW |
| t_3 | _FW, Z0, RD_0, RD_2, RD_3 |
| t_4 | _ScR |


## `MOV $A, [$CD]` (0x85)

| Microstep | Control Signals |
| :---: | :---: |
| t_0 | IR_in, RD_2, PCC, _PCE |
| t_1 | BRlW, RD_0, RD_2, RD_3 |
| t_2 | RD_1, RD_2, RD_3, BRhW |
| t_3 | RD_2, WR_1, _BRE |
| t_4 | _ScR |


## `MOV [$CD], $A` (0x86)

| Microstep | Control Signals |
| :---: | :---: |
| t_0 | IR_in, RD_2, PCC, _PCE |
| t_1 | BRlW, RD_0, RD_2, RD_3 |
| t_2 | RD_1, RD_2, RD_3, BRhW |
| t_3 | RD_2, RD_3, _BRE, _MW |
| t_4 | _ScR |


## `ADD $A, [$CD]` (0x87)

| Microstep | Control Signals |
| :---: | :---: |
| t_0 | IR_in, RD_2, PCC, _PCE |
| t_1 | BRlW, RD_0, RD_2, RD_3 |
| t_2 | RD_1, RD_2, RD_3, BRhW |
| t_3 | Z1, ZS, Z0, RD_2, RD_3 |
| t_4 | ZS, ZW |
| t_5 | _FW, Z1, Z0, RD_2, _BRE, ZW |
| t_6 | RD_0, RD_1, RD_2, RD_3, WR_1 |
| t_7 | _ScR |


## `SUB $A, [$CD]` (0x88)

| Microstep | Control Signals |
| :---: | :---: |
| t_0 | IR_in, RD_2, PCC, _PCE |
| t_1 | BRlW, RD_0, RD_2, RD_3 |
| t_2 | RD_1, RD_2, RD_3, BRhW |
| t_3 | Z1, ZS, Z0, RD_2, RD_3 |
| t_4 | ZS, ZW |
| t_5 | _FW, Z0, RD_2, _BRE, ZW |
| t_6 | RD_0, RD_1, RD_2, RD_3, WR_1 |
| t_7 | _ScR |


## `AND $A, [$CD]` (0x89)

| Microstep | Control Signals |
| :---: | :---: |
| t_0 | IR_in, RD_2, PCC, _PCE |
| t_1 | BRlW, RD_0, RD_2, RD_3 |
| t_2 | RD_1, RD_2, RD_3, BRhW |
| t_3 | Z1, ZS, Z0, RD_2, RD_3 |
| t_4 | ZS, ZW |
| t_5 | _FW, Z1, Z2, RD_2, _BRE, ZW |
| t_6 | RD_0, RD_1, RD_2, RD_3, WR_1 |
| t_7 | _ScR |


## `OR $A, [$CD]` (0x8A)

| Microstep | Control Signals |
| :---: | :---: |
| t_0 | IR_in, RD_2, PCC, _PCE |
| t_1 | BRlW, RD_0, RD_2, RD_3 |
| t_2 | RD_1, RD_2, RD_3, BRhW |
| t_3 | Z1, ZS, Z0, RD_2, RD_3 |
| t_4 | ZS, ZW |
| t_5 | _FW, Z2, Z0, RD_2, _BRE, ZW |
| t_6 | RD_0, RD_1, RD_2, RD_3, WR_1 |
| t_7 | _ScR |


## `XOR $A, [$CD]` (0x8B)

| Microstep | Control Signals |
| :---: | :---: |
| t_0 | IR_in, RD_2, PCC, _PCE |
| t_1 | BRlW, RD_0, RD_2, RD_3 |
| t_2 | RD_1, RD_2, RD_3, BRhW |
| t_3 | Z1, ZS, Z0, RD_2, RD_3 |
| t_4 | ZS, ZW |
| t_5 | _FW, Z2, RD_2, _BRE, ZW |
| t_6 | RD_0, RD_1, RD_2, RD_3, WR_1 |
| t_7 | _ScR |


## `CMP $A, [$CD]` (0x8C)

| Microstep | Control Signals |
| :---: | :---: |
| t_0 | IR_in, RD_2, PCC, _PCE |
| t_1 | BRlW, RD_0, RD_2, RD_3 |
| t_2 | RD_1, RD_2, RD_3, BRhW |
| t_3 | Z1, ZS, Z0, RD_2, RD_3 |
| t_4 | ZS, ZW |
| t_5 | _FW, Z0, RD_2, _BRE |
| t_6 | _ScR |


## `MOV $B, [$CD]` (0x8D)

| Microstep | Control Signals |
| :---: | :---: |
| t_0 | IR_in, RD_2, PCC, _PCE |
| t_1 | BRlW, RD_0, RD_2, RD_3 |
| t_2 | RD_1, RD_2, RD_3, BRhW |
| t_3 | _BW, RD_2, _BRE |
| t_4 | _ScR |


## `MOV [$CD], $B` (0x8E)

| Microstep | Control Signals |
| :---: | :---: |
| t_0 | IR_in, RD_2, PCC, _PCE |
| t_1 | BRlW, RD_0, RD_2, RD_3 |
| t_2 | RD_1, RD_2, RD_3, BRhW |
| t_3 | RD_0, RD_1, RD_3, _BRE, _MW |
| t_4 | _ScR |


## `ADD $B, [$CD]` (0x8F)

| Microstep | Control Signals |
| :---: | :---: |
| t_0 | IR_in, RD_2, PCC, _PCE |
| t_1 | BRlW, RD_0, RD_2, RD_3 |
| t_2 | RD_1, RD_2, RD_3, BRhW |
| t_3 | Z1, ZS, Z0, RD_0, RD_1, RD_3 |
| t_4 | ZS, ZW |
| t_5 | _FW, Z1, Z0, RD_2, _BRE, ZW |
| t_6 | _BW, RD_0, RD_1, RD_2, RD_3 |
| t_7 | _ScR |


## `SUB $B, [$CD]` (0x90)

| Microstep | Control Signals |
| :---: | :---: |
| t_0 | IR_in, RD_2, PCC, _PCE |
| t_1 | BRlW, RD_0, RD_2, RD_3 |
| t_2 | RD_1, RD_2, RD_3, BRhW |
| t_3 | Z1, ZS, Z0, RD_0, RD_1, RD_3 |
| t_4 | ZS, ZW |
| t_5 | _FW, Z0, RD_2, _BRE, ZW |
| t_6 | _BW, RD_0, RD_1, RD_2, RD_3 |
| t_7 | _ScR |


## `AND $B, [$CD]` (0x91)

| Microstep | Control Signals |
| :---: | :---: |
| t_0 | IR_in, RD_2, PCC, _PCE |
| t_1 | BRlW, RD_0, RD_2, RD_3 |
| t_2 | RD_1, RD_2, RD_3, BRhW |
| t_3 | Z1, ZS, Z0, RD_0, RD_1, RD_3 |
| t_4 | ZS, ZW |
| t_5 | _FW, Z1, Z2, RD_2, _BRE, ZW |
| t_6 | _BW, RD_0, RD_1, RD_2, RD_3 |
| t_7 | _ScR |


## `OR $B, [$CD]` (0x92)

| Microstep | Control Signals |
| :---: | :---: |
| t_0 | IR_in, RD_2, PCC, _PCE |
| t_1 | BRlW, RD_0, RD_2, RD_3 |
| t_2 | RD_1, RD_2, RD_3, BRhW |
| t_3 | Z1, ZS, Z0, RD_0, RD_1, RD_3 |
| t_4 | ZS, ZW |
| t_5 | _FW, Z2, Z0, RD_2, _BRE, ZW |
| t_6 | _BW, RD_0, RD_1, RD_2, RD_3 |
| t_7 | _ScR |


## `XOR $B, [$CD]` (0x93)

| Microstep | Control Signals |
| :---: | :---: |
| t_0 | IR_in, RD_2, PCC, _PCE |
| t_1 | BRlW, RD_0, RD_2, RD_3 |
| t_2 | RD_1, RD_2, RD_3, BRhW |
| t_3 | Z1, ZS, Z0, RD_0, RD_1, RD_3 |
| t_4 | ZS, ZW |
| t_5 | _FW, Z2, RD_2, _BRE, ZW |
| t_6 | _BW, RD_0, RD_1, RD_2, RD_3 |
| t_7 | _ScR |


## `CMP $B, [$CD]` (0x94)

| Microstep | Control Signals |
| :---: | :---: |
| t_0 | IR_in, RD_2, PCC, _PCE |
| t_1 | BRlW, RD_0, RD_2, RD_3 |
| t_2 | RD_1, RD_2, RD_3, BRhW |
| t_3 | Z1, ZS, Z0, RD_0, RD_1, RD_3 |
| t_4 | ZS, ZW |
| t_5 | _FW, Z0, RD_2, _BRE |
| t_6 | _ScR |


## `MOV $C, [$CD]` (0x95)

| Microstep | Control Signals |
| :---: | :---: |
| t_0 | IR_in, RD_2, PCC, _PCE |
| t_1 | BRlW, RD_0, RD_2, RD_3 |
| t_2 | RD_1, RD_2, RD_3, BRhW |
| t_3 | RD_2, WR_0, WR_1, _BRE |
| t_4 | _ScR |


## `MOV [$CD], $C` (0x96)

| Microstep | Control Signals |
| :---: | :---: |
| t_0 | IR_in, RD_2, PCC, _PCE |
| t_1 | BRlW, RD_0, RD_2, RD_3 |
| t_2 | RD_1, RD_2, RD_3, BRhW |
| t_3 | RD_0, RD_2, RD_3, _BRE, _MW |
| t_4 | _ScR |


## `ADD $C, [$CD]` (0x97)

| Microstep | Control Signals |
| :---: | :---: |
| t_0 | IR_in, RD_2, PCC, _PCE |
| t_1 | BRlW, RD_0, RD_2, RD_3 |
| t_2 | RD_1, RD_2, RD_3, BRhW |
| t_3 | Z1, ZS, Z0, RD_0, RD_2, RD_3 |
| t_4 | ZS, ZW |
| t_5 | _FW, Z1, Z0, RD_2, _BRE, ZW |
| t_6 | RD_0, RD_1, RD_2, RD_3, WR_0, WR_1 |
| t_7 | _ScR |


## `SUB $C, [$CD]` (0x98)

| Microstep | Control Signals |
| :---: | :---: |
| t_0 | IR_in, RD_2, PCC, _PCE |
| t_1 | BRlW, RD_0, RD_2, RD_3 |
| t_2 | RD_1, RD_2, RD_3, BRhW |
| t_3 | Z1, ZS, Z0, RD_0, RD_2, RD_3 |
| t_4 | ZS, ZW |
| t_5 | _FW, Z0, RD_2, _BRE, ZW |
| t_6 | RD_0, RD_1, RD_2, RD_3, WR_0, WR_1 |
| t_7 | _ScR |


## `AND $C, [$CD]` (0x99)

| Microstep | Control Signals |
| :---: | :---: |
| t_0 | IR_in, RD_2, PCC, _PCE |
| t_1 | BRlW, RD_0, RD_2, RD_3 |
| t_2 | RD_1, RD_2, RD_3, BRhW |
| t_3 | Z1, ZS, Z0, RD_0, RD_2, RD_3 |
| t_4 | ZS, ZW |
| t_5 | _FW, Z1, Z2, RD_2, _BRE, ZW |
| t_6 | RD_0, RD_1, RD_2, RD_3, WR_0, WR_1 |
| t_7 | _ScR |


## `OR $C, [$CD]` (0x9A)

| Microstep | Control Signals |
| :---: | :---: |
| t_0 | IR_in, RD_2, PCC, _PCE |
| t_1 | BRlW, RD_0, RD_2, RD_3 |
| t_2 | RD_1, RD_2, RD_3, BRhW |
| t_3 | Z1, ZS, Z0, RD_0, RD_2, RD_3 |
| t_4 | ZS, ZW |
| t_5 | _FW, Z2, Z0, RD_2, _BRE, ZW |
| t_6 | RD_0, RD_1, RD_2, RD_3, WR_0, WR_1 |
| t_7 | _ScR |


## `XOR $C, [$CD]` (0x9B)

| Microstep | Control Signals |
| :---: | :---: |
| t_0 | IR_in, RD_2, PCC, _PCE |
| t_1 | BRlW, RD_0, RD_2, RD_3 |
| t_2 | RD_1, RD_2, RD_3, BRhW |
| t_3 | Z1, ZS, Z0, RD_0, RD_2, RD_3 |
| t_4 | ZS, ZW |
| t_5 | _FW, Z2, RD_2, _BRE, ZW |
| t_6 | RD_0, RD_1, RD_2, RD_3, WR_0, WR_1 |
| t_7 | _ScR |


## `CMP $C, [$CD]` (0x9C)

| Microstep | Control Signals |
| :---: | :---: |
| t_0 | IR_in, RD_2, PCC, _PCE |
| t_1 | BRlW, RD_0, RD_2, RD_3 |
| t_2 | RD_1, RD_2, RD_3, BRhW |
| t_3 | Z1, ZS, Z0, RD_0, RD_2, RD_3 |
| t_4 | ZS, ZW |
| t_5 | _FW, Z0, RD_2, _BRE |
| t_6 | _ScR |


## `MOV $D, [$CD]` (0x9D)

| Microstep | Control Signals |
| :---: | :---: |
| t_0 | IR_in, RD_2, PCC, _PCE |
| t_1 | BRlW, RD_0, RD_2, RD_3 |
| t_2 | RD_1, RD_2, RD_3, BRhW |
| t_3 | _DW, RD_2, _BRE |
| t_4 | _ScR |


## `MOV [$CD], $D` (0x9E)

| Microstep | Control Signals |
| :---: | :---: |
| t_0 | IR_in, RD_2, PCC, _PCE |
| t_1 | BRlW, RD_0, RD_2, RD_3 |
| t_2 | RD_1, RD_2, RD_3, BRhW |
| t_3 | RD_1, RD_2, RD_3, _BRE, _MW |
| t_4 | _ScR |


## `ADD $D, [$CD]` (0x9F)

| Microstep | Control Signals |
| :---: | :---: |
| t_0 | IR_in, RD_2, PCC, _PCE |
| t_1 | BRlW, RD_0, RD_2, RD_3 |
| t_2 | RD_1, RD_2, RD_3, BRhW |
| t_3 | Z1, ZS, Z0, RD_1, RD_2, RD_3 |
| t_4 | ZS, ZW |
| t_5 | _FW, Z1, Z0, RD_2, _BRE, ZW |
| t_6 | _DW, RD_0, RD_1, RD_2, RD_3 |
| t_7 | _ScR |


## `SUB $D, [$CD]` (0xA0)

| Microstep | Control Signals |
| :---: | :---: |
| t_0 | IR_in, RD_2, PCC, _PCE |
| t_1 | BRlW, RD_0, RD_2, RD_3 |
| t_2 | RD_1, RD_2, RD_3, BRhW |
| t_3 | Z1, ZS, Z0, RD_1, RD_2, RD_3 |
| t_4 | ZS, ZW |
| t_5 | _FW, Z0, RD_2, _BRE, ZW |
| t_6 | _DW, RD_0, RD_1, RD_2, RD_3 |
| t_7 | _ScR |


## `AND $D, [$CD]` (0xA1)

| Microstep | Control Signals |
| :---: | :---: |
| t_0 | IR_in, RD_2, PCC, _PCE |
| t_1 | BRlW, RD_0, RD_2, RD_3 |
| t_2 | RD_1, RD_2, RD_3, BRhW |
| t_3 | Z1, ZS, Z0, RD_1, RD_2, RD_3 |
| t_4 | ZS, ZW |
| t_5 | _FW, Z1, Z2, RD_2, _BRE, ZW |
| t_6 | _DW, RD_0, RD_1, RD_2, RD_3 |
| t_7 | _ScR |


## `OR $D, [$CD]` (0xA2)

| Microstep | Control Signals |
| :---: | :---: |
| t_0 | IR_in, RD_2, PCC, _PCE |
| t_1 | BRlW, RD_0, RD_2, RD_3 |
| t_2 | RD_1, RD_2, RD_3, BRhW |
| t_3 | Z1, ZS, Z0, RD_1, RD_2, RD_3 |
| t_4 | ZS, ZW |
| t_5 | _FW, Z2, Z0, RD_2, _BRE, ZW |
| t_6 | _DW, RD_0, RD_1, RD_2, RD_3 |
| t_7 | _ScR |


## `XOR $D, [$CD]` (0xA3)

| Microstep | Control Signals |
| :---: | :---: |
| t_0 | IR_in, RD_2, PCC, _PCE |
| t_1 | BRlW, RD_0, RD_2, RD_3 |
| t_2 | RD_1, RD_2, RD_3, BRhW |
| t_3 | Z1, ZS, Z0, RD_1, RD_2, RD_3 |
| t_4 | ZS, ZW |
| t_5 | _FW, Z2, RD_2, _BRE, ZW |
| t_6 | _DW, RD_0, RD_1, RD_2, RD_3 |
| t_7 | _ScR |


## `CMP $D, [$CD]` (0xA4)

| Microstep | Control Signals |
| :---: | :---: |
| t_0 | IR_in, RD_2, PCC, _PCE |
| t_1 | BRlW, RD_0, RD_2, RD_3 |
| t_2 | RD_1, RD_2, RD_3, BRhW |
| t_3 | Z1, ZS, Z0, RD_1, RD_2, RD_3 |
| t_4 | ZS, ZW |
| t_5 | _FW, Z0, RD_2, _BRE |
| t_6 | _ScR |


## `MOV $A, [@]` (0xA5)

| Microstep | Control Signals |
| :---: | :---: |
| t_0 | IR_in, RD_2, PCC, _PCE |
| t_1 | BRlW, RD_2, PCC, _PCE |
| t_2 | RD_2, _PCE, BRhW |
| t_3 | RD_2, WR_1, PCC, _BRE |
| t_4 | _ScR |


## `MOV [@], $A` (0xA6)

| Microstep | Control Signals |
| :---: | :---: |
| t_0 | IR_in, RD_2, PCC, _PCE |
| t_1 | BRlW, RD_2, PCC, _PCE |
| t_2 | RD_2, _PCE, BRhW |
| t_3 | RD_2, RD_3, PCC, _BRE, _MW |
| t_4 | _ScR |


## `ADD $A, [@]` (0xA7)

| Microstep | Control Signals |
| :---: | :---: |
| t_0 | IR_in, RD_2, PCC, _PCE |
| t_1 | BRlW, RD_2, PCC, _PCE |
| t_2 | RD_2, _PCE, BRhW |
| t_3 | Z1, ZS, Z0, RD_2, RD_3, PCC |
| t_4 | ZS, ZW |
| t_5 | _FW, Z1, Z0, RD_2, _BRE, ZW |
| t_6 | RD_0, RD_1, RD_2, RD_3, WR_1 |
| t_7 | _ScR |


## `SUB $A, [@]` (0xA8)

| Microstep | Control Signals |
| :---: | :---: |
| t_0 | IR_in, RD_2, PCC, _PCE |
| t_1 | BRlW, RD_2, PCC, _PCE |
| t_2 | RD_2, _PCE, BRhW |
| t_3 | Z1, ZS, Z0, RD_2, RD_3, PCC |
| t_4 | ZS, ZW |
| t_5 | _FW, Z0, RD_2, _BRE, ZW |
| t_6 | RD_0, RD_1, RD_2, RD_3, WR_1 |
| t_7 | _ScR |


## `AND $A, [@]` (0xA9)

| Microstep | Control Signals |
| :---: | :---: |
| t_0 | IR_in, RD_2, PCC, _PCE |
| t_1 | BRlW, RD_2, PCC, _PCE |
| t_2 | RD_2, _PCE, BRhW |
| t_3 | Z1, ZS, Z0, RD_2, RD_3, PCC |
| t_4 | ZS, ZW |
| t_5 | _FW, Z1, Z2, RD_2, _BRE, ZW |
| t_6 | RD_0, RD_1, RD_2, RD_3, WR_1 |
| t_7 | _ScR |


## `OR $A, [@]` (0xAA)

| Microstep | Control Signals |
| :---: | :---: |
| t_0 | IR_in, RD_2, PCC, _PCE |
| t_1 | BRlW, RD_2, PCC, _PCE |
| t_2 | RD_2, _PCE, BRhW |
| t_3 | Z1, ZS, Z0, RD_2, RD_3, PCC |
| t_4 | ZS, ZW |
| t_5 | _FW, Z2, Z0, RD_2, _BRE, ZW |
| t_6 | RD_0, RD_1, RD_2, RD_3, WR_1 |
| t_7 | _ScR |


## `XOR $A, [@]` (0xAB)

| Microstep | Control Signals |
| :---: | :---: |
| t_0 | IR_in, RD_2, PCC, _PCE |
| t_1 | BRlW, RD_2, PCC, _PCE |
| t_2 | RD_2, _PCE, BRhW |
| t_3 | Z1, ZS, Z0, RD_2, RD_3, PCC |
| t_4 | ZS, ZW |
| t_5 | _FW, Z2, RD_2, _BRE, ZW |
| t_6 | RD_0, RD_1, RD_2, RD_3, WR_1 |
| t_7 | _ScR |


## `CMP $A, [@]` (0xAC)

| Microstep | Control Signals |
| :---: | :---: |
| t_0 | IR_in, RD_2, PCC, _PCE |
| t_1 | BRlW, RD_2, PCC, _PCE |
| t_2 | RD_2, _PCE, BRhW |
| t_3 | Z1, ZS, Z0, RD_2, RD_3, PCC |
| t_4 | ZS, ZW |
| t_5 | _FW, Z0, RD_2, _BRE |
| t_6 | _ScR |


## `MOV $B, [@]` (0xAD)

| Microstep | Control Signals |
| :---: | :---: |
| t_0 | IR_in, RD_2, PCC, _PCE |
| t_1 | BRlW, RD_2, PCC, _PCE |
| t_2 | RD_2, _PCE, BRhW |
| t_3 | _BW, RD_2, PCC, _BRE |
| t_4 | _ScR |


## `MOV [@], $B` (0xAE)

| Microstep | Control Signals |
| :---: | :---: |
| t_0 | IR_in, RD_2, PCC, _PCE |
| t_1 | BRlW, RD_2, PCC, _PCE |
| t_2 | RD_2, _PCE, BRhW |
| t_3 | RD_0, RD_1, RD_3, PCC, _BRE, _MW |
| t_4 | _ScR |


## `ADD $B, [@]` (0xAF)

| Microstep | Control Signals |
| :---: | :---: |
| t_0 | IR_in, RD_2, PCC, _PCE |
| t_1 | BRlW, RD_2, PCC, _PCE |
| t_2 | RD_2, _PCE, BRhW |
| t_3 | Z1, ZS, Z0, RD_0, RD_1, RD_3, PCC |
| t_4 | ZS, ZW |
| t_5 | _FW, Z1, Z0, RD_2, _BRE, ZW |
| t_6 | _BW, RD_0, RD_1, RD_2, RD_3 |
| t_7 | _ScR |


## `SUB $B, [@]` (0xB0)

| Microstep | Control Signals |
| :---: | :---: |
| t_0 | IR_in, RD_2, PCC, _PCE |
| t_1 | BRlW, RD_2, PCC, _PCE |
| t_2 | RD_2, _PCE, BRhW |
| t_3 | Z1, ZS, Z0, RD_0, RD_1, RD_3, PCC |
| t_4 | ZS, ZW |
| t_5 | _FW, Z0, RD_2, _BRE, ZW |
| t_6 | _BW, RD_0, RD_1, RD_2, RD_3 |
| t_7 | _ScR |


## `AND $B, [@]` (0xB1)

| Microstep | Control Signals |
| :---: | :---: |
| t_0 | IR_in, RD_2, PCC, _PCE |
| t_1 | BRlW, RD_2, PCC, _PCE |
| t_2 | RD_2, _PCE, BRhW |
| t_3 | Z1, ZS, Z0, RD_0, RD_1, RD_3, PCC |
| t_4 | ZS, ZW |
| t_5 | _FW, Z1, Z2, RD_2, _BRE, ZW |
| t_6 | _BW, RD_0, RD_1, RD_2, RD_3 |
| t_7 | _ScR |


## `OR $B, [@]` (0xB2)

| Microstep | Control Signals |
| :---: | :---: |
| t_0 | IR_in, RD_2, PCC, _PCE |
| t_1 | BRlW, RD_2, PCC, _PCE |
| t_2 | RD_2, _PCE, BRhW |
| t_3 | Z1, ZS, Z0, RD_0, RD_1, RD_3, PCC |
| t_4 | ZS, ZW |
| t_5 | _FW, Z2, Z0, RD_2, _BRE, ZW |
| t_6 | _BW, RD_0, RD_1, RD_2, RD_3 |
| t_7 | _ScR |


## `XOR $B, [@]` (0xB3)

| Microstep | Control Signals |
| :---: | :---: |
| t_0 | IR_in, RD_2, PCC, _PCE |
| t_1 | BRlW, RD_2, PCC, _PCE |
| t_2 | RD_2, _PCE, BRhW |
| t_3 | Z1, ZS, Z0, RD_0, RD_1, RD_3, PCC |
| t_4 | ZS, ZW |
| t_5 | _FW, Z2, RD_2, _BRE, ZW |
| t_6 | _BW, RD_0, RD_1, RD_2, RD_3 |
| t_7 | _ScR |


## `CMP $B, [@]` (0xB4)

| Microstep | Control Signals |
| :---: | :---: |
| t_0 | IR_in, RD_2, PCC, _PCE |
| t_1 | BRlW, RD_2, PCC, _PCE |
| t_2 | RD_2, _PCE, BRhW |
| t_3 | Z1, ZS, Z0, RD_0, RD_1, RD_3, PCC |
| t_4 | ZS, ZW |
| t_5 | _FW, Z0, RD_2, _BRE |
| t_6 | _ScR |


## `MOV $C, [@]` (0xB5)

| Microstep | Control Signals |
| :---: | :---: |
| t_0 | IR_in, RD_2, PCC, _PCE |
| t_1 | BRlW, RD_2, PCC, _PCE |
| t_2 | RD_2, _PCE, BRhW |
| t_3 | RD_2, WR_0, WR_1, PCC, _BRE |
| t_4 | _ScR |


## `MOV [@], $C` (0xB6)

| Microstep | Control Signals |
| :---: | :---: |
| t_0 | IR_in, RD_2, PCC, _PCE |
| t_1 | BRlW, RD_2, PCC, _PCE |
| t_2 | RD_2, _PCE, BRhW |
| t_3 | RD_0, RD_2, RD_3, PCC, _BRE, _MW |
| t_4 | _ScR |


## `ADD $C, [@]` (0xB7)

| Microstep | Control Signals |
| :---: | :---: |
| t_0 | IR_in, RD_2, PCC, _PCE |
| t_1 | BRlW, RD_2, PCC, _PCE |
| t_2 | RD_2, _PCE, BRhW |
| t_3 | Z1, ZS, Z0, RD_0, RD_2, RD_3, PCC |
| t_4 | ZS, ZW |
| t_5 | _FW, Z1, Z0, RD_2, _BRE, ZW |
| t_6 | RD_0, RD_1, RD_2, RD_3, WR_0, WR_1 |
| t_7 | _ScR |


## `SUB $C, [@]` (0xB8)

| Microstep | Control Signals |
| :---: | :---: |
| t_0 | IR_in, RD_2, PCC, _PCE |
| t_1 | BRlW, RD_2, PCC, _PCE |
| t_2 | RD_2, _PCE, BRhW |
| t_3 | Z1, ZS, Z0, RD_0, RD_2, RD_3, PCC |
| t_4 | ZS, ZW |
| t_5 | _FW, Z0, RD_2, _BRE, ZW |
| t_6 | RD_0, RD_1, RD_2, RD_3, WR_0, WR_1 |
| t_7 | _ScR |


## `AND $C, [@]` (0xB9)

| Microstep | Control Signals |
| :---: | :---: |
| t_0 | IR_in, RD_2, PCC, _PCE |
| t_1 | BRlW, RD_2, PCC, _PCE |
| t_2 | RD_2, _PCE, BRhW |
| t_3 | Z1, ZS, Z0, RD_0, RD_2, RD_3, PCC |
| t_4 | ZS, ZW |
| t_5 | _FW, Z1, Z2, RD_2, _BRE, ZW |
| t_6 | RD_0, RD_1, RD_2, RD_3, WR_0, WR_1 |
| t_7 | _ScR |


## `OR $C, [@]` (0xBA)

| Microstep | Control Signals |
| :---: | :---: |
| t_0 | IR_in, RD_2, PCC, _PCE |
| t_1 | BRlW, RD_2, PCC, _PCE |
| t_2 | RD_2, _PCE, BRhW |
| t_3 | Z1, ZS, Z0, RD_0, RD_2, RD_3, PCC |
| t_4 | ZS, ZW |
| t_5 | _FW, Z2, Z0, RD_2, _BRE, ZW |
| t_6 | RD_0, RD_1, RD_2, RD_3, WR_0, WR_1 |
| t_7 | _ScR |


## `XOR $C, [@]` (0xBB)

| Microstep | Control Signals |
| :---: | :---: |
| t_0 | IR_in, RD_2, PCC, _PCE |
| t_1 | BRlW, RD_2, PCC, _PCE |
| t_2 | RD_2, _PCE, BRhW |
| t_3 | Z1, ZS, Z0, RD_0, RD_2, RD_3, PCC |
| t_4 | ZS, ZW |
| t_5 | _FW, Z2, RD_2, _BRE, ZW |
| t_6 | RD_0, RD_1, RD_2, RD_3, WR_0, WR_1 |
| t_7 | _ScR |


## `CMP $C, [@]` (0xBC)

| Microstep | Control Signals |
| :---: | :---: |
| t_0 | IR_in, RD_2, PCC, _PCE |
| t_1 | BRlW, RD_2, PCC, _PCE |
| t_2 | RD_2, _PCE, BRhW |
| t_3 | Z1, ZS, Z0, RD_0, RD_2, RD_3, PCC |
| t_4 | ZS, ZW |
| t_5 | _FW, Z0, RD_2, _BRE |
| t_6 | _ScR |


## `MOV $D, [@]` (0xBD)

| Microstep | Control Signals |
| :---: | :---: |
| t_0 | IR_in, RD_2, PCC, _PCE |
| t_1 | BRlW, RD_2, PCC, _PCE |
| t_2 | RD_2, _PCE, BRhW |
| t_3 | _DW, RD_2, PCC, _BRE |
| t_4 | _ScR |


## `MOV [@], $D` (0xBE)

| Microstep | Control Signals |
| :---: | :---: |
| t_0 | IR_in, RD_2, PCC, _PCE |
| t_1 | BRlW, RD_2, PCC, _PCE |
| t_2 | RD_2, _PCE, BRhW |
| t_3 | RD_1, RD_2, RD_3, PCC, _BRE, _MW |
| t_4 | _ScR |


## `ADD $D, [@]` (0xBF)

| Microstep | Control Signals |
| :---: | :---: |
| t_0 | IR_in, RD_2, PCC, _PCE |
| t_1 | BRlW, RD_2, PCC, _PCE |
| t_2 | RD_2, _PCE, BRhW |
| t_3 | Z1, ZS, Z0, RD_1, RD_2, RD_3, PCC |
| t_4 | ZS, ZW |
| t_5 | _FW, Z1, Z0, RD_2, _BRE, ZW |
| t_6 | _DW, RD_0, RD_1, RD_2, RD_3 |
| t_7 | _ScR |


## `SUB $D, [@]` (0xC0)

| Microstep | Control Signals |
| :---: | :---: |
| t_0 | IR_in, RD_2, PCC, _PCE |
| t_1 | BRlW, RD_2, PCC, _PCE |
| t_2 | RD_2, _PCE, BRhW |
| t_3 | Z1, ZS, Z0, RD_1, RD_2, RD_3, PCC |
| t_4 | ZS, ZW |
| t_5 | _FW, Z0, RD_2, _BRE, ZW |
| t_6 | _DW, RD_0, RD_1, RD_2, RD_3 |
| t_7 | _ScR |


## `AND $D, [@]` (0xC1)

| Microstep | Control Signals |
| :---: | :---: |
| t_0 | IR_in, RD_2, PCC, _PCE |
| t_1 | BRlW, RD_2, PCC, _PCE |
| t_2 | RD_2, _PCE, BRhW |
| t_3 | Z1, ZS, Z0, RD_1, RD_2, RD_3, PCC |
| t_4 | ZS, ZW |
| t_5 | _FW, Z1, Z2, RD_2, _BRE, ZW |
| t_6 | _DW, RD_0, RD_1, RD_2, RD_3 |
| t_7 | _ScR |


## `OR $D, [@]` (0xC2)

| Microstep | Control Signals |
| :---: | :---: |
| t_0 | IR_in, RD_2, PCC, _PCE |
| t_1 | BRlW, RD_2, PCC, _PCE |
| t_2 | RD_2, _PCE, BRhW |
| t_3 | Z1, ZS, Z0, RD_1, RD_2, RD_3, PCC |
| t_4 | ZS, ZW |
| t_5 | _FW, Z2, Z0, RD_2, _BRE, ZW |
| t_6 | _DW, RD_0, RD_1, RD_2, RD_3 |
| t_7 | _ScR |


## `XOR $D, [@]` (0xC3)

| Microstep | Control Signals |
| :---: | :---: |
| t_0 | IR_in, RD_2, PCC, _PCE |
| t_1 | BRlW, RD_2, PCC, _PCE |
| t_2 | RD_2, _PCE, BRhW |
| t_3 | Z1, ZS, Z0, RD_1, RD_2, RD_3, PCC |
| t_4 | ZS, ZW |
| t_5 | _FW, Z2, RD_2, _BRE, ZW |
| t_6 | _DW, RD_0, RD_1, RD_2, RD_3 |
| t_7 | _ScR |


## `CMP $D, [@]` (0xC4)

| Microstep | Control Signals |
| :---: | :---: |
| t_0 | IR_in, RD_2, PCC, _PCE |
| t_1 | BRlW, RD_2, PCC, _PCE |
| t_2 | RD_2, _PCE, BRhW |
| t_3 | Z1, ZS, Z0, RD_1, RD_2, RD_3, PCC |
| t_4 | ZS, ZW |
| t_5 | _FW, Z0, RD_2, _BRE |
| t_6 | _ScR |


## `SDL $A` (0xC5)

| Microstep | Control Signals |
| :---: | :---: |
| t_0 | IR_in, RD_2, PCC, _PCE |
| t_1 | RD_2, RD_3, WR_0, WR_2 |
| t_2 | _ScR |


## `SDL $B` (0xC6)

| Microstep | Control Signals |
| :---: | :---: |
| t_0 | IR_in, RD_2, PCC, _PCE |
| t_1 | RD_0, RD_1, RD_3, WR_0, WR_2 |
| t_2 | _ScR |


## `SDH $A` (0xC7)

| Microstep | Control Signals |
| :---: | :---: |
| t_0 | IR_in, RD_2, PCC, _PCE |
| t_1 | RD_2, RD_3, WR_0, WR_1, WR_2 |
| t_2 | _ScR |


## `SDH $B` (0xC8)

| Microstep | Control Signals |
| :---: | :---: |
| t_0 | IR_in, RD_2, PCC, _PCE |
| t_1 | RD_0, RD_1, RD_3, WR_0, WR_1, WR_2 |
| t_2 | _ScR |


## `OUT #, $A` (0xC9)

| Microstep | Control Signals |
| :---: | :---: |
| t_0 | IR_in, RD_2, PCC, _PCE |
| t_1 | RD_2, _PS, PCC, _PCE |
| t_2 | _PSW, RD_2, RD_3 |
| t_3 | _ScR |


## `INP $A, #` (0xCA)

| Microstep | Control Signals |
| :---: | :---: |
| t_0 | IR_in, RD_2, PCC, _PCE |
| t_1 | RD_2, _PS, PCC, _PCE |
| t_2 | _PSE, WR_1 |
| t_3 | _ScR |


## `OUT $B, $A` (0xCB)

| Microstep | Control Signals |
| :---: | :---: |
| t_0 | IR_in, RD_2, PCC, _PCE |
| t_1 | RD_0, RD_1, RD_3, _PS |
| t_2 | _PSW, RD_2, RD_3 |
| t_3 | _ScR |


## `INP $A, $B` (0xCC)

| Microstep | Control Signals |
| :---: | :---: |
| t_0 | IR_in, RD_2, PCC, _PCE |
| t_1 | RD_0, RD_1, RD_3, _PS |
| t_2 | _PSE, WR_1 |
| t_3 | _ScR |


## `OLR` (0xCD)

| Microstep | Control Signals |
| :---: | :---: |
| t_0 | IR_in, RD_2, PCC, _PCE |
| t_1 | _OC |
| t_2 | _OC |
| t_3 | _OC |
| t_4 | _OC |
| t_5 | _OC |
| t_6 | _OC |
| t_7 | _ScR |


## `OLD #` (0xCE)

| Microstep | Control Signals |
| :---: | :---: |
| t_0 | IR_in, RD_2, PCC, _PCE |
| t_1 | RD_2, _PCE |
| t_2 | OE, RD_2, PCC, _PCE |
| t_3 | _ScR |


## `OLC #` (0xCF)

| Microstep | Control Signals |
| :---: | :---: |
| t_0 | IR_in, RD_2, PCC, _PCE |
| t_1 | _OS, RD_2, _PCE |
| t_2 | OE, _OS, RD_2, PCC, _PCE |
| t_3 | _ScR |


## `OLD $A` (0xD0)

| Microstep | Control Signals |
| :---: | :---: |
| t_0 | IR_in, RD_2, PCC, _PCE |
| t_1 | RD_2, RD_3 |
| t_2 | OE, RD_2, RD_3 |
| t_3 | _ScR |


## `OLD $B` (0xD1)

| Microstep | Control Signals |
| :---: | :---: |
| t_0 | IR_in, RD_2, PCC, _PCE |
| t_1 | RD_0, RD_1, RD_3 |
| t_2 | OE, RD_0, RD_1, RD_3 |
| t_3 | _ScR |


## `OLC $A` (0xD2)

| Microstep | Control Signals |
| :---: | :---: |
| t_0 | IR_in, RD_2, PCC, _PCE |
| t_1 | _OS, RD_2, RD_3 |
| t_2 | OE, _OS, RD_2, RD_3 |
| t_3 | _ScR |


## `OLC $B` (0xD3)

| Microstep | Control Signals |
| :---: | :---: |
| t_0 | IR_in, RD_2, PCC, _PCE |
| t_1 | _OS, RD_0, RD_1, RD_3 |
| t_2 | OE, _OS, RD_0, RD_1, RD_3 |
| t_3 | _ScR |


## `LSL $A` (0xD4)

| Microstep | Control Signals |
| :---: | :---: |
| t_0 | IR_in, RD_2, PCC, _PCE |
| t_1 | Z1, ZS, Z0, RD_2, RD_3 |
| t_2 | _FW, ZS, Z0, RD_2, RD_3 |
| t_3 | ZS, ZW |
| t_4 | RD_0, RD_1, RD_2, RD_3, WR_1 |
| t_5 | _ScR |


## `LSL $B` (0xD5)

| Microstep | Control Signals |
| :---: | :---: |
| t_0 | IR_in, RD_2, PCC, _PCE |
| t_1 | Z1, ZS, Z0, RD_0, RD_1, RD_3 |
| t_2 | _FW, ZS, Z0, RD_0, RD_1, RD_3 |
| t_3 | ZS, ZW |
| t_4 | _BW, RD_0, RD_1, RD_2, RD_3 |
| t_5 | _ScR |


## `LSL $C` (0xD6)

| Microstep | Control Signals |
| :---: | :---: |
| t_0 | IR_in, RD_2, PCC, _PCE |
| t_1 | Z1, ZS, Z0, RD_0, RD_2, RD_3 |
| t_2 | _FW, ZS, Z0, RD_0, RD_2, RD_3 |
| t_3 | ZS, ZW |
| t_4 | RD_0, RD_1, RD_2, RD_3, WR_0, WR_1 |
| t_5 | _ScR |


## `LSL $D` (0xD7)

| Microstep | Control Signals |
| :---: | :---: |
| t_0 | IR_in, RD_2, PCC, _PCE |
| t_1 | Z1, ZS, Z0, RD_1, RD_2, RD_3 |
| t_2 | _FW, ZS, Z0, RD_1, RD_2, RD_3 |
| t_3 | ZS, ZW |
| t_4 | _DW, RD_0, RD_1, RD_2, RD_3 |
| t_5 | _ScR |


## `LSL [@]` (0xD8)

| Microstep | Control Signals |
| :---: | :---: |
| t_0 | IR_in, RD_2, PCC, _PCE |
| t_1 | BRlW, RD_2, PCC, _PCE |
| t_2 | RD_2, _PCE, BRhW |
| t_3 | Z1, ZS, Z0, RD_2, PCC, _BRE |
| t_4 | _FW, ZS, Z0, RD_2, _BRE |
| t_5 | ZS, ZW |
| t_6 | RD_0, RD_1, RD_2, RD_3, _BRE, _MW |
| t_7 | _ScR |


## `LSL [$CD]` (0xD9)

| Microstep | Control Signals |
| :---: | :---: |
| t_0 | IR_in, RD_2, PCC, _PCE |
| t_1 | BRlW, RD_0, RD_2, RD_3 |
| t_2 | RD_1, RD_2, RD_3, BRhW |
| t_3 | Z1, ZS, Z0, RD_2, _BRE |
| t_4 | _FW, ZS, Z0, RD_2, _BRE |
| t_5 | ZS, ZW |
| t_6 | RD_0, RD_1, RD_2, RD_3, _BRE, _MW |
| t_7 | _ScR |


## `LSR $A` (0xDA)

| Microstep | Control Signals |
| :---: | :---: |
| t_0 | IR_in, RD_2, PCC, _PCE |
| t_1 | Z1, ZS, Z0, RD_2, RD_3 |
| t_2 | _FW, Z1, ZS, RD_2, RD_3 |
| t_3 | ZS, ZW |
| t_4 | RD_0, RD_1, RD_2, RD_3, WR_1 |
| t_5 | _ScR |


## `LSR $B` (0xDB)

| Microstep | Control Signals |
| :---: | :---: |
| t_0 | IR_in, RD_2, PCC, _PCE |
| t_1 | Z1, ZS, Z0, RD_0, RD_1, RD_3 |
| t_2 | _FW, Z1, ZS, RD_0, RD_1, RD_3 |
| t_3 | ZS, ZW |
| t_4 | _BW, RD_0, RD_1, RD_2, RD_3 |
| t_5 | _ScR |


## `LSR $C` (0xDC)

| Microstep | Control Signals |
| :---: | :---: |
| t_0 | IR_in, RD_2, PCC, _PCE |
| t_1 | Z1, ZS, Z0, RD_0, RD_2, RD_3 |
| t_2 | _FW, Z1, ZS, RD_0, RD_2, RD_3 |
| t_3 | ZS, ZW |
| t_4 | RD_0, RD_1, RD_2, RD_3, WR_0, WR_1 |
| t_5 | _ScR |


## `LSR $D` (0xDD)

| Microstep | Control Signals |
| :---: | :---: |
| t_0 | IR_in, RD_2, PCC, _PCE |
| t_1 | Z1, ZS, Z0, RD_1, RD_2, RD_3 |
| t_2 | _FW, Z1, ZS, RD_1, RD_2, RD_3 |
| t_3 | ZS, ZW |
| t_4 | _DW, RD_0, RD_1, RD_2, RD_3 |
| t_5 | _ScR |


## `LSR [@]` (0xDE)

| Microstep | Control Signals |
| :---: | :---: |
| t_0 | IR_in, RD_2, PCC, _PCE |
| t_1 | BRlW, RD_2, PCC, _PCE |
| t_2 | RD_2, _PCE, BRhW |
| t_3 | Z1, ZS, Z0, RD_2, PCC, _BRE |
| t_4 | _FW, Z1, ZS, RD_2, _BRE |
| t_5 | ZS, ZW |
| t_6 | RD_0, RD_1, RD_2, RD_3, _BRE, _MW |
| t_7 | _ScR |


## `LSR [$CD]` (0xDF)

| Microstep | Control Signals |
| :---: | :---: |
| t_0 | IR_in, RD_2, PCC, _PCE |
| t_1 | BRlW, RD_0, RD_2, RD_3 |
| t_2 | RD_1, RD_2, RD_3, BRhW |
| t_3 | Z1, ZS, Z0, RD_2, _BRE |
| t_4 | _FW, Z1, ZS, RD_2, _BRE |
| t_5 | ZS, ZW |
| t_6 | RD_0, RD_1, RD_2, RD_3, _BRE, _MW |
| t_7 | _ScR |


## `PSH $A` (0xE0)

| Microstep | Control Signals |
| :---: | :---: |
| t_0 | IR_in, RD_2, PCC, _PCE |
| t_1 | SPD, RD_2, RD_3, _MW, _SPE |
| t_2 | _SPC, SPD |
| t_3 | _ScR |


## `PUL $A` (0xE1)

| Microstep | Control Signals |
| :---: | :---: |
| t_0 | IR_in, RD_2, PCC, _PCE |
| t_1 | _SPC |
| t_2 | RD_2, WR_1, _SPE |
| t_3 | _ScR |


## `PSH $B` (0xE2)

| Microstep | Control Signals |
| :---: | :---: |
| t_0 | IR_in, RD_2, PCC, _PCE |
| t_1 | SPD, RD_0, RD_1, RD_3, _MW, _SPE |
| t_2 | _SPC, SPD |
| t_3 | _ScR |


## `PUL $B` (0xE3)

| Microstep | Control Signals |
| :---: | :---: |
| t_0 | IR_in, RD_2, PCC, _PCE |
| t_1 | _SPC |
| t_2 | _BW, RD_2, _SPE |
| t_3 | _ScR |


## `PSH $C` (0xE4)

| Microstep | Control Signals |
| :---: | :---: |
| t_0 | IR_in, RD_2, PCC, _PCE |
| t_1 | SPD, RD_0, RD_2, RD_3, _MW, _SPE |
| t_2 | _SPC, SPD |
| t_3 | _ScR |


## `PUL $C` (0xE5)

| Microstep | Control Signals |
| :---: | :---: |
| t_0 | IR_in, RD_2, PCC, _PCE |
| t_1 | _SPC |
| t_2 | RD_2, WR_0, WR_1, _SPE |
| t_3 | _ScR |


## `PSH $D` (0xE6)

| Microstep | Control Signals |
| :---: | :---: |
| t_0 | IR_in, RD_2, PCC, _PCE |
| t_1 | SPD, RD_1, RD_2, RD_3, _MW, _SPE |
| t_2 | _SPC, SPD |
| t_3 | _ScR |


## `PUL $D` (0xE7)

| Microstep | Control Signals |
| :---: | :---: |
| t_0 | IR_in, RD_2, PCC, _PCE |
| t_1 | _SPC |
| t_2 | _DW, RD_2, _SPE |
| t_3 | _ScR |


## `PSF` (0xE8)

| Microstep | Control Signals |
| :---: | :---: |
| t_0 | IR_in, RD_2, PCC, _PCE |
| t_1 | SPD, RD_1, RD_3, _MW, _SPE |
| t_2 | _SPC, SPD |
| t_3 | _ScR |


## `PLF` (0xE9)

| Microstep | Control Signals |
| :---: | :---: |
| t_0 | IR_in, RD_2, PCC, _PCE |
| t_1 | _SPC, ZW |
| t_2 | _FW, Z1, ZS, Z0, RD_2, _SPE |
| t_3 | _ScR |


## `MOV $SP, $CD` (0xEA)

| Microstep | Control Signals |
| :---: | :---: |
| t_0 | IR_in, RD_2, PCC, _PCE |
| t_1 | BRlW, RD_0, RD_2, RD_3 |
| t_2 | RD_1, RD_2, RD_3, BRhW |
| t_3 | SPW, _BRE |
| t_4 | _ScR |


## `MOV $CD, $SP` (0xEB)

| Microstep | Control Signals |
| :---: | :---: |
| t_0 | IR_in, RD_2, PCC, _PCE |
| t_1 | RD_1, RD_2, WR_0, WR_1 |
| t_2 | _DW, RD_0, RD_1, RD_2 |
| t_3 | _ScR |


## `JMP [@]` (0xEC)

| Microstep | Control Signals |
| :---: | :---: |
| t_0 | IR_in, RD_2, PCC, _PCE |
| t_1 | BRlW, RD_2, PCC, _PCE |
| t_2 | RD_2, _PCE, BRhW |
| t_3 | _PCW, _BRE |
| t_4 | _ScR |


## `JSR [@]` (0xED)

| Microstep | Control Signals |
| :---: | :---: |
| t_0 | IR_in, RD_2, PCC, _PCE |
| t_1 | BRlW, RD_2, PCC, _PCE |
| t_2 | RD_2, PCC, _PCE, BRhW |
| t_3 | SPD, _PClE, _MW, _SPE |
| t_4 | _SPC, SPD |
| t_5 | SPD, _PChE, _MW, _SPE |
| t_6 | _SPC, SPD, _PCW, _BRE |
| t_7 | _ScR |


## `JMP [$CD]` (0xEE)

| Microstep | Control Signals |
| :---: | :---: |
| t_0 | IR_in, RD_2, PCC, _PCE |
| t_1 | BRlW, RD_0, RD_2, RD_3 |
| t_2 | RD_1, RD_2, RD_3, BRhW |
| t_3 | _PCW, _BRE |
| t_4 | _ScR |


## `JSR [$CD]` (0xEF)

| Microstep | Control Signals |
| :---: | :---: |
| t_0 | IR_in, RD_2, PCC, _PCE |
| t_1 | BRlW, RD_0, RD_2, RD_3 |
| t_2 | RD_1, RD_2, RD_3, BRhW |
| t_3 | SPD, _PClE, _MW, _SPE |
| t_4 | _SPC, SPD |
| t_5 | SPD, _PChE, _MW, _SPE |
| t_6 | _SPC, SPD, _PCW, _BRE |
| t_7 | _ScR |


## `RTS` (0xF0)

| Microstep | Control Signals |
| :---: | :---: |
| t_0 | IR_in, RD_2, PCC, _PCE |
| t_1 | _SPC |
| t_2 | RD_2, BRhW, _SPE |
| t_3 | _SPC |
| t_4 | BRlW, RD_2, _SPE |
| t_5 | _PCW, _BRE |
| t_6 | _ScR |


## `JZ [@]` (0xF1)

| Microstep | Control Signals |
| :---: | :---: |
| t_0 | IR_in, RD_2, PCC, _PCE |
| t_1 | PCC |
| t_2 | PCC |
| t_3 | _ScR |


## `JO [@]` (0xF2)

| Microstep | Control Signals |
| :---: | :---: |
| t_0 | IR_in, RD_2, PCC, _PCE |
| t_1 | PCC |
| t_2 | PCC |
| t_3 | _ScR |


## `JN [@]` (0xF3)

| Microstep | Control Signals |
| :---: | :---: |
| t_0 | IR_in, RD_2, PCC, _PCE |
| t_1 | PCC |
| t_2 | PCC |
| t_3 | _ScR |


## `JC [@]` (0xF4)

| Microstep | Control Signals |
| :---: | :---: |
| t_0 | IR_in, RD_2, PCC, _PCE |
| t_1 | PCC |
| t_2 | PCC |
| t_3 | _ScR |


## `JNZ [@]` (0xF5)

| Microstep | Control Signals |
| :---: | :---: |
| t_0 | IR_in, RD_2, PCC, _PCE |
| t_1 | BRlW, RD_2, PCC, _PCE |
| t_2 | RD_2, _PCE, BRhW |
| t_3 | _PCW, _BRE |
| t_4 | _ScR |


## `JNO [@]` (0xF6)

| Microstep | Control Signals |
| :---: | :---: |
| t_0 | IR_in, RD_2, PCC, _PCE |
| t_1 | BRlW, RD_2, PCC, _PCE |
| t_2 | RD_2, _PCE, BRhW |
| t_3 | _PCW, _BRE |
| t_4 | _ScR |


## `JP [@]` (0xF7)

| Microstep | Control Signals |
| :---: | :---: |
| t_0 | IR_in, RD_2, PCC, _PCE |
| t_1 | BRlW, RD_2, PCC, _PCE |
| t_2 | RD_2, _PCE, BRhW |
| t_3 | _PCW, _BRE |
| t_4 | _ScR |


## `JNC [@]` (0xF8)

| Microstep | Control Signals |
| :---: | :---: |
| t_0 | IR_in, RD_2, PCC, _PCE |
| t_1 | BRlW, RD_2, PCC, _PCE |
| t_2 | RD_2, _PCE, BRhW |
| t_3 | _PCW, _BRE |
| t_4 | _ScR |


## `JGZ [@]` (0xF9)

| Microstep | Control Signals |
| :---: | :---: |
| t_0 | IR_in, RD_2, PCC, _PCE |
| t_1 | BRlW, RD_2, PCC, _PCE |
| t_2 | RD_2, _PCE, BRhW |
| t_3 | _PCW, _BRE |
| t_4 | _ScR |


## `SII` (0xFA)

| Microstep | Control Signals |
| :---: | :---: |
| t_0 | IR_in, RD_2, PCC, _PCE |
| t_1 | TI |
| t_2 | _ScR |


## `CII` (0xFB)

| Microstep | Control Signals |
| :---: | :---: |
| t_0 | IR_in, RD_2, PCC, _PCE |
| t_1 | _ScR |


## `ITR` (0xFC)

| Microstep | Control Signals |
| :---: | :---: |
| t_0 | IR_in, RD_2, PCC, _PCE |
| t_1 | TI, Z1, Z2, SPD, Z0, RD_1, RD_3, ZW, _MW, _SPE |
| t_2 | ZS, _SPC, SPD, Z0, RD_0, RD_1, RD_2, RD_3, BRhW |
| t_3 | ZS, SPD, _PClE, ZW, _MW, _SPE |
| t_4 | _SPC, SPD, BRlW, RD_0, RD_1, RD_2, RD_3 |
| t_5 | Z1, Z2, SPD, _PChE, Z0, ZW, _MW, _SPE |
| t_6 | Z1, Z2, _SPC, SPD, RD_2, _BRE, ZW |
| t_7 | SPD, RD_0, RD_1, RD_2, RD_3, _MW, _SPE |
| t_8 | Z1, Z2, Z0, ZW |
| t_9 | BRlW, RD_0, RD_1, RD_2, RD_3 |
| t_10 | Z1, Z2, RD_2, _BRE, ZW |
| t_11 | RD_0, RD_1, RD_2, RD_3, BRhW |
| t_12 | BRlW, RD_2, _SPE |
| t_13 | _FW, Z2, ZS, _PCW, _BRE |
| t_14 | _ScR |


## `RTI` (0xFD)

| Microstep | Control Signals |
| :---: | :---: |
| t_0 | IR_in, RD_2, PCC, _PCE |
| t_1 | _SPC |
| t_2 | RD_2, BRhW, _SPE |
| t_3 | _SPC |
| t_4 | BRlW, RD_2, _SPE |
| t_5 | _SPC, _PCW, _BRE |
| t_6 | TI, _FW, Z1, ZS, Z0, RD_2, _SPE |
| t_7 | _ScR |


## `NOP` (0xFE)

| Microstep | Control Signals |
| :---: | :---: |
| t_0 | IR_in, RD_2, PCC, _PCE |
| t_1 | _ScR |


## `HLT` (0xFF)

| Microstep | Control Signals |
| :---: | :---: |
| t_0 | IR_in, RD_2, PCC, _PCE |
| t_1 | HLT |
| t_2 | _ScR |