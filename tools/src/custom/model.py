#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np

from modules.math import Math
from modules.base import Model

"""Add your defined classes to this dictionary with a unique name
 to use it with PolarisTools.
"""
def update_model_dict(dictionary):
    model_dict = {
        'cube': Cube,
        'filament': Filament,
        'galaxy': Galaxy,
        'mhd_bastian': MhdBastian,
        'mhd_binary': MhdFlock,
        'gg_tau_disk': GGTauDisk,
        'gg_cs_disk': GGTauCSDisk,
        'hd97048': HD97048,
        'pp_disk': ProtoplanetaryDisk,
        'test': TestModel,
        'multi_disk': MultiDisk,
        'custom': CustomModel,
    }
    dictionary.update(model_dict)


class CustomModel(Model):
    """Change this to the model you want to use.
    """

    def __init__(self):
        """Initialisation of the model parameters.
        """
        Model.__init__(self)

        # Set parameters of the custom model (see parent Model class for all available options)
        self.parameter['distance'] = 140.0 * self.math.const['pc']
        self.parameter['grid_type'] = 'spherical'
        self.parameter['inner_radius'] = 0.1 * self.math.const['au']
        self.parameter['outer_radius'] = 100.0 * self.math.const['au']
        self.parameter['gas_mass'] = 1e-2 * self.math.const['M_sun']
        # Define which other choise are default for this model
        self.parameter['background_source'] = 'bg_plane'
        self.parameter['stellar_source'] = 't_tauri'
        self.parameter['dust_composition'] = 'mrn'
        self.parameter['gas_species'] = 'oh'
        self.parameter['detector'] = 'cartesian'

    def use_extra_parameter(self, extra_parameter):
        """Use this function to set model parameter with the extra parameters.
        """
        # Use extra_parameter to adjust the model without changing the model.py file


    def gas_density_distribution(self):
        """Define here your routine to calculate the density at a given position
        in the model space.

        Notes:
            Use 'self.position' to calculate the quantity depending on position.

            Define also the following routines if necessary:
                dust_density_distribution(self), gas_temperature(self),
                dust_temperature(self), velocity_field(self), magnetic_field(self),
                dust_id(self), dust_min_size(self), dust_max_size(self)

            xyz_density_distribution can return a density or 2D list of densities.
                - The first dimension is used to define multiple density distributions
                    for different dust compositions (see CustomDust in dust.py for explanation)
                - With the second dimension, multiple regions of the density distribution
                    of the same dust composition can be normalized individually to different total masses.
                - The self.parameter['gas_mass'] needs to have the same dimension and size as the return of this

        Returns:
            float: Gas density at a given position.
        """
        gas_density = 1.0
        # Or a function that depends on the position!
        # See other models to find prewritten distributions (shakura & sunyaev, ...)
        return gas_density


class Cube(Model):
    """A cube model with constant density
    """

    def __init__(self):
        """Initialisation of the model parameters.
        """
        Model.__init__(self)

        #: Set parameters of the sphere model
        self.parameter['distance'] = 140.0 * self.math.const['pc']
        self.parameter['gas_mass'] = 1e-6 * self.math.const['M_sun']
        self.octree_parameter['sidelength'] = 200.0 * self.math.const['au']
        self.parameter['stellar_source'] = 't_tauri'
        self.parameter['dust_composition'] = 'mrn_oblate'
        self.parameter['detector'] = 'cartesian'

    def dust_temperature(self):
        """Calculates the dust temperature at a given position.

        Returns:
            float: Dust temperature at a given position.
        """
        dust_temperature = 10.
        return dust_temperature

    def gas_temperature(self):
        """Calculates the dust temperature at a given position.

        Returns:
            float: Dust temperature at a given position.
        """
        gas_temperature = 10.
        return gas_temperature

    def gas_density_distribution(self):
        """Calculates the gas density at a given position.

        Returns:
            float: Gas density at a given position.
        """
        #gas_density = self.math.bonor_ebert_density(self.position, outer_radius=self.spherical_parameter['outer_radius'],
        #                                        truncation_radius=1 * self.math.const['au'])
        gas_density = 1.0
        return gas_density

    def magnetic_field(self):
        """Calculates the magnetic field strength at a given position.

        Returns:
            List[float, float, float]: Magnetic field strength at the given
            position.
        """
        return self.math.simple_mag_field(mag_field_strength=1e-10, axis='z')

