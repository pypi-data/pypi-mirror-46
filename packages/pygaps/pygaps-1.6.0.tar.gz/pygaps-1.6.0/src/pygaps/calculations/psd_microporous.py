"""
Module contains 'classical' methods of calculating a pore size distribution for pores in
the micropore range (<2 nm).
"""

import numpy
import scipy.constants as const
import scipy.optimize as opt

from ..utilities.exceptions import ParameterError


def psd_horvath_kawazoe(loading, pressure, temperature, pore_geometry,
                        adsorbate_properties,
                        adsorbent_properties=None):
    r"""
    Calculate the pore size distribution using the Horvath-Kawazoe method.

    Parameters
    ----------
    loading : array
        Adsorbed amount in mmol/g.
    pressure : array
        Relative pressure.
    temperature : float
        Temperature of the experiment, in K.
    pore_geometry : str
        The geometry of the pore, eg. 'sphere', 'cylinder' or 'slit'.
    adsorbate_properties : dict
        Properties for the adsorbate in the form of::

            adsorbate_properties = dict(
                'molecular_diameter'=0,           # nm
                'polarizability'=0,               # nm3
                'magnetic_susceptibility'=0,      # nm3
                'surface_density'=0,              # molecules/m2
                'liquid_density'=0,               # g/cm3
                'adsorbate_molar_mass'=0,         # g/mol
            )

    adsorbent_properties : dict
        Properties for the adsorbate in the same form
        as 'adsorbate_properties'. A list of common models
        can be found in .calculations.models_hk.

    Returns
    -------
    pore widths : array
        The widths of the pores.
    pore_dist : array
        The distributions for each width.

    Notes
    -----

    *Description*

    The H-K method [#]_ attempts to describe the adsorption within pores by calculation
    of the average potential energy for a pore. The method starts by assuming the
    relationship between the gas phase as being:

    .. math::

        R_g T \ln(\frac{p}{p_0}) = U_0 + P_a

    Here :math:`U_0` is the potential function describing the surface to adsorbent
    interactions and :math:`P_a` is the potential function describing the adsorbate-
    adsorbate interactions. This equation is derived from the equation of the free energy
    of adsorption at constant temperature where term :math:`T \Delta S^{tr}(w/w_{\infty})`
    is assumed to be negligible.

    If a Lennard-Jones-type potential function describes the interactions between the
    adsorbate molecules and the adsorbent molecules then the two contributions to the
    total potential can be replaced by the extended function. The resulting equation becomes:

    .. math::

        RT\ln(p/p_0) =   & N_A\frac{n_a A_a + n_A A_A}{2 \sigma^{4}(l-d)} \\
                        & \times \int_{d/_2}^{1-d/_2}
                            \Big[
                            - \Big(\frac{\sigma}{r}\Big)^{4}
                            + \Big(\frac{\sigma}{r}\Big)^{10}
                            - \Big(\frac{\sigma}{l-r}\Big)^{4}
                            + \Big(\frac{\sigma}{l-r}\Big)^{4}
                            \Big] \mathrm{d}x

    Where:

    * :math:`R` -- gas constant
    * :math:`T` -- temperature
    * :math:`l` -- width of pore
    * :math:`d` -- defined as :math:`d=d_a+d_A` the sum of the diameters of the adsorbate and
      adsorbent molecules
    * :math:`N_A` -- Avogadro's number
    * :math:`n_a` -- number of molecules of adsorbent
    * :math:`A_a` -- the Lennard-Jones potential constant of the adsorbent molecule defined as

        .. math::
            A_a = \frac{6mc^2\alpha_a\alpha_A}{\alpha_a/\varkappa_a + \alpha_A/\varkappa_A}

    * :math:`A_A` -- the Lennard-Jones potential constant of the adsorbate molecule defined as

        .. math::
            A_a = \frac{3 m_e c_l ^2\alpha_A\varkappa_A}{2}

    * :math:`m_e` -- mass of an electron
    * :math:`c_l` -- speed of light in vacuum
    * :math:`\alpha_a` -- polarizability of the adsorbate molecule
    * :math:`\alpha_A` -- polarizability of the adsorbent molecule
    * :math:`\varkappa_a` -- magnetic susceptibility of the adsorbate molecule
    * :math:`\varkappa_A` -- magnetic susceptibility of the adsorbent molecule


    *Limitations*

    The assumptions made by using the H-K method are:

        - It does not have a description of capillary condensation. This means that the
          pore size distribution can only be considered accurate up to a maximum of 5 nm.

        - Each pore is uniform and of infinite length. Materials with varying pore
          shapes or highly interconnected networks may not give realistic results.

        - The wall is made up of single layer atoms. Furthermore, since the HK method
          is reliant on knowing the properties of the surface atoms as well as the
          adsorbent molecules the material should ideally be homogenous.

        - Only dispersive forces are accounted for. If the adsorbate-adsorbent interactions
          have other contributions, the Lennard-Jones potential function will not be
          an accurate description of pore environment.

    References
    ----------
    .. [#] K. Kutics, G. Horvath, Determination of Pore size distribution in MSC from
       Carbon-dioxide Adsorption Isotherms, 86

    """
    # Parameter checks
    if pore_geometry == 'slit':
        pass
    elif pore_geometry == 'cylinder':
        raise NotImplementedError
    elif pore_geometry == 'sphere':
        raise NotImplementedError

    if adsorbent_properties is None:
        raise ParameterError(
            "A dictionary of adsorbent properties must be provided"
            " for the HK method. The properties required are:"
            "molecular_diameter, polarizability,"
            "magnetic_susceptibility and surface_density"
            "Some standard models can be found in "
            " .calculations.adsorbent_parameters")
    missing = [x for x in adsorbent_properties if x not in ['molecular_diameter',
                                                            'polarizability',
                                                            'magnetic_susceptibility',
                                                            'surface_density']]
    if len(missing) != 0:
        raise ParameterError(
            "Adsorbent properties dictionary is missing parameters: "
            "{}".format(' '.join(missing)))

    if adsorbate_properties is None:
        raise ParameterError(
            "A dictionary of adsorbate properties must be provided"
            " for the HK method. The properties required are:"
            " molecular_diameter, liquid_density, polarizability,"
            " magnetic_susceptibility, surface_density, adsorbate_molar_mass")
    missing = [x for x in ['molecular_diameter',
                           'liquid_density',
                           'polarizability',
                           'magnetic_susceptibility',
                           'surface_density',
                           'adsorbate_molar_mass'] if x not in adsorbate_properties]
    if len(missing) != 0:
        raise ParameterError(
            "Adsorbate properties dictionary is missing parameters: "
            "{}".format(' '.join(missing)))

    # dictionary unpacking
    d_adsorbate = adsorbate_properties.get('molecular_diameter')
    d_adsorbent = adsorbent_properties.get('molecular_diameter')
    p_adsorbate = adsorbate_properties.get('polarizability') * 1e-27            # to m3
    p_adsorbent = adsorbent_properties.get('polarizability') * 1e-27            # to m3
    m_adsorbate = adsorbate_properties.get('magnetic_susceptibility') * 1e-27   # to m3
    m_adsorbent = adsorbent_properties.get('magnetic_susceptibility') * 1e-27   # to m3
    n_adsorbate = adsorbate_properties.get('surface_density')
    n_adsorbent = adsorbent_properties.get('surface_density')
    liquid_density = adsorbate_properties.get('liquid_density')
    adsorbate_molar_mass = adsorbate_properties.get('adsorbate_molar_mass')

    # calculation of constants and terms
    e_m = const.electron_mass
    c_l = const.speed_of_light
    effective_diameter = d_adsorbate + d_adsorbent
    sigma = (2 / 5)**(1 / 6) * effective_diameter / 2
    sigma_si = sigma * 1e-9

    a_adsorbent = 6 * e_m * c_l ** 2 * p_adsorbate * p_adsorbent /\
        (p_adsorbate / m_adsorbate + p_adsorbent / m_adsorbent)
    a_adsorbate = 3 * e_m * c_l**2 * p_adsorbate * m_adsorbate / 2

    constant_coefficient = const.Avogadro / \
        (const.gas_constant * temperature) * \
        (n_adsorbate * a_adsorbate + n_adsorbent * a_adsorbent) / \
        (sigma_si**4)

    constant_interaction_term = - \
        ((sigma**4) / (3 * (effective_diameter / 2)**3) -
         (sigma**10) / (9 * (effective_diameter / 2)**9))

    def h_k_pressure(l_pore):
        pressure = numpy.exp(constant_coefficient / (l_pore - effective_diameter) *
                             ((sigma**4) / (3 * (l_pore - effective_diameter / 2)**3) -
                              (sigma**10) / (9 * (l_pore - effective_diameter / 2)**9) +
                              constant_interaction_term))

        return pressure

    p_w = []

    for p_point in pressure:
        # minimise to find pore length
        def h_k_minimization(l_pore):
            return numpy.abs(h_k_pressure(l_pore) - p_point)
        res = opt.minimize_scalar(h_k_minimization)
        p_w.append(res.x - d_adsorbent)

    # finally calculate pore distribution
    pore_widths = numpy.array(p_w)
    avg_pore_widths = numpy.add(pore_widths[:-1], pore_widths[1:]) / 2          # nm
    volume_adsorbed = loading * adsorbate_molar_mass / liquid_density / 1000    # cm3/g
    pore_dist = numpy.diff(volume_adsorbed) / numpy.diff(pore_widths)

    return avg_pore_widths, pore_dist
