"""
NMEA 0183 XOR checksum calculation and verification.

The checksum is computed as the XOR of all characters between "$" and "*",
and emitted as two uppercase hexadecimal digits.
"""

from __future__ import annotations


def compute_checksum(sentence: str) -> str:
    """
    Compute the XOR checksum of an NMEA 0183 sentence body.

    The "$" prefix and "*XX" suffix are stripped automatically if present.
    """
    if sentence.startswith("$"):
        sentence = sentence[1:]

    asterisk = sentence.find("*")
    if asterisk != -1:
        sentence = sentence[:asterisk]

    checksum = 0
    for ch in sentence:
        checksum ^= ord(ch)

    return f"{checksum:02X}"


def verify_checksum(sentence: str) -> bool:
    """Verify the checksum of a complete NMEA sentence."""
    sentence = sentence.rstrip("\r\n")

    asterisk = sentence.find("*")
    if asterisk == -1 or len(sentence) < asterisk + 3:
        return False

    provided = sentence[asterisk + 1 : asterisk + 3].upper()
    if not all(c in "0123456789ABCDEF" for c in provided):
        return False

    return compute_checksum(sentence[:asterisk]) == provided


def append_checksum(payload: str) -> str:
    """Wrap a bare payload into a complete NMEA sentence terminated with CR/LF."""
    return f"${payload}*{compute_checksum(payload)}\r\n"


if __name__ == "__main__":
    cases = [
        ("$GPGGA,123519,4807.038,N,01131.000,E,1,08,0.9,545.4,M,46.9,M,,*47", True),
        ("$GPRMC,123519,A,4807.038,N,01131.000,E,022.4,084.4,230394,003.1,W*6A", True),
        ("$GNGGA,072446.00,3114.562,N,12128.050,E,4,21,0.6,15.2,M,8.9,M,1.0,0031*50", True),
        ("$GPGGA,corrupt,stream*FF", False),
    ]
    for sentence, expected in cases:
        result = verify_checksum(sentence)
        status = "PASS" if result == expected else "FAIL"
        print(f"[{status}] expected={expected} got={result} :: {sentence[:72]}...")
