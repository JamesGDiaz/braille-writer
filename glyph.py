import itertools
import math


mm_to_in = 25.4


def braille_glyph_factory(bits):
    """
    Generates an SVG path command for a 6-dot braille character.

    Parameters:
    bits (int): A 6-bit integer (0 to 63) representing the braille dots.
                Each bit corresponds to a dot in the braille cell:
                - Bit 0 (LSB): Dot 1 (top-left)
                - Bit 1: Dot 2 (middle-left)
                - Bit 2: Dot 3 (bottom-left)
                - Bit 3: Dot 4 (top-right)
                - Bit 4: Dot 5 (middle-right)
                - Bit 5: Dot 6 (bottom-right)
    r (float): Radius of each dot
    dx (float): Horizontal distance between columns
    dy (float): Vertical distance between rows
    x0 (float): Starting x-coordinate
    y0 (float): Starting y-coordinate

    Returns:
    str: An SVG path command that draws the specified braille character.
    """

    """ The following sizes are set according to https://www.brailleauthority.org/size-and-spacing-braille-characters """
    """ Units are in mm """
    r = 0.75
    dx = 2.34
    dy = 2.34
    x0 = 0
    y0 = 0

    # Positions of the dots (cx, cy) in the braille cell
    positions = [
        (x0, y0),  # Dot 1 (bit 0)
        (x0, y0 + dy),  # Dot 2 (bit 1)
        (x0, y0 + 2 * dy),  # Dot 3 (bit 2)
        (x0 + dx, y0),  # Dot 4 (bit 3)
        (x0 + dx, y0 + dy),  # Dot 5 (bit 4)
        (x0 + dx, y0 + 2 * dy),  # Dot 6 (bit 5)
    ]

    path_data = ""
    for i in range(6):
        if bits & (1 << i):
            # The bit is set; include this dot
            cx, cy = positions[i]
            # Move to the starting point of the circle
            path_data += f"M {cx + r} {cy} "
            # Draw the circle using two arcs
            path_data += f"A {r} {r} 0 1 0 {cx - r} {cy} "
            path_data += f"A {r} {r} 0 1 0 {cx + r} {cy} "
    return path_data


def get_svg_line_paths(braille_chars: list[int], pageW=0, margin_x=0, interline=0):
    """
    Spacing found at https://www.brailleauthority.org/size-and-spacing-braille-characters
    Checked on October 22th, 2024
    """

    svg_paths = []

    x = margin_x

    used_lines = 1

    # Process each character in the line
    for i, char in enumerate(braille_chars):
        path_data = braille_glyph_factory(char)

        # Apply transformations to position and scale the cell
        transform = f"translate({x},{(used_lines-1)*interline})"

        # Create the SVG path element
        svg_path = f'<path d="{path_data}" transform="{transform}" fill="black"/>\n'
        svg_paths.append(svg_path)

        # Update x position based on the standard cell width
        advance_width = 6.2
        x += advance_width

        if x > (pageW - margin_x):
            used_lines += 1
            x = margin_x

    return svg_paths, used_lines


def make_svg_pages(
    lines: list[tuple[list[int], str]],
    interline: int = 4,
    pageW=210,
    pageH=297,
    dpi=96,
    margin_x=20,
    margin_y=20,
    page_number=1,
    mirror=False,
):
    """
    Create the SVG content
    All units in mm
    """
    svg_pages = []
    text_pages = []

    current_line = 0
    svg_lines = []
    text_lines = []

    for i, (braille_line, regular_text) in enumerate(lines):
        y_pos = margin_y + ((current_line) * interline)

        if y_pos >= pageH - margin_y:
            # print(f"Creating page break, remaining {len(lines[i:])}")
            s, t = make_svg_pages(
                lines[i:],
                interline=interline,
                pageW=pageW,
                pageH=pageH,
                dpi=dpi,
                margin_x=margin_x,
                margin_y=margin_y,
                page_number=page_number + 1,
                mirror=mirror,
            )
            svg_pages.append(s)
            text_pages.append(t)
            break

        paths, used_lines = get_svg_line_paths(
            braille_line, pageW=pageW, margin_x=margin_x, interline=interline
        )
        svg_lines.append(
            f"""<g transform="translate(0,{y_pos}) scale({1 if not mirror else -1}, 1)" """
            f"""{"" if not mirror else f"transform-origin=\"50% 50%\""}>{''.join(paths)}"""
            """</g>"""
        )
        text_lines.append(
            f"""<text transform="translate({margin_x},{y_pos}) scale({1 if not mirror else -1}, 1)" """
            f""" font-size="5.5" font-family="Times New Roman" """
            f""" {"" if not mirror else f"transform-origin=\"{(pageW-margin_x*2)/2} 0\""}>{regular_text}"""
            """</text>"""
        )
        current_line += used_lines
    svg_content = f"""<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<svg
   xmlns="http://www.w3.org/2000/svg"
   version="1.1"
   xmlns:inkscape="http://www.inkscape.org/namespaces/inkscape"
   xmlns:sodipodi="http://sodipodi.sourceforge.net/DTD/sodipodi-0.dtd"
   xmlns:svg="http://www.w3.org/2000/svg"
   id="svg_page_{page_number}"
   width="{math.ceil(pageW * dpi / mm_to_in)}"
   height="{math.ceil(pageH * dpi / mm_to_in)}"
   viewBox="0 0 {pageW} {pageH}"
   preserveAspectRatio="none">
{''.join(svg_lines)}
</svg>"""

    text_content = f"""<svg
   xmlns="http://www.w3.org/2000/svg"
   version="1.1"
   xmlns:inkscape="http://www.inkscape.org/namespaces/inkscape"
   xmlns:sodipodi="http://sodipodi.sourceforge.net/DTD/sodipodi-0.dtd"
   xmlns:svg="http://www.w3.org/2000/svg"
   id="text_page_{page_number}"
   width="{math.ceil(pageW * dpi / mm_to_in)}"
   height="{math.ceil(pageH * dpi / mm_to_in)}"
   viewBox="0 0 {pageW} {pageH}"
   preserveAspectRatio="none">
{''.join(text_lines)}
</svg>"""

    svg_pages.append(svg_content)
    text_pages.append(text_content)

    return flatten(svg_pages), flatten(text_pages)


def flatten(l):
    return list(
        itertools.chain.from_iterable(
            itertools.repeat(x, 1) if isinstance(x, str) else x for x in l
        )
    )
