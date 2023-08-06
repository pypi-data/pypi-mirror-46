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

   $ python examples/sample_line_fit_extended.py
   uhammer: perform 84 steps of emcee sampler
   Parameters(a=3.745401e-01, b=9.507143e-01, c=1.463988e+00)
   Parameters(a=5.986585e-01, b=1.560186e-01, c=3.119890e-01)
   Parameters(a=5.808361e-02, b=8.661761e-01, c=1.202230e+00)
   Parameters(a=7.080726e-01, b=2.058449e-02, c=1.939820e+00)
   Parameters(a=8.324426e-01, b=2.123391e-01, c=3.636499e-01)
   uhammer: persisted sampler after iteration 84

   continue sampling
   uhammer: perform 50 steps of emcee sampler
   ✗ passed: 00:00:00.6 left: 00:00:00.0 - [∣∣∣∣∣∣∣∣∣∣∣∣∣∣∣∣∣∣∣∣∣∣∣∣∣∣∣∣∣∣∣∣∣∣∣∣∣∣∣∣∣∣∣∣∣∣∣∣∣∣]

   $ ls -l output_run_0000.txt
   -rw-r--r--  1 uweschmitt  staff  295 May 22 15:48 output_run_0000.txt

   $ head -2 output_run_0000.txt
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
   ✗ passed: 00:00:00.7 left: 00:00:00.0 - [∣]
   NEEDED 0.7649698257446289

   uhammer: perform 1 steps of emcee sampler
   ✗ passed: 00:00:04.7 left: 00:00:00.0 - [∣]
   speedup: 6.10

   $ ls -l out_run_000*.txt
   -rw-r--r--  1 uweschmitt  staff   304 May 22 15:57 out_run_0000_worker_1.txt
   -rw-r--r--  1 uweschmitt  staff   312 May 22 15:57 out_run_0000_worker_2.txt
   -rw-r--r--  1 uweschmitt  staff   264 May 22 15:57 out_run_0000_worker_3.txt
   -rw-r--r--  1 uweschmitt  staff   306 May 22 15:57 out_run_0000_worker_4.txt
   -rw-r--r--  1 uweschmitt  staff   296 May 22 15:57 out_run_0000_worker_5.txt
   -rw-r--r--  1 uweschmitt  staff   300 May 22 15:57 out_run_0000_worker_6.txt
   -rw-r--r--  1 uweschmitt  staff   300 May 22 15:57 out_run_0000_worker_7.txt
   -rw-r--r--  1 uweschmitt  staff  2040 May 22 15:57 out_run_0001.txt


Sampling from a distribution
----------------------------


.. literalinclude:: ../examples/sample_from_distribution.py

.. code-block:: shell-session

   $ python examples/sample_from_distribution.py
   uhammer: perform 100 steps of emcee sampler
   [1.19346601 1.11656067]


Fitting a model
---------------

.. literalinclude:: ../examples/fit_model.py

.. code-block:: shell-session

   $ python examples/fit_model.py
   uhammer: perform 9 steps of emcee sampler
   ✗ passed: 00:00:00.2 left: 00:00:00.0 - [∣∣∣∣∣∣∣∣∣]
   [0.56275974 0.42042152 1.00929049]
