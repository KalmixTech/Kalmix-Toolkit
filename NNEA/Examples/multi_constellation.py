"""
Multi-constellation Talker ID compatibility demo.

Hard-coding "$GPGGA" breaks when a receiver emits "$GNGGA", "$GBGGA",
or other multi-constellation talker IDs. The correct approach is to match
on the 3-character sentence ID, not the 2-character talker ID.

Run:
    python NMEA/examples/multi_constellation.py
"""

from __future__ import annotations

import sys
from pathlib import Path

_REPO_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(_REPO_ROOT))

from NMEA.parser import TALKER_IDS, parse  # noqa: E402


SAMPLE_STREAM = [
    "$GPGGA,123519,4807.038,N,01131.000,E,1,08,0.9,545.4,M,46.9,M,,*47",
    "$GNGGA,072446.00,3114.562,N,12128.050,E,4,21,0.6,15.2,M,8.9,M,1.0,0031*50",
    "$GLGSV,2,1,08,72,58,310,45,74,55,085,44,75,47,215,42,79,27,300,38*60",
    "$GAGSV,2,1,06,07,60,180,48,12,42,220,42,25,30,090,41,30,15,345,36*76",
    "$GBGSV,3,1,10,21,70,045,48,22,65,120,46,23,55,200,45,24,45,280,44*60",
    "$GQGSV,1,1,01,02,55,150,45*44",
]


def buggy_parser(line: str) -> bool:
    """Classic bug: hard-code the GP talker ID."""
    return line.startswith("$GPGGA")


def correct_parser(line: str) -> str | None:
    """Correct pattern: parse by sentence ID."""
    result = parse(line, validate_checksum=False)
    return result.get("sentence_type")


def main() -> None:
    print("=" * 78)
    print("Demo: why hard-coding '$GPGGA' breaks multi-constellation receivers")
    print("=" * 78)
    print(f"\n{'Sentence':55} {'buggy?':<8} {'correct parser'}")
    print("-" * 78)

    buggy_hits = 0
    correct_hits = 0

    for line in SAMPLE_STREAM:
        buggy_hit = buggy_parser(line)
        sentence_id = correct_parser(line)

        if buggy_hit:
            buggy_hits += 1
        if sentence_id:
            correct_hits += 1

        talker_name = TALKER_IDS.get(line[1:3], "?")
        buggy_label = "MATCH" if buggy_hit else "—"
        sentence_label = f"{sentence_id} ({talker_name})" if sentence_id else "—"

        print(f"{line[:55]:55} {buggy_label:<8} {sentence_label}")

    print()
    print(f"Buggy parser matched:   {buggy_hits} / {len(SAMPLE_STREAM)} sentences")
    print(f"Correct parser matched: {correct_hits} / {len(SAMPLE_STREAM)} sentences")


if __name__ == "__main__":
    main()
