# Licensed under a 3-clause BSD style license - see LICENSE.rst
"""
io_utils - commonly used I/O routines for JSON, FITS, and possibly other formats.
"""

from __future__ import division, absolute_import

import os
import json
import errno
import numpy as np
import astropy.io.fits as fits
import pysynphot as psyn

from .custom_exceptions import EngineInputError, DataError
from .constants import PANDEIA_WAVEUNITS, PANDEIA_FLUXUNITS


class NumPyArangeEncoder(json.JSONEncoder):

    """
    custom encoder to handle numpy arrays that might show up in inputs and outputs:

    http://stackoverflow.com/questions/11561932/why-does-json-dumpslistnp-arange5-fail-while-json-dumpsnp-arange5-tolis

    Parameters
    ----------
    obj: python object
        currently only supports translating np.ndarray and np.float32 objects

    Returns
    -------
    e: json.JSONEncoder object
        JSONEncoder that now understands the custom data types
    """

    def default(self, obj):
        # turn ndarrays into lists
        if isinstance(obj, np.ndarray):
            return obj.tolist()  # or map(int, obj)
        # numpy.float32's started showing up when refactoring refdata FITS files
        # catch them and make them into normal float()'s
        if isinstance(obj, (np.float32, np.float64)):
            return float(obj)
        if isinstance(obj, (np.int32, np.int64)):
            return int(obj)
        e = json.JSONEncoder.default(self, obj)
        return e

def get_full_refwave_dict(data_dir, telescope, inst_list, modename_list):
    """
    Traverse the pandeia_data tree for the instruments and modenames given
    and find all refwave info (min, max, midpoint) that there is and return it in
    a tree of dicts.

    Parameters
    ----------
    data_dir: str
        Path to pandeia_data dir (e.g. $pandeia_refdata value)
    telescope: str
        E.g. 'jwst'
    inst_list: list of str
        instrument names for data desired, e.g. ['miri','nircam','niriss','nirspec'],
    modename_list: list of str
        mode names desired for all instruments listed above, e.g. ['imaging','mrs','soss','wfgrism']
    """
    retval = {}
    for inst in inst_list:
        this_inst = {}
        inst_cfg_fname = data_dir+os.sep+telescope+os.sep+inst+os.sep+'config.json'
        assert os.path.exists(inst_cfg_fname), "Error: cfg file not found: "+inst_cfg_fname
        inst_cfg = read_json(inst_cfg_fname, raise_except=True)
        all_inst_modes = inst_cfg['modes']
        mode_cfg = inst_cfg['mode_config']
        range_cfg = inst_cfg['range']
        assert sorted(all_inst_modes) == sorted(mode_cfg.keys()) or (inst == 'nirspec' and 1+len(all_inst_modes) == len(mode_cfg.keys())), "Error: modes list mismatch for: "+inst
        requested_modes = [m for m in modename_list if m in all_inst_modes]
        for mode in requested_modes:
            this_mode = {}
            inst_mode_apers = mode_cfg[mode]['apertures']
            for aper in inst_mode_apers:
                this_aper = {}
                if aper in range_cfg:
                    # we have matching range data !
                    for item in range_cfg[aper]:
                        if isinstance(range_cfg[aper][item], dict) and 'wmin' in range_cfg[aper][item] and 'wmax' in range_cfg[aper][item]:
                            this_item = range_cfg[aper][item].copy() # use a copy for below
                            mid = (this_item['wmin'] + this_item['wmax'])/2.0
                            mid = (int(1000*mid))/1000. # keep only to 3rd decimal place
                            this_item['wmidpoint'] = mid
                            this_aper[item] = this_item
                # done with aper
                if len(this_aper.keys()) > 0:
                    this_mode[aper] = this_aper
            # done with mode
            if len(this_mode.keys()) > 0:
                this_inst[mode] = this_mode
        # done with inst
        if len(this_inst.keys()) > 0:
            retval[inst] = this_inst
    return retval


def read_json(filename, raise_except=False, **kwargs):
    """
    read in a JSON format file.  return None if the file is not there.

    Parameters
    ----------
    filename: string
        name of the JSON file to read
    except: bool
        if true, raise exception if file is missing. if false, return empty dict.

    Returns
    -------
    d: python object
        data from JSON file decoded into python object
    """
    try:
        with open(filename, 'r') as f:
            json_data = json.load(f, **kwargs)
    except IOError as e:
        if e.errno == errno.ENOENT and raise_except is False:  # No such file
            json_data = {}
        else:
            msg = "Missing JSON file: %s" % filename
            raise EngineInputError(value=msg)
    d = json_data
    return d


def write_json(data, filename, **kwargs):
    """
    write python object into a JSON format file

    Parameters
    ----------
    data: python object
        python object to encode and write to JSON
    filename: string
        name of file to write JSON-encoded data to
    """
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4, cls=NumPyArangeEncoder, separators=(',', ': '), **kwargs)
        f.write('\n')


