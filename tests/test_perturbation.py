# -*- coding: utf-8 -*-
import numpy as np
import unittest
import os
import shutil
import PIL

import fractalshades as fs
import fractalshades.utils as fsutils
import fractalshades.models as fsmodels
import fractalshades.colors as fscolors

import test_config

#def compare_png(ref_file, test_file):
#    ref_image = PIL.Image.open(ref_file)
#    test_image = PIL.Image.open(test_file)
#    
#    root, ext = os.path.splitext(test_file)
#    diff_file = root + ".diff" + ext
#    diff_image = PIL.ImageChops.difference(ref_image, test_image)
#    diff_image.save(diff_file)
#    errors = np.asarray(diff_image) / 255.
#    return np.mean(errors)


class Test_Perturbation_mandelbrot(unittest.TestCase):
        
    def setUp(self):
        image_dir = os.path.join(test_config.test_dir, "_images_comparison")

        fsutils.mkdir_p(image_dir)
        self.image_dir = image_dir

        image_dir_ref = os.path.join(test_config.test_dir, "images_REF")
        fsutils.mkdir_p(image_dir_ref)
        self.image_dir_ref = image_dir_ref

        purple = np.array([181, 40, 99]) / 255.
        gold = np.array([255, 210, 66]) / 255.

        colors = np.vstack((purple[np.newaxis, :], gold[np.newaxis, :]))
        self.colormap = fscolors.Fractal_colormap(kinds="Lch", colors=colors,
             grad_npts=200, grad_funcs="x", extent="mirror")

#        color_gradient = fscolors.Color_tools.Lch_gradient(purple, gold,  200)
#        self.colormap = fscolors.Fractal_colormap(color_gradient)
#        self.colormap.extent = "mirror"

    @test_config.no_stdout
    def test_M2_E20(self):
        """
        Testing all datatype options, 5e-20 test case."""
        # TODO: KNOWN fail: ("Xrange", np.complex128) 
        x, y = "-1.74928893611435556407228", "0."
        dx = "5.e-20"
        precision = 30
        nx = 600
        test_name = self.test_M2_E20.__name__
        #with tests.suppress_stdout():
#        for complex_type in [np.complex64, np.complex128,
#                ("Xrange", np.complex64), ("Xrange", np.complex128)]:
        for complex_type in [np.complex128]: #, ("Xrange", np.complex128)]:
            if type(complex_type) is tuple:
                _, base_complex_type = complex_type
                prefix = "Xr_" + np.dtype(base_complex_type).name
            else:
                prefix = np.dtype(complex_type).name 
            with self.subTest(complex_type=complex_type):


                test_file = self.make_M2_img(x, y, dx, precision, nx,
                                             complex_type, test_name, prefix)
                ref_file = os.path.join(self.image_dir_ref, test_name + ".png")
                err = test_config.compare_png(ref_file, test_file)
                self.assertTrue(err < 0.01)

    # @test_config.no_stdout
    def test_M2_int_E11(self):
        """
        Testing interior detection, 5e-12 test case.
        """
        x, y = "-1.74920463345912691e+00", "-2.8684660237361114e-04"
        dx = "5e-12"
        precision = 16
        nx = 600
        test_name = self.test_M2_int_E11.__name__
        complex_type = np.complex128

        for SA_params in [{"cutdeg": 64, "cutdeg_glitch": 8}, None]:
            with self.subTest(SA_params=SA_params):
                if SA_params is None:
                    prefix = "noSA"
                else:
                    prefix = str(SA_params["cutdeg"]) + "SA"
                test_file = self.make_M2_img(x, y, dx, precision, nx,
                    complex_type, test_name, prefix, interior_detect=True,
                    mask_codes=[2], SA_params=SA_params)
                ref_file = os.path.join(self.image_dir_ref, test_name + ".png")
                err = test_config.compare_png(ref_file, test_file)
                if SA_params is not None:
                    self.assertTrue(err < 0.05)
                else:
                    self.assertTrue(err < 0.1)


    @test_config.no_stdout
    def test_M2_antialias_E0(self):
        """
        Testing field lines, and antialiasing. Full Mandelbrot
        """
        with self.subTest(zoom=1):
            x, y = "-0.75", "0."
            dx = "5.e0"
            precision = 10
            nx = 1600
            test_name = self.test_M2_antialias_E0.__name__
            complex_type = np.complex128
            prefix = "antialiasing"
    
            gold = np.array([255, 210, 66]) / 255.
            black = np.array([0, 0, 0]) / 255.
            colors = np.vstack((gold[np.newaxis, :], black[np.newaxis, :]))
            colormap = fscolors.Fractal_colormap(kinds="Lch", colors=colors,
             grad_npts=200, grad_funcs="x", extent="clip")
            
            
