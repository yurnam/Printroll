import evilprinter




rickroll_lyrics = [
    "001 Never gonna give you up",
    "002 Never gonna let you down",
    "003 Never gonna run around and desert you",
    "004 Never gonna make you cry",
    "005 Never gonna say goodbye",]


if __name__ == '__main__':
    for i in rickroll_lyrics:
        ricks_printer = evilprinter.FakePrinter()
        ricks_printer.name = i
        ricks_printer.location = ''
        ricks_printer.note = 'Astley Corp'
        ricks_printer.publish()



