"""Parser subpackage for the Kalmix NMEA toolkit."""

from .checksum import compute_checksum, verify_checksum, append_checksum
from .coordinates import (
    ddmm_to_decimal,
    decimal_to_ddmm,
    dms_to_decimal,
    knots_to_kmh,
    knots_to_mph,
    ellipsoidal_height,
)
from .nmea_parser import (
    parse,
    GSVAssembler,
    FIX_QUALITY,
    TALKER_IDS,
    RMC_MODE,
    GSA_FIX_TYPE,
)

__all__ = [
    "compute_checksum",
    "verify_checksum",
    "append_checksum",
    "ddmm_to_decimal",
    "decimal_to_ddmm",
    "dms_to_decimal",
    "knots_to_kmh",
    "knots_to_mph",
    "ellipsoidal_height",
    "parse",
    "GSVAssembler",
    "FIX_QUALITY",
    "TALKER_IDS",
    "RMC_MODE",
    "GSA_FIX_TYPE",
]
