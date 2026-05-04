"""
Kalmix NMEA Toolkit — parse and work with NMEA 0183 GNSS sentences.

Companion code to the Kalmix GNSS Handbook:
https://www.kalmixtech.com/blogs/blog/mastering-nmea-0183-guide
"""

from .Parser import (
    parse,
    GSVAssembler,
    verify_checksum,
    compute_checksum,
    append_checksum,
    ddmm_to_decimal,
    decimal_to_ddmm,
    dms_to_decimal,
    ellipsoidal_height,
    knots_to_kmh,
    knots_to_mph,
    FIX_QUALITY,
    TALKER_IDS,
    RMC_MODE,
    GSA_FIX_TYPE,
)

__version__ = "0.1.0"

__all__ = [
    "parse",
    "GSVAssembler",
    "verify_checksum",
    "compute_checksum",
    "append_checksum",
    "ddmm_to_decimal",
    "decimal_to_ddmm",
    "dms_to_decimal",
    "ellipsoidal_height",
    "knots_to_kmh",
    "knots_to_mph",
    "FIX_QUALITY",
    "TALKER_IDS",
    "RMC_MODE",
    "GSA_FIX_TYPE",
]
