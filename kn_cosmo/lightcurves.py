"""Lightcurve models"""
import h5py
import pkg_resources

from astropy import (
    cosmology, constants as const, coordinates,
    units as u
)
import numpy as np
from scipy import interpolate
import sncosmo


class Lightcurve(object):
    """A lightcurve using `sncosmo`"""
    def __init__(self, source, peak_abs_mag, z, t0, skycoord,
                 ebv=0., delta_t_minus=20., delta_t_plus=200.,
                 cosmology=cosmology.Planck15, peak_mag_band='standard::b',
                 magsys='ab', **extra_model_parameters):
        """
        Lightcurve properties

        Parameters
        ----------
        source : str or `sncosmo.TimeSeriesSource`
            lightcurve source used to create `sncosmo.Model`.
            E.g. 'nugent-sn1a', assumed present in `sncosmo.registry`.
            Optionally, provide `sncosmo.TimeSeriesSource`
        peak_abs_mag : float
            SNe peak absolute magnitude
        z : float
            SNe redshift
        t0 : float
            SNe peak time in JD.
        skycoord: `astropy.coordinates.Skycoord`
            SNe sky coordinates
        ebv : float
            SNe host galaxy extinction E(B-V)
        delta_t_minus : float
            lower limit of phases is `t0 - delta_t_minus`
        delta_t_plus : float
            upper limit of phases is `t0 + delta_t_plus`
        cosmology : `astropy.cosmology`
            cosmology. WMAP9 by default.
        peak_mag_band : str
            Band where to set absolute mag. "standard::b" by default.
            Assumed present in `sncosmo.registry`.
        magsys : str
            Magnitude system. E.g. "ab", "vega".
            Assumed present in `sncosmo.registry`.
        **extra_model_parameters
            Additional parameters going into `sncosmo.Model`.
            E.g. `x1`, `c` for `sncosmo.SALT2Model`.

        Notes
        -----
        `sncosmo` can potentially return `inf` for the magnitude values.
        `self.tmin` and `self.tmax` attributes contain the JDs such that the
        in between values of magnitude are finite.
        """
        self.skycoord = skycoord
        self.cosmology = cosmology
        self.model = sncosmo.Model(source) if isinstance(
            source, sncosmo.TimeSeriesSource
        ) else sncosmo.Model(sncosmo.get_source(source))
        # set model parameters
        self.model.set(z=z)
        self.model.set(t0=t0)
        self.model.update(extra_model_parameters)
        # add host galaxy extinction E(B-V)
        self.model.add_effect(sncosmo.CCM89Dust(), 'host', 'rest')
        self.model.set(hostebv=ebv)
        # add MW extinction to observing frame
        self.model.add_effect(sncosmo.F99Dust(), 'mw', 'obs')
        # set source peak magnitude
        self.model.set_source_peakabsmag(
            peak_abs_mag, band=peak_mag_band, magsys=magsys, cosmo=cosmology)
        # define an interpolater for m(t) in R and g bands
        # FIXME currently linspacing 1000 points
        p = np.linspace(-delta_t_minus, delta_t_plus, 1000)
        # observer frame times to go in sncosmo bandflux, bandmag functions
        t = t0 + p
        m, _ = self.get_mag_flux(['desg', 'desr'], t)
        finite_mask = np.isfinite(m[0]) * np.isfinite(m[1])
        # FIXME failure mode if finite_mask is an empty array
        self.tmin = np.min(t[finite_mask])
        self.tmax = np.max(t[finite_mask])
        self._m_R_interpolator = interpolate.interp1d(t[finite_mask],
                                                      m[0][finite_mask])
        self._m_g_interpolator = interpolate.interp1d(t[finite_mask],
                                                      m[1][finite_mask])

    def get_mag_flux(self, bands, phases, **kwargs):
        """
        Return flux and magnitude in a particular band.

        Parameters
        ----------
        band : list
            string values of band(s) of interest.
            Assumed present in `sncosmo.registry`
        phases : list
            Times in JD

        Returns
        -------
        mags, fluxes
            list of mags and fluxes based on band(s) supplied.

        Examples
        --------
        >>> coords = astropy.coordinates.SkyCoord(10, 20, unit="deg")
        >>> phase = np.linspace(-2 100, 50)
        >>> supernova = SupernovaLightcurve(
        ... 'nugent-sn1a', -16.0, 0.5, 0., coords)
        >>> mags, fluxes = supernova.get_mag_flux(['iptfR', 'iptfg'], phase)
        """
        mags = []
        fluxes = []
        magsys = kwargs.get('magsys', "ab")
        for band in bands:
            mags.append(
                self.model.bandmag(band, magsys, phases))
            fluxes.append(
                self.model.bandflux(band, phases))
        return mags, fluxes

    def plot_lightcurve(self, band, phases,
                        magsys="ab",
                        show=True,
                        filename=None):
        """
        Plots (using Matplotlib) lightcurve apparent magnitude
        in band of interest.

        Parameters
        ----------
        band : str
            Band of interest. Assumed present in `sncosmo.registry`
        phases : list
            List of Phases.
        magsys : str
            Magnitude system.
        """
        from matplotlib import pyplot as plt
        mag, _ = self.get_mag_flux([band], phases, magsys=magsys)
        plt.plot(phases, mag[0], label=r'{} band'.format(band))
        plt.xlabel(r'Phase (days)')
        plt.ylabel('$m$', fontsize=14)
        plt.ylim(plt.ylim()[::-1])
        plt.legend()
        plt.grid(linestyle='--')
        if filename:
            plt.savefig(filename)
        if show:
            plt.show()


