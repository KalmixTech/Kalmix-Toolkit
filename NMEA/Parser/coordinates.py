"""NMEA coordinate and unit conversion helpers."""

from __future__ import annotations

from typing import Optional, Tuple


def ddmm_to_decimal(ddmm: str, hemisphere: str) -> Optional[float]:
    """Convert NMEA DDMM.MMMM / DDDMM.MMMM format to decimal degrees."""
    if not ddmm or not hemisphere:
        return None

    hemisphere = hemisphere.upper()

    try:
        dot = ddmm.find(".")
        if dot < 0:
            dot = len(ddmm)
        if dot < 2:
            return None

        degrees = int(ddmm[: dot - 2])
        minutes = float(ddmm[dot - 2 :])
        decimal = degrees + minutes / 60.0

        if hemisphere in ("S", "W"):
            return -decimal
        if hemisphere in ("N", "E"):
            return decimal
        return None
    except (ValueError, IndexError):
        return None


def decimal_to_ddmm(decimal: float, is_latitude: bool = True) -> Tuple[str, str]:
    """Convert decimal degrees back to NMEA DDMM.MMMM / DDDMM.MMMM format."""
    if is_latitude:
        hemisphere = "N" if decimal >= 0 else "S"
    else:
        hemisphere = "E" if decimal >= 0 else "W"

    decimal = abs(decimal)
    degrees = int(decimal)
    minutes = (decimal - degrees) * 60.0
    width = 2 if is_latitude else 3

    return f"{degrees:0{width}d}{minutes:07.4f}", hemisphere


def dms_to_decimal(degrees: int, minutes: int, seconds: float, hemisphere: str = "N") -> float:
    """Convert degrees-minutes-seconds to decimal degrees."""
    decimal = degrees + minutes / 60.0 + seconds / 3600.0
    if hemisphere.upper() in ("S", "W"):
        decimal = -decimal
    return decimal


def knots_to_kmh(knots: float) -> float:
    """Convert knots to km/h. 1 knot = 1.852 km/h."""
    return knots * 1.852


def knots_to_mph(knots: float) -> float:
    """Convert knots to statute miles per hour."""
    return knots * 1.15077945


def ellipsoidal_height(msl_altitude: float, geoid_separation: float) -> float:
    """Recover ellipsoidal height from GGA altitude fields: h = H + N."""
    return msl_altitude + geoid_separation


if __name__ == "__main__":
    print(f"4807.038 N       -> {ddmm_to_decimal('4807.038', 'N'):.6f}°")
    print(f"12128.050 E      -> {ddmm_to_decimal('12128.050', 'E'):.6f}°")
    print(f"10.5 knots       -> {knots_to_kmh(10.5):.2f} km/h")
    print(f"MSL 15.2 + N 8.9 -> h = {ellipsoidal_height(15.2, 8.9):.1f} m")
