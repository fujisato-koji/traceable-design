# Design

Facts live in `record/`, and this page cites them by id.

## Deflection {#deflection}

The board is modelled as simply supported on two brackets, with the load at mid-span.
The deflection is the load times the span cubed, divided by 48 times the modulus times the second moment of area.
The second moment of area follows from board.width_mm and board.thickness_mm.
The modulus board.modulus_mpa is an assumption, tracked as Q-001, and not a sourced value.
The result shelf.deflection_mm is therefore only as good as that assumption.
Check K-001 records the hand calculation against shelf.deflection_limit_mm.

## Values

<!-- tdr:table kind=value fields=key,v,unit,status -->
| key | v | unit | status |
|---|---|---|---|
| shelf.load_n | 200 | N | decided |
| shelf.span_mm | 600 | mm | decided |
| shelf.deflection_limit_mm | 3 | mm | decided |
| board.width_mm | 200 | mm | decided |
| board.thickness_mm | 18 | mm | decided |
| board.modulus_mpa | 9000 | MPa | assumed |
| board.property_table | Wood Handbook chapter on mechanical properties |  | sourced |
| shelf.deflection_mm | 1.03 | mm | calculated |
| screw.count | 4 |  | decided |
<!-- tdr:end -->
