# imagemapping

> Map an image into a perspective transform under another one.

Useful for memes.

## Usage

```sh
python3 imagemapping.py input.png output.png \
  --template tmpl.png \
  --coords '[(0, 0), (256, 0), (256, 256), (0, 256)]'
```

e.g., with the template provided in the tree:

```sh
python3 imagemapping.py input.png output.png -t kid.png -f kidcoords.png
```

## License

This project is licensed under the MIT license. Please see the
[LICENSE](LICENSE) file for more details.