#            colors1 = np.vstack((gold[np.newaxis, :]))
#            colors2 = np.vstack((black[np.newaxis, :]))
#            colormap = fscolors.Fractal_colormap(kinds="Lch", colors1=colors1,
#                colors2=colors2, n=200, funcs=None, extent="clip")
            
            
    #        color_gradient = fscolors.Color_tools.Lch_gradient(gold, black, 200)
    #        colormap = fscolors.Fractal_colormap(color_gradient)
    
            test_file = self.make_M2_img(x, y, dx, precision, nx,
                complex_type, test_name, prefix, interior_detect=True,
                mask_codes=[2], antialiasing=True, colormap=colormap,
                probes_val=[0., 0.05], grey_layer_key=
                        ("field_lines", {"n_iter": 10, "swirl": 1.}),
                blur_ranges=[[0.8, 0.95, 1.0]], hardness=0.9, intensity=0.8)
            ref_file = os.path.join(self.image_dir_ref, test_name + ".png")
            err = test_config.compare_png(ref_file, test_file)
            self.assertTrue(err < 0.02)
            
        with self.subTest(zoom=2):
            x, y = "-0.1", "0.975"
            dx = "0.8e0"
            prefix = "antialiasing_2"
            test_file = self.make_M2_img(x, y, dx, precision, nx,
                complex_type, test_name, prefix, interior_detect=True,
                mask_codes=[2], antialiasing=True, colormap=colormap,
                probes_val=[0., 0.1], grey_layer_key=("field_lines", {}),
                blur_ranges=[[0.8, 0.95, 1.0]], hardness=0.9, intensity=0.8)
            ref_file = os.path.join(self.image_dir_ref, test_name + "_2.png")
            err = test_config.compare_png(ref_file, test_file)
            self.assertTrue(err < 0.01)


    @test_config.no_stdout
    def test_glitch_divref(self):
        """
        Testing based on fail2 test case
        """
        x = '-1.36768994867991128'
        y = '0.00949048853859240532'
        dx = '2.477633848347765e-8'
        precision = 18
        nx = 1600
        test_name = self.test_glitch_divref.__name__
        prefix="fail2"

        black = np.array([0, 0, 0]) / 255.
        citrus2 = np.array([103, 189, 0]) / 255.
        
        colors = np.vstack((citrus2[np.newaxis, :], black[np.newaxis, :]))
        colormap = fscolors.Fractal_colormap(kinds="Lch", colors=colors,
             grad_npts=200, grad_funcs="x", extent="mirror")

#        colors1 = np.vstack((citrus2[np.newaxis, :]))
#        colors2 = np.vstack((black[np.newaxis, :]))
#        colormap = fscolors.Fractal_colormap(kinds="Lch", colors1=colors1,
#            colors2=colors2, n=200, funcs=None, extent="mirror")
        

        grey_layer_key = ("DEM_shade", {"kind": "potential",
                            "theta_LS": 30.,
                            "phi_LS": 70.,
                            "shininess": 300.,
                            "ratio_specular": 15000.})
    
        test_file = self.make_M2_img(x, y, dx, precision, nx,
            np.complex128, test_name, prefix, interior_detect=True,
            mask_codes=[2], antialiasing=True, colormap=colormap,
            probes_val=[0.25, 0.75], grey_layer_key=grey_layer_key,
            blur_ranges=[[0.8, 0.95, 1.0]], hardness=0.9, intensity=0.8,
            glitch_max_attempt=10)
        ref_file = os.path.join(self.image_dir_ref, test_name + ".png")
        err = test_config.compare_png(ref_file, test_file)
        self.assertTrue(err < 0.02)

    @test_config.no_stdout
    def test_glitch_dyn(self):
        """
        Testing based on Dinkydau "Flake" test case
        """
        x = "-1.99996619445037030418434688506350579675531241540724851511761922944801584242342684381376129778868913812287046406560949864353810575744772166485672496092803920095332"
        y = "0.00000000000000000000000000000000030013824367909383240724973039775924987346831190773335270174257280120474975614823581185647299288414075519224186504978181625478529"
        dx = "1.8e-157"
        precision = 200

        nx = 1600
        test_name = self.test_glitch_dyn.__name__
        prefix="flake"

        black = np.array([0, 0, 0]) / 255.
        purple = np.array([181, 40, 99]) / 255.