def append_json(obj, filename):
    """
    read data structure from JSON, append it to a python object, and return the result.
    currently only supported for lists and dicts

    Parameters
    ----------
    obj: python object
        object to be appended to
    filename: string
        filename containing JSON data to be appended

    Returns
    -------
    obj: python object
        input python object now updated with appended data
    """
    json_data = read_json(filename)
    if isinstance(obj, list):
        if isinstance(json_data, list):
            for k in json_data:
                obj.append(k)
        else:
            obj.append(json_data)
    elif isinstance(obj, dict):
        if isinstance(json_data, dict):
            obj.update(json_data)
    else:
        raise ValueError("Can only append to list or dict.")
    return obj


def convert_nd2list_in_place(obj):
    """
    Traverse a dict (with possible nested dicts) finding any numpy
    ndarray instances and converting them to Python lists (or lists of lists),
    but do so in place without making a second copy of the data structure.

    Returns nothing; modifies the dict passed in.

    Parameters
    ----------
    obj: python dict
        data structure to be traversed

    Returns
    -------
    Nothing
    """
    if isinstance(obj, dict):
        for key in obj:
            if isinstance(obj[key], np.ndarray):
                as_list = obj[key].tolist()
                del obj[key]
                obj[key] = as_list
            elif isinstance(obj[key], list) and len(obj[key]) > 0 and isinstance(obj[key][0], np.ndarray):
                # here we have a list of arrays, so convert them all
                as_list_list = []
                for item in obj[key]:
                    as_list_list.append(item.tolist())
                del obj[key]
                obj[key] = as_list_list
            elif isinstance(obj[key], dict):
                # recurse !
                convert_nd2list_in_place(obj[key])
            else:
                pass # leave this key of dict untouched
    else:
        pass


def ref_data_interp(filename, wave, colname=None):
    """
    Read reference data from a FITS file and interpolate it to a provided wavelength array

    Parameters
    ----------
    filename: str
        Filename of reference data
    wave: numpy.ndarray
        Wavelength vector that the reference data will be interpolated onto
    colname: str
        Name of column within the reference file to read and interpolate

    Returns
    -------
    interp_col: numpy.ndarray
        Vector containing reference data interpolated onto wave
    """
    if colname is None:
        raise EngineInputError(value="Must specify name of column to read from reference file.")
    try:
        data = fits.getdata(filename)
    except IOError as e:
        error_msg = "Error reading reference file: " + filename
        raise DataError(value=error_msg)
    if np.any(np.diff(data['wavelength']) < 0):
        indices = np.where(np.diff(data['wavelength']) < 0)[0]
        error_msg = "Wavelengths must be increasing in reference file: %s\n" % (filename)
        error_msg += "Out-of-order indices: %s" % repr(indices)
        raise DataError(value=error_msg)
    try:
        columns = set(k.name.lower() for k in data.columns)
        if colname.lower() not in columns:
            msg = "Column %s not found in %s" % (colname, filename)
            raise DataError(value=msg)
        interp_col = np.interp(wave, data['wavelength'], data[colname])
    except Exception as e:
        error_msg = "Error interpolating reference file: %s : %s" % (filename, type(e))
        raise DataError(value=error_msg)
    return interp_col


def ref_data_column(filename, colname=None, error_msg="Error loading reference file."):
    """
    Read reference data from a FITS file and provide it directly with no interpolation

    Parameters
    ----------
    filename: str
        Filename of reference data
    colname: str
        Name of column within the reference file to read and return
    error_msg: str
        Custom error message to produce in case of an error

    Returns
    -------
    col: numpy.ndarray
        Vector containing requested reference data
    """
    if colname is None:
        raise EngineInputError(value="Must specify name of column to read from reference file.")
    try:
        data = fits.getdata(filename)
    except IOError as e:
        raise DataError(value="I/O " + error_msg)
    try:
        col = data[colname]
    except KeyError as e:
        raise DataError(value="Column not found in reference file: %s" % colname)
    return col


def read_psyn_spectrum(path):
    """
    Read spectrum in FITS or compliant ascii format (wavelength in angstroms, flux in flam).
    See http://etc.stsci.edu/etcstatic/users_guide/1_ref_5_user_spectra.html for details of
    acceptable files for pysynphot.

    Parameters
    ----------
    path: string
        Full pathname to FITS file containing spectrum

    Returns
    -------
    wave, flux:  1D np.ndarray, 1D np.ndarray
        Wavelength and flux vectors in 'PANDEIA_WAVEUNITS' and 'PANDEIA_FLUXUNITS', respectively
    """
    sp = psyn.FileSpectrum(path)
    sp.convert(PANDEIA_WAVEUNITS)
    sp.convert(PANDEIA_FLUXUNITS)
    wave, flux = sp.wave, sp.flux
    return wave, flux


def mkdir_p(path):
    """
    Implement 'mkdir -p' functionality with pure python

    Parameters
    ----------
    path: valid path specification
    """
    try:
        os.makedirs(path)
    except OSError as exc:
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            raise
