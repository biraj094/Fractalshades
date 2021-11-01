# -*- coding: utf-8 -*-
"""
==============================
Colormaps: available templates
==============================

Colormaps can be created either:
 - directly in batch mode,
 - or in the GUI via the colormap table editor
 - or in the GUI tool to extract a colormap from a line drawn
   on an image


However, for convenience a few colormaps templates are also available.

To list them all ::

    import fractalshades.colors as fscolors
    fscolors.cmap_register.keys()

To access one by its name ::

    import fractalshades.colors as fscolors
    fscolors.cmap_register["atoll"]

Attached are the auto-generated images of the colormap templates available.
"""
import os
import importlib.resources

import PIL
from PIL import ImageDraw, ImageFont, PngImagePlugin

import fractalshades as fs
import fractalshades.colors as fscolors


def plot_cmap(cmap_identifier, plot_dir, nx=600, ny=80):
    cmap_register = fscolors.cmap_register
    cmap = cmap_register[cmap_identifier]
    B = cmap._output(nx, ny)
    B[:(ny // 2), :, :] = 255
    im = PIL.Image.fromarray(B)
    draw = ImageDraw.Draw(im)

    with importlib.resources.path('fractalshades', 'data') as data_path:
        font = ImageFont.truetype(
            os.path.join(data_path, "GidoleFont", "Gidole-Regular.ttf"),
            size=26
        )
        draw.text((0,0), cmap_identifier, (0, 0, 0), font=font)
        fs.utils.mkdir_p(plot_dir)

        if fs.settings.output_context["doc"]:
            tag_dict = {"Software": "fractalshades " + fs.__version__,
                        "colormap template": cmap_identifier}
            pnginfo = PngImagePlugin.PngInfo()
            for k, v in tag_dict.items():
                pnginfo.add_text(k, str(v))
            fs.settings.add_figure(fs._Pillow_figure(im, pnginfo))

        else:
            im.save(os.path.join(plot_dir, cmap_identifier + ".png"))

def plot_cmaps(plot_dir):
    cmap_register = fscolors.cmap_register
    for cmap_identifier in cmap_register.keys():
        plot_cmap(cmap_identifier, plot_dir)


if __name__ == "__main__":
    # Some magic to get the directory for plotting: with a name that matches
    # the file or a temporary dir if we are building the documentation
    try:
        realpath = os.path.realpath(__file__)
        plot_dir = os.path.splitext(realpath)[0]
        plot_cmaps(plot_dir)
    except NameError:
        import tempfile
        with tempfile.TemporaryDirectory() as plot_dir:
            plot_cmaps(plot_dir)

