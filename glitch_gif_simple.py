"""
Steam Long Workshop / Guide GIF Glitcher
========================================
https://github.com/notderw/SteamArtworkTools/
========================================

THIS SCRIPT IS EXPERIMENTAL!
If you have any issues, please leave a comment detailing any errors you are having.
If this script does not work on your GIF, try using the HEX editor method detailed
in the guide below.

Original Guide: https://steamcommunity.com/sharedfiles/filedetails/?id=1627692828

This script replaces the hex editor step in the above guide.

Requirements: Python 3.6+ (?) (Tested on 3.7.0)

TLDR steps:
1. Split your gif into 160px wide sections
2. Add 100px of extra space to the bottom of each
3. Run this script on each, Ex: 'python glitch_gif_simple.py <source image(s)>'
4. Upload to Steam (see guide for specific instructions)
"""

import os, sys
import glob

from lib.glitch import sub_res

if len(sys.argv) < 2:
    print(f'Usage: {sys.argv[0]} <source>')
    sys.exit(1)

for infile in glob.glob(sys.argv[1]):
    print(f'Glitching {infile}')

    outfile = os.path.splitext(infile)[0] + "_glitched.gif"

    with open(infile, "rb") as fp:
        glitched = sub_res(fp.read())

        with open(outfile, 'wb') as of:
            of.write(glitched)
            print(f'Wrote file {outfile}')