class Galaxy(Model):
    """A galaxy model.
    """

    def __init__(self):
        """Initialisation of the model parameters.
        """
        Model.__init__(self)

        #: Set parameters of the Bok globule model
        self.parameter['distance'] = 100.0 * self.math.const['pc']
        self.parameter['dust_composition'] = 'mrn'
        self.parameter['detector'] = 'cartesian'
        # Density factor to convert MHD simulation from g/cm^3 to kg/m^3
        self.conv_parameter['conv_dens'] = 6195019.204559535
        # Lengths factor to convert MHD simulation from cm to m
        self.conv_parameter['conv_len'] = 1e-2
        # Magnetic field factor to convert MHD simulation from Gauss to Tesla
        self.conv_parameter['conv_mag'] = 1e-4
        # Velocity factor to convert MHD simulation from cm/s to m/s
        self.conv_parameter['conv_vel'] = 1e-2


class TestModel(Model):
    """The test grid model.
    """

    def __init__(self):
        """Initialisation of the model parameters.
        """
        Model.__init__(self)

        #: Set parameters of the disk model
        self.parameter['distance'] = 140.0 * self.math.const['pc']
        self.parameter['inner_radius'] = 0.1 * self.math.const['au']
        self.parameter['outer_radius'] = 100.0 * self.math.const['au']
        self.parameter['grid_type'] = 'spherical'
        self.spherical_parameter['n_r'] = 100
        self.spherical_parameter['n_th'] = 91
        self.spherical_parameter['n_ph'] = 1
        self.spherical_parameter['sf_r'] = 1.03
        #self.parameter['gas_mass'] = [[1.22138e-07 * self.math.const['M_sun']],
        #                              [8.77862e-07 * self.math.const['M_sun']]]
        self.parameter['gas_mass'] = [[1e-6 * self.math.const['M_sun']],
                                      [1e-5 * self.math.const['M_sun']]]
        self.parameter['stellar_source'] = 't_tauri'
        self.parameter['dust_composition'] = 'silicate'
        self.parameter['detector'] = 'cartesian'
        self.parameter['variable_dust'] = True
        self.parameter['variable_size_limits'] = True

    def gas_density_distribution(self):
        """Calculates the gas density at a given position.

        Returns:
            float: Gas density at a given position.
        """
        gas_density1 = self.math.sphere_density(self.position,
            inner_radius=self.parameter['inner_radius'],
            outer_radius=self.parameter['outer_radius'])
        gas_density2 = self.math.sphere_density(self.position,
            inner_radius=100. * self.parameter['inner_radius'],
            outer_radius=self.parameter['outer_radius'])
        #return [[gas_density1], [gas_density2]]
        if np.linalg.norm(self.position) < 0.5 * self.spherical_parameter['outer_radius']:
            return [[gas_density1], [0]]
        else:
            return [[0], [gas_density1]]

    def dust_id(self):
        """Calculates the dust ID depending on the position in the grid.
        The dust ID is related to the dust composition. With this, one can
        change the dust properties inside the disk.

        Returns:
            int: dust ID.
        """
        if np.linalg.norm(self.position) < 0.5 * self.spherical_parameter['outer_radius']:
            dust_id = 0
        else:
            dust_id = 1
        return dust_id

    def dust_min_size(self):
        """Calculates the minimum dust grain size depending on the position in the grid.
        This overwrites the global minimum grain size, but has no effect if it is smaller than it.

        Returns:
            float: minimum grain size
        """
        dust_min_size = 5e-9
        return dust_min_size

    def dust_max_size(self):
        """Calculates the maximum dust grain size depending on the position in the grid.
        This overwrites the global maximum grain size, but has no effect if it is larger than it.

        Returns:
            float: maximum grain size
        """
        if np.linalg.norm(self.position) < 0.5 * self.spherical_parameter['outer_radius']:
            dust_max_size = 0.25e-6
        else:
            dust_max_size = 0.001
        return dust_max_size


class Filament(Model):
    """A sphere model with constant density
    """

    def __init__(self):
        """Initialisation of the model parameters.
        """
        Model.__init__(self)

        #: Set parameters of the sphere model
        self.parameter['distance'] = 100.0 * self.math.const['pc']
        self.octree_parameter['sidelength'] = 2. * 4.7305e+17
        self.parameter['detector'] = 'cartesian'
        # Density factor to convert MHD simulation from g/cm^3 to kg/m^3
        self.conv_parameter['conv_dens'] = 1e3
        # Lengths factor to convert MHD simulation from cm to m
        self.conv_parameter['conv_len'] = 1e-2
        # Magnetic field factor to convert MHD simulation from Gauss to Tesla
        self.conv_parameter['conv_mag'] = 1e-4
        # Velocity factor to convert MHD simulation from cm/s to m/s
        self.conv_parameter['conv_vel'] = 1e-2


