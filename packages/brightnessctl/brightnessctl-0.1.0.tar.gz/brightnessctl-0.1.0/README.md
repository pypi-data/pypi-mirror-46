# brightnessctl - Control screen brightness on Linux
Inspired by [brightnessctl](https://github.com/Hummer12007/brightnessctl)


# Installation
`pip install --user brightnessctl`


# Usage
```sh
usage: brightnessctl [-h] [-v] [-p N | -d N | -r N] [--duration S]
                     [--save | --restore]

optional arguments:
  -h, --help          show this help message and exit
  -v, --verbose
  -p N, --percent N   Set brightness to <N> %
  -d N, --delta N     Adjust brightness by <N> % of max brightness
  -r N, --relative N  Adjust brightness by <N> % of current brightness
  --duration S        How long to take to get to final value
  --save              Save current value to disk before changing value
  --restore           Restore saved value from disk
```
