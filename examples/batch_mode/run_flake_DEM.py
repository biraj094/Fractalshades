# -*- coding: utf-8 -*-
"""
==================
Deeper DEM example
==================

This example shows how to create a color layer, displaying the 
distance estimation for Mandelbrot (power 2) fractal.

The location, at 1.e-54, is below the reach of double, pertubation theory must
be used.
"""

import os
import numpy as np

import fractalshades as fs
import fractalshades.models as fsm
import fractalshades.settings as settings
import fractalshades.colors as fscolors


from fractalshades.postproc import (
    Postproc_batch,
    DEM_pp,
    Continuous_iter_pp,
    Raw_pp,
    DEM_normal_pp,
    # Fieldlines_pp,
)
from fractalshades.colors.layers import (
    Color_layer,
    Bool_layer,
    # Blinn_lighting,
    # Normal_map_layer,
    Virtual_layer,
)

def plot(directory):
    """
    Example plot of distance estimation method
    """
    # A simple showcas using perturbation technique
    precision = 164
    nx = 1800
    x = '-1.99996619445037030418434688506350579675531241540724851511761922944801584242342684381376129778868913812287046406560949864353810575744772166485672496092803920095332'
    y = '-0.00000000000000000000000000000000030013824367909383240724973039775924987346831190773335270174257280120474975614823581185647299288414075519224186504978181625478529'
    dx = '1.8e-157'

#    x = "-0.746223962861"
#    y = "-0.0959468433527"
#    dx = "0.00745"
#    nx = 800

    colormap = fscolors.cmap_register["valensole"]

    # Set to True if you only want to rerun the post-processing part
    settings.skip_calc = False
    # Set to True to enable multi-processing
    settings.enable_multiprocessing = True

#    xy_ratio = 1.0
#    theta_deg = 0.
    # complex_type = np.complex128

    f = fsm.Perturbation_mandelbrot(directory)
    f.zoom(precision=precision,
            x=x,
            y=y,
            dx=dx,
            nx=nx,
            xy_ratio=1.0,
            theta_deg=0., 
            projection="cartesian",
            antialiasing=False)

    f.calc_std_div(
            datatype=np.complex128,
            calc_name="div",
            subset=None,
            max_iter=1000000, #00,
            M_divergence=1.e3,
            epsilon_stationnary=1.e-3,
            SA_params={"cutdeg": 8,
                       "cutdeg_glitch": 8,
                       "SA_err": 1.e-4},
            glitch_eps=1.e-6,
            interior_detect=True,
            glitch_max_attempt=20)

    f.run()
    
    # Plot the image
    pp = Postproc_batch(f, "div")
    pp.add_postproc("potential", Continuous_iter_pp())
    pp.add_postproc("DEM", DEM_pp())
    pp.add_postproc("interior", Raw_pp("stop_reason", func="x != 1."))
    pp.add_postproc("DEM_map", DEM_normal_pp(kind="potential"))
    
    plotter = fs.Fractal_plotter(pp)   
    plotter.add_layer(Bool_layer("interior", output=False))
#    plotter.add_layer(Normal_map_layer("DEM_map", max_slope=60, output=True))
#    plotter.add_layer(Color_layer(
#            "DEM2",
#            func="np.log(x)", #"np.log(np.log(x))",
#            colormap=colormap,
#            probes_z=[0.0, 1.0],
#            probes_kind="relative",
#            output=True
#    ))
    plotter.add_layer(Virtual_layer("potential", func=None, output=False))
    plotter.add_layer(Color_layer(
            "DEM",
            func="np.log(x)",
            colormap=colormap,
            probes_z=[0., 5.],
            probes_kind="absolute",
            output=True
    ))
    plotter["DEM"].set_mask(
            plotter["interior"],
            mask_color=(0., 0., 0.)
    )
    
    plotter.plot()

if __name__ == "__main__":
    # Some magic to get the directory for plotting: with a name that matches
    # the file or a temporary dir if we are building the documentation
    try:
        realpath = os.path.realpath(__file__)
        plot_dir = os.path.splitext(realpath)[0]
        plot(plot_dir)
    except NameError:
        import tempfile
        with tempfile.TemporaryDirectory() as plot_dir:
            plot(plot_dir)
