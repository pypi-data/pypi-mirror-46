=====
Usage
=====

Persist and restart sampler
---------------------------

The following example

 - persists the state of the sampler to a file
 - continues sampling from the persisted sampler
 - demonstrates how to write output of the ``lnprob`` function to stdout or a file
 - shows how to set a seed

 Below we use :py:func:`~uhammer.persisting.persist_final`, other options are 
 :py:func:`~uhammer.persisting.persist_every_n_iterations` 
 and
 :py:func:`~uhammer.persisting.persist_on_error`.

.. literalinclude:: ../examples/sample_line_fit_extended.py


.. code-block:: shell-session

   $ python sample_line_fit_extended.py
   uhammer: perform 84 steps of emcee sampler
   Parameters(a=0.3745401188473625, b=0.9507143064099162, c=1.4639878836228102)
   Parameters(a=0.5986584841970366, b=0.15601864044243652, c=0.3119890406724053)
   Parameters(a=0.05808361216819946, b=0.8661761457749352, c=1.2022300234864176)
   Parameters(a=0.7080725777960455, b=0.020584494295802447, c=1.9398197043239886)
   Parameters(a=0.8324426408004217, b=0.21233911067827616, c=0.36364993441420124)
   uhammer: persisted sampler after iteration 84

   continue sampling
   uhammer: capture output to /Users/uweschmitt/Projects/uhammer/output.txt
   uhammer: perform 50 steps of emcee sampler
   ✗ passed: 00:00:00.1 left: 00:00:00.0 - [∣∣∣∣∣∣∣∣∣∣∣∣∣∣∣∣∣∣∣∣∣∣∣∣∣∣∣∣∣∣∣∣∣∣∣∣∣∣∣∣∣∣∣∣∣∣∣∣∣∣]

   $ ls -l output.txt
   -rw-r--r--  1 uweschmitt  staff  385 Sep  3 17:50 output.txt

   $ head -2 output.txt
   Parameters(a=0.4591726382942836, b=0.5968783255152834, c=0.9867551523205441)
   Parameters(a=0.34492701778793583, b=0.5968000537205522, c=1.0672690581906268)


The sampler function returns computed samples as a ``numpy`` array of shape
``(n_samples, len(p)`` arranged as follows:

.. table::

      +----------------------------------------+
      | samples                                |
      +========================================+
      | p-dimensional sample from walker 0     |
      +----------------------------------------+
      | p-dimensional sample from walker 1     |
      +----------------------------------------+
      | ...                                    |
      +----------------------------------------+
      | p-dimensional sample from walker n - 1 |
      +----------------------------------------+
      | p-dimensional sample from walker 0     |
      +----------------------------------------+
      | p-dimensional sample from walker 1     |
      +----------------------------------------+
      | ...                                    |
      +----------------------------------------+

Using parallel mode
-------------------

Setting the argument `parallel=True` enables parallel mode. `uhammer` detects
if your script runs with `mpirun` or not. Without MPI `uhammer` spawns workers
on all available cores.

On euler this means you can either start your script using MPI:

.. code-block:: shell-session

   $ bsub -n 200 mpirun python examples/sample_line_fit_parallel.py

or using cores on one compute node:

.. code-block:: shell-session

   $ bsub -n 32 -R fullnode python examples/sample_line_fit_parallel.py

In case you allocate more cores than available, or if number of walkers is not
a multiple of number of workers, `uhammer` will show you some warnings.

.. literalinclude:: ../examples/sample_line_fit_parallel.py

.. code-block:: shell-session

   $ python examples/sample_line_fit_parallel.py
   uhammer: capture (hide) output during sampling.
   uhammer: started MultiProcessingPool with 3 workers
   uhammer: perform 25 steps of emcee sampler
   ✗ passed: 00:00:02.9 left: 00:00:00.0 - [∣∣∣∣∣∣∣∣∣∣∣∣∣∣∣∣∣∣∣∣∣∣∣∣∣]

   uhammer: capture (hide) output during sampling.
   uhammer: perform 25 steps of emcee sampler
   ✗ passed: 00:00:09.2 left: 00:00:00.0 - [∣∣∣∣∣∣∣∣∣∣∣∣∣∣∣∣∣∣∣∣∣∣∣∣∣]
   speedup: 3.12


Sampling from a distribution
----------------------------


.. literalinclude:: ../examples/sample_from_distribution.py

.. code-block:: shell-session

   $ python examples/sample_from_distribution.py
   uhammer: capture (hide) output during sampling.
   uhammer: perform 100 steps of emcee sampler
   [1.19346601 1.11656067]


Fitting a model
---------------

.. literalinclude:: ../examples/fit_model.py

.. code-block:: shell-session

   $ python examples/fit_model.py
   uhammer: capture (hide) output during sampling.
   uhammer: perform 9 steps of emcee sampler
   ✗ passed: 00:00:00.2 left: 00:00:00.0 - [∣∣∣∣∣∣∣∣∣]
   [0.52620406 0.48047746 1.023023  ]
