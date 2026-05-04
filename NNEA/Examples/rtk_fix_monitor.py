"""
Monitor RTK Fix status transitions from GGA sentences.

Input:
    - A recorded NMEA log file, or
    - A live stream on stdin.

Usage:
    python NMEA/examples/rtk_fix_monitor.py path/to/session.log
    cat session.log | python NMEA/examples/rtk_fix_monitor.py
"""

from __future__ import annotations

import sys
import time
from pathlib import Path

_REPO_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(_REPO_ROOT))

from NMEA.parser import parse  # noqa: E402


def _display(value, missing: str = "?"):
    return value if value is not None else missing


def monitor(lines) -> None:
    last_quality = None
    start = time.monotonic()

    for raw in lines:
        raw = raw.strip()
        if not raw.startswith("$"):
            continue

        result = parse(raw)
        if not result["valid"] or result["sentence_type"] != "GGA":
            continue

        data = result["data"]
        quality = data.get("fix_quality")
        label = data.get("fix_quality_label")
        sats = _display(data.get("satellites_used"))
        hdop = _display(data.get("hdop"))
        age = _display(data.get("dgps_age_sec"), "-")
        elapsed = time.monotonic() - start

        print(
            f"[{elapsed:7.1f}s] quality={quality} ({label:<14s}) "
            f"sats={sats}  HDOP={hdop}  age={age}s"
        )

        if quality != last_quality:
            if last_quality is not None:
                print(
                    f"           >>> TRANSITION {last_quality} -> {quality} "
                    f"({label}) after {elapsed:.1f}s"
                )
            last_quality = quality

            if quality == 4:
                print(f"           *** RTK FIXED achieved at t={elapsed:.1f}s ***")


def main() -> None:
    if len(sys.argv) > 1:
        path = sys.argv[1]
        print(f"Reading NMEA log from: {path}\n")
        with open(path, "r", encoding="ascii", errors="ignore") as fh:
            monitor(fh)
    else:
        print("Reading NMEA from stdin — Ctrl+C to stop\n")
        try:
            monitor(sys.stdin)
        except KeyboardInterrupt:
            print("\nStopped.")


if __name__ == "__main__":
    main()
