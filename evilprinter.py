import socket
import random
from zeroconf import Zeroconf, ServiceInfo
from time import sleep

class FakePrinter:
    _zeroconf = Zeroconf()
    _published_printers = []

    def __init__(self, name=None):
        self.name = name or f"FakePrinter-{random.randint(1000, 99999)}"
        self.location = "Unknown"
        self.manufacturer = "EvilCorp"
        self.note = "Just a printer"
        self.model = "PwnJet"
        self.port = random.randint(1025, 65535)
        self.ip = socket.gethostbyname(socket.gethostname())
        self._info = None
        self._published = False

    def _build_txt(self):
        return {
            "txtvers": "1",
            "qtotal": "1",
            "note": self.note,
            "product": f"({self.model})",
            "printer-state": "3",
            "printer-type": "0x809e4",
            "usb_MFG": self.manufacturer,
            "usb_MDL": self.model,
            "UUID": f"{random.randint(10000000,99999999)}-0000-1000-8000-{random.randint(10000000,99999999)}",
            "adminurl": f"http://{self.ip}",
            "ty": self.name,
            "priority": "0",
            "location": self.location,
        }

    def publish(self):
        if self._published:
            return

        props = self._build_txt()

        self._info = ServiceInfo(
            "_ipp._tcp.local.",
            f"{self.name}._ipp._tcp.local.",
            addresses=[socket.inet_aton(self.ip)],
            port=self.port,
            properties=props,
            server=f"{self.name.replace(' ', '-')}.local."
        )

        FakePrinter._zeroconf.register_service(self._info)
        FakePrinter._published_printers.append(self._info)
        self._published = True
        print(f"[+] Published printer: {self.name} on port {self.port}")

    def unpublish(self):
        if self._info and self._published:
            FakePrinter._zeroconf.unregister_service(self._info)
            self._published = False
            print(f"[-] Unpublished printer: {self.name}")

    @classmethod
    def cleanup(cls):
        for info in cls._published_printers:
            try:
                cls._zeroconf.unregister_service(info)
            except:
                pass
        cls._zeroconf.close()
        print("[*] Zeroconf cleaned up all fake printers.")



if __name__ == '__main__':

    try:
        for i in range(1000):
            p = FakePrinter()
            p.name = f"JK OfficeJunk {i:04d}"
            p.location = f"Room {i % 50}"
            p.manufacturer = "Nestle"
            p.note = "coffee"
            p.publish()
              # Tune for speed vs detection vs load
    except KeyboardInterrupt:
        print("\n[!] Interrupted, cleaning up...")
        FakePrinter.cleanup()




