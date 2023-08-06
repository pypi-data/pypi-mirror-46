# Licensed under a 3-clause BSD style license - see LICENSE.rst
from __future__ import division, absolute_import

import numpy as np
import numpy.ma as ma
from .custom_exceptions import EngineInputError
from .constants import SLOPE_CLIP


class ExposureSpecification:

    """
    Encapsulates all data associated with exposure specification
    """

    def __init__(self, pattern, ngroup, nint, nexp, tframe, nframe=1, nsample=1, nsample_skip=0, tfffr=0,
                 subarray='Full', nskip=0, nprerej=0, npostrej=0, nreset1=1, ndrop1=0, ndrop3=0, nreset2=1,
                 frame0=False, det_type='h2rg'):
        """
        Create a generic Exposure Specification.

        Inputs
        ------
        pattern: str
            name of readout pattern

        ngroup: int
            number of groups per integration

        nint: int
            number of integrations per exposure

        nexp: int
            number of exposures

        tframe: float
            number of seconds per frame

        nframe: int (optional, default 1)
            number of frames per group

        nsample: int (optional, default 1)
            number of samples averaged while reading a single pixel.
            Used by MIR detectors.

        nsample_skip: int (optional, default 0)
            number of samples skipped while reading a single pixel.
            Used by MIR detectors.

        tfffr: float
            Extra time factor

        subarray: str (optional, default 'Full')
            name of subarray to be read.
            If None, readout is full frame

        nskip: int (optional, default 0)
            number of skipped frames per group. Only
            supported by some readout patterns.

        nprerej: int (optional, default 0)
            The MIR detectors (i.e. MIRI) may reject the first and/or last groups of a ramp.

        npostrej: int (optional, default 0)
            Number of rejected frames at the end of the integration

        nreset1: int (optional, default 1)
            Number of reset frames before the integration starts

        ndrop1: int (optional, default 0)
            Number of frames dropped at the beginning of an integration

        ndrop3: int (optional, default 0)
            Number of frames dropped at the end of an integration

        nreset2: int (optional, default 1)
            Number of reset frames after the integration ends

        frame0: bool (optional, default False)
            Some instruments can downlink the frame0 read. Set to True if frame0 is used in the ramp fit.

        det_type: string
            Detector type, used to determine timing calculation types.

        """

        # Eventually we might do some value checking at this point
        # to ensure that the specified values are consistent with the
        # named pattern. For now, pattern is unused.

        # Required parameters
        self.det_type = det_type
        self.pattern = pattern
        self.ngroup = ngroup
        self.nint = nint
        self.nexp = nexp
        self.tframe = tframe
        self.tfffr = tfffr

        # Optional parameters
        self.nframe = nframe
        self.subarray = subarray
        self.nskip = nskip
        self.nprerej = nprerej
        self.npostrej = npostrej
        self.nreset1 = nreset1
        self.nreset2 = nreset2
        self.ndrop1 = ndrop1
        self.ndrop3 = ndrop3
        self.nsample = nsample
        self.nsample_skip = nsample_skip
        self.frame0 = frame0

        if det_type == 'sias':
            self.get_times_mir()
            # This is where we adjust values so we can still use the same
            # MULTIACCUM formula as for the NIR detectors. We need the effective
            # "average time per sample" for MIRI.
            self.tsample = self.tframe / (self.nsample + self.nsample_skip)
            # 'nsample_total' for MIRI is the total number of non-skipped samples X number of averaged frames.
            # Note that in practice, it currently never happens that both the number of samples and number of
            # averaged frames are >1 (i.e., no SLOWGRPAVG exists). However, this will deal with that situation,
            # should it occur.
            self.nsample_total = self.nframe * self.nsample

        elif det_type == 'h2rg':
            self.get_times_nir()
        else:
            raise ValueError('Unknown detector type %s' % (det_type))

        # Derived quantities
        self.nramps = self.nint * self.nexp

    def get_times_nir(self):
        """
        The time formulae are defined in Valenti et al. 2017, JWST-STScI-006013

        The equations in this method are duplicated in the front-end
        (workbook.js, update_detector_time_labels function). Please ensure
        that changes to these equations are reflected there.
        """
        self.tgroup = self.tframe * (self.nframe + self.nskip)

        # Equation 4
        self.measurement_time = self.tframe * self.nint * ((self.ngroup - 1) * (self.nframe + self.nskip))
        # Equation 5
        if self.frame0:
            self.measurement_time += 0.5 * self.nint * self.tframe * self.nframe

        # Equation 1
        self.exposure_time = (self.tfffr * self.nint) + self.tframe * (self.nreset1 + (self.nint - 1) * self.nreset2 +
                                self.nint * (self.ndrop1 + (self.ngroup - 1) * (self.nframe + self.nskip) +
                                self.nframe + self.ndrop3))
        # Equation 7
        self.saturation_time = self.tfffr + self.tframe * (self.ndrop1 +
                               (self.ngroup - 1) * (self.nframe + self.nskip) + self.nframe)

        self.duty_cycle = self.measurement_time / self.exposure_time
        self.total_exposure_time = self.nexp * self.exposure_time
        self.total_integrations = self.nexp * self.nint

    def get_times_mir(self):
        """
        The time formulae are defined in Valenti et al. 2017, JWST-STScI-006013. Note that we have to subtract the
        groups that are rejected (by the pipeline) from the measurement time (nprerej+npostrej). The saturation time
        conservatively considers the ramp saturated even if saturation occurs in a rejected frame.

        The equations in this method are duplicated in the front-end
        (workbook.js, update_detector_time_labels function). Please ensure
        that changes to these equations are reflected there.
        """

        self.tgroup = self.tframe * (self.nframe + self.nskip)

        # Valenti et al. 2017 defines the very bright regime for MIRI as ngroup>=5.
        # This could eventually be pulled out to data, rather than hardcoded.
        # Equation 6
        if self.ngroup >= 5:
            self.measurement_time = self.nint * (self.ngroup - 1 - (self.nprerej + self.npostrej)) * self.tgroup
        else:
            # very bright regime
            # Equation 10
            self.measurement_time = self.nint * (self.tfffr + self.ngroup * self.tgroup) \
                - self.nint * self.tframe * 0.5 * (self.nframe - 1)

        # Equation 3
        self.exposure_time = self.nint * (self.tfffr + self.ngroup * self.nframe * self.tframe)
        # Equation 8
        self.saturation_time = self.tfffr + self.ngroup * self.nframe * self.tframe

        self.duty_cycle = self.measurement_time / self.exposure_time
        self.total_exposure_time = self.nexp * self.exposure_time

        self.total_integrations = self.nexp * self.nint

    def get_unsaturated_groups(self, slope, fullwell, full_saturation=2):
        """
        Calculate the number of unsaturated groups in each pixel, given a specified slope and full well value.
        There is a minimum sensible value of unsaturated number of groups that defines full saturation.
        The default is 2, but this can potentially be set to a higher value, or even 1(!) for certain observing modes.
        It is not expected that a value of 0 can ever be anything but saturated.

        Parameters
        ----------
        slope: ndarray
            The measured slope of the ramp (ie, the rate) per pixel

        fullwell: positive integer
            The number of electrons defining a full well (beyond which the pixel reads become unusable for science
            due to saturation).

        full_saturation: positive integer
            The minimum number of groups allowed to define an unsaturated measurement.

        Returns
        -------
        unsat_ngroups: MaskedArray
            The number of unsaturated groups present in the ramp. The mask separates pixels that have full saturation
            from those that do not. The former will not have a valid noise measurement and cannot be used in a strategy.

        """

        # get the number of groups to saturation
        ngroups_to_sat = self.get_groups_before_sat(slope, fullwell)

        # the number of unsaturated groups is clipped by the ngroups_to_sat value for every pixel
        max_ngroups = ngroups_to_sat.clip(0,self.ngroup)

        # Mask values that are fully saturated - if the maximum before saturation is less than full_saturation, it's
        # clearly saturated.
        unsat_ngroups = ma.masked_less(max_ngroups, full_saturation)

        return unsat_ngroups

    def get_groups_before_sat(self, slope, fullwell):
        """
        This method returns a map of the maximum number of groups each pixel can be exposed to, before saturation.
        The formula is calculated by equating the time-to-saturation to the saturation time formula and isolating
        ngroup. The resulting fractional value is then rounded down to an integer.

        These equations are derived by setting saturation_time = time_to_saturation in equation 7 (for NIR H2RG
        detectors) or equation 8 (for MIR SiAs detectors) of the timing document, Valenti et al. 2017,
        JWST-STScI-006013, and solving for n_groups.

        Technically speaking, we are getting the groups BEFORE saturation by rounding the number of groups down to the
        nearest integer. If groups_before_sat is EXACTLY an integer (which is unlikely), we will get one partially
        saturated pixel.

        Parameters
        ----------
        slope: ndarray
            The measured slope of the ramp (ie, the rate) per pixel

        fullwell: positive integer
            The number of electrons defining a full well (beyond which the pixel reads become unusable for science
            due to saturation).
        """
        # we clip to 1e-10 to avoid division by zero errors even if the slope is tiny.
        time_to_saturation = fullwell / slope.clip(SLOPE_CLIP, np.max(slope))
        if self.det_type == 'sias':
            groups_before_sat = (time_to_saturation - self.tfffr) / (self.nframe * self.tframe)
        elif self.det_type == 'h2rg':
            groups_before_sat = (((time_to_saturation - self.tfffr) / self.tframe) - self.nframe) / (self.nframe +
                                                                                                     self.nskip) + 1.
        else:
            raise ValueError('Unknown detector type %s' % (self.det_type))
        # The groups_before_sat value should never be less than 0 - that would imply saturation before we started
        # collecting any photons.
        groups_before_sat = np.maximum(groups_before_sat,np.zeros_like(groups_before_sat))

        return np.floor(groups_before_sat)

    def get_saturation_fraction(self, slope, fullwell):
        """
        This method returns a map of the fraction of saturation that each pixel reaches, given the current
        exposure setup.

        Parameters
        ----------
        slope: ndarray
            The measured slope of the ramp (ie, the rate) per pixel

        """
        # we clip to 1e-10 to avoid division by zero errors even if the slope is tiny.
        return self.saturation_time / (fullwell / slope.clip(SLOPE_CLIP, np.max(slope)))

    def slope_variance(self, rate, dark_current, readnoise, unsat_ngroups,
                       rn_fudge=1.0, excessp1=0.0, excessp2=0.0):
        """
        Calculate the variance of a specified MULTIACCUM slope.

        Inputs
        ------
        rate: ndarray
            The measured slope of the ramp (ie, the rate) per pixel
            This can be a one-dimensional wavelength spectrum (for a 1D ETC)
            or a three-dimensional cube ([wave,x,y] for a 3D ETC).

        dark_current: float
            Dark current (electrons/s).

        readnoise: float
            Readnoise per pixel.

        unsat_ngroups: ndarray
            Number of unsaturated groups for each pixel

        rn_fudge: float
            Fudge factor to apply to readnoise to match IDT results

        excessp1: float
             empirical correction for excess variance for long ramps

        excessp2: float
             empirical correction for excess variance for long ramps

        Returns
        -------
        slope_var: ndarray
            Variance associated with the input slope.
        slope_rn_var: ndarray
            The associated variance of the readnoise only
        """

        # Rename variables for ease of comparison with Robberto (35).
        # The noise calculation depends on the pixel rate BEFORE IPC convolution. fp_pix_variance takes that pre-IPC
        # rate and scales it by the quantum yield and Fano factor to get the per-pixel variance in the electron rate.
        variance_per_pix = rate['fp_pix_variance']

        rn = readnoise

        # we discard any saturated groups. Copy unsat_ngroups, because we may modify it for rejected groups before using
        # it for noise calculations.
        n = ma.copy(unsat_ngroups)

        # removing with any pre- and post-rejected groups here. This is not stictly directly related to saturation, bu
        # behaves in a similar way (if there is <2 groups available, we cannot define a slope). The very bright regime
        # in which groups are not rejected can be implemented (in parts) by setting nprerej=npostrej=0.
        # Important: frames are not rejected in the Very Bright Regime (self.ngroup<5).
        # Therefore we disable it here in that regime.
        if ((self.nprerej != 0) or (self.npostrej != 0)) and (self.ngroup>=5):
            # If a group is already rejected because of saturation, there is no need to reject another at the end of
            # the ramp.
            unsat_pixels = (self.ngroup-np.ceil(n))<self.npostrej
            n[unsat_pixels] -= self.nprerej
            # we do have to reject any post-rejected frames from all pixels
            n -= self.npostrej

        # maybe nsample_sample_total and tsample are defined. If so then use them for the effect frame time and number
        # of reads (Issue #2996)
        # This is similar to two other places in this file
        if hasattr(self, 'nsample_total') and hasattr(self, 'tsample'):
            m = self.nsample_total
            tframe = self.tsample
        else:
            m = self.nframe # This does not include skipped frames!
            tframe = self.tframe

        tgroup = self.tgroup

        # Compute the variance of a MULTIACCUM slope using Robberto's formula (35). The rn_variance is also
        # calculated using the unsaturated number of groups.
        slope_rn_var = self.rn_variance(rn, unsat_ngroups=n, rn_fudge=rn_fudge, excessp1=excessp1, excessp2=excessp2)
        # The final slope variance slope may also be worse than the theoretical best value.
        # (also from Glasse et al. 2015, PASP 127 686).
        slope_var = (6. / 5.) * (n ** 2. + 1.) / (n * (n ** 2. - 1.)) * \
            ((variance_per_pix + dark_current) / tgroup) * \
            (1. - (5. / 3.) * (m ** 2. - 1.) / (m * (n ** 2. + 1.)) * (tframe / tgroup)) + \
            slope_rn_var

        # The default fill value for masked arrays is a finite number, so convert to ndarrays, and fill with NaNs
        # to make sure missing values are interpreted as truly undefined downstream.

        slope_var = ma.filled(slope_var, fill_value=np.nan)
        slope_rn_var = ma.filled(slope_rn_var, fill_value=np.nan)

        return slope_var, slope_rn_var

    def rn_variance(self, readnoise, unsat_ngroups=None, rn_fudge=1.0, excessp1=0.0, excessp2=0.0):
        """
        Calculate the variance due to read noise only.

        Inputs
        ------
        readnoise: float
          Readnoise per pixel.

        unsat_ngroups: ndarray
           The number of unsaturated groups.

           If unsat_ngroups not supplied, the approximation is that the read noise is
           negligible for pixels with signal rates high enough to saturate in part of the ramp.
           This is probably always a good approximation.

        readnoise: float
          Readnoise per pixel.

        rn_fudge: float
            fudge factor for readnoise on the slope as it may be worse than the theoretical best value

        excessp1: float
             empirical correction for excess variance for long ramps

        excessp2: float
             empirical correction for excess variance for long ramps

        Returns
        -------
        var_rn: ndarray if unsat_ngroups is supplied, float if unsat_ngroups is not supplied.
           Variance associated with the read noise only.

        """
        if unsat_ngroups is None:
            n = self.ngroup - (self.nprerej + self.npostrej)
        else:
            n = unsat_ngroups

        # It was decided that only one of the fudge factors are allowed to be used, not both.
        # Issue #2261#issuecomment-260737726
        if rn_fudge != 1.0 and (excessp1 != 0.0 or excessp2 != 0.0):
            raise ValueError('Only one of rn_fudge or excessp1/p2 maybe used, not both.')

        rn = readnoise

        # maybe nsample_sample_total is defined. If so then use them for the effect frame time and number of reads
        # Issue #2996
        # This is similar to two other places in this file
        if hasattr(self, 'nsample_total'):
            m = self.nsample_total
        else:
            m = self.nframe # This does not include skipped frames!

        tgroup = self.tgroup

        var_rn = 12. * rn ** 2. / (m * n * (n ** 2. - 1.) * tgroup ** 2.)

        # The readnoise on the slope may be worse than the theoretical best value
        # (see Glasse et al. 2015, PASP 127 686).
        if rn_fudge != 1:
            var_rn *= rn_fudge

        # Include the empirical correction for excess variance for long ramps
        # (Issue #2091)
        if excessp1 != 0.0 or excessp2 != 0.0:
            excess_variance = (12.0 * (n-1)/(n+1) * excessp1**2 - excessp2/np.sqrt(m)) / ((1 - n) * tgroup)**2
            var_rn += excess_variance
        return var_rn


