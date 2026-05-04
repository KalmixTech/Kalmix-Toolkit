from NMEA.parser import parse


def test_parse_valid_gga():
    sentence = "$GNGGA,072446.00,3114.562,N,12128.050,E,4,21,0.6,15.2,M,8.9,M,1.0,0031*50"
    result = parse(sentence)

    assert result["valid"]
    assert result["sentence_type"] == "GGA"
    assert result["talker_id"] == "GN"
    assert result["data"]["fix_quality"] == 4
    assert result["data"]["fix_quality_label"] == "RTK Fixed"
    assert result["data"]["satellites_used"] == 21


def test_parse_bad_checksum():
    sentence = "$GNGGA,072446.00,3114.562,N,12128.050,E,4,21,0.6,15.2,M,8.9,M,1.0,0031*4B"
    result = parse(sentence)

    assert not result["valid"]
    assert result["error"] == "checksum mismatch"


def test_parse_without_checksum_validation():
    sentence = "$GNGGA,072446.00,3114.562,N,12128.050,E,4,21,0.6,15.2,M,8.9,M,1.0,0031*4B"
    result = parse(sentence, validate_checksum=False)

    assert result["valid"]
    assert result["sentence_type"] == "GGA"
