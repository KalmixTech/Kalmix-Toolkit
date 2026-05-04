# Kalmix Toolkit

Python tools and developer cheatsheets for GNSS/RTK integration.

This repository is the developer companion to the [Kalmix GNSS Handbook](https://www.kalmixtech.com/blogs/blog). It starts with practical NMEA 0183 parsing examples and will expand based on real integration needs.

---

## Current status

| Area | Status |
|---|---|
| NMEA parser | Available |
| NMEA examples | Available |
| GNSS Handbook companion guides | In progress |
| NTRIP client | Planned |
| RTCM decoder | Planned |
| Coordinate utilities | Planned |

---

## Quick Start

```bash
git clone https://github.com/KalmixTech/Kalmix-Toolkit.git
cd Kalmix-Toolkit
python NMEA/examples/multi_constellation.py
```

Parse a GGA sentence:

```python
from NMEA.parser import parse

line = "$GNGGA,072446.00,3114.562,N,12128.050,E,4,21,0.6,15.2,M,8.9,M,1.0,0031*50"
result = parse(line)

print(result["valid"])
print(result["data"]["fix_quality_label"])
```

Expected output:

```text
True
RTK Fixed
```

---

## Repository structure

```text
Kalmix-Toolkit/
├── NMEA/       # NMEA parser, coordinate helpers, and examples
├── guides/     # GNSS Handbook companion references
├── tests/      # pytest test cases
└── README.md
```

---

## NMEA module

The first working module is [`NMEA/`](NMEA/).

It includes:

- NMEA checksum verification
- GGA / RMC / VTG / GSA / GSV parsing
- Coordinate conversion helpers
- Multi-constellation Talker ID demo
- GSV page reassembly
- RTK Fix transition monitor

Run smoke tests:

```bash
python -m NMEA.parser.checksum
python -m NMEA.parser.coordinates
python -m NMEA.parser.nmea_parser
python NMEA/examples/multi_constellation.py
python NMEA/examples/gsv_reassembly.py
```

---

## Guides

See [`guides/`](guides/) for condensed developer references based on the Kalmix GNSS Handbook.

Key topics:

- NMEA 0183
- NTRIP
- RTCM
- GNSS accuracy
- Coordinate systems
- GNSS signals
- GNSS fundamentals

---

## Related repositories

- [Kalmix-Hardware](https://github.com/KalmixTech/Kalmix-Hardware) — datasheets, pinout diagrams, 3D STEP files, compliance documents, and protocol references.

---

## License

Code in this repository is released under the MIT License.

Kalmix product names, logos, hardware files, and proprietary documentation remain the property of Shanghai IOTARS Co., Ltd.
