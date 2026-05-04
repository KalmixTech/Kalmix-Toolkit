import pytest

from NMEA.parser import ddmm_to_decimal, decimal_to_ddmm, ellipsoidal_height, knots_to_kmh


def test_ddmm_to_decimal_latitude():
    assert ddmm_to_decimal("4807.038", "N") == pytest.approx(48.1173)


def test_ddmm_to_decimal_longitude():
    assert ddmm_to_decimal("12128.050", "E") == pytest.approx(121.4675)


def test_decimal_to_ddmm_roundtrip():
    value = 31.2427
    ddmm, hemi = decimal_to_ddmm(value, is_latitude=True)
    assert ddmm == "3114.5620"
    assert hemi == "N"
    assert ddmm_to_decimal(ddmm, hemi) == pytest.approx(value)


def test_units_and_height():
    assert knots_to_kmh(10.0) == pytest.approx(18.52)
    assert ellipsoidal_height(15.2, 8.9) == pytest.approx(24.1)
