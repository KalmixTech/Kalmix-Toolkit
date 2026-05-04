"""
Read NMEA sentences from a serial port and parse them live.

Usage:
    python NMEA/Examples/read_serial.py <port> [baudrate]

Examples:
    python NMEA/Examples/read_serial.py /dev/ttyUSB0 115200
    python NMEA/Examples/read_serial.py COM3 115200

Requires:
    pip install pyserial
"""

from __future__ import annotations

import sys
from pathlib import Path

_REPO_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(_REPO_ROOT))

try:
    import serial
except ImportError:
    print("This example requires pyserial. Install with: pip install pyserial")
    sys.exit(1)

from NMEA.Parser import parse  # noqa: E402


def main() -> None:
    if len(sys.argv) < 2:
        print(f"Usage: python {sys.argv[0]} <port> [baudrate]")
        print(f"Example: python {sys.argv[0]} /dev/ttyUSB0 115200")
        sys.exit(1)

    port = sys.argv[1]
    baudrate = int(sys.argv[2]) if len(sys.argv) > 2 else 115200

    print(f"Opening {port} @ {baudrate} baud — Ctrl+C to stop\n")

    try:
        ser = serial.Serial(port, baudrate=baudrate, timeout=1.0)
    except serial.SerialException as exc:
        print(f"Failed to open {port}: {exc}")
        sys.exit(1)

    with ser:
        while True:
            try:
                raw = ser.readline().decode("ascii", errors="ignore").strip()
            except KeyboardInterrupt:
                print("\nStopped.")
                return

            if not raw or not raw.startswith("$"):
                continue

            result = parse(raw)
            if not result["valid"]:
                continue

            sentence_type = result["sentence_type"]
            data = result["data"]

            if sentence_type == "GGA":
                lat = data.get("latitude")
                lon = data.get("longitude")
                if lat is not None and lon is not None:
                    print(
                        f"GGA  {lat:+.7f}, {lon:+.7f}  "
                        f"fix={data.get('fix_quality_label')}  "
                        f"sats={data.get('satellites_used')}  "
                        f"HDOP={data.get('hdop')}"
                    )
            elif sentence_type == "RMC":
                if data.get("is_valid") and data.get("speed_kmh") is not None:
                    print(
                        f"RMC  {data['speed_kmh']:.1f} km/h  "
                        f"course={data.get('course_deg')}°  "
                        f"mode={data.get('mode_label')}"
                    )
            elif sentence_type == "GSA":
                print(
                    f"GSA  {data.get('fix_type_label')}  "
                    f"PDOP={data.get('pdop')}  "
                    f"HDOP={data.get('hdop')}  "
                    f"VDOP={data.get('vdop')}"
                )


if __name__ == "__main__":
    main()
