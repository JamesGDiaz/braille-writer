braille_chars = {
    "a": 0x01,
    "á": 0x37,
    "b": 0x03,
    "c": 0x09,
    "d": 0x19,
    "e": 0x11,
    "é": 0x2E,
    "f": 0x0B,
    "g": 0x1B,
    "h": 0x13,
    "i": 0x0A,
    "í": 0x0C,
    "j": 0x1A,
    "k": 0x05,
    "l": 0x07,
    "m": 0x0D,
    "n": 0x1D,
    "ñ": 0x3B,
    "o": 0x15,
    "ó": 0x2C,
    "p": 0x0F,
    "q": 0x1F,
    "r": 0x17,
    "s": 0x0E,
    "t": 0x1E,
    "u": 0x25,
    "ú": 0x3E,
    "ü": 0x33,
    "v": 0x27,
    "w": 0x3A,
    "x": 0x2D,
    "y": 0x3D,
    "z": 0x35,
    " ": 0x00,
    "\n": None,
}
uppercase = 0x28

number_prefix = 0x3C
numbers = {
    "1": 0x01,
    "2": 0x03,
    "3": 0x09,
    "4": 0x19,
    "5": 0x11,
    "6": 0x0B,
    "7": 0x1B,
    "8": 0x13,
    "9": 0x0A,
    "0": 0x1A,
}

punctuation = {
    ".": 0x04,
    ",": 0x02,
    ";": 0x06,
    ":": 0x12,
    "-": 0x24,
    "¿": 0x22,
    "?": 0x22,
    "¡": 0x16,
    "!": 0x16,
    '"': 0x26,
    "“": 0x26,
    "”": 0x26,
    "´": 0x04,
    "`": 0x04,
    "'": 0x04,
    "(": 0x23,
    ")": 0x1C,
}

alphabet = braille_chars | numbers | punctuation
