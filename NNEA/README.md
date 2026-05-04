# NMEA 0183 Toolkit

Python helpers for parsing common NMEA 0183 GNSS sentences, validating checksums, converting coordinates, and reassembling paginated GSV satellite-view messages.

This module is the first practical code companion to the Kalmix GNSS Handbook article:

[Mastering NMEA 0183: Why Your Device Needs to Read Between the Commas](https://www.kalmixtech.com/blogs/blog/mastering-nmea-0183-guide)

---

## What is included

| File | Purpose |
|---|---|
| `Parser/checksum.py` | Compute, verify, and append NMEA XOR checksums |
| `Parser/coordinates.py` | Convert DDMM.MMMM coordinates, speeds, and height fields |
| `Parser/nmea_parser.py` | Parse GGA, RMC, VTG, GSA, and GSV sentences |
| `Examples/multi_constellation.py` | Demonstrate why hard-coding `$GPGGA` is wrong |
| `Examples/gsv_reassembly.py` | Reassemble paginated GSV messages into full satellite lists |
| `Examples/read_serial.py` | Read and parse a live serial stream |
| `Examples/rtk_fix_monitor.py` | Monitor RTK Fix status transitions from GGA sentences |

---

## Quick Start

```python
from NMEA.parser import parse

line = "$GNGGA,072446.00,3114.562,N,12128.050,E,4,21,0.6,15.2,M,8.9,M,1.0,0031*50"
result = parse(line)

if result["valid"]:
    data = result["data"]
    print(data["latitude"], data["longitude"])
    print(data["fix_quality_label"])
```

Expected output:

```text
31.2427 121.4675
RTK Fixed
```

---

## Run examples

From the repository root:

```bash
python NMEA/Examples/multi_constellation.py
python NMEA/Examples/gsv_reassembly.py
python -m NMEA.parser.checksum
python -m NMEA.parser.coordinates
python -m NMEA.parser.nmea_parser
```

For live serial input:

```bash
python NMEA/Examples/read_serial.py /dev/ttyUSB0 115200
```

---

## Supported sentence types

| Sentence | Description |
|---|---|
| `GGA` | Fix data, coordinates, RTK status, satellite count, altitude |
| `RMC` | Recommended minimum navigation data |
| `VTG` | Course and ground speed |
| `GSA` | DOP values and active satellites |
| `GSV` | Satellites in view, split across multiple pages |

---

## Key rules

### 1. Do not hard-code `$GPGGA`

Modern receivers often emit `$GNGGA`, `$GBGGA`, or other talker IDs. Match on the 3-character sentence ID (`GGA`), not the 2-character talker ID (`GP`, `GN`, `GB`, etc.).

### 2. Always verify the checksum

Treat checksum mismatch as a dropped packet. Do not attempt to repair corrupted NMEA data.

### 3. Convert coordinates before using map APIs

NMEA coordinates use DDMM.MMMM / DDDMM.MMMM format, not decimal degrees.

```text
Raw NMEA: 4807.038
Correct:  48 + 7.038 / 60 = 48.1173°
```

---

## Related resources

- [Kalmix GNSS Handbook](https://www.kalmixtech.com/blogs/blog)
- [AN-001: NMEA 0183 Protocol Structure & Sentence Dictionary](https://www.kalmixtech.com/blogs/blog/an-001-kalmix-nmea-0183-v4-protocol-sentence-dictionary)
- [Kalmix-Hardware](https://github.com/KalmixTech/Kalmix-Hardware)