class MhdBastian(Model):
    """A MHD simulation model. Made to import MHD simulation grids with
    all needed conversion factors.
    """

    def __init__(self):
        """Initialisation of the model parameters.
        """
        Model.__init__(self)

        #: Set parameters of the MHD-simulation model
        self.parameter['distance'] = 100.0 * self.math.const['pc']
        self.octree_parameter['sidelength'] = 2. * 0.0125 * self.math.const['pc']
        # self.octree_parameter['sidelength'] = 2. * 0.5 * self.math.const['pc']
        # self.octree_parameter['sidelength'] = 2. * 2.9167 * self.math.const['pc']
        self.parameter['detector'] = 'cartesian'
        # Density factor to convert MHD simulation from g/cm^3 to kg/m^3
        self.conv_parameter['conv_dens'] = 1e3
        # Lengths factor to convert MHD simulation from cm to m
        self.conv_parameter['conv_len'] = 1e-2
        # Magnetic field factor to convert MHD simulation from Gauss to Tesla
        self.conv_parameter['conv_mag'] = 1e-4
        # Velocity factor to convert MHD simulation from cm/s to m/s
        self.conv_parameter['conv_vel'] = 1e-2


class MhdFlock(Model):
    """The disk model with the Shakura and Sunyaev disk density profile.
    """

    def __init__(self):
        """Initialisation of the model parameters.

        Notes:
            Shakura and Sunyaev (1973)
            Link: http://adsabs.harvard.edu/abs/1973A&A....24..337S
        """
        Model.__init__(self)

        #: Set parameters of the disk model
        self.parameter['distance'] = 100.0 * self.math.const['pc']
        self.parameter['inner_radius'] = 20.0 * self.math.const['au']
        self.parameter['outer_radius'] = 100.0 * self.math.const['au']
        self.parameter['grid_type'] = 'spherical'
        self.spherical_parameter['n_r'] = 256
        self.spherical_parameter['n_th'] = 562
        self.spherical_parameter['n_ph'] = 512
        self.spherical_parameter['sf_r'] = 1.0063066707156978
        self.parameter['gas_mass'] = 1e-2 * self.math.const['M_sun']
        self.parameter['external_input_name'] = 350
        self.parameter['vel_is_speed_of_sound'] = True
        self.parameter['stellar_source'] = 'binary'
        self.parameter['dust_composition'] = 'mrn_oblate'
        self.parameter['detector'] = 'cartesian'


