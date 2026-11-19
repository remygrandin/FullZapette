# FullZapette

An open, 3D-printable universal remote in the spirit of the Logitech Harmony:
real buttons, a colour touchscreen, an IR blaster and a native Home Assistant link.

**Status:** design phase — nothing is built yet.

- [Design document](docs/DESIGN.md) — requirements, architecture, part choices, key layout, power budget, open questions.

At a glance (draft v0.1):

| | |
|---|---|
| Size | ≈ 200 × 50 × 20 mm |
| Screen | 2.4" IPS, 240 × 320, capacitive touch |
| Brain | ESP32-S3 (Wi-Fi + BLE) |
| Control | IR send + learn, Home Assistant (WebSocket), BLE HID |
| Keys | 37 hard keys: D-pad, navigation, volume/channel, transport, colour, numpad |
| Wake | Pick-up (accelerometer), any key |
| Battery | 2000 mAh Li-Po, ≈ 1–5 weeks (estimated), USB-C + pogo-pin cradle |
| Enclosure | Fully FDM-printable |
