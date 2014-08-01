# Split Text

Take some text and render multiple images. Each image looks like gibberish by itself. Put them together and your message magically* appears!

*Note: No fairy dust was used in the making of this software.

Requires `python3` and `python3-cairo`.

## Usage

```
usage: drawtext.py [-h] [-s S] [-z S] [-n N] [--break-on-char] [-f] [-w W]
                   [-t T] [-v]
                   [FILE]

Render split messages.

positional arguments:
  FILE              an ASCII/UTF-7 encoded text file to render. If not
                    specified, defaults to STDIN.

optional arguments:
  -h, --help        show this help message and exit
  -s S, --split S   set the number of images to split the image into (default:
                    2)
  -z S, --scale S   set the size of each block in the block font (default: 5)
  -n N, --noise N   set the amount of noise in the white part of the image
                    (default: 0.2)
  --break-on-char   break lines on character boundaries (default: words are
                    not broken across lines)
  -f, --first-line  do not split the first line
  -w W, --width W   set the width of the output in blocks (default: set by
                    output type)
  -t T, --type T    output as TXT, HTML, PNG (default: TXT). PNG requires
                    PyCairo.
  -v, --verbose     output additional images
```

## License

See License.md