class GGTauDisk(Model):
    """The disk model for GG Tau.

    Notes:
        Based on Duchêne et al. 2004
    """

    def __init__(self):
        """Initialisation of the model parameters.

        Notes:
            - Shakura and Sunyaev 1973 (Disk density distribution)
                "http://adsabs.harvard.edu/abs/1973A&A....24..337S"
            - Duchêne et. al 2004 (Total dust mass and size constaints)
                "https://e-reports-ext.llnl.gov/pdf/304661.pdf"
        """
        Model.__init__(self)

        #: Set parameters of the disk model
        self.parameter['distance'] = 140. * self.math.const['pc']
        self.parameter['grid_type'] = 'spherical'
        self.parameter['gas_mass'] = 0.0013 * self.math.const['M_sun'] / self.parameter['mass_fraction']
        self.parameter['stellar_source'] = 'gg_tau_stars'
        self.parameter['dust_composition'] = 'silicate'
        self.parameter['detector'] = 'gg_tau'

        # Parameter for the spherical grid
        self.parameter['inner_radius'] = 10. * self.math.const['au']  # 180 AU
        self.parameter['outer_radius'] = 300. * self.math.const['au']
        self.spherical_parameter['n_th'] = 91
        self.spherical_parameter['n_ph'] = 720
        self.spherical_parameter['sf_th'] = 1
        # --- own radial spacing of cells
        self.spherical_parameter['sf_r'] = 0
        list_cs_disks = np.linspace(10., 30., 200)
        list_cb_disk = self.math.exp_list(180., 300., 100, 1.03)
        full_r_list = np.hstack((list_cs_disks, 140, list_cb_disk)).ravel()
        self.spherical_parameter['radius_list'] = np.multiply(full_r_list, self.math.const['au'])

        # Parameter for the density distribution
        self.beta = 1.05
        surf_dens_exp = -1.7
        self.alpha = -surf_dens_exp + self.beta
        self.cut_off = 2. * self.math.const['au']  # 2 AU
        # Position angle of the stars (Ab12 is Ab1 and Ab2)
        self.angle_Aa = 3. / 2. * np.pi
        self.angle_Ab12 = self.angle_Aa + np.pi
        # Position angle of the stars (Ab12 is Ab1 and Ab2)
        self.a_Aab = 36. / 2. * self.math.const['au']
        self.a_Ab12 = 4.5 / 2. * self.math.const['au']
        self.a_planet = 260. * self.math.const['au']
        # Extend of the circumstellar disks around the stars
        self.inner_radius = 0.15 * self.math.const['au']
        self.outer_radius_Aa = 7. * self.math.const['au']
        self.outer_radius_Ab1 = 2. * self.math.const['au']
        self.outer_radius_Ab2 = 2. * self.math.const['au']
        # Density factors of the circumstellar disk around Aa, Ab1 and Ab2
        # self.factor = 0.9818414311641336
        self.factor = 1.082494125545485 * 1.0079425074596415
        # self.factor_Aa = 24.94246485180343
        self.factor_Aa = 2.494246485180343 * 0.5061500961721862
        # self.factor_Ab = 25.762784158640205
        self.factor_Ab = 0.25762784158640205 * 0.32974081598463123
        # Init
        self.disk_density = 0
        self.disk_density_Aa = 0
        self.disk_density_Ab1 = 0
        self.disk_density_Ab2 = 0

    def gas_density_distribution(self):
        """Calculates the gas density at a given position.

        Returns:
            float: Gas density at a given position.
        """
        radius_cy = np.sqrt(self.position[0] ** 2 + self.position[1] ** 2)
        radius_cy_disk_Aa = np.sqrt((self.position[0]) ** 2 +
                                    (self.position[1] - self.a_Aab * np.sin(self.angle_Aa)) ** 2)
        radius_cy_disk_Ab1 = np.sqrt((self.position[0] + self.a_Ab12) ** 2 +
                                     (self.position[1] - self.a_Aab * np.sin(self.angle_Ab12)) ** 2)
        radius_cy_disk_Ab2 = np.sqrt((self.position[0] - self.a_Ab12) ** 2 +
                                     (self.position[1] - self.a_Aab * np.sin(self.angle_Ab12)) ** 2)
        planet_tunnel = np.sqrt((radius_cy - self.a_planet) ** 2 + self.position[2] ** 2)
        # Init density values with zero
        pos_Aa = self.math.rotate_coord_system([radius_cy_disk_Aa, 0, self.position[2]],
            rotation_axis=[0, 1, 0], rotation_angle=(20. / 180. * np.pi))
        disk_density_Aa = self.factor_Aa * self.math.default_disk_density(pos_Aa, outer_radius=self.outer_radius_Aa,
            inner_radius=self.inner_radius, ref_scale_height = 20. * self.math.const['au'])
        pos_Ab1 = self.math.rotate_coord_system([radius_cy_disk_Ab1, 0, self.position[2]],
            rotation_axis=[0, 1, 0], rotation_angle=(20. / 180. * np.pi))
        disk_density_Ab1 = self.factor_Ab * self.math.default_disk_density(pos_Ab1, outer_radius=self.outer_radius_Ab1,
            inner_radius=self.inner_radius, ref_scale_height = 20. * self.math.const['au'])
        pos_Ab2 = self.math.rotate_coord_system([radius_cy_disk_Ab2, 0, self.position[2]],
            rotation_axis=[0, 1, 0], rotation_angle=-(20. / 180. * np.pi))
        disk_density_Ab2 = self.factor_Ab * self.math.default_disk_density(pos_Ab2, outer_radius=self.outer_radius_Ab2,
            inner_radius=self.inner_radius, ref_scale_height = 20. * self.math.const['au'])
        disk_density = self.math.default_disk_density(self.position, outer_radius=260. * self.math.const['au'],
            inner_radius=180. * self.math.const['au'], ref_scale_height=32. * self.math.const['au'],
            ref_radius=180. * self.math.const['au'], alpha=self.alpha, beta=self.beta)
        if radius_cy < 190. * self.math.const['au']:
            disk_density *= np.exp(-0.5 * ((190. * self.math.const['au'] - radius_cy)
                                           / self.cut_off) ** 2)
        #if planet_tunnel < 35. * self.math.const['au']:
        #    disk_density /= 100.

        return (self.factor * disk_density) + disk_density_Aa + \
            disk_density_Ab1 + disk_density_Ab2


