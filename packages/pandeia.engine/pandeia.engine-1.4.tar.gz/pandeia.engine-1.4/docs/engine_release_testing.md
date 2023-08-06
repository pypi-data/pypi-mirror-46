DO NOT MAKE TESTS INCOMPATIBLE WITH THE RELEASE BRANCH
From the moment we branch for a release to the moment we actually publish that release, DO NOT regenerate the tests and
do not do a large-scale redefinition of truth. It will make testing the branch nearly impossible: testrefs and tests
themselves have to match, and it is much easier to do that if nothing at all changes during release preparation.

Regression tests will be run on the engine throughout the release process as part of tracking the progress of the
release. It should not be necessary to run another engine test if one was done on the final RC, though at least one
needs to be done on the code to be released.

1. Run the sensitivity tool and generate sensitivity plots. These should be regenerated and shown to the Working Group
   when each RC is announced.
 - it checks the results of a branch (using the benchmark background read in as an input file) to determine where our
   sensitivies lie.
   According to Klaus, any change in properties larger than 10% must be well-understood and well-justified. NASA will
   want to know about it.

2. Update the release text for pypi (in pandeia.engine.egg-info/README.md), checking that all URLs point to what will be
   valid pages after JDOCs is updated to the new release.

3. Update the authorship and release version in pandeia.engine.egg-info/setup.cfg as needed.

4. Get a complete engine regression test - must be clean, or at least fully explicable.

5. Update and test the installation procedure. As implied by our JDOCs steps information, there are five installation
   steps:

   1.) install anaconda (implied - some kinda python 2.7)
   2.) install astroconda
   3a.) download the correct branch from pandeia_data
   3b.) define $pandeia_refdata pointing to that data
   4a.) Download the correct version of CDBS data from /eng/etc/cdbs_trees
   4b.) define $PYSYN_CDBS pointing to it
   5.) generate a preview package with `python setup.py sdist` (it will create a tarball in the dist/ folder),
       and then install it with `pip install <packagefile>.tar.gz`)

Those steps should be tested prior to each release.

6. Also, we should test for functionality after installation by running the engine (devtools/run_engine.py will work) on
several files.
