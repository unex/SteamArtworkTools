import os, sys
import glob

from lib.glitch import GIF, sub_res

if len(sys.argv) < 2:
    print(f'Usage: {sys.argv[0]} <source>')
    sys.exit(1)

for infile in glob.glob(sys.argv[1]):
    print(f'Glitching {infile}')

    outfile = os.path.splitext(infile)[0] + "_glitched.gif"

    im = GIF(infile)
    frames = im.prepare_glitch()

    with open(outfile, 'wb') as fp:
        im.write_gif(fp, frames)

    with open(outfile, "rb") as fp:
        glitched = sub_res(fp.read())

        with open(outfile, 'wb') as of:
            of.write(glitched)
            print(f'Wrote file {outfile}')