"""
Reassemble paginated GSV messages into complete satellite lists.

A single GSV line carries at most four satellites. Modern receivers output
multiple GSV pages per constellation and signal band.

Run:
    python NMEA/Examples/gsv_reassembly.py
"""

from __future__ import annotations

import sys
from pathlib import Path

_REPO_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(_REPO_ROOT))

from NMEA.Parser import GSVAssembler, parse  # noqa: E402


SAMPLE_CYCLE = [
    "$GPGSV,3,1,10,01,45,120,42,02,30,060,38,03,60,180,45,04,10,300,20,1*6B",
    "$GPGSV,3,2,10,05,22,015,35,06,18,335,31,07,55,270,43,08,40,215,39,1*6E",
    "$GPGSV,3,3,10,09,12,095,28,10,08,150,22,1*65",
    "$GAGSV,2,1,06,07,60,180,48,12,42,220,42,25,30,090,41,30,15,345,36,7*76",
    "$GAGSV,2,2,06,36,50,050,44,27,22,275,33,7*77",
    "$GBGSV,3,1,10,21,70,045,48,22,65,120,46,23,55,200,45,24,45,280,44,1*60",
    "$GBGSV,3,2,10,25,40,010,43,26,30,320,40,27,25,170,36,28,18,255,30,1*6F",
    "$GBGSV,3,3,10,29,15,095,28,30,12,200,22,1*65",
]


def main() -> None:
    assembler = GSVAssembler()

    print("Feeding GSV pages to the assembler...\n")
    for line in SAMPLE_CYCLE:
        result = parse(line, validate_checksum=False)
        if result.get("sentence_type") != "GSV":
            continue

        talker = result["talker_id"]
        page = result["data"]["message_number"]
        total = result["data"]["total_messages"]
        signal_id = result["data"].get("signal_id")

        print(f"  feed: {talker}GSV  page {page}/{total}  signal_id={signal_id}")

        complete = assembler.feed(result)
        if complete:
            satellites = complete["satellites"]
            snrs = [s["snr_dbhz"] for s in satellites if s.get("snr_dbhz") is not None]
            avg_snr = sum(snrs) / len(snrs) if snrs else 0

            print(
                f"    ==> {complete['talker']} complete: "
                f"{len(satellites)} satellites  "
                f"signal_id={complete.get('signal_id')}  "
                f"avg SNR={avg_snr:.1f} dB-Hz\n"
            )


if __name__ == "__main__":
    main()
