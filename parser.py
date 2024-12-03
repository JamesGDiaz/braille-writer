import re

import charmap


def __replace_string(s: str):
    r = [charmap.alphabet[ch] for ch in s]
    return r


def braille_parser(full_text: str):
    lines = full_text.splitlines()

    parsed_text = []

    for text in lines:
        result = []
        i = 0
        while i < len(text):
            if text[i].isdigit():
                # Detect numbers (one digit or more)
                num_match = re.match(r"\d+", text[i:])
                num_str = num_match.group()
                result += [charmap.number_prefix] + __replace_string(num_str)
                i += len(num_str)
            elif text[i].isupper():
                # Check for uppercase words (more than one uppercase letter)
                upper_match = re.match(r"[ÑA-ZÁ-Ú]+", text[i:])
                upper_str = upper_match.group()
                if len(upper_str) == 1:
                    # Single uppercase letter
                    result += [charmap.uppercase] + __replace_string(upper_str.lower())
                else:
                    # Uppercase word (more than one uppercase letter)
                    result += [charmap.uppercase, charmap.uppercase] + __replace_string(
                        upper_str.lower()
                    )
                i += len(upper_str)
            elif text[i] == "\n" or text[i] == "\r":
                print(f"new line detected at pos {i}")
                i += 1
            else:
                # Other characters remain the same
                result += __replace_string(text[i])
                i += 1
        parsed_text.append((result, text))
    return parsed_text


if __name__ == "__main__":
    # Example usage:
    input_text = "The QUICK brown FOX jumps over 13 lazy DOGS.\nAnd then..."
    parsed_text = braille_parser(input_text)
    print(parsed_text)
