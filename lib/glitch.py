import re
import struct
import itertools

from PIL import Image, ImageSequence, GifImagePlugin

def sub_res(b, offset=100):
    # Get the 4 resolution bytes
    res = b[6:10]

    # Get the actual resolution pixels
    h, w = divmod(struct.unpack("<I", res)[0], 256)
    h //= 256

    print(f'Image size: {w}x{h} ({w}x{h - offset} after resize)')
    print(f'Found {len(re.findall(b[6:10], b))} resolution instances')

    # Create glitched resolution bytes
    new_res = struct.pack('<I', ((h - offset) * 256) * 256 + w)

    # Replace normal resolution bytes with glitched ones
    glitched = re.sub(b[6:10], new_res, b)

    return glitched

class GIF(object):
    def __init__(self, filename):
        self.source = Image.open(filename)
        self.palette = GifImagePlugin._get_palette_bytes(self.source)

        self.source.info["disposal"] = 2 # This should get set automatically, but it doesn't so whatever, if your GIF looks fucked then its probably this
        self.source.encoderinfo = self.source.info

    def prepare_glitch(self, offset=100):
        # MODIFIED FROM
        # https://github.com/python-pillow/Pillow/blob/48a05e6cf3fc98b6385034372143f06fe6719e4e/src/PIL/GifImagePlugin.py#L416

        duration = self.source.encoderinfo.get("duration", self.source.info.get("duration"))
        disposal = self.source.encoderinfo.get("disposal", self.source.info.get("disposal"))

        im_frames = []
        frame_count = 0
        for imSequence in itertools.chain([self.source],
                                        self.source.encoderinfo.get("append_images", [])):
            for im_frame in ImageSequence.Iterator(imSequence):
                # a copy is required here since seek can still mutate the image
                im_frame = GifImagePlugin._normalize_mode(im_frame.copy())
                if frame_count == 0:
                    for k, v in im_frame.info.items():
                        self.source.encoderinfo.setdefault(k, v)
                im_frame = GifImagePlugin._normalize_palette(im_frame, self.palette, self.source.encoderinfo)

                encoderinfo = self.source.encoderinfo.copy()
                if isinstance(duration, (list, tuple)):
                    encoderinfo['duration'] = duration[frame_count]
                if isinstance(disposal, (list, tuple)):
                    encoderinfo["disposal"] = disposal[frame_count]
                frame_count += 1

                # Crop the image to add <glitch_offset> px to the bottom
                im_frame = im_frame.crop((0, 0, self.source.size[0], self.source.size[1] + offset))

                im_frames.append({
                    'im': im_frame,
                    'encoderinfo': encoderinfo
                })

            return im_frames

    def write_gif(self, fp, im_frames):
        frame_count = 0
        if len(im_frames) > 1:
            for frame_data in im_frames:
                im_frame = frame_data['im']

                if frame_count == 0:
                    # global header
                    for s in GifImagePlugin._get_global_header(im_frame,
                                                frame_data['encoderinfo']):
                        fp.write(s)
                else:
                    frame_data['encoderinfo']['include_color_table'] = True

                offset = (0, 0)
                GifImagePlugin._write_frame_data(fp, im_frame, offset, frame_data['encoderinfo'])

                frame_count += 1

            fp.write(b";")

        print(f'Wrote {frame_count} frames')