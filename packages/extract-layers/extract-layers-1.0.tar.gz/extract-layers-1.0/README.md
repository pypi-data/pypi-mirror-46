# extract-layers

extract-layers is a simple command-line tool that can extract the layers of an Illustrator-exported SVG and save them as individual SVG files. Unlike Illustrator's "Asset Export" feature, extract-layers will preserve the position of each layer relative to the artboard. Running extract-layers is roughly equivalent to performing the following steps within Illustrator for each layer:

1. Hide all layers except the current layer.
2. Export the document to an SVG file named after the current layer.

If `my-file.svg` has layers named `a`, `b`, and `c`, the following command will extract those layers to `my-file-layers/a.svg`, `my-file-layers/b.svg`, and `my-file-layers/c.svg`:

```
extract-layers --output-directory my-file-layers/ < my-file.svg
```

## Installation

```
pip3 install --user --upgrade extract-layers
```

## Usage

```
Usage: extract-layers [OPTIONS]

  Extracts layers of an Illustrator-exported SVG and saves them as
  individual SVG files

Options:
  --output-directory TEXT  Directory in which to save the layers.  [required]
  --overwrite              Clobber existing files.
  --help                   Show this message and exit.
```

## License

[AGPLv3](https://www.gnu.org/licenses/agpl-3.0.en.html)
