0. Make sure the tagged release of pandeia_data does not have the devtools/, hst/ or wfirst/ directories. (These should already have been removed during the release testing process)

1. Generate and upload the data file
  - Create data tar file
      - Mark it as a release
      - Go to [pandeia_data](https://github.com/spacetelescope/pandeia_data), and click on the "Releases" link. Look for the latest release and download the source code (in tar.gz format).
  - Go to the folder you had downloaded the tar file located.
  - Make a directory named `/eng/ssb/websites/ssbpublic/pandeia/engine/X.Y.Z` where X.Y.Z is the name of the release.
  - Move the tar file just downloaded into that directory.


2. Follow instruction [here](http://peterdowns.com/posts/first-time-with-pypi.html) to generate and upload the source code to the https://pypi.python.org/pypi/pandeia.engine
  - In section 'Create a .pypirc configuration file' if the .pypirc file does not exist.
  - In a fresh checkout of pandeia vX.Y.Z
    - `cd engine/`
    - Test creating an installation on test.pypi.org (you only have one shot at uploading to pypi for real - uploads cannot be edited or replaced.)
       - see "Using TestPyPi" for instructions on using twine to upload to TestPyPi)
       - Edit the pypirc file to point to test.pypi.org
       - Create source distribution with `python setup.py sdist`; it should make a tar.gz file
       - Use twine to upload to testpypi
       - check test.pypi to make sure it uploaded correctly.

    - Generate source distribution and upload to pypi: `python setup.py sdist upload -r pypi`

3. Test
 - Go to https://pypi.python.org/pypi/pandeia.engine to see if the package is sucessfully uploaded.
 - Install a fresh version of the latest third party software and load that environment by typing `source /path/to/third/party pandeia_<third_party_version>`.
 - `pip freeze | grep pandeia.engine` (note the version, e.g. 1.2.1dev0)
 - `pip install pandeia.engine --upgrade`
 - test it by running the `pip freeze | grep pandeia.engine` command again and note the version should have changed (e.g. v1.3)
 - Follow the usage instruction in [pypi](https://pypi.python.org/pypi/pandeia.engine) to check if the users can follow the instruction as well.
 - Ask the engine dev to do a simple test and see if the new changes apply.

4. Email the person who is responsible for updating the jwst website
 - Notify both Bryan and Klaus that the engine is on pypi and the [jwst docs](https://jwst.stsci.edu/science-planning/proposal-planning-toolbox/exposure-time-calculator-etc) need to be updated.

--------------------

Making a WFIRST data release (on the assumption that running the engine for WFIRST requires only different data files):

1. Check out the release branch
2. Rewind the release branch to the commit before the hst and wfirst directories were removed with git reset --hard <commit>
3. Branch from that commit to vX.Y.Z_wfirst
4. Make a commit removing the jwst and hst directories
5. Make a `vX.Y.Z_wfirst` release
6. Download the resulting tarball and move it to a folder on the central store
7. As the IRAF user on the SSB machine, copy that file out of the central store to ``/eng/ssb/websites/ssbpublic/pandeia/engine/X.Y.Z`