class GGTauCSDisk(Model):
    """The disk model with the Shakura and Sunyaev disk density profile.
    """

    def __init__(self):
        """Initialisation of the model parameters.

        Notes:
            Shakura and Sunyaev (1973)
            Link: http://adsabs.harvard.edu/abs/1973A&A....24..337S
        """
        Model.__init__(self)

        #: Set parameters of the disk model
        self.parameter['distance'] = 140. * self.math.const['pc']
        self.parameter['grid_type'] = 'spherical'
        self.parameter['inner_radius'] = 0.07 * self.math.const['au']
        self.parameter['outer_radius'] = 2. * self.math.const['au']  # 2 AU / 7 AU
        self.parameter['grid_type'] = 'spherical'
        self.spherical_parameter['n_r'] = 100
        self.spherical_parameter['n_th'] = 91
        self.spherical_parameter['sf_th'] = 1
        self.spherical_parameter['n_ph'] = 1
        self.spherical_parameter['sf_r'] = 1.03
        # GG Tau Aa M_disk = 0.01
        # GG Tau Ab1 and Ab2 M_disk = 0.0015 each
        self.parameter['gas_mass'] = 0.0015 * self.math.const['M_sun']
        self.parameter['stellar_source'] = 't_tauri'
        self.parameter['dust_composition'] = 'silicate'
        self.parameter['detector'] = 'cartesian'

    def gas_density_distribution(self):
        """Calculates the gas density at a given position.

        Returns:
            float: Gas density at a given position.
        """
        gas_density = self.math.default_disk_density(self.position,
            inner_radius=self.spherical_parameter['inner_radius'],
            outer_radius=self.spherical_parameter['outer_radius'],
            ref_scale_height=20. * self.math.const['au'],
            ref_radius=100. * self.math.const['au'])
        return gas_density


