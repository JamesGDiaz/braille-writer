import argparse
import glob
import math
import os
from parser import braille_parser
from glyph import make_svg_pages, mm_to_in


def parse_args():
    parser = argparse.ArgumentParser(description="UTF-8 Text to Braille in SVG")
    parser.add_argument(
        "-m","--mirror",
        action='store_true',
        help="Mirror SVG objects with respect to the center of the page",
        default=False,
        required=False
    )
    parser.add_argument(
        "-i",
        "--input",
        help="Input text file",
        required=False,
        type=str,
        default="input.txt",
    )
    parser.add_argument(
        "-o",
        "--output",
        help="Output name",
        required=False,
        type=str,
        default="output",
    )

    args = vars(parser.parse_args())

    return args


def create_svg_output(
    input_txt: str, output_name: str, output_directory: os.PathLike, mirror_svg: bool
):
    parsed_text = braille_parser(input_txt)

    margin_x = 20
    margin_y = 20
    interline = 10
    dpi = 96

    pageW = 210
    pageH = 297

    max_lines = math.ceil((pageH - 2 * margin_y) / interline)
    pageWpx = math.ceil(pageW * dpi / mm_to_in)
    pageHpx = math.ceil(pageH * dpi / mm_to_in)

    print(f"Page Width: {pageWpx}px ({pageW}mm)\nPage Height: {pageH}px ({pageH}mm)")
    print(f"Total lines: {len(parsed_text)}")
    print(f"Max lines per page: {max_lines}")
    result = make_svg_pages(
        parsed_text,
        pageH=pageH,
        pageW=pageW,
        interline=interline,
        margin_x=margin_x,
        margin_y=margin_y,
        mirror=mirror_svg,
    )
    svg_content = list(reversed(result[0]))
    text_content = list(reversed(result[1]))

    print(f"Found {len(svg_content)} pages")

    # Write the SVG content to output.svg
    print(f"Writing pages to {output_directory}")
    for i, page in enumerate(svg_content):
        n_page = i + 1

        path = os.path.join(output_directory, f"{output_name}_{n_page}.svg")
        with open(path, "w", encoding="utf-8") as f:
            f.write(page)

    with open("output_templ.html", "r", encoding="utf-8") as html_cont:
        html = html_cont.read()

        path = os.path.join(output_directory, f"{output_name}.html")
        with open(path, "w", encoding="utf-8") as f:
            html = html.replace("[[TITLE]]", output_name)
            html = html.replace("[[INPUT]]", input_txt.replace("\n", "<br/>"))
            html = html.replace(
                "[[SVG_PAGES]]",
                "".join(
                    [
                        f"""<div class="svg-content">"""
                        f"""<!-- SVG Content -->"""
                        f"""{page}"""
                        f"""</div>"""
                        for page in svg_content
                    ]
                ),
            )
            html = html.replace(
                "[[TEXT_PAGES]]",
                "".join(
                    [
                        f"""<div class="svg-content regular-text">"""
                        f"""<!-- SVG Content -->"""
                        f"""{page}"""
                        f"""</div>"""
                        for page in text_content
                    ]
                ),
            )
            f.write(html)


if __name__ == "__main__":
    args = parse_args()

    print("Program arguments: ", args)

    output_directory = os.path.abspath(f"./output/{args['output']}")
    os.makedirs(output_directory, exist_ok=True)
    for filepath in glob.glob(os.path.join(output_directory, "*")):
        os.remove(filepath)

    with open(args["input"], "r", encoding="utf-8") as f:
        text_content = f.read()

    create_svg_output(text_content, args["output"], output_directory, mirror_svg=args['mirror'])
