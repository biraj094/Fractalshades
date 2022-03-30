# -*- coding: utf-8 -*-
"""
====================================================
19 - "Perpendicular" Burning Ship: hidden Koch curve
====================================================

Another hidden feature in this fractal: here, a reminiscence of Koch curve 
in a very skewed area at a depth of 5.e-42.

Reference:
`fractalshades.models.Perturbation_perpendicular_burning_ship`
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
    DEM_pp,
    Raw_pp,
)
from fractalshades.colors.layers import (
    Color_layer,
    Bool_layer,
    Normal_map_layer,
    Virtual_layer,
    Blinn_lighting,
)


def plot(plot_dir):
    fs.settings.enable_multithreading = True
    fs.settings.inspect_calc = True

    # A simple showcase using perturbation technique
    calc_name = 'test'

    # _1 = 'Zoom parameters'
    x = '-1.701694514129370633991199556392981353373480294378294'
    y = '-0.0000127758408732701278495806991010523157399218726366029'
    dx = '5.427776726359545e-42'
    xy_ratio = 1.8
    theta_deg = 45
    dps = 55
    nx = 2400

    # _1b = 'Skew parameters /!\\ Re-run when modified!'
    has_skew = True
    skew_00 = 0.9588240701305322
    skew_01 = 1.5690686189165641
    skew_10 = -2.725909971344448
    skew_11 = -3.417873931327341

    # _2 = 'Calculation parameters'
    max_iter = 20000

    # _3 = 'Bilinear series parameters'
    eps = 1e-06

    # _4 = 'Plotting parameters: base field'
    base_layer = 'distance_estimation'
    interior_color = (0.6627451181411743, 0.4313725531101227, 0.0)
    colormap = fscolors.Fractal_colormap(
        colors=[
            [1.        , 1.        , 0.        ],
            [0.05098039, 0.03921569, 0.3137255 ],
            [0.10588235, 0.78039217, 0.78039217],
            [0.33333334, 1.        , 1.        ]
        ],
        kinds=['Lch', 'Lch', 'Lch', 'Lch'],
        grad_npts=[ 3,  3, 32, 32],
        grad_funcs=['x', 'x**2', 'x', 'x'],
        extent='mirror'
    )
    invert_cmap = True
    DEM_min = 1e-08
    cmap_z_kind = 'relative'
    zmin = 0.0
    zmax = 1.10

    # _5 = 'Plotting parameters: shading'
    shade_kind = 'glossy'
    gloss_intensity = 100.0
    light_angle_deg = 35.0
    light_color = (1.0, 1.0, 1.0)
    gloss_light_color = (1.0, 1.0, 1.0)

    # Run the calculation
    fractal = fsm.Perturbation_perpendicular_burning_ship(plot_dir)
    # f.clean_up()

    fractal.zoom(precision=dps, x=x, y=y, dx=dx, nx=nx, xy_ratio=xy_ratio,
                 theta_deg=theta_deg, projection="cartesian", antialiasing=False,
                 has_skew=has_skew, skew_00=skew_00, skew_01=skew_01,
                 skew_10=skew_10, skew_11=skew_11
            )

    fractal.calc_std_div(
        calc_name=calc_name,
        subset=None,
        max_iter=max_iter,
        M_divergence=1.e3,
        BLA_params={"eps": eps},
    )

    if fractal.res_available():
        print("RES AVAILABLE, no compute")
    else:
        print("RES NOT AVAILABLE, clean-up")
        fractal.clean_up(calc_name)

    fractal.run()

    pp = Postproc_batch(fractal, calc_name)
    
    if base_layer == "continuous_iter":
        pp.add_postproc(base_layer, Continuous_iter_pp())
    elif base_layer == "distance_estimation":
        pp.add_postproc("continuous_iter", Continuous_iter_pp())
        pp.add_postproc(base_layer, DEM_pp())

    pp.add_postproc("interior", Raw_pp("stop_reason",
                    func=lambda x: x != 1))
    if shade_kind != "None":
        pp.add_postproc("DEM_map", DEM_normal_pp(kind="potential"))

    plotter = fs.Fractal_plotter(pp)   
    plotter.add_layer(Bool_layer("interior", output=False))

    if shade_kind != "None":
        plotter.add_layer(Normal_map_layer(
            "DEM_map", max_slope=60, output=False
        ))

    if base_layer != 'continuous_iter':
        plotter.add_layer(
            Virtual_layer("continuous_iter", func=None, output=False)
        )

    sign = {False: 1., True: -1.}[invert_cmap]
    if base_layer == 'distance_estimation':
        cmap_func = lambda x: sign * np.where(
           np.isinf(x),
           np.log(DEM_min),
           np.log(np.clip(x, DEM_min, None))
        )
    else:
        cmap_func = lambda x: sign * np.log(x)

    plotter.add_layer(Color_layer(
            base_layer,
            func=cmap_func,
            colormap=colormap,
            probes_z=[zmin, zmax],
            probes_kind=cmap_z_kind,
            output=True))
    plotter[base_layer].set_mask(
        plotter["interior"], mask_color=interior_color
    )
    if shade_kind != "None":
        light = Blinn_lighting(0.6, np.array([1., 1., 1.]))
        light.add_light_source(
            k_diffuse=0.8,
            k_specular=.0,
            shininess=350.,
            angles=(light_angle_deg, 20.),
            coords=None,
            color=np.array(light_color))

        if shade_kind == "glossy":
            light.add_light_source(
                k_diffuse=0.2,
                k_specular=gloss_intensity,
                shininess=400.,
                angles=(light_angle_deg, 20.),
                coords=None,
                color=np.array(gloss_light_color))

        plotter[base_layer].shade(plotter["DEM_map"], light)

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