class HD97048(Model):
    """The disk model for HD97048.
    """

    def __init__(self):
        """Initialisation of the model parameters.

        Notes:
            Shakura and Sunyaev (1973)
            Link: http://adsabs.harvard.edu/abs/1973A&A....24..337S
        """
        Model.__init__(self)

        #: Set parameters of the disk model
        self.parameter['distance'] = 185.0 * self.math.const['pc']
        self.parameter['inner_radius'] = 0.3 * self.math.const['au']
        self.parameter['outer_radius'] = 400.0 * self.math.const['au']
        self.parameter['grid_type'] = 'cylindrical'
        # In the case of a spherical grid
        self.spherical_parameter['n_r'] = 300
        self.spherical_parameter['n_th'] = 141
        self.spherical_parameter['n_ph'] = 1
        self.spherical_parameter['sf_r'] = 1.04
        self.spherical_parameter['sf_th'] = 1.0
        # In the case of a cylindrical grid
        self.cylindrical_parameter['n_r'] = 300
        self.cylindrical_parameter['n_z'] = 142
        self.cylindrical_parameter['n_ph'] = 1
        self.cylindrical_parameter['sf_r'] = 1.04
        self.cylindrical_parameter['sf_z'] = -1
        # Define the used sources, dust composition and gas species
        self.parameter['detector'] = 'hd97048'
        self.parameter['stellar_source'] = 'hd97048'
        self.parameter['dust_composition'] = 'olivine_pah'
        # Use multiple dust compositionas depending on the region in the grid
        self.parameter['variable_dust'] = True
    
    def use_extra_parameter(self, extra_parameter):
        """Use this function to set model parameter with the extra parameters.
        """
        # Use the continuum or ring version of the model and set PAH to silicate ration
        if len(extra_parameter) == 2:
            self.use_cont = bool(int(extra_parameter[0]))
            self.mf_pah = float(extra_parameter[1])
        elif len(extra_parameter) == 1:
            self.use_cont = bool(int(extra_parameter[0]))
            self.mf_pah = 1e-3
        else:
            self.use_cont = False
            self.mf_pah = 1e-3

        # Set the gas density
        if self.use_cont:
            self.parameter['gas_mass'] = np.array([
                    [1e-4, 4e-3, 5e-3, 1e-1, 0], 
                    [0, 0, 0, 0, 0.2*self.mf_pah],
                    [0, 0, 0, 0, 0.8*self.mf_pah]
                ]) * self.math.const['M_sun']
        else:
            self.parameter['gas_mass'] = np.array([
                    [1e-4, (1-self.mf_pah)*4e-3, (1-self.mf_pah)*5e-3, (1-self.mf_pah)*1e-1], 
                    [0, self.mf_pah*4e-3, self.mf_pah*5e-3, self.mf_pah*1e-1]
                ]) * self.math.const['M_sun']

    def gas_density_distribution(self):
        """Calculates the gas density at a given position.


        Returns:
            float: Gas density at a given position.
        """
        # Real zeros in density distribution?
        real_zero = True
        # INNER DISK
        inner_disk = self.math.default_disk_density(self.position,
            beta=1.0, surface_dens_exp=-1.0,
            inner_radius=0.3 * self.math.const['au'],
            outer_radius=2.6 * self.math.const['au'], 
            ref_scale_height=5. * self.math.const['au'], 
            ref_radius=100. * self.math.const['au'], real_zero=real_zero)
        # RINGS
        beta = 1.26
        surf_dens_exp = -0.5
        ref_radius = 100. * self.math.const['au']
        ref_scale_height = 12. * self.math.const['au']
        # RING #1
        ring_1 = self.math.default_disk_density(self.position,
            beta=beta, surface_dens_exp=surf_dens_exp,
            inner_radius=41. * self.math.const['au'],
            outer_radius=51. * self.math.const['au'],
            ref_scale_height=ref_scale_height, ref_radius=ref_radius, real_zero=real_zero)
        # RING #2
        ring_2 = self.math.default_disk_density(self.position,
            beta=beta, surface_dens_exp=surf_dens_exp,
            inner_radius=155. * self.math.const['au'],
            outer_radius=165. * self.math.const['au'],
            ref_scale_height=ref_scale_height, ref_radius=ref_radius, real_zero=real_zero)
        # RING #3
        ring_3 = self.math.default_disk_density(self.position,
            beta=beta, surface_dens_exp=surf_dens_exp,
            inner_radius=269. * self.math.const['au'],
            outer_radius=400. * self.math.const['au'],
            ref_scale_height=ref_scale_height, ref_radius=ref_radius, real_zero=real_zero)
        # PAH continuum
        if self.use_cont:
            pah_cont = self.math.default_disk_density(self.position,
                beta=beta, surface_dens_exp=surf_dens_exp,
                inner_radius=41 * self.math.const['au'],
                outer_radius=400 * self.math.const['au'], 
                ref_scale_height=ref_scale_height, ref_radius=ref_radius, real_zero=real_zero)
            return [[inner_disk, ring_1, ring_2, ring_3, 0], 
                    [0, 0, 0, 0, pah_cont],
                    [0, 0, 0, 0, pah_cont],]
        return [[inner_disk, ring_1, ring_2, ring_3], [0, ring_1, ring_2, ring_3]]

    def scale_height(self, radius):
        """Calculates the scale height at a certain position.

        Args:
            radius (float) : Cylindrical radius of current position

        Returns:
            float: Scale height.
        """
        if(0.3 * self.math.const['au'] <= radius <= 2.6 * self.math.const['au']):
            beta = 1.
            ref_scale_height=5. * self.math.const['au'] 
            ref_radius=100. * self.math.const['au']
            scale_height = ref_scale_height * (radius / ref_radius) ** beta
        else:
            beta = 1.26
            ref_radius = 100. * self.math.const['au']
            ref_scale_height = 12. * self.math.const['au']
            scale_height = ref_scale_height * (radius / ref_radius) ** beta
        return scale_height


