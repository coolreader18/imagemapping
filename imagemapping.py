import os
import sys
from PIL import Image
import numpy as np
import argparse
import ast


def find_coeffs(source_coords, target_coords):
    matrix = []
    for s, t in zip(source_coords, target_coords):
        matrix.append([t[0], t[1], 1, 0, 0, 0, -s[0] * t[0], -s[0] * t[1]])
        matrix.append([0, 0, 0, t[0], t[1], 1, -s[1] * t[0], -s[1] * t[1]])
    A = np.matrix(matrix, dtype=np.float)
    B = np.array(source_coords).reshape(8)
    res = np.dot(np.linalg.inv(A.T * A) * A.T, B)
    return np.array(res).reshape(8)


def overlay(tmpl, img, coords) -> Image.Image:
    coeffs = find_coeffs([(0, 0), (img.size[0], 0), img.size, (0, img.size[1])], coords)

    img = img.transform(img.size, Image.PERSPECTIVE, coeffs, Image.BICUBIC)
    img = img.crop((0, 0, *tmpl.size))
    img.paste(tmpl, (0, 0), tmpl)
    return img


parser = argparse.ArgumentParser(prog="imagemapping", description="Map image")
parser.add_argument("input", nargs="?", default=sys.stdin.buffer)
parser.add_argument("output", nargs="?", default=sys.stdout.buffer)
parser.add_argument("--template", "-t", required=True)

group = parser.add_mutually_exclusive_group(required=True)
group.add_argument("--coords", "-c")
group.add_argument("--coords-file", "-f")


def main(args):
    args = parser.parse_args(args)

    input = sys.stdin.buffer if args.input == "-" else args.input
    output = sys.stdout.buffer if args.output == "-" else args.output

    print(args)

    if args.coords_file:
        with open(args.coords_file) as f:
            coords = f.read()
    else:
        coords = args.coords

    coords = ast.literal_eval(coords)

    tmpl: Image.Image = Image.open(args.template)
    img: Image.Image = Image.open(input)
    format = "png" if output is sys.stdout.buffer else None

    overlay(tmpl, img, coords).save(output, format)


if __name__ == "__main__":
    main(sys.argv[1:])
