"""
NMEA 0183 sentence parser for common GNSS integration workflows.

Supported sentence types:
    GGA - Global Positioning System Fix Data
    RMC - Recommended Minimum Specific GNSS Data
    VTG - Track Made Good and Ground Speed
    GSA - GNSS DOP and Active Satellites
    GSV - GNSS Satellites in View

Design principle: match on the 3-character sentence ID, not the 2-character
talker ID. A parser that hard-codes "$GPGGA" will fail on modern receivers
that emit "$GNGGA", "$GBGGA", or other multi-constellation talkers.
"""

from __future__ import annotations

from typing import Any, Dict, List, Optional, Tuple

from .checksum import verify_checksum
from .coordinates import ddmm_to_decimal, knots_to_kmh


FIX_QUALITY = {
    0: "Invalid",
    1: "GPS fix (SPS)",
    2: "DGPS fix",
    3: "PPS fix",
    4: "RTK Fixed",
    5: "RTK Float",
    6: "Estimated (DR)",
    7: "Manual input",
    8: "Simulation",
}

TALKER_IDS = {
    "GP": "GPS",
    "GL": "GLONASS",
    "GA": "Galileo",
    "GB": "BeiDou",
    "BD": "BeiDou (legacy manufacturer)",
    "GQ": "QZSS",
    "GI": "NavIC / IRNSS",
    "GN": "Combined multi-constellation",
}

RMC_MODE = {
    "A": "Autonomous",
    "D": "Differential",
    "E": "Estimated (DR)",
    "F": "Float RTK",
    "M": "Manual",
    "N": "Data not valid",
    "P": "Precise",
    "R": "Fixed RTK",
    "S": "Simulator",
}

GSA_FIX_TYPE = {
    1: "No fix",
    2: "2D fix",
    3: "3D fix",
}


def _to_float(value: str) -> Optional[float]:
    if value == "":
        return None
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def _to_int(value: str) -> Optional[int]:
    if value == "":
        return None
    try:
        return int(value)
    except (TypeError, ValueError):
        return None


def _strip_cs(value: str) -> str:
    """Drop any trailing '*XX' checksum suffix from a field."""
    idx = value.find("*")
    return value if idx < 0 else value[:idx]


def _parse_gga(fields: List[str]) -> Dict[str, Any]:
    quality_val = _to_int(fields[6]) if len(fields) > 6 else None

    return {
        "utc_time": fields[1] if len(fields) > 1 else None,
        "latitude": ddmm_to_decimal(fields[2], fields[3]) if len(fields) > 3 else None,
        "longitude": ddmm_to_decimal(fields[4], fields[5]) if len(fields) > 5 else None,
        "fix_quality": quality_val,
        "fix_quality_label": FIX_QUALITY.get(quality_val, "Unknown"),
        "satellites_used": _to_int(fields[7]) if len(fields) > 7 else None,
        "hdop": _to_float(fields[8]) if len(fields) > 8 else None,
        "msl_altitude_m": _to_float(fields[9]) if len(fields) > 9 else None,
        "geoid_separation_m": _to_float(fields[11]) if len(fields) > 11 else None,
        "dgps_age_sec": _to_float(fields[13]) if len(fields) > 13 else None,
        "station_id": _strip_cs(fields[14]) if len(fields) > 14 else None,
    }


def _parse_rmc(fields: List[str]) -> Dict[str, Any]:
    speed_knots = _to_float(fields[7]) if len(fields) > 7 else None
    mode = _strip_cs(fields[12]) if len(fields) > 12 else None

    return {
        "utc_time": fields[1] if len(fields) > 1 else None,
        "status": fields[2] if len(fields) > 2 else None,
        "is_valid": fields[2] == "A" if len(fields) > 2 else False,
        "latitude": ddmm_to_decimal(fields[3], fields[4]) if len(fields) > 4 else None,
        "longitude": ddmm_to_decimal(fields[5], fields[6]) if len(fields) > 6 else None,
        "speed_knots": speed_knots,
        "speed_kmh": knots_to_kmh(speed_knots) if speed_knots is not None else None,
        "course_deg": _to_float(fields[8]) if len(fields) > 8 else None,
        "date": fields[9] if len(fields) > 9 else None,
        "mode": mode if mode else None,
        "mode_label": RMC_MODE.get(mode, "Unknown") if mode else None,
    }


def _parse_vtg(fields: List[str]) -> Dict[str, Any]:
    return {
        "course_true_deg": _to_float(fields[1]) if len(fields) > 1 else None,
        "course_magnetic_deg": _to_float(fields[3]) if len(fields) > 3 else None,
        "speed_knots": _to_float(fields[5]) if len(fields) > 5 else None,
        "speed_kmh": _to_float(fields[7]) if len(fields) > 7 else None,
        "mode": _strip_cs(fields[9]) if len(fields) > 9 else None,
    }


