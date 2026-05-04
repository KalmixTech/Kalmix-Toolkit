<p align="center">
  <img src="https://raw.githubusercontent.com/KalmixTech/Kalmix-Hardware/main/Assets/KALMIX-Logo.png" alt="Kalmix" width="260">
</p>

<h3 align="center">Developer Toolkit Repository</h3>

<p align="center">
  Python tools, protocol examples, and developer cheatsheets for GNSS/RTK integration.<br>
  Companion resources for the Kalmix GNSS Handbook.
</p>

<p align="center">
  <a href="https://www.kalmixtech.com">Website</a> ·
  <a href="https://www.kalmixtech.com/blogs/blog">GNSS Handbook</a> ·
  <a href="https://github.com/KalmixTech/Kalmix-Hardware">Hardware Resources</a>
</p>

---

## Overview

**Kalmix-Toolkit** provides lightweight developer tools and practical references for working with GNSS/RTK data streams.

The repository currently starts with a working **NMEA 0183 parser** and example scripts. Additional NTRIP, RTCM, coordinate-system, and accuracy-analysis utilities will be added based on real integration needs.

---

## Current Status

| Area | Status |
|---|---|
| NMEA 0183 parser | Available |
| NMEA examples | Available |
| GNSS Handbook companion guides | In progress |
| NTRIP client examples | Planned |
| RTCM frame utilities | Planned |
| Coordinate utilities | Planned |
| Accuracy analysis utilities | Planned |

---

## Quick Start

Clone the repository:

```bash
git clone https://github.com/KalmixTech/Kalmix-Toolkit.git
cd Kalmix-Toolkit
```

Run a built-in example:

```bash
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

## Repository Structure

```text
Kalmix-Toolkit/
├── NMEA/
│   ├── parser/
│   ├── examples/
│   └── README.md
│
├── guides/
│   ├── README.md
│   └── *.md
│
├── tests/
│   └── test_*.py
│
├── requirements.txt
├── LICENSE
└── README.md
```

---

## NMEA Module

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

Run the test suite:

```bash
pip install -r requirements.txt
python -m pytest -q
```

---

## Guides

The [`guides/`](guides/) directory contains condensed developer references based on the Kalmix GNSS Handbook.

| Guide | Purpose |
|---|---|
| `nmea-0183-cheatsheet.md` | NMEA sentence structure, common fields, checksum rules, and parsing traps |
| `ntrip-quickstart.md` | NTRIP workflow, caster connection basics, and RTK correction setup notes |
| `rtk-accuracy-explained.md` | CEP, RMS, R95, RTK Fixed / Float, and accuracy interpretation |
| `coordinate-systems-guide.md` | WGS84, datums, coordinate formats, and height-reference pitfalls |
| `rtcm-frame-reference.md` | RTCM 3.x frame structure and MSM message reference |
| `gnss-signals-reference.md` | GNSS constellations, L1/L2/L5 bands, and signal-selection notes |
| `how-gnss-works.md` | GNSS fundamentals: pseudorange, four satellites, and receiver clock bias |

For the full articles, visit the [Kalmix GNSS Handbook](https://www.kalmixtech.com/blogs/blog).

---

## Related Repository

For product-level hardware files, see:

[Kalmix-Hardware](https://github.com/KalmixTech/Kalmix-Hardware)

It contains datasheets, interface diagrams, 3D STEP models, compliance files, and product-specific protocol references for Kalmix GNSS hardware.

---

## Requirements

The core parser uses only the Python standard library.

Optional dependencies:

```text
pyserial>=3.5
pytest>=8.0.0
```

- `pyserial` is required only for live serial-port examples.
- `pytest` is required only for running tests.

---

## License

Code in this repository is released under the MIT License.

Kalmix product names, logos, hardware files, and proprietary documentation remain the property of **Shanghai IOTARS Co., Ltd.**

---

<p align="center">
  <sub>Shanghai IOTARS Co., Ltd. · <a href="https://www.kalmixtech.com">kalmixtech.com</a></sub>
</p>
