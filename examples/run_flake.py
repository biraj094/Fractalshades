# -*- coding: utf-8 -*-
import numpy as np

import fractalshades as fs
import fractalshades.models as fsm
import fractalshades.settings as settings
import fractalshades.colors as fscolors

def plot():
    """
    Example plot of "Dinkydau flake" location, classic test case for 
    perturbation technique and glitch correction.
    """
    directory = "./flake"

    # Dinkydau flake
    # http://www.fractalforums.com/announcements-and-news/pertubation-theory-glitches-improvement/msg73027/#msg73027
    # Ball method 1 found period: 7884
    x = "-1.99996619445037030418434688506350579675531241540724851511761922944801584242342684381376129778868913812287046406560949864353810575744772166485672496092803920095332"
    y = "0.00000000000000000000000000000000030013824367909383240724973039775924987346831190773335270174257280120474975614823581185647299288414075519224186504978181625478529"
    dx = "1.8e-157"
    precision = 200

    # Set to True if you only want to rerun the post-processing part
    settings.skip_calc = False
    # Set to True to enable multi-processing
    settings.enable_multiprocessing = True

    nx = 3200
    xy_ratio = 0.5
    theta_deg = 0.
    complex_type = np.complex128

    mandelbrot = fsm.Perturbation_mandelbrot(directory)
    mandelbrot.zoom(
            precision=precision,
            x=x,
            y=y,
            dx=dx,
            nx=nx,
            xy_ratio=xy_ratio,
            theta_deg=theta_deg,
            projection="cartesian",
            antialiasing=False)

    mandelbrot.calc_std_div(
            complex_type=complex_type,
            file_prefix="dev",
            subset=None,
            max_iter=50000,
            M_divergence=1.e3,
            epsilon_stationnary=1.e-3,
            pc_threshold=0.1,
            SA_params={"cutdeg": 8,
                       "cutdeg_glitch": 8,
                       "SA_err": 1.e-4,
                       "use_Taylor_shift": True},
            glitch_eps=1.e-6,
            interior_detect=False,
            glitch_max_attempt=20)

    mandelbrot.run()

    glitched = fs.Fractal_Data_array(mandelbrot, file_prefix="dev",
                postproc_keys=('stop_reason', lambda x: x == 3), mode="r+raw")
    potential_data_key = ("potential", {})


    citrus2 = np.array([103, 189, 0]) / 255.
    citrus_white = np.array([252, 251, 226]) / 255.

    wheat1 = np.array([244, 235, 158]) / 255.
    wheat2 = np.array([246, 207, 106]) / 255.
    wheat3 = np.array([191, 156, 96]) / 255.

    lavender1 = np.array([154, 121, 144]) / 255.
    lavender2 = np.array([140, 94, 134]) / 255.
    lavender3 = np.array([18, 16, 58]) / 255.
    

    def wave(x):
        return 0.5 + (0.4 * (x - 0.5) - 0.6 * 0.5 * np.cos(x * np.pi * 3.))



    colormap = fscolors.Fractal_colormap(
        kinds="Lch",
        colors1=np.vstack((citrus_white, wheat2, wheat1, wheat2, wheat1, wheat2, wheat3,
                 wheat1, lavender2, wheat1, wheat2, wheat3, wheat1, lavender2, wheat1,
                 lavender3, lavender2, lavender3, lavender1, lavender3, 
                 lavender2)),
        colors2=None,
        n = 100,
        funcs= lambda x: wave(x),
        extent="mirror")
        
            


#    colormap.extent = "mirror" #"repeat"

    plotter = fs.Fractal_plotter(
        fractal=mandelbrot,
        base_data_key=potential_data_key, # potential_data_key, #glitch_sort_key,
        base_data_prefix="dev",
        base_data_function=lambda x:x,# np.sin(x*0.0001),
        colormap=colormap,
        probes_val=np.linspace(0., 1., 22) **0.2,# 200. + 200, #* 428  - 00.,#[0., 0.5, 1.], #phi * k * 2. + k * np.array([0., 1., 1.5, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0]) / 3.5,
        probes_kind="qt",#"z", "qt"
        mask=glitched)
    
    
    #plotter.add_calculation_layer(postproc_key=potential_data_key)
    
    layer1_key = ("DEM_shade", {"kind": "potential",
                                "theta_LS": 30.,
                                "phi_LS": 50.,
                                "shininess": 30.,
                                "ratio_specular": 15000.})
    plotter.add_grey_layer(postproc_key=layer1_key, intensity=0.75, 
                         blur_ranges=[],#[[0.99, 0.999, 1.0]],
                        disp_layer=False, #skewness=0.2,
                         normalized=False, hardness=0.35,  
            skewness=0.0, shade_type={"Lch": 1.0, "overlay": 1., "pegtop": 4.})
    
    layer2_key = ("field_lines", {})
    plotter.add_grey_layer(postproc_key=layer2_key,
                         hardness=1.0, intensity=0.68, skewness=0.4,
                         blur_ranges=[[0.50, 0.60, 1.0]], 
                         shade_type={"Lch": 0., "overlay": 2., "pegtop": 1.}) 


    plotter.plot("dev", mask_color=(0., 0., 1.))

if __name__ == "__main__":
    plot()
