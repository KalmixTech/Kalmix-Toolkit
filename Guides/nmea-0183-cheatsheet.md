# NMEA 0183 Cheatsheet

A practical reference for parsing NMEA 0183 GNSS streams.

Full article: [Mastering NMEA 0183: Why Your Device Needs to Read Between the Commas](https://www.kalmixtech.com/blogs/blog/mastering-nmea-0183-guide)

Code companion: [`NMEA/`](../NMEA/)

---

## Sentence structure

```text
$GNGGA,072446.00,3114.562,N,12128.050,E,4,21,0.6,15.2,M,8.9,M,1.0,0031*50
```

| Part | Example | Meaning |
|---|---|---|
| Start delimiter | `$` | Start of sentence |
| Talker ID | `GN` | Multi-constellation GNSS |
| Sentence ID | `GGA` | Fix data sentence |
| Payload | comma-separated fields | Data fields |
| Checksum | `*50` | XOR checksum |

---

## Talker IDs

| ID | Meaning |
|---|---|
| `GP` | GPS |
| `GL` | GLONASS |
| `GA` | Galileo |
| `GB` | BeiDou |
| `GQ` | QZSS |
| `GI` | NavIC / IRNSS |
| `GN` | Combined multi-constellation solution |

Rule: match on the sentence ID, not the talker ID.

Good:

```python
sentence_id = header[2:5]
if sentence_id == "GGA":
    ...
```

Bad:

```python
if line.startswith("$GPGGA"):
    ...
```

---

## The Big Five

| Sentence | Primary use |
|---|---|
| `GGA` | Coordinates, fix quality, satellites used, HDOP, altitude |
| `RMC` | Minimal navigation data: position, speed, course, date |
| `VTG` | Course and speed over ground |
| `GSA` | Fix type, active satellites, PDOP / HDOP / VDOP |
| `GSV` | Satellites in view, signal strength, skyplot data |

---

## GGA fix quality

| Value | Meaning |
|---|---|
| `0` | Invalid |
| `1` | GPS fix / single-point positioning |
| `2` | Differential GNSS |
| `4` | RTK Fixed |
| `5` | RTK Float |
| `6` | Estimated / dead reckoning |

For RTK integration, monitor field 6 and look for:

```text
1 → 2 → 5 → 4
```

Where `4` means RTK Fixed.

---

## Coordinate conversion

NMEA does not output decimal degrees. It uses degrees + decimal minutes.

```text
3114.562,N = 31 + 14.562 / 60 = 31.242700°
12128.050,E = 121 + 28.050 / 60 = 121.467500°
```

Use:

```python
from NMEA.parser import ddmm_to_decimal

lat = ddmm_to_decimal("3114.562", "N")
lon = ddmm_to_decimal("12128.050", "E")
```

---

## Checksum rule

The checksum is the XOR of all characters between `$` and `*`.

Use:

```python
from NMEA.parser import verify_checksum

verify_checksum("$GNGGA,072446.00,3114.562,N,12128.050,E,4,21,0.6,15.2,M,8.9,M,1.0,0031*50")
```

Treat checksum mismatch as a dropped packet.

---

## GSV page reassembly

A single `GSV` sentence can carry up to four satellites. A full satellite-view snapshot often arrives across multiple pages.

Use `GSVAssembler`:

```python
from NMEA.parser import parse, GSVAssembler

assembler = GSVAssembler()

for line in nmea_lines:
    parsed = parse(line, validate_checksum=False)
    if parsed["sentence_type"] == "GSV":
        complete = assembler.feed(parsed)
        if complete:
            print(complete["talker"], len(complete["satellites"]))
```

---

## Common bugs

| Bug | Result |
|---|---|
| Hard-coding `$GPGGA` | Breaks on `$GNGGA` and multi-constellation receivers |
| Treating `DDMM.MMMM` as decimal degrees | Position appears kilometers away |
| Ignoring checksum | Corrupted serial data enters the application |
| Treating one GSV page as full sky view | Satellite UI appears to drop satellites |
| Using GGA altitude as ellipsoidal height | Height conversion errors in precision workflows |
