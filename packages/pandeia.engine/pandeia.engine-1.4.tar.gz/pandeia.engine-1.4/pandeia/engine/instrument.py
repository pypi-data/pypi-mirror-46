# Licensed under a 3-clause BSD style license - see LICENSE.rst
from __future__ import division, absolute_import

import os
from functools import reduce
from warnings import warn
import numpy as np
import scipy.sparse as sparse
import operator

import astropy.io.fits as fits
from astropy.convolution import Gaussian1DKernel, convolve

from . import exposure as exp
from . import config as cf
from .psf_library import PSFLibrary
from .io_utils import read_json, ref_data_interp, ref_data_column
from .utils import merge_data, spectrum_resample
from .telescope import TelescopeConfig
from .custom_exceptions import EngineInputError, DataError, UnsupportedError, InternalError, DataConfigurationError
from .constants import DEFAULT_DISPERSION

default_refdata_directory = cf.default_refdata_directory


class InstrumentConfig(TelescopeConfig):

    """
    This is a trivial top-level class for now. It overrides TelescopeConfig._get_config() to get the configuration
    information from a different place, currently under $pandeia_refdata/<tel_name>/<inst_name>
    """

    def _get_config(self):
        """
        Read default source configuration from JSON

        Returns
        -------
        config: dict
            All desired class attributes should have defaults defined in the config file
        """
        # use this trick to key the configuration file name off the name of the instantiated subclass
        self.inst_name = self.__class__.__name__.lower()
        self.ref_dir = os.path.join(default_refdata_directory, self.telescope.tel_name, self.inst_name)
        config = read_json(os.path.join(self.ref_dir, "config.json"), raise_except=True)

        # Grab the warning list, if it exists, in the config file.
        self.warning_list = []
        if 'warning_list' in config.keys():
            self.warning_list = config['warning_list']

        # pop the defaults entry out
        if "defaults" in config:
            defaults = config.pop("defaults")
            if self.mode is None:
                # if no mode specified, then get default mode
                if "mode" in defaults:
                    self.mode = defaults.pop("mode")
                else:
                    message = "No mode or default mode specified."
                    raise DataConfigurationError(value=message)
            # make sure mode is valid and if so use it to key the values to put into config
            if self.mode in defaults:
                config.update(defaults[self.mode])
            else:
                message = "Invalid %s mode: %s" % (self.inst_name, self.mode)
                raise DataConfigurationError(value=message)
        return config


