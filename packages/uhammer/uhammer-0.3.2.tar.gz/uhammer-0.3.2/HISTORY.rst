=======
History
=======

0.3.2 (2019-05-24)
-------------------
- Less chatty and simpler progress report on euler. The existing progressbar
  cluttered the lsf output files. Now we report in min time intervals of 
  at least 30 seconds.


0.3.1 (2019-05-22)
-------------------
- removed `mpipool` from installation dependencies, else installation always needs
  a working MPI setup. Still `mpirpool` is needed when run in parallel MPI mode.

0.3.0 (2019-05-22)
-------------------
- sample functions now return two arrays: the samples and the related log probabilities
- `Parameters.add` now has an optional argument for providing a starting value.
- `load_samples` function allows extracting samples from a persisted sampler file.
- Replaced `capture_output` argument of `sample` and `continue_sampling` by two
  arguments `show_output` and `output_prefix`.
- Fixed bug in output recording in `continue_sampling` function.
- Use `mpipool` librariy now + added test for `mpi` based parallel sampling.

0.2.13 (2019-05-15)
-------------------
- fix persisting pickler error in parallel mode

0.2.12 (2019-05-02)
-------------------
- minor tweaks for mpi
- fix for emcee 3 dev version

0.2.11 (2019-04-30)
-------------------
- shutdown mpi pool in case a worker throws an exception, before
  this fix mpirun would hang.
- fix handling of capture output file names when running with mpi

0.2.10 (2019-04-19)
-------------------
- fix race condition when removing marker file
- deactivate unnecessary warnings about missing mpi4py


0.2.9 (2019-04-16)
------------------
* Don't show progressbar when run on euler node
* Works with Python 3.7

0.2.8 (2019-04-12)
------------------
* Fix to work with dev version of emcee 3

0.2.7 (2019-03-20)
------------------
* Fix issue with capuring output in parallel mode
* Stop progress bar in case of unhandled exception


0.2.6 (2019-03-20)
------------------
* Fix dependencies for Python 3.7 in setup.py


0.2.5 (2019-03-20)
------------------

* Fix package lookup in requirements_dev.txt
* Fix error in error handling when output redirection fails.

0.2.4 (2018-10-29)
------------------

* fix ordering of sampler output rows.

0.2.3 (2018-10-24)
------------------

* check OMP_NUM_THREADS to warn of possible  over subscription.
* better pickling support for posterior function.

0.2.2 (2018-10-11)
------------------

* Fix detection if uhammer runs on full node on euler.
* Dont show statusbar if direct write to fid 1 is not possible.
* Supress some unappropriate error messages from MPI, even if
  uhammer is not run using mpirun.
* Fix ip check to detect if uhammer runs on euler.

0.2.1 (2018-09-28)
------------------

* Fix of regression due to implementation of Python 2 support.

0.2.0 (2018-09-28)
------------------

* Introduced Python 2 support.

0.1.0 (2018-08-23)
------------------

* Initial version.
