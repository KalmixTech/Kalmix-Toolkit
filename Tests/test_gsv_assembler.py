from NMEA.Parser import GSVAssembler, parse


def test_gsv_assembler_basic_cycle():
    assembler = GSVAssembler()

    lines = [
        "$GPGSV,2,1,05,01,45,120,42,02,30,060,38,03,60,180,45,04,10,300,20,1*00",
        "$GPGSV,2,2,05,05,22,015,35,1*00",
    ]

    complete = None
    for line in lines:
        parsed = parse(line, validate_checksum=False)
        complete = assembler.feed(parsed)

    assert complete is not None
    assert complete["talker"] == "GP"
    assert complete["signal_id"] == 1
    assert len(complete["satellites"]) == 5


def test_gsv_assembler_keeps_signal_ids_separate():
    assembler = GSVAssembler()

    l1_page = "$GPGSV,1,1,01,01,45,120,42,1*00"
    l5_page = "$GPGSV,1,1,01,01,45,120,42,5*00"

    l1 = assembler.feed(parse(l1_page, validate_checksum=False))
    l5 = assembler.feed(parse(l5_page, validate_checksum=False))

    assert l1 is not None
    assert l5 is not None
    assert l1["signal_id"] == 1
    assert l5["signal_id"] == 5
