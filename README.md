# 🖨️ Printroll

> A high-performance LAN printer spoofer for stress testing and surprise rickrolling.  
> Create thousands of fake IPP printers — each one singing the lyrics of *Never Gonna Give You Up*.

![Screenshot](screenshot.png)

---

## 💡 What is this?

**Printroll** lets you broadcast thousands of fake IPP printers via mDNS/zeroconf.  
It's useful for:

- Stress testing printer discovery (e.g. `cups-browsed`, Bonjour, Windows WSD)
- Simulating chaotic enterprise networks
- Dropping a surprise Rick Astley across the LAN 🎶

---

## 🚀 Features

- Dynamic printer creation using a Python class
- Each printer can have its own:
  - Name
  - Location
  - Manufacturer
  - Custom note
- Can spawn thousands of printers instantly
- Uses `zeroconf` to advertise printers over the network
- Cleans up on shutdown or CTRL+C
- Fully scriptable and extendable

---

## 🛠️ Requirements

```bash
pip install zeroconf
