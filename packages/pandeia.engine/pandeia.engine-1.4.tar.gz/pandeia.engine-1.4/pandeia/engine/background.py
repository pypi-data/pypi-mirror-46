# Licensed under a 3-clause BSD style license - see LICENSE.rst
from __future__ import division, absolute_import

import os
from warnings import warn
import numpy as np
import pysynphot as psyn

from . import config as cf
from .config import DefaultConfig
from .io_utils import ref_data_column
from .utils import spectrum_resample
from .custom_exceptions import EngineInputError, DataError, PysynphotError
import six

default_refdata_directory = cf.default_refdata_directory


class Background(cf.DefaultConfig):

    """
    This class provides the background flux.  The background can be computed from the engine's
    notional reference data or passed as a spectrum of a form [wave, sb] where wave is an array of
    wavelengths in microns and sb is an array of surface brightnesses in MJy/sr.

    Parameters
    ----------
    observation: Observation instance
        Contains needed instrument and background configuration data.
    config: dict
        Extra configuration information
    webapp: bool
        Enable strict API checking (not yet implemented here)

    Attributes
    ----------
    ref_dir: string
        Directory containing data for notional background model
    bg_level: string or list-like or array-like
        Input background level. Can be string for configuring notional model or lists/arrays for user-input background.
    instrument: Instrument instance
        Instrument configuration data is required to determine pixel scale and telescope/instrument contributions
        to the background model.
    aperture_pars: dict
        Instrument configuration data containing pixel scale required to calculate per-pixel background flux
    bg_spec: pysynphot.ArraySpectrum
        Original full-length, full-resolution background spectrum with wavelengths in microns and surface brightness in MJy/sr.
        pysynphot doesn't natively support mega-janskys so fake it for now by using fluxunits='jy' so that it at least knows
        the flux density is in F_nu.
    wave: 1D np.ndarray
        Binned/trimmed wavelength set
    MJy_sr: 1D np.ndarray
        Binned/trimmed background spectrum in units of MJy/sr

    Properties
    ----------
    mjy_pix: 1D np.ndarray
        Convert self.MJy_sr to units of mJy (milli-janskys) per pixel
    flambda_pix: 1D np.ndarray
        Convert self.MJy_sr to units of F_lambda per pixel, photons/cm^2/s/micron/pixel.
    """

    def __init__(self, observation, config={}, webapp=False, **kwargs):
        DefaultConfig.__init__(self, config=config, webapp=webapp, **kwargs)

        self.webapp = webapp
        self.telescope = observation.instrument.telescope.tel_name
        self.ref_dir = os.path.join(default_refdata_directory, self.telescope, 'background')
        self.bg_location = observation.background
        self.instrument = observation.instrument
        self.aperture_pars = self.instrument.get_aperture_pars()
        # if the background spectrum is provided, the 0th index is wavelength and the 1st is the surface brightness
        if isinstance(self.bg_location, (list, tuple, np.ndarray)):
            try:
                # wavelength set for background that will get resampled to match wavelength set for a scene
                self.wave = np.array(self.bg_location[0], dtype=np.float64)
                # background spectrum in standard units of MJy/sr. use properties mjy_pix and flambda_pix to convert units.
                self.MJy_sr = np.array(self.bg_location[1], dtype=np.float64)
                # we store the original bg spectrum in a pysynphot spectrum so that resampling operations
                # are done on the original data.
                self.bg_spec = psyn.ArraySpectrum(wave=self.wave, flux=self.MJy_sr, waveunits='microns', fluxunits='jy')
            except Exception as e:
                msg = "Malformed input background spectrum: %s (%s)" % (repr(self.bg_location), e)
                raise EngineInputError(value=msg)
        elif isinstance(self.bg_location, (str, six.text_type)):
            # Handle deprecated pre-1.3 background behavior
            if self.bg_location in ["low", "medium", "high"]:
                self.bg_level = self.bg_location
                self.bg_location = "minzodi"
                warn('Backgrounds are now specified with background and background_level. Existing ' \
                              'functionality will be removed in v1.5. \n Your inputs have been changed to ' \
                            'background={0} and background_level={1}'.format(self.bg_location,self.bg_level), category=FutureWarning)
            elif self.bg_location == "none":
                pass
            else:
                self.bg_level = observation.background_level
            self.get_canned_background()
        else:
            msg = "Must provide a valid background spectrum or background signifier string: %s" % repr(self.bg_location)
            raise EngineInputError(value=msg)

    #def _get_config(self):
    #    """
    #    Read default configuration from JSON
    #
    #   Returns
    #    -------
    #    config: dict
    #        All desired class attributes should have defaults defined in the config file
    #    """
    #    # use this trick to key the configuration file name off the name of the instantiated subclass
    #    ref_dir = os.path.join(default_refdata_directory, "background")
    #    config = read_json(os.path.join(ref_dir, "config.json"), raise_except=True)
    #    defaults = config.pop("defaults")
    #    config.update(defaults)
    #    return config


    def resample(self, wavelengths):
        """
        Re-bin background onto a new set of wavelengths.

        This method modifies self.wave and self.MJy_sr, but leaves self.bg_spec alone.

        Parameters
        ----------
        wavelengths: 1D numpy array
            Array of new wavelengths to sample spectrum onto
        """
        self.MJy_sr = spectrum_resample(self.bg_spec.flux, self.bg_spec.wave, wavelengths)
        self.wave = wavelengths

    def telescope(self):
        """
        Load the telescope background.

        Returns
        -------
        bg_spec : pysynphot.ArraySpectrum
            Telescope background in MJy/sr
        """
        try:
            bg_tel_wave, bg_tel = self.instrument.telescope.get_bg_tel()
            bg_spec = psyn.ArraySpectrum(wave=bg_tel_wave, flux=bg_tel, waveunits='microns')
        except Exception as e:
            msg = "Problem loading telescope background model. "
            if self.webapp:
                msg += "(%s)" % type(e)
            else:
                msg += repr(e)
            raise DataError(value=msg)
        return bg_spec

    def get_canned_background(self):
        """
        Read reference data for pandeia's canned background models and configure self.wave, self.bg_location,
        self.bg_level, and self.bg_spec to use it.
        """

        # set default value, if background is unset. We will use the benchmark minzodi background as the default,
        # as this is where the backgrounds were extensively tested and calibrated.
        if self.bg_location is None:
            self.bg_location = 'minzodi'
            self.bg_level = 'benchmark'

        if self.bg_location == 'none':
            bg_wave = np.array([0.1, 30.0])
            bg_sb = np.array([0.0, 0.0])
            try:
                tot_bg = psyn.ArraySpectrum(wave=bg_wave, flux=bg_sb, waveunits='microns', fluxunits='jy')
            except Exception as e:
                msg = "Problem creating background spectrum with Pysynphot."
                if self.webapp:
                    msg += "(%s)" % type(e)
                else:
                    msg += repr(e)
                raise PysynphotError(value=msg)
        else:
            bg_file = os.path.join(default_refdata_directory, self.telescope, "background", "{0}_{1}.fits".format(self.bg_location,self.bg_level))
            try:
                bg_wave = ref_data_column(bg_file, colname='wavelength')
                bg = ref_data_column(bg_file, colname='background')
                tot_bg = psyn.ArraySpectrum(wave=bg_wave, flux=bg, waveunits='microns', fluxunits='jy')
            except Exception as e:
                msg = "Problem loading background model. "
                if self.webapp:
                    msg += "(%s)" % type(e)
                else:
                    msg += repr(e)
                raise DataError(value=msg)

        self.bg_spec = tot_bg
        self.wave = tot_bg.wave
        self.MJy_sr = tot_bg.flux

    @property
    def mjy_pix(self):
        """
        Convert background surface brightness in MJy/sr to F_nu per pixel in
        mJy/pixel (self.wave assumed to be in microns)

        Returns
        -------
        i_pix: 1D np.ndarray
            Flux per pixel in mJy/pixel
        """
        i_nu = 1e9 * self.MJy_sr * 2.3504e-11  # 1e9 convert MJy to mJy; 2.3504e-11 converts sr to square arcsec

        i_nu_pix = i_nu * self.aperture_pars['pix'] ** 2
        return i_nu_pix

    @property
    def flambda_pix(self):
        """
        Convert background surface brightness in MJy/sr to F_lambda per pixel in
        photons/cm^2/s/micron/pixel (self.wave assumed to be in microns)

        Returns
        -------
        i_pix: 1D np.ndarray
            Flux per pixel in photons/s/cm^2/pixel
        """
        i_lambda = 1.50916e9 / self.wave * self.MJy_sr * 2.3504e-11
        i_lambda_pix = i_lambda * self.aperture_pars['pix'] ** 2
        return i_lambda_pix