class ProtoplanetaryDisk(Model):
    """The default disk model with the Shakura and Sunyaev disk density profile.
    Made for studies about protoplanetary disks at CEA and IAS.

    Notes:
        Disk parameters/quantities which will be varied to investigate their influence on observables.
        - Stellar source/component:
            1. A-type star (Herbig Ae)    -> T=8500 K, R=2.0 R_sun (--source herbig_ae)
            2. F-type star (intermediate) -> T=6500 K, R=1.3 R_sun (--source f_type)
            3. K/G-type star (T Tauri)    -> T=4000 K, R=0.9 R_sun (--source t_tauri)
        - Dust grain compositions:
            1. Pure silicate grains       -> (--dust silicate)
            2. MRN dust grains            -> (--dust mrn)
            3. Grains from Themis model   -> (--dust themis)
        - Dust grain sizes:
            1. 5 nm - 250 nm (silicate/mrn) -> (--amin=1, --amax=)
                             (themis)       -> (default size distribution)
            3. 5 nm - 1 mm   (silicate/mrn) -> (--amin=1, --amax=)
                             (themis)       -> (only large pure silicates)
    """

    def __init__(self):
        """Initialisation of the model parameters.

        Notes:
            Shakura and Sunyaev (1973)
            Link: http://adsabs.harvard.edu/abs/1973A&A....24..337S
        """
        Model.__init__(self)

        #: Set parameters of the disk model
        self.parameter['distance'] = 140.0 * self.math.const['pc']
        self.parameter['inner_radius'] = 1.0 * self.math.const['au']
        self.parameter['outer_radius'] = 300.0 * self.math.const['au']
        self.parameter['grid_type'] = 'spherical'
        self.spherical_parameter['n_r'] = 100
        self.spherical_parameter['n_th'] = 182
        self.spherical_parameter['n_ph'] = 1
        self.spherical_parameter['sf_r'] = 1.058
        # self.spherical_parameter['sf_th'] = 1.0
        self.parameter['gas_mass'] = 1e-4 * self.math.const['M_sun']
        self.parameter['stellar_source'] = 't_tauri'
        self.parameter['dust_composition'] = 'silicate'
        self.parameter['detector'] = 'cartesian'

    def gas_density_distribution(self):
        """Calculates the gas density at a given position.

        Returns:
            float: Gas density at a given position.
        """
        gas_density = self.math.default_disk_density(self.position,
            inner_radius=self.parameter['inner_radius'],
            outer_radius=self.parameter['outer_radius'], alpha=1.625)
        return gas_density


class MultiDisk(Model):
    """The disk model with the Shakura and Sunyaev disk density profile.
    """

    def __init__(self):
        """Initialisation of the model parameters.

        Notes:
            Shakura and Sunyaev (1973)
            Link: http://adsabs.harvard.edu/abs/1973A&A....24..337S
        """
        Model.__init__(self)

        #: Set parameters of the disk model
        self.parameter['distance'] = 140.0 * self.math.const['pc']
        self.parameter['gas_mass'] = np.array([[1e-2], [1e-2 * 1e-3]]) * self.math.const['M_sun']
        self.parameter['grid_type'] = 'spherical'
        self.parameter['inner_radius'] = 1. * self.math.const['au']
        self.parameter['outer_radius'] = 300. * self.math.const['au']
        # Define the used sources, dust composition and gas species
        self.parameter['stellar_source'] = 't_tauri'
        self.parameter['dust_composition'] = 'silicate_pah'
        self.parameter['gas_species'] = 'co'
        self.parameter['detector'] = 'cartesian'
        # In the case of a spherical grid
        self.spherical_parameter['n_r'] = 100
        self.spherical_parameter['n_th'] = 181
        self.spherical_parameter['n_ph'] = 1
        self.spherical_parameter['sf_r'] = 1.03
        # sf_th = -1 is linear; sf_th = 1 is sinus; rest is exp with step width sf_th
        self.spherical_parameter['sf_th'] = 1.0
        # In the case of a cylindrical grid
        self.cylindrical_parameter['n_r'] = 100
        self.cylindrical_parameter['n_z'] = 181
        self.cylindrical_parameter['n_ph'] = 1
        self.cylindrical_parameter['sf_r'] = 1.03
        # sf_z = -1 is linear; sf_z = 1 is sinus; rest is exp with step width sf_z
        self.cylindrical_parameter['sf_z'] = 1.0
        # Default disk parameter
        self.ref_radius = 100. * self.math.const['au']
        self.ref_scale_height = 10.  * self.math.const['au']
        self.parameter['variable_dust'] = True

    def gas_density_distribution(self):
        """Calculates the gas density at a given position.


        Returns:
            float: Gas density at a given position.
        """
        gas_density = self.math.default_disk_density(self.position,
                inner_radius=self.parameter['inner_radius'],
                outer_radius=self.parameter['outer_radius'])
        return [[gas_density], [gas_density]]