#        colors1 = np.vstack((black[np.newaxis, :]))
#        colors2 = np.vstack((purple[np.newaxis, :]))
#        colormap = fscolors.Fractal_colormap(kinds="Lab", colors1=colors1,
#            colors2=colors2, n=200, funcs=None, extent="mirror")
        
        colors = np.vstack((black[np.newaxis, :], purple[np.newaxis, :]))
        colormap = fscolors.Fractal_colormap(kinds="Lab", colors=colors,
             grad_npts=200, grad_funcs="x", extent="mirror")

        grey_layer_key = ("DEM_shade", {"kind": "potential",
                            "theta_LS": 30.,
                            "phi_LS": 70.,
                            "shininess": 300.,
                            "ratio_specular": 15000.})
        SA_params={"cutdeg": 8,
                   "cutdeg_glitch": 8,
                   "SA_err": 1.e-4,
                   "use_Taylor_shift": True}

        test_file = self.make_M2_img(x, y, dx, precision, nx,
            np.complex128, test_name, prefix, interior_detect=True,
            mask_codes=[2], antialiasing=True, colormap=colormap,
            probes_val=[0.3, 0.5], grey_layer_key=grey_layer_key,
            blur_ranges=[[0.98, 0.995, 1.0]], hardness=0.9, intensity=0.8,
            glitch_max_attempt=10, xy_ratio=0.5,SA_params=SA_params)
        ref_file = os.path.join(self.image_dir_ref, test_name + ".png")
        err = test_config.compare_png(ref_file, test_file)
        self.assertTrue(err < 0.02)

    @test_config.no_stdout
    def make_M2_img(self, x, y, dx, precision, nx, complex_type, test_name,
                    prefix, interior_detect=False, mask_codes=[3, 4], 
                    SA_params={"cutdeg": 64, "cutdeg_glitch": 8},
                    antialiasing=False, colormap=None, hardness=0.75,
                    intensity=0.95,
                    probes_val=[0., 0.25], blur_ranges=[],
                    grey_layer_key=None,
                    glitch_max_attempt=1, xy_ratio=1.0):
        """
        
        """
        test_dir = os.path.join(self.image_dir, test_name)

        mandelbrot = fsmodels.Perturbation_mandelbrot(test_dir)
        mandelbrot.zoom(
             precision=precision,
             x=x,
             y=y,
             dx=dx,
             nx=nx,
             xy_ratio=xy_ratio,
             theta_deg=0.,
             projection="cartesian",
             antialiasing=antialiasing)

        mandelbrot.prepare_calc(
            kind="calc_std_div",
            complex_type=complex_type,
            file_prefix=prefix,
            subset=None,
            max_iter=50000,
            M_divergence=1.e3,
            epsilon_stationnary=1.e-3,
            pc_threshold=0.1,
            SA_params=SA_params,
            glitch_eps=1.e-6,
            interior_detect=interior_detect,
            glitch_max_attempt=glitch_max_attempt)

        mandelbrot.run()

        mask = fs.Fractal_Data_array(mandelbrot, file_prefix=prefix,
            postproc_keys=('stop_reason', lambda x: np.isin(x, mask_codes)),
            mode="r+raw")

        potential = ("potential", {})
        if colormap is None:
            colormap = self.colormap
        if grey_layer_key is None:
            grey_layer_key = ("DEM_shade", 
                {"kind": "potential", "theta_LS": 50., "phi_LS": 40.,
                 "shininess": 40., "ratio_specular": 8.})

        plotter = fs.Fractal_plotter(
            fractal=mandelbrot,
            base_data_key=potential,
            base_data_prefix=prefix,
            base_data_function=lambda x:x,
            colormap=colormap,
            probes_val=probes_val,
            probes_kind="qt",
            mask=mask)

        plotter.add_grey_layer(
                postproc_key=grey_layer_key,
                blur_ranges=blur_ranges,
                hardness=hardness,
                intensity=intensity,
                shade_type={"Lch": 1.0, "overlay": 0., "pegtop": 4.})

        plotter.plot(prefix, mask_color=(0., 0., 1.))
        new_file = os.path.join(self.image_dir,
                                test_name + "_" + prefix + ".png")
        shutil.move(os.path.join(test_dir, prefix + ".png"), new_file)
        shutil.rmtree(test_dir)
        return new_file


if __name__ == "__main__":
    full_test = False
    runner = unittest.TextTestRunner(verbosity=2)
    if full_test:
        runner.run(test_config.suite([Test_Perturbation_mandelbrot]))
    else:
        suite = unittest.TestSuite()
        suite.addTest(Test_Perturbation_mandelbrot("test_M2_antialias_E0"))
        runner.run(suite)