_dhawan_flux_filename = pkg_resources.resource_filename(
    __name__, 'data/best-fit-AT-2017-gfo.txt'
)
_dhawan_data = np.loadtxt(_dhawan_flux_filename, skiprows=3)
_dhawan_waves = _dhawan_data.T[0] * u.AA
_dhawan_fluxes = _dhawan_data[:, 1:].T * u.erg / (u.s*u.cm**2*u.AA)
_T_i = 0.25
_T_f = 15.25
_N_t = 30
_D_t = (_T_f - _T_i) / _N_t
_dhawan_phases = [_T_i + _D_t*(n + 0.5) for n in range(30)] * u.day
dhawan_at2017gfo_source = sncosmo.TimeSeriesSource(
    _dhawan_phases.value, _dhawan_waves.value, _dhawan_fluxes.value,
    zero_before=True
)
"""TimeSeriesSource using Dhawan et. al. (2020) AT2017gfo best fit."""


class DhawanLightcurve(Lightcurve):
    """Lightcurve based on kilonovae by Dhawan et. al. (2020)
    DOI:10.3847/1538-4357/ab5799
    """
    def __init__(self, *args, **kwargs):
        """Model initial using predefined :class:`TimeSeriesSource`.

        Parameters
        ----------
        *args
            argument list passed to :meth:`Lightcurve.__init__`
            First argument is the `source` variable. Defaults to
            best-fit AT2017gfo fit by Dhawan et. al. (2020).
        **kwargs
            keyword arguments passed to :meth:`Lightcurve.__init__`
        """
        try:
            source, *args = args
        except ValueError:
            source = dhawan_at2017gfo_source
            args = (-15.7, 0.01, 0., coordinates.SkyCoord(
                '02:42:40.771', '-00:00:47.84', unit=(u.hour, u.deg)))
            kwargs = dict(ebv=0., delta_t_minus=-2., delta_t_plus=12.)
        super().__init__(source, *args, **kwargs)


_kasen_flux_filename = pkg_resources.resource_filename(
    __name__, 'data/kasen_knova_d1_n10_m0.040_vk0.03_fd1.0_Xlan1e-4.0.h5'
)
_kasen_data = h5py.File(_kasen_flux_filename, "r")
_kasen_nu = np.array(_kasen_data['nu'], dtype='d') * u.Hz
_kasen_lam = (const.c / _kasen_nu).to('angstrom')
# wavelength values are decreasing, reverse
_kasen_lam = np.flipud(_kasen_lam)
_L_nu = np.array(_kasen_data['Lnu'], dtype='d') * u.erg/u.s/u.Hz
_L_lam = _L_nu*_kasen_nu**2.0 / const.c
# flux at 10 pc
_scaling_distance = 10 * u.pc
_F_lam = (
    _L_lam / (4 * np.pi * _scaling_distance**2)
).to('erg / (s * angstrom * cm^2)')
_F_lam = np.fliplr(_F_lam)
_kasen_phases = np.array(_kasen_data['time']) / 3600.0 / 24.0 * u.day
kasen_at2017gfo_source = sncosmo.TimeSeriesSource(
    _kasen_phases.value, _kasen_lam.value, _F_lam.value,
    zero_before=True
)
"""Kasen time series source at 10 pc"""


class KasenLightCurve(Lightcurve):
    """Lightcurve model based on Kasen et. al. (2017) kilonova
    grid DOI:10.1038/nature24453
    """
    def __init__(self, *args, **kwargs):
        """Model initial using predefined :class:`TimeSeriesSource`.

        Parameters
        ----------
        *args
            argument list passed to :meth:`Lightcurve.__init__`
            First argument is the `source` variable. Defaults to
            best-fit AT2017gfo fit by Dhawan et. al. (2020).
        **kwargs
            keyword arguments passed to :meth:`Lightcurve.__init__`
        """
        try:
            source, *args = args
        except ValueError:
            source = kasen_at2017gfo_source
            args = (-15.7, 0.01, 0., coordinates.SkyCoord(
                '02:42:40.771', '-00:00:47.84', unit=(u.hour, u.deg)))
            kwargs = dict(ebv=0., delta_t_minus=-2., delta_t_plus=12.)
        super().__init__(source, *args, **kwargs)
