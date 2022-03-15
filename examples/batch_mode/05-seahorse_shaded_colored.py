# -*- coding: utf-8 -*-
"""
===================================
Seahorse shaded and colored example
===================================

This example shows how to create a normal map layer, and link it to a base
color layer to enable scene lighting.
Here a:
    
    - A colored background based on the continuous iteration number is used, and
      the normal map layer is based on "potential estimator".
    - The normal map itself is also output (OpenGL normal map format)

The location is a shallow one in the main Seahorse valley.
"""

import os
import numpy as np

import fractalshades as fs
import fractalshades.models as fsm
import fractalshades.colors as fscolors
from fractalshades.postproc import (
    Postproc_batch,
    Continuous_iter_pp,
    DEM_normal_pp,
    Raw_pp,
)
from fractalshades.colors.layers import (
    Color_layer,
    Bool_layer,
    Normal_map_layer,
    Blinn_lighting
)

def plot(plot_dir):
    """
    Using lighting : a shallow zoom in the Seahorses valley
    Coloring based on continuous iteration + lighting with a normal maps from
    distance estimation method
    """
    # Define the parameters for this calculation
    x = -0.746223962861
    y = -0.0959468433527
    dx = 0.00745
    nx = 2400

    calc_name="mandelbrot"
    colormap = fscolors.cmap_register["legacy"]

    # Run the calculation
    f = fsm.Mandelbrot(plot_dir)
    f.zoom(x=x, y=y, dx=dx, nx=nx, xy_ratio=1.0,
           theta_deg=0., projection="cartesian", antialiasing=False)
    f.base_calc(
        calc_name=calc_name,
        subset=None,
        max_iter=5000,
        M_divergence=100.,
        epsilon_stationnary= 0.001,
    )
    # f.clean_up(calc_name) # keep this line if you want to force recalculation
    f.run()

    # Plot the image
    pp = Postproc_batch(f, calc_name)
    pp.add_postproc("cont_iter", Continuous_iter_pp())
    pp.add_postproc("interior", Raw_pp("stop_reason", func="x != 1."))
    pp.add_postproc("DEM_map", DEM_normal_pp(kind="potential"))

    plotter = fs.Fractal_plotter(pp)   
    plotter.add_layer(Bool_layer("interior", output=False))
    plotter.add_layer(Normal_map_layer("DEM_map", max_slope=60, output=False))
    plotter.add_layer(Color_layer(
            "cont_iter",
            func="np.log(x)",
            colormap=colormap,
            probes_z=[1., 2.],
            probes_kind="absolute",
            output=True
    ))

    plotter["cont_iter"].set_mask(plotter["interior"], mask_color=(0., 0., 0.))
    plotter["DEM_map"].set_mask(plotter["interior"], mask_color=(0., 0., 0.))

    # This is where we define the lighting (here 3 ccolored light sources)
    # and apply the shading
    light = Blinn_lighting(0.2, np.array([1., 1., 1.]))
    light.add_light_source(
        k_diffuse=0.2,
        k_specular=10.,
        shininess=400.,
        angles=(-135., 20.),
        coords=None,
        color=np.array([0.05, 0.05, 1.0]))
    light.add_light_source(
        k_diffuse=0.2,
        k_specular=10.,
        shininess=400.,
        angles=(135., 20.),
        coords=None,
        color=np.array([0.5, 0.5, .4]))
    light.add_light_source(
        k_diffuse=1.3,
        k_specular=0.,
        shininess=0.,
        angles=(90., 40.),
        coords=None,
        color=np.array([1.0, 1.0, 1.0]))
    plotter["cont_iter"].shade(plotter["DEM_map"], light)
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