def _parse_gsa(fields: List[str]) -> Dict[str, Any]:
    prns = [_to_int(f) for f in fields[3:15]]
    prns = [p for p in prns if p is not None]
    fix_type = _to_int(fields[2]) if len(fields) > 2 else None

    return {
        "mode": fields[1] if len(fields) > 1 else None,
        "fix_type": fix_type,
        "fix_type_label": GSA_FIX_TYPE.get(fix_type, "Unknown"),
        "satellite_prns": prns,
        "pdop": _to_float(fields[15]) if len(fields) > 15 else None,
        "hdop": _to_float(fields[16]) if len(fields) > 16 else None,
        "vdop": _to_float(_strip_cs(fields[17])) if len(fields) > 17 else None,
        "system_id": _to_int(_strip_cs(fields[18])) if len(fields) > 18 else None,
    }


def _parse_gsv(fields: List[str]) -> Dict[str, Any]:
    total_messages = _to_int(fields[1]) if len(fields) > 1 else None
    message_number = _to_int(fields[2]) if len(fields) > 2 else None
    total_sats = _to_int(fields[3]) if len(fields) > 3 else None

    satellites = []
    i = 4

    while i + 3 < len(fields):
        prn_str = fields[i]
        if not prn_str:
            break

        satellites.append(
            {
                "prn": _to_int(prn_str),
                "elevation_deg": _to_int(fields[i + 1]),
                "azimuth_deg": _to_int(fields[i + 2]),
                "snr_dbhz": _to_int(_strip_cs(fields[i + 3])),
            }
        )
        i += 4

    signal_id = None
    if i < len(fields):
        signal_id = _to_int(_strip_cs(fields[i]))

    return {
        "total_messages": total_messages,
        "message_number": message_number,
        "total_satellites_in_view": total_sats,
        "satellites": satellites,
        "signal_id": signal_id,
    }


_PARSERS = {
    "GGA": _parse_gga,
    "RMC": _parse_rmc,
    "VTG": _parse_vtg,
    "GSA": _parse_gsa,
    "GSV": _parse_gsv,
}


def parse(sentence: str, validate_checksum: bool = True) -> Dict[str, Any]:
    """Parse a single NMEA 0183 sentence."""
    result: Dict[str, Any] = {
        "valid": False,
        "sentence_type": None,
        "talker_id": None,
        "talker_label": None,
        "raw": sentence.strip(),
        "data": {},
        "error": None,
    }

    sentence = sentence.strip()
    if not sentence.startswith("$"):
        result["error"] = "missing $ prefix"
        return result

    if validate_checksum and not verify_checksum(sentence):
        result["error"] = "checksum mismatch"
        return result

    try:
        fields = sentence[1:].split(",")
        header = fields[0]
        if len(header) < 5:
            result["error"] = "malformed header"
            return result

        talker_id = header[:2]
        sentence_id = header[2:5]

        result["talker_id"] = talker_id
        result["talker_label"] = TALKER_IDS.get(talker_id, "Unknown")
        result["sentence_type"] = sentence_id

        parser_func = _PARSERS.get(sentence_id)
        if parser_func is None:
            result["error"] = f"unsupported sentence type: {sentence_id}"
            return result

        data = parser_func(fields)
        if not data:
            result["error"] = "field extraction failed"
            return result

        result["data"] = data
        result["valid"] = True
        return result
    except Exception as exc:
        result["error"] = f"parse error: {exc}"
        return result


class GSVAssembler:
    """
    Reassemble paginated GSV messages into a complete satellite list.

    Buffers are grouped by (talker_id, total_messages, signal_id) so that
    multi-signal GSV pages, such as L1 and L5, do not get mixed together.
    """

    def __init__(self) -> None:
        self._buffers: Dict[Tuple[str, int, Optional[int]], Dict[int, list]] = {}

    def feed(self, parsed_gsv: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Submit one parsed GSV sentence."""
        if not parsed_gsv.get("valid") or parsed_gsv.get("sentence_type") != "GSV":
            return None

        data = parsed_gsv["data"]
        talker = parsed_gsv["talker_id"]
        total = data.get("total_messages")
        msg_num = data.get("message_number")
        signal_id = data.get("signal_id")

        if total is None or msg_num is None:
            return None

        key = (talker, total, signal_id)
        pages = self._buffers.setdefault(key, {})
        pages[msg_num] = data.get("satellites", [])

        if len(pages) == total:
            satellites = []
            for n in sorted(pages.keys()):
                satellites.extend(pages[n])

            total_in_view = data.get("total_satellites_in_view")
            del self._buffers[key]

            return {
                "talker": talker,
                "talker_label": TALKER_IDS.get(talker, "Unknown"),
                "total_messages": total,
                "total_satellites_in_view": total_in_view,
                "signal_id": signal_id,
                "satellites": satellites,
            }

        return None


if __name__ == "__main__":
    samples = [
        "$GPGGA,123519,4807.038,N,01131.000,E,1,08,0.9,545.4,M,46.9,M,,*47",
        "$GNGGA,072446.00,3114.562,N,12128.050,E,4,21,0.6,15.2,M,8.9,M,1.0,0031*50",
    ]

    for line in samples:
        parsed = parse(line)
        print(
            f"[{parsed['sentence_type']}] valid={parsed['valid']} "
            f"talker={parsed['talker_id']} error={parsed['error']}"
        )
        if parsed["valid"]:
            print(f"    data keys: {list(parsed['data'].keys())}")