class ExposureSpecificationTA(ExposureSpecification):

    """
    Target acquisition uses a special exposure specification and noise formula. Readout patterns have the same
    model as a regular MULTIACCUM exposure.

    Pontoppi 2017 Technical Report, SOCCER number tbd
    """

    def __init__(self, pattern, ngroup, ngroup_extract, nint, nexp, tframe, nframe=1, nsample=1, tfffr=0,
                 nsample_skip=1, subarray='Full', nskip=0, nprerej=0, npostrej=0, nreset1=1, ndrop1=0, ndrop3=0,
                 nreset2=1, det_type='h2rg'):
        """
        Create a Target Acquisition Exposure Specification.

        Inputs
        ------
        pattern: str
            name of readout pattern

        ngroup: int
            number of groups per integration

        ngroup_extrac: int
            number of groups actually used by the TA script (it ignores most of them). 3 is a
            common value. Note that this has to be <ngroup.

        nint: int
            number of integrations per exposure

        nexp: int
            number of exposures

        tframe: float
            number of seconds per frame

        nframe: int (optional, default 1)
            number of frames per group

        nsample: int (optional, default 1)
            number of samples averaged while reading a single pixel.
            Used by MIR detectors.

        nsample_skip: int (optional, default 0)
            number of samples skipped while reading a single pixel.
            Used by MIR detectors.

        subarray: str (optional, default 'Full')
            name of subarray to be read.
            If None, readout is full frame

        nskip: int (optional, default 0)
            number of skipped frames per group. Only
            supported by some readout patterns.

        nprerej: int (optional, default 0)
            The MIR detectors (i.e. MIRI) reject the first and last reads of a ramp (and maybe more eventually).
            For checking saturation, we need to handle them separately.  We need to account for signal accrued
            during frames rejected before the ramp, but don't care about the signal afterwards.

        npostrej: int (optional, default 0)
            Frames rejected after a ramp don't count towards saturation time, but need to be included in total exposure time.

        frame0: bool (optional, default False)
            Some instruments can downlink the frame0 read. Set to True if frame0 is used in the ramp fit.

        det_type: string (optional, default 'h2rg')
            Detector type, timing calculation is dependent on detector type

        """

        ExposureSpecification.__init__(self, pattern, ngroup, nint, nexp, tframe, nframe=nframe,
                 subarray=subarray, nskip=nskip, nsample_skip=nsample_skip, tfffr=tfffr,
                 nprerej=nprerej, npostrej=npostrej, nreset1=nreset1, ndrop1=ndrop1, ndrop3=ndrop3,
                 nreset2=nreset2, det_type=det_type)

        # Target acqs only use a subset of the groups
        self.ngroup_extract = ngroup_extract

    def slope_variance(self, rate, dark_current, readnoise, unsat_ngroups,
                       rn_fudge=1.0, excessp1=0.0, excessp2=0.0):
        """
        Calculate the slope variance

        Inputs
        ------
        rate: ndarray
            Rate

        dark_current: float


        readnoise: float
          Readnoise per pixel.

        unsat_ngroups: ndarray
           The number of unsaturated groups.

           If unsat_ngroups not supplied, the approximation is that the read noise is
           negligible for pixels with signal rates high enough to saturate in part of the ramp.
           This is probably always a good approximation.

        rn_fudge: float
            fudge factor for readnoise on the slope as it may be worse than the theoretical best value

        excessp1: float
             empirical correction for excess variance for long ramps

        excessp2: float
             empirical correction for excess variance for long ramps

        Returns
        -------
        var_rn: ndarray if unsat_ngroups is supplied, float if unsat_ngroups is not supplied.
           Variance associated with the read noise only.

        """

        # Rename variables for ease of comparison with Robberto (35).
        # The noise calculation depends on the pixel rate BEFORE IPC convolution. fp_pix_variance takes that pre-IPC
        # rate and scales it by the quantum yield and Fano factor to get the per-pixel variance in the electron rate.
        variance_per_pix = rate['fp_pix_variance']

        rn = readnoise
        n = unsat_ngroups  # we discard any saturated groups
        # maybe nsample_sample_total and tsample are defined. If so then use them for the effect frame time and number
        # of reads (Issue #2996)
        # This is similar to two other places in this file
        if hasattr(self, 'nsample_total') and hasattr(self, 'tsample'):
            m = self.nsample_total
            tframe = self.tsample
        else:
            m = self.nframe # This does not include skipped frames!
            tframe = self.tframe

        nextract = self.ngroup_extract

        # Throw error if the number of extract groups is >= number of groups.
        if self.ngroup_extract > self.ngroup:
            raise EngineInputError("Number of groups to extract, {}, must be less than or equal to the number of groups {}".format(
                self.ngroup_extract, self.ngroup
            ))

        tgroup = self.tgroup

        # The effective group time. This is the time from the first group to the next extracted group. For instance,
        # if ngroups=11 and nextract=3, textract = tgroup * 5
        textract = tgroup * (n-1)/(nextract-1)

        # The TA script will take the minimum of co-subtracted pairs. This has non-Gaussian error properties,
        # but a Monte Carlo Simulation indicates an improvement of 2/3 on the variance for the minimum of two
        # correlated pairs in a single ramp (as compared to a factor 1/2 for the average). It would be good to
        # demonstrate this analytically, but that has not yet been accomplished.

        # Number of possible pairs.
        npairs = nextract-1
        if npairs == 1:
            min_factor = 1.0
        elif npairs == 2:
            min_factor = 2./3.
        else:
            raise EngineInputError("Target acquisition currently only supports 2 or 3 extracted groups.")

        # Modification of MULTIACCUM formula for n=2 and a revised "effective" group time that takes into
        # account that only some groups obtained may be used to create the TA images.
        slope_rn_var = min_factor * (2*rn**2)/m/textract**2
        slope_var = min_factor * (variance_per_pix+dark_current)/textract * (1.-(1./3.)*(m**2-1)/m *
                                                                             tframe/textract) + slope_rn_var

        # The default fill value for masked arrays is a finite number, so convert to ndarrays, and fill with NaNs
        # to make sure missing values are interpreted as truly undefined downstream.

        slope_var = ma.filled(slope_var, fill_value=np.nan)
        slope_rn_var = ma.filled(slope_rn_var, fill_value=np.nan)

        return slope_var, slope_rn_var
