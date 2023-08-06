Welcome to uhammers's documentation!
======================================

`uhammer` offers a convenience layer for `emcee` 

Contents
--------

.. toctree::
   :maxdepth: 2

   installation
   usage
   modules
   authors
   history


Example usage
-------------

To use `uhammer` you need:

- an instance of :py:class:`~uhammer.parameters.Parameters` for declaring the
  parameters you want to sample from.

- a function, e.g. named ``lnprob``, which takes a parameters object and possible
  extra arguments. This function returns the logarithic value of the computed
  posterior probability.

- finally you call :py:func:`~uhammer.sampler.sample` for running the sampler.
  Click at         :py:func:`~uhammer.sampler.sample` to see all options.

.. literalinclude:: ../examples/sample_line_fit.py

.. code-block:: shell-session

  $ python examples/sample_line_fit.py
  uhammer: capture (hide) output during sampling.
  uhammer: perform 25 steps of emcee sampler
  ✗ passed: 00:00:00.4 left: -1:59:60.0 - [∣∣∣∣∣∣∣∣∣∣∣∣∣∣∣∣∣∣∣∣∣∣∣∣∣]

  [0.50197292 0.48450715 0.96744469]



Indices and tables
==================
* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
