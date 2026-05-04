from NMEA.Parser import append_checksum, compute_checksum, verify_checksum


def test_compute_checksum_canonical_gga():
    payload = "GPGGA,123519,4807.038,N,01131.000,E,1,08,0.9,545.4,M,46.9,M,,"
    assert compute_checksum(payload) == "47"


def test_verify_checksum_valid():
    sentence = "$GNGGA,072446.00,3114.562,N,12128.050,E,4,21,0.6,15.2,M,8.9,M,1.0,0031*50"
    assert verify_checksum(sentence)


def test_verify_checksum_invalid():
    sentence = "$GNGGA,072446.00,3114.562,N,12128.050,E,4,21,0.6,15.2,M,8.9,M,1.0,0031*4B"
    assert not verify_checksum(sentence)


def test_append_checksum_roundtrip():
    payload = "GNGGA,072446.00,3114.562,N,12128.050,E,4,21,0.6,15.2,M,8.9,M,1.0,0031"
    sentence = append_checksum(payload)
    assert sentence == "$GNGGA,072446.00,3114.562,N,12128.050,E,4,21,0.6,15.2,M,8.9,M,1.0,0031*50\r\n"
    assert verify_checksum(sentence)