class Instrument(InstrumentConfig):

    """
    This is the primary Instrument class that sets up the configuration and provides methods common
    to all instruments.

    Parameters
    ----------
    telescope: Telescope sub-class instance
        The telescope that contains the instrument
    mode: str
        Desired instrument mode
    config: dict
        dictionary containing necessary configuration information
    **kwargs: list of keyword/value pairs
        parameter keyword and value pairs to augment defaults and config
    """

    def __init__(self, telescope=None, mode=None, config={}, webapp=False, **kwargs):
        self.webapp = webapp
        if telescope is None:
            msg = "Telescope not defined for %s!" % self.__class__.__name__
            raise EngineInputError(value=msg)
        if mode is None:
            msg = "Instrument mode not defined for %s!" % self.__class__.__name__
            raise EngineInputError(value=msg)
        self.telescope = telescope
        self.mode = mode
        self.order = None
        self.detector_key = 'detector' # default value

        InstrumentConfig.__init__(self, config, webapp=webapp, **kwargs)

        # make sure telescope is configured properly. if not, the reference data directory
        # is likely not defined or doesn't exist.
        try:
            # make sure instrument is supported
            if self.inst_name not in self.telescope.instruments:
                message = "Unsupported %s instrument: %s" % (self.telescope.tel_name, self.inst_name)
                raise EngineInputError(value=message)
        except AttributeError as e:
            message = "Telescope/instrument configuration data missing.  "
            message += "Reference data directory possibly missing or not defined: %s" % default_refdata_directory
            message += "Original exception: %s" % e
            raise InternalError(value=message)

        # make sure required parameters are defined and do strict API checking if webapp is true
        all_config = merge_data(config, dict(**kwargs))
        self._nested_api_checks(all_config, webapp=webapp)

        self.exposure_spec = self.get_exposure_pars()
        self._loadpsfs()

        # Check the instrument and strategy for the calculation against
        # the configured warnings in the instrument's config.json file.
        #
        # There are times that an Instrument instance will be created in order to just read
        # some values (e.g., bandpass in normalization.py's function _get_bandpass()) and in
        # these cases the only thing passed in is the instrument information. So, we are going
        # to check the warnings only if 'detector' and 'instrument' are passed in through all_config.
        if 'detector' in all_config and 'instrument' in all_config:
            self.check_warnings(all_config)

    def _nested_api_checks(self, conf, webapp=False):
        for section in self.instrument_pars:
            for p in self.instrument_pars[section]:
                # if parameter is not already set, then it's a DataError since config file should have set it to a default.
                if p not in getattr(self, section):
                    msg = "Missing required %s parameter %s from default configuration for %s." % (
                        section,
                        p,
                        self.__class__.__name__
                    )
                    raise DataError(value=msg)
                # if we're doing API checking, make sure everything we need is specified by the inputs.
                if webapp:
                    if p not in conf[section]:
                        key = "%s_missing_%s_%s" % (
                            self.__class__.__name__.lower(),
                            section,
                            p
                        )
                        self.warnings[key] = "Missing %s API parameter %s for %s. Using default value of %s." % (
                            section,
                            p,
                            self.__class__.__name__,
                            getattr(self, section)[p]
                        )

    def check_warnings(self, input_dict):
        """

        :param warnings_list: list of warnings to check for and add to the warnings list
        :param input_dict: input as passed into the function
        :return:
        """

        # Each thing we want to be able to get the value of in the input dictionary
        # should be listed here. The "value" part is a list of nested keys to get the actual value.
        value_lookup = {
            'instrument': ['instrument', 'instrument'],
            'mode':       ['instrument', 'mode'],
            'filter':     ['instrument', 'filter'],
            'disperser':  ['instrument', 'disperser'],
            'aperture':   ['instrument', 'aperture'],
            'nexp':       ['detector', 'nexp'],
            'ngroup':     ['detector', 'ngroup'],
            'nint':       ['detector', 'nint'],
            'max_total_groups': ['detector', 'max_total_groups'],
            'readmode':   ['detector', 'readmode'],
            'subarray':   ['detector', 'subarray'],
        }

        # Run through each warning in the warnings_list to see if we need to return it.
        for warning in self.warning_list:

            # Run through all the parameters for this warning to see if all are true
            need_warning = True
            thewarning = warning['warning_text']
            for key, expected_value in warning['parameters'].items():

                # Get the value from the json dict sent to the engine.  This does a lookup
                # based on the value_lookup above to see where in the input json dict we
                # have to look for the value that was input.
                # https://stackoverflow.com/questions/13687924/setting-a-value-in-a-nested-python-dictionary-given-a-list-of-indices-and-value

                operator_text = '=='
                if '__' in key:
                    key, operator_text = key.split('__', 1)

                # https://stackoverflow.com/questions/9320335/accessing-python-dict-with-multiple-key-lookup-string
                input_value = reduce(dict.get, value_lookup[key], input_dict)

                # Setup the comparison operator to use below.
                cmp = '=='
                if operator_text == '==':
                    cmp = operator.eq
                elif operator_text == 'ge':
                    cmp = operator.ge
                elif operator_text == 'le':
                    cmp = operator.le
                elif operator_text == 'gt':
                    cmp = operator.gt
                elif operator_text == 'lt':
                    cmp = operator.lt
                elif operator_text == 'notin':
                    cmp = 'notin'
                else:
                    raise InternalError(value="Unknown operator on key {}__{}".format(key, operator_text))

                # For some reason there started to be collisions on comparison of str vs unicode so I am
                # going to convert things to string that might be string or unicode.  That way the comparison
                # will work properly.  In Python3 this will likely be able to be removed.
                if isinstance(input_value, (str, unicode)):
                    input_value = str(input_value)
                    if isinstance(expected_value, (str, unicode)):
                        expected_value = str(expected_value)
                    elif isinstance(expected_value, list):
                        expected_value = [str(x) for x in expected_value]

                # Compare the input_value with the expected value
                if ( # do operator comparison for value
                        (isinstance(expected_value, (str, unicode, int, long, float)) and cmp(input_value, expected_value)) or
                      # do set inclusion or exclusion for list
                        (isinstance(expected_value, list) and
                             ( (operator_text=='==' and input_value in expected_value) or
                             (operator_text=='notin' and not input_value in expected_value) )
                        )
                    ):
                    pass  # we do need a warning, based on this test
                else:
                    need_warning = False

                # Replace $mode, $instrument, $filter etc in the output warning with the actual value.
                # special syntax if we don't want it to be uppercase.
                if '$~'+key in thewarning:
                    thewarning = thewarning.replace('$~' + key, input_value)
                if '$'+key in thewarning:
                    thewarning = thewarning.replace('$'+key, input_value.upper())

            if need_warning:
                self.warnings[thewarning] = thewarning

    def _loadpsfs(self):
        """
        Load the PSF library for the current instrument configuration.  In most cases, this is based on the aperture.
        In some cases (e.g. NIRCam coronagraphy with bar-shaped masks), other configuration parameters come into play.
        """
        self.psf_library = self._load_psf_library(self.instrument['aperture'])

    def _load_psf_library(self,psf_key):

        psf_path = os.path.join(self.ref_dir, "psfs")
        library = PSFLibrary(path=psf_path, aperture=psf_key)

        return library

    @property
    def qe_key(self):
        """
        set default qe_key for looking up QE reference data. MIRI different from others and overloads this.
        """
        return 'qe'

    def get_detector_pars(self):
        """
        set default detector_key for looking up the detector that is used with a certain aperture. This can be
        overloaded for specific instruments.
        """
        return self.read_detector_pars()

    def get_name(self):
        """
        Return instrument's name
        """
        return self.inst_name

    def get_aperture(self):
        """
        Return configured aperture
        """
        return self.instrument['aperture']

    def _interp_refdata(self, wave, key, colname, default=None):
        """
        Read in requested reference file and return requested data interpolated onto wave

        Parameters
        ----------
        wave: numpy.ndarray
            Wavelength array onto which the reference data is to be interpolated
        key: str
            Key to get filename from self.paths
        colname: str
            Column to retrieve from reference file
        default: None or float
            Default value to return in case of missing file or column

        Returns
        -------
        ref: numpy.ndarray or float
            If file exists, return reference_data(wave). Else return default.
        """
        ref = None
        if key is not None and key in self.paths:
            ref_file = os.path.join(self.ref_dir, self.paths[key])
            if ref_file is not None:
                ref = ref_data_interp(ref_file, wave, colname)
        if ref is None and default is None:
            msg = "No reference data found and no default value supplied for %s in %s." % (colname, key)
            raise DataError(value=msg)
        elif ref is None and default is not None:
            ref = np.ones_like(wave)*default
        return ref

    def _get_throughput(self, wave, key):
        """
        Wrap self._interp_refdata for getting throughput data

        Parameters
        ----------
        wave: numpy.ndarray
            Wavelength array onto which the throughput curve is to be interpolated
        key: str
            Key to get filename from self.paths

        Returns
        -------
        eff: numpy.ndarray or float
            If ref file exists, return efficiency(wave), else return 1.0
        """
        eff = self._interp_refdata(wave, key, colname='throughput', default=1.0)
        return eff

    def _get_disperser(self):
        """
        The same disperser can have different configurations depending on which order is
        being used. Use self.order to build a new key for looking up configuration data for the
        given order.

        Returns
        -------
        key: str
            Key to look up order-specific configuration data
        """
        key = self.instrument['disperser']
        if self.order is not None:
            key = "%s_%d" % (key, self.order)
            key = key.replace('-','m')
        return key

    def _get_dispersion_key(self):
        """
        Different instruments have different ways to figure out which disperser to use. This is also used
        to look up reference data for multiple orders from the same disperser.

        Returns
        -------
        key: str
            Key used to get dispersion file out of self.paths
        """
        disperser = self._get_disperser()
        key = "%s_disp" % disperser
        return key

    def get_filter_eff(self, wave):
        """
        Read in filter throughput curve

        Parameters
        ----------
        wave: numpy.ndarray
            Wavelength vector to interpolate throughput onto

        Returns
        -------
        eff: numpy.ndarray or float
            Filter throughput as a function of wave
        """
        eff = self._get_throughput(wave, self.instrument['filter'])
        return eff

    def get_disperser_eff(self, wave):
        """
        Read in efficiency curve for configured grating

        Parameters
        ----------
        wave: numpy.ndarray
            Wavelength vector to interpolate throughput onto

        Returns
        -------
        eff: numpy.ndarray or float
            Disperser efficiency as a function of wave
        """
        key = self._get_disperser()
        eff = self._get_throughput(wave, key)
        return eff

    def get_internal_eff(self, wave):
        """
        Read in internal efficiency

        Parameters
        ----------
        wave: numpy.ndarray
            Wavelength vector to interpolate throughput onto

        Returns
        -------
        eff: numpy.ndarray or float
            Internal throughput as a function of wave
        """
        eff = self._get_throughput(wave, 'internal')
        return eff

    def get_detector_qe(self, wave):
        """
        Read in detector quantum efficiency. This will likely need to be
        overloaded on a per detector basis.

        Parameters
        ----------
        wave: numpy.ndarray
            Wavelength vector to interpolate throughput onto

        Returns
        -------
        qe: numpy.ndarray or float
            Quantum efficiency as a function of wave
        """
        qe = self._get_throughput(wave, self.qe_key)
        return qe

    def get_quantum_yield(self, wave):
        """
        Read in detector quantum yield if it's there. If not, return unity (trivial yield).

        Parameters
        ----------
        wave: numpy.ndarray
            Wavelength vector to interpolate throughput onto

        Returns
        -------
        quantum_yield: numpy.ndarray or float
            Quantum efficiency as a function of wave
        """
        q_yield = self._interp_refdata(wave, self.qe_key, colname='conversion', default=1.0)
        fano_factor = (3.0 * q_yield - q_yield**2. - 2.) / q_yield  # two level model, valid for quantum yield between 1 and ~2.
        return q_yield, fano_factor

    def get_total_eff(self, wave):
        """
        Calculate combined throughput of entire telescope/instrument/detector system

        Parameters
        ----------
        wave: numpy.ndarray
            Wavelength vector to interpolate throughput onto

        Returns
        -------
        eff: numpy.ndarray or float
            Total system throughput as a function of wave
        """
        ote_int = self.telescope.get_ote_eff(wave)
        filter_eff = self.get_filter_eff(wave)
        disperser_eff = self.get_disperser_eff(wave)
        internal_eff = self.get_internal_eff(wave)
        det_qe = self.get_detector_qe(wave)

        eff = ote_int * filter_eff * disperser_eff * internal_eff * det_qe
        return eff

    def get_dispersion(self, wave):
        """
        Read in dispersion

        Parameters
        ----------
        wave: numpy.ndarray
            Wavelength vector to interpolate/trim dispersion data onto

        Returns
        -------
        dispersion: numpy.ndarray or float
            Dispersion as a function of wave
        """
        disperser = self._get_disperser()
        if disperser is not None:
            key = self._get_dispersion_key()
            dispersion = self._interp_refdata(wave, key, colname='dlds', default=DEFAULT_DISPERSION)
        else:
            dispersion = 0.0
        return dispersion

    def get_trace(self, wave):
        """
        Implement spectral traces, wavelength-dependent shifts of the spatial axis.  This base implementation only returns
        an array of 0's of the appropriate size.  This is to make the code implementation of this fully general.
        Instruments that need to account for such spatial distortions will need to overload this to load and implement
        the appropriate reference data.

        Parameters
        ----------
        wave: numpy.ndarray
            Wavelength vector to interpolate/trim trace data onto

        Returns
        -------
        trace: numpy.ndarray or float
            Spectral trace offset from center of FOV as a function of wave
        """
        trace = np.zeros_like(wave)

        return trace

    def get_detector_pixels(self, wave):
        """
        Read in detector pixel positions for each wavelength in wave_pix

        Parameters
        ----------
        wave: numpy.ndarray
            Wavelength vector to interpolate/trim pixel position data onto

        Returns
        -------
        pixels: numpy.ndarray or None
            Detector pixel positions corresponding to each element of wave
        """
        disperser = self._get_disperser()
        if disperser is not None:
            key = "%s_wavepix" % disperser
            try:
                pixels = self._interp_refdata(wave, key, colname='pixels', default=0.0)
            except DataError as e:
                pixels = None
        else:
            pixels = None
        return pixels

    def get_resolving_power(self, wave):
        """
        Read in resolving power

        Parameters
        ----------
        wave: numpy.ndarray
            Wavelength vector to interpolate resolving power onto

        Returns
        -------
        rpower: numpy.ndarray or None
            Resolving power as a function of wave
        """
        disperser = self._get_disperser()
        if disperser is not None:
            key = self._get_dispersion_key()
            rpower = self._interp_refdata(wave, key, colname='R', default=wave/(DEFAULT_DISPERSION*2))
        else:
            rpower = None
        return rpower

    def get_wave_blaze(self):
        """
        Get wavelength vector used in the grating efficiency (blaze) file

        Returns
        -------
        wave_blaze: numpy.ndarray
            Wavelength vector from the grating efficiency file
        """
        key = self._get_disperser()
        blaze_file = os.path.join(self.ref_dir, self.paths[key])
        msg = "Blaze file not found: %s" % blaze_file
        wave_blaze = ref_data_column(blaze_file, colname='wavelength', error_msg=msg)
        return wave_blaze

    def get_wave_filter(self):
        """
        Get wavelength vector used in the filter throughput file

        Returns
        -------
        wave_filter: numpy.ndarray
            Wavelength vector from the filter throughput file
        """
        key = self.instrument['filter']
        filter_file = os.path.join(self.ref_dir, self.paths[key])
        msg = "Filter file not found: %s" % filter_file
        wave_filter = ref_data_column(filter_file, colname='wavelength', error_msg=msg)
        return wave_filter

    def get_wave_pix(self):
        """
        Get wavelength vector to convert pixel position to wavelength

        Returns
        -------
        wavepix: numpy.ndarray
            Wavelength vector mapping pixels to wavelengths
        """
        # usually wavepix is lifted from the dispersion file, but in some cases (e.g. NIRISS SOSS)
        # there is a specific, calibrated mapping of wavelength to pixels. look for that first and then
        # fall back to the dispersion file.
        wavepix_key = "%s_wavepix" % self._get_disperser()
        if wavepix_key in self.paths:
            # if we have a specifically calibrated mapping of wavelengths to pixels (e.g. for SOSS),
            # look up that file and use that mapping.
            wavecal_file = os.path.join(self.ref_dir, self.paths[wavepix_key])
            msg = "Wavelength calibration file not found: %s" % wavecal_file
            wavepix = ref_data_column(wavecal_file, colname='wavelength', error_msg=msg)
        else:

            # in dispersion files, there is no guarantee that the table is sampled in pixel spacing. This information
            # is encoded in the dlds column so calculate it from there.
            key = self._get_dispersion_key()
            if key in self.paths:
                dispersion_file = os.path.join(self.ref_dir, self.paths[key])
                msg = "Dispersion file not found: %s" % dispersion_file
                wave = ref_data_column(dispersion_file, colname='wavelength', error_msg=msg)
                dlds = ref_data_column(dispersion_file, colname='dlds', error_msg=msg)
            else:
                # for spectroscopic order 0, there will be no dispersion file, and thus no reference in the
                # config.json path{} block.
                wave = self.get_wave_blaze()
                dlds = np.ones_like(wave) * DEFAULT_DISPERSION
            pixel = np.cumsum(1.0 / dlds * np.gradient(wave))
            pixel_integer = np.arange(int(pixel[0]), int(pixel[-1]))
            wavepix = np.interp(pixel_integer, pixel, wave)

        return wavepix

    def get_ipc_kernel(self):
        """
        Get inter-pixel capacitance (IPC) kernel

        Returns
        -------
        kernel: numpy.ndarray
            IPC kernel data
        """
        key = "ipc_kernel"
        ipc_file = os.path.join(self.ref_dir, self.paths[key])
        try:
            kernel = fits.getdata(ipc_file)
        except IOError as e:
            msg = "Error reading IPC kernel reference file: %s. " % ipc_file
            if self.webapp:
                msg += "(%s)" % type(e)
            else:
                msg += repr(e)
            raise DataError(value=msg)
        return kernel

    def read_detector_pars(self):
        """
        Return detector-specific parameters.

        This reads the JSON structure so values can be dependent on aperture, subarray
        readmode and/or instrument mode.

        Returns
        -------
        det_dict: dict
            A dictionary of the correct detector parameters
        """
        det_dict = {}

        for parameter_key in self.det_pars:
            parameter_value = self.read_config_param(self.det_pars,parameter_key)

            det_dict[parameter_key] = parameter_value

        return det_dict

    def get_variance_fudge(self, wave):
        """
        Some instruments (e.g. MIRI) have measured noise properties that are not well explained
        or modeled by Pandeia's current noise model. This method returns the multiplicative fudge factor
        that is to be applied to the pixel rate variance to match IDT expectations. The fudge factor can be
        chromatic so needs to accept an array of wavelengths to interpolate over. By default this returns
        a 1's array the same length as wave scaled by the 'var_fudge' scalar value defined in det_pars.

        Parameters
        ----------
        wave: 1D numpy.ndarray
            Wavelengths to interpolate chromatic variance over
        """
        det_pars = self.get_detector_pars()
        var_fudge = det_pars.get('var_fudge', 1.0) * np.ones(len(wave))
        return var_fudge

    def get_readnoise_correlation_matrix(self, shape):
        """
        Grab correlated readnoise data out of reference file and build a correlation
        matrix out of it.

        Parameters
        ----------
        shape: list-like

        Returns
        -------
        correlation_matrix: Scipy.sparse.csr_matrix
            Compressed sparse row correlation matrix
        """
        key = "rn_corr"
        correlation_file = os.path.join(self.ref_dir, self.paths[key])
        try:
            correlation = fits.getdata(correlation_file)
        except IOError as e:
            msg = "Error reading RN correlation reference file: %s. " % correlation_file
            if self.webapp:
                msg += "(%s)" % type(e)
            else:
                msg += repr(e)
            raise DataError(value=msg)

        nframe_range = correlation.shape[0]
        nx = correlation.shape[2]
        ny = correlation.shape[1]

        if nx != ny:
            message = 'Only square correlation matrices are supported.'
            raise UnsupportedError(value=message)

        if self.exposure_spec.nframe > nframe_range:
            # nframe longer than full range of correlation so use the full range
            corr_range = nframe_range
        else:
            # nframe shorter than range of correlation so use subset of correlation data
            corr_range = self.exposure_spec.nframe
        correlation_data = sparse.csr_matrix(correlation[corr_range, :, :])

        empty_matrix = sparse.coo_matrix((1024, 1024))
        correlation_matrix = sparse.bmat([[empty_matrix, None, empty_matrix],
                                          [None, correlation_data, None],
                                          [empty_matrix, None, empty_matrix]])
        correlation_matrix = sparse.csr_matrix(correlation_matrix)

        return correlation_matrix

    def get_exposure_pars(self, name="pattern_name"):
        """
        Define exposure parameters from instrument and environment.

        Parameters
        ----------
        name: str
            Optional name to assign ExposureSpecification instance

        Returns
        -------
        exposure_spec: pandeia.engine.exposure.ExposureSpecification instance
            Exposure parameters encapsulated within ExposureSpecification instance
        """
        # These are values that get set when the Instrument is instantiated, either from defaults
        # or passed configuration data.
        readmode = self.detector["readmode"]
        subarray = self.detector["subarray"]
        ngroup = self.detector["ngroup"]
        nexp = self.detector["nexp"]
        nint = self.detector["nint"]

        det_type = self.get_detector_pars()['det_type']

        # These are defined by the Instrument's reference data as Instrument properties.
        tframe = self.subarray_config['default'][subarray]["tframe"]
        tfffr = self.subarray_config['default'][subarray]["tfffr"]
        if readmode in self.subarray_config and subarray in self.subarray_config[readmode]:
            tframe = self.subarray_config[readmode][subarray]["tframe"]
            tfffr = self.subarray_config[readmode][subarray]["tfffr"]
        nframe = self.readmode_config[readmode]["nframe"]
        nskip = self.readmode_config[readmode]["nskip"]

        # If these are trivial, we don't have to define them.
        if "nsample" in self.readmode_config[readmode]:
            nsample = self.readmode_config[readmode]["nsample"]
            nsample_skip = self.readmode_config[readmode]["nsample_skip"]
        else:
            nsample = 1
            nsample_skip = 0

        # Going from general to specific: start with the default reset values, then check the defaults, then check
        # the actual readmode for this subarray. Use the most appropriate reset values for this setup, otherwise
        # the defaults
        nreset1 = 1
        nreset2 = 1
        if "nreset1" in self.subarray_config['default'][subarray]:
            nreset1 = self.subarray_config['default'][subarray]["nreset1"]
            nreset2 = self.subarray_config['default'][subarray]["nreset2"]
        if readmode in self.subarray_config and subarray in self.subarray_config[readmode]:
            if "nreset1" in self.subarray_config[readmode][subarray]:
                nreset1 = self.subarray_config[readmode][subarray]["nreset1"]
                nreset2 = self.subarray_config[readmode][subarray]["nreset2"]


        # These are defined in the reference data as "ramp_config" and apply to a whole instrument
        nprerej = self.read_config_param(self.ramp_config, "nprerej")
        npostrej = self.read_config_param(self.ramp_config, "npostrej")

        # We allow alternate ways to derive a signal from a detector slope,
        # but multiaccum is the default if no mode is provided. Slopemode
        # must be matched with a corresponding ExposureSpecification class.

        slopemode = self.detector.get("slopemode", "multiaccum")

        if slopemode == "multiaccum":
            exposure_spec = exp.ExposureSpecification(
                name,
                ngroup,
                nint,
                nexp,
                tframe,
                nframe=nframe,
                subarray=subarray,
                nskip=nskip,
                nsample=nsample,
                nsample_skip=nsample_skip,
                nprerej=nprerej,
                npostrej=npostrej,
                nreset1=nreset1,
                nreset2=nreset2,
                det_type=det_type,
                tfffr=tfffr
            )
        elif slopemode == "target_acq":
            ngroup_extract = self.detector["ngroup_extract"]
            exposure_spec = exp.ExposureSpecificationTA(
                name,
                ngroup,
                ngroup_extract,
                nint,
                nexp,
                tframe,
                nframe=nframe,
                subarray=subarray,
                nskip=nskip,
                nsample=nsample,
                nsample_skip=nsample_skip,
                nprerej=nprerej,
                npostrej=npostrej,
                nreset1=nreset1,
                nreset2=nreset2,
                det_type=det_type,
                tfffr=tfffr
            )
        else:
            msg = "%s is not a valid slope mode." % (slopemode)
            raise DataConfigurationError(value=msg)


        return exposure_spec

    def read_config_param(self, item, parameter_key):
        """
        Some instrument parameters are dependent on the specifics of detector or instrument setup. This is a generic
        function to pull the correct values out of a dictionary block.

        This is meant to work on dictionaries that are not themselves broken into different filters, gratings, or
        readmodes; it's for what would otherwise be a flat dictionary of configuration values, like det_pars.

        Values that depend on multiple parameters can be used; the key_format list will contain both parameters and
        the options will contain both relevant values concatenated by "__"

        An example of what a dictionary to be parsed would look like:
        "det_pars": {
            "det_type": "h2rg",
            "dark_current": 0.00636,
            "excessp1": 0.0,
            "excessp2": 0.0,
            "ff_electrons": 62500,
            "fullwell": {
    			"default": 65000.0,
    			"key_format": ["subarray", "readmode"],
    			"full__nrsrapid": 30000.0,
    			"s200a1__nrs": 22000.0
    		},
            "ipc": true,
            "mingroups": 2,
            "pix_size": 18.0,
            "rn": {
    			"default": 16.8,
    			"key_format": ["aperture"],
    			"sw": 17
    		},
            "rn_correlation": true
        }

        item: dict
            Dictionary within which we need to search for the correct detector configuration parameter.
        parameter_key: string
            The parameter we want to search for

        returns: string, int, float, or bool
             The value of parameter_key for the given instrument and detector setup.
        """

        value_lookup = {
            'detector': self.detector_key,
            'aperture': self.instrument['aperture'],
            'subarray': self.detector['subarray'],
            'readmode': self.detector['readmode'],
            'instmode': self.instrument['mode']
        }

        if parameter_key in item:
            if not isinstance(item[parameter_key], dict):
                # If the field exists and is not a dict then just return the value
                parameter_value = item[parameter_key]

            elif isinstance(item[parameter_key], dict) and 'key_format' in item[parameter_key]:
                # If the field exists and it is a dict then we have to check the key_format
                # In this case the format of the parameter will be something like:
                # "rn": {
                #     "default": 16.8,
                #     "key_format": ["aperture"],
                #     "sw": 17
                # },

                # Create the key lookup
                key_lookup = []
                for kf in item[parameter_key]['key_format']:
                    kfelement = kf.split('__')
                    for kfe in kfelement:
                        try:
                            key_lookup.append(value_lookup[kfe])
                        except KeyError as e:
                            raise DataError(
                                "Unknown key format {} value {} listed in {}".format(kfe, value_lookup[kfe],
                                                                                     item[parameter_key]))

                # Now squish the list to a "__" separated key and see if it exists
                # If all required keys were passed in, then create the string lookup.
                # If the string is present in the dict, return it.
                if not any([x is None for x in key_lookup]):
                    key_lookup = '__'.join(key_lookup)

                    if key_lookup in item[parameter_key]:
                        parameter_value = item[parameter_key][key_lookup]

                    # If the key_lookup was not present then just return the default.
                    elif "default" in item[parameter_key]:
                        parameter_value = item[parameter_key]['default']
                    else:
                        raise DataError("There is no default value in {}".format(item[parameter_key]))
            else:
                raise DataError("Improperly formatted parameter {}".format(item))
        else:
            raise DataError("There is no {} key in {}".format(parameter_key, item))

        return parameter_value

    def get_aperture_pars(self):
        """
        Collect instrument aperture parameters into a dict and return it

        Returns
        -------
        aperture_dict: dict
            Contains the following parameters describing the instrument aperture:
                disp - size of aperture in dispersion direction (X-axis)
                xdisp - size of aperture perpindicular to dispersion (Y-axis)
                disp_pitch - distance between adjacent apertures in the dispersion direction
                             (None unless a multi-shutter instrument)
                xdisp_pitch - distance between adjacent apertures in the cross-dispersion direction
                              (None unless a multi-shutter instrument)
                pix - pixel scale in arcsec/pixel
                nslice - number of slices the aperture is divided into
        """
        aperture = self.get_aperture()
        if "disp" in self.aperture_config[aperture]:
            disp = self.aperture_config[aperture]["disp"]
            xdisp = self.aperture_config[aperture]["xdisp"]
            nslice = self.aperture_config[aperture]["nslice"]

            """
            For multi-shutter instruments, the shutter aperture size can be smaller than the offset between the
            individual shutters (the pitch). If so, the pitch should be provided in the instrument configuration.
            """
            if "disp_pitch" in self.aperture_config[aperture]:
                try:
                    disp_pitch = self.aperture_config[aperture]['disp_pitch']
                    xdisp_pitch = self.aperture_config[aperture]['xdisp_pitch']
                except KeyError as e:
                    raise DataError("Malformed config file: missing entry for shutter pitch (%s)" % e)
            else:
                """
                If the pitch is not on the config, assume it is the same as the shutter/aperture size.
                """
                disp_pitch = disp
                xdisp_pitch = xdisp

            if "slitlet_shape" in self.instrument:
                slitlet_shape = self.instrument['slitlet_shape']
                """
                The shutter pattern user input is in units of shutter pitch, so convert to internal angular units here.
                """
                multishutter = [(disp_pitch * shutter[0], xdisp_pitch * shutter[1]) for shutter in slitlet_shape]
            else:
                multishutter = None

        else:
            disp = None
            xdisp = None
            disp_pitch = None
            xdisp_pitch = None
            nslice = None
            multishutter = None

        pix = self.aperture_config[aperture]["pix"]

        aperture_dict = {
            'disp': disp,
            'xdisp': xdisp,
            'multishutter': multishutter,
            'pix': pix,
            'nslice': nslice
        }
        return aperture_dict

    def get_wave_range(self):
        """
        Get the wavelength range of the current instrument configuration. The wavelength
        range information is organized in the configuration files on a per aperture basis.

        Returns
        -------
        range_dict: dict
            Contains the instrument wavelength range in microns described by:
                wmin - minimum wavelength
                wmax - maximum wavelength
        """
        disperser = self._get_disperser()
        aperture = self.instrument['aperture']
        filt = self.instrument['filter']

        # if disperser is defined and there are range entries for it, it takes precendence
        # For multiorder projections, we need to scan through a number of dispersion orders, named disperser_n in the
        # ranges section of the configuration file:
        if self.projection_type in "multiorder":
            wmins = []
            wmaxes = []
            for disp in self.range[aperture]:
                # make sure this is one of the disperser's ranges.
                if disperser in disp:
                    wmins.append(self.range[aperture][disp]["wmin"])
                    wmaxes.append(self.range[aperture][disp]["wmax"])
            # get the min of mins and max of maxes
            wmin = min(wmins)
            wmax = max(wmaxes)
        elif disperser is not None and disperser in self.range[aperture]:
            wmin = self.range[aperture][disperser]["wmin"]
            wmax = self.range[aperture][disperser]["wmax"]
        # if filter is defined and has range entries, use it next
        elif filt is not None and filt in self.range[aperture]:
            # Possibility for dependency of the filter on the wavelength range.
            wmin = self.range[aperture][filt]["wmin"]
            wmax = self.range[aperture][filt]["wmax"]
        # otherwise fall back to the generic range for the current aperture
        else:
            wmin = self.range[aperture]["wmin"]
            wmax = self.range[aperture]["wmax"]

        # now check wmin and wmax against wave_pix for sanity, if applicable
        if self.projection_type in ('slitless', 'spec'):
            wave_pix = self.get_wave_pix()
            wmin = max(wmin, wave_pix.min())
            wmax = min(wmax, wave_pix.max())

        range_dict = {"wmin": wmin, "wmax": wmax}
        return range_dict

    @property
    def projection_type(self):
        """
        Determine the appropriate projection type based on the configured instrument mode

        Returns
        -------
        proj_type: str
            The projection type, currently one of 'slitless', 'spec', or 'image'.
        """
        mode = self.mode
        slitless_modes = self.telescope.slitless_modes
        spec_modes = self.telescope.spec_modes
        image_modes = self.telescope.image_modes
        if hasattr(self.telescope, 'multiorder_modes'):
            multiorder_modes = self.telescope.multiorder_modes
        else:
            multiorder_modes = []

        if mode in slitless_modes:
            proj_type = 'slitless'
        if mode in spec_modes:
            proj_type = 'spec'
        if mode in image_modes:
            proj_type = 'image'
        if mode in multiorder_modes:
            proj_type = 'multiorder'
        return proj_type

    def dispersion_axis(self):
        """
        The dispersion axis is either along rows (the X axis) or along columns (Y axis).  By default
        it is along the X axis.  Instrument subclasses will overload this method to deal with cases
        where it is along the Y axis (e.g. NIRISS GR150C).

        Returns
        -------
        disp_axis: str
            Axis along with spectra are dispersed.  Allowed values are 'x' or 'y'.
        """
        disp_axis = "x"
        return disp_axis

    def get_pix_size(self):
        """
        Shortcut to get the size of the pixels in the current observing mode/aperture combination.

        Returns
        -------
        pix_size: float
            The pixel scale in arcsec/pixel
        """
        aperture_dict = self.get_aperture_pars()
        pix_size = aperture_dict['pix']
        return pix_size

    def get_exposure_time(self):
        """
        Shortcut to get the total on-source time for the current detector configuration

        Returns
        -------
        time: float
            Total on-source time in seconds
        """
        time = self.exposure_spec.exposure_time
        return time

    def create_gap_mask(self, wave):
        """
        Use the gap configuration and a wavelength vector, wave, to build a masked array that
        masks out the location of the gap.  Wavelengths between and including both gap endpoints
        will be masked out.

        For now this is a stub and instrument subclasses are expected to overload this to provide
        a gap mask.  Currently only NIRSpec does this.

        Parameters
        ----------
        wave: numpy.ndarray
            Wavelength vector to construct mask from

        Returns
        -------
        mask: float (default: 1.0)
            1D array masked at the locations within the configured detector gap and 1.0 elsewhere
        """
        return 1.0

    def spectrometer_convolve(self, spec):
        """
        This method convolves a spectrum with a wavelength-dependent spectral
        resolving power R=lambda/delta lambda, where delta lambda is the FWHM of an
        unresolved line at a wavelength lambda. This is accomplished by internally
        changing the sampling of the spectrum, such that delta-lambda is sampled by
        exactly a constant number of samples as a function of wavelength. The convolution
        is then accomplished using the convolution theorem and knowledge that the kernel is
        independent of wavelength.

        Parameters
        ----------
        spec: pandeia.engine.astro_spectrum.AstroSpectrum instance
            The input spectrum to convolve

        Returns
        -------
        spec: pandeia.engine.astro_spectrum.AstroSpectrum instance
            Same dimensions as input spec, but now convolved according to the wavelength-dependent resolving
            power of the instrument, if applicable.  Same as the input spec in the case of no dispersion (i.e. imaging).
        """
        r = self.get_resolving_power(spec.wave)
        if r is None:
            # no dispersion defined so return unmolested spectrum
            return spec

        # find the minimum spacing between wavelengths
        dws = np.abs(spec.wave - np.roll(spec.wave, 1))
        dw_min = np.min(dws)
        dw_arg = np.argmin(dws)

        # check that the minimum spacing is not too small, as this can lead to huge arrays. We will not
        # support sampling better than 2e5 (1e5 is the highest current resoling power of any IR spectrometer).
        if (spec.wave[dw_arg]/dw_min>self.telescope.minimal_spectral_spacing):
            dw_min = spec.wave[dw_arg]/self.telescope.minimal_spectral_spacing
            key = 'spectral_resampling_too_small'
            self.warnings[key] = "Spectrum for source {} has been resampled to a spacing " \
                                 "of {} microns for performance reasons. This is smaller" \
                                 " than the minimum spectral resolution {}.".format(
                self.inst_name,
                spec.wave[dw_arg] / dw_min,
                self.telescope.minimal_spectral_spacing
            )

        fwhm = spec.wave / r  # FWHM of resolution element as a function of wavelength
        fwhm_s = np.min(fwhm / dw_min)  # find min of FWHM expressed in units of minimum spacing (i.e. sampling)

        # but do not allow the sampling FWHM to be less than Nyquist
        fwhm_s = np.max([2., fwhm_s])

        # divide FWHM(wave) by the FWHM of the sampling to get sampling as a function of wavelength
        ds = fwhm / fwhm_s

        # use the min as a starting point; initialize array
        w = np.min(spec.wave)

        # it's much faster (~50%) to append to lists than np.array()'s
        wave_constfwhm = []

        # doing this as a loop is slow, but straightforward.
        while w < np.max(spec.wave):
            # use interpolation to get delta-wavelength from the sampling as a function of wavelength.
            # this method is over 5x faster than the original use of scipy.interpolate.interp1d.
            w += np.interp(w, spec.wave, ds)
            wave_constfwhm.append(w)

        wave_constfwhm.pop()  # remove last point which is an extrapolation
        wave_constfwhm = np.array(wave_constfwhm)

        # interpolate the flux onto the new wavelength set
        flux_constfwhm = spectrum_resample(spec.flux, spec.wave, wave_constfwhm)

        # convolve the flux with a gaussian kernel; first convert the FWHM to sigma
        sigma_s = fwhm_s / 2.3548
        try:
            # for astropy < 0.4
            g = Gaussian1DKernel(width=sigma_s)
        except TypeError:
            # for astropy >= 0.4
            g = Gaussian1DKernel(sigma_s)

        # use boundary='extend' to set values outside the array to nearest array value.
        # this is the best approximation in this case.
        flux_conv = convolve(flux_constfwhm, g, normalize_kernel=True, boundary='extend')
        flux_oldsampling = np.interp(spec.wave, wave_constfwhm, flux_conv)

        spec.flux = flux_oldsampling
        return spec
