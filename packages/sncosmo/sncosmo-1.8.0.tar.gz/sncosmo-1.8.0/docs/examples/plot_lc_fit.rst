.. note::
    :class: sphx-glr-download-link-note

    Click :ref:`here <sphx_glr_download_examples_plot_lc_fit.py>` to download the full example code
.. rst-class:: sphx-glr-example-title

.. _sphx_glr_examples_plot_lc_fit.py:


=====================
Fitting a light curve
=====================

This example shows how to fit the parameters of a SALT2 model to photometric
light curve data.

First, we'll load an example of some photometric data.



.. code-block:: python


    from __future__ import print_function

    import sncosmo

    data = sncosmo.load_example_data()

    print(data)





.. rst-class:: sphx-glr-script-out

 Out:

 .. code-block:: none

    time      band       flux         fluxerr      zp  zpsys
    ------------- ----- --------------- -------------- ---- -----
          55070.0 sdssg   0.36351153597 0.672843847541 25.0    ab
    55072.0512821 sdssr -0.200801295864 0.672843847541 25.0    ab
    55074.1025641 sdssi  0.307494232981 0.672843847541 25.0    ab
    55076.1538462 sdssz   1.08776103656 0.672843847541 25.0    ab
    55078.2051282 sdssg  -0.43667895645 0.672843847541 25.0    ab
    55080.2564103 sdssr   1.09780966779 0.672843847541 25.0    ab
    55082.3076923 sdssi    3.7562685627 0.672843847541 25.0    ab
    55084.3589744 sdssz   5.34858894966 0.672843847541 25.0    ab
    55086.4102564 sdssg   2.82614187269 0.672843847541 25.0    ab
    55088.4615385 sdssr   7.56547045054 0.672843847541 25.0    ab
              ...   ...             ...            ...  ...   ...
    55129.4871795 sdssr    2.6597485586 0.672843847541 25.0    ab
    55131.5384615 sdssi   3.99520404021 0.672843847541 25.0    ab
    55133.5897436 sdssz   5.73989458094 0.672843847541 25.0    ab
    55135.6410256 sdssg  0.330702283107 0.672843847541 25.0    ab
    55137.6923077 sdssr  0.565286726579 0.672843847541 25.0    ab
    55139.7435897 sdssi   3.04318346795 0.672843847541 25.0    ab
    55141.7948718 sdssz   5.62692686384 0.672843847541 25.0    ab
    55143.8461538 sdssg -0.722654789013 0.672843847541 25.0    ab
    55145.8974359 sdssr   1.12091764262 0.672843847541 25.0    ab
    55147.9487179 sdssi    2.1246695264 0.672843847541 25.0    ab
          55150.0 sdssz    5.3482175645 0.672843847541 25.0    ab
    Length = 40 rows


An important additional note: a table of photometric data has a
``band`` column and a ``zpsys`` column that use strings to identify
the bandpass (e.g., ``'sdssg'``) and zeropoint system (``'ab'``) of
each observation. If the bandpass and zeropoint systems in your data
are *not* built-ins known to sncosmo, you must register the
corresponding `~sncosmo.Bandpass` or `~sncosmo.MagSystem` to the
right string identifier using the registry.



.. code-block:: python


    # create a model
    model = sncosmo.Model(source='salt2')

    # run the fit
    result, fitted_model = sncosmo.fit_lc(
        data, model,
        ['z', 't0', 'x0', 'x1', 'c'],  # parameters of model to vary
        bounds={'z':(0.3, 0.7)})  # bounds on parameters (if any)







The first object returned is a dictionary-like object where the keys
can be accessed as attributes in addition to the typical dictionary
lookup like ``result['ncall']``:



.. code-block:: python

    print("Number of chi^2 function calls:", result.ncall)
    print("Number of degrees of freedom in fit:", result.ndof)
    print("chi^2 value at minimum:", result.chisq)
    print("model parameters:", result.param_names)
    print("best-fit values:", result.parameters)
    print("The result contains the following attributes:\n", result.keys())





.. rst-class:: sphx-glr-script-out

 Out:

 .. code-block:: none

    Number of chi^2 function calls: 133
    Number of degrees of freedom in fit: 35
    chi^2 value at minimum: 33.809882360762884
    model parameters: ['z', 't0', 'x0', 'x1', 'c']
    best-fit values: [5.15154859e-01 5.51004778e+04 1.19625368e-05 4.67270999e-01
     1.93951997e-01]
    The result contains the following attributes:
     dict_keys(['success', 'message', 'ncall', 'chisq', 'ndof', 'param_names', 'parameters', 'vparam_names', 'covariance', 'errors', 'nfit', 'data_mask'])


The second object returned is a shallow copy of the input model with
the parameters set to the best fit values. The input model is
unchanged.



.. code-block:: python


    sncosmo.plot_lc(data, model=fitted_model, errors=result.errors)




.. image:: /examples/images/sphx_glr_plot_lc_fit_001.png
    :class: sphx-glr-single-img




Suppose we already know the redshift of the supernova we're trying to
fit.  We want to set the model's redshift to the known value, and then
make sure not to vary `z` in the fit.



.. code-block:: python


    model.set(z=0.5)  # set the model's redshift.
    result, fitted_model = sncosmo.fit_lc(data, model,
                                          ['t0', 'x0', 'x1', 'c'])
    sncosmo.plot_lc(data, model=fitted_model, errors=result.errors)



.. image:: /examples/images/sphx_glr_plot_lc_fit_002.png
    :class: sphx-glr-single-img




**Total running time of the script:** ( 0 minutes  0.979 seconds)


.. _sphx_glr_download_examples_plot_lc_fit.py:


.. only :: html

 .. container:: sphx-glr-footer
    :class: sphx-glr-footer-example



  .. container:: sphx-glr-download

     :download:`Download Python source code: plot_lc_fit.py <plot_lc_fit.py>`



  .. container:: sphx-glr-download

     :download:`Download Jupyter notebook: plot_lc_fit.ipynb <plot_lc_fit.ipynb>`


.. only:: html

 .. rst-class:: sphx-glr-signature

    `Gallery generated by Sphinx-Gallery <https://sphinx-gallery.readthedocs.io>`_
