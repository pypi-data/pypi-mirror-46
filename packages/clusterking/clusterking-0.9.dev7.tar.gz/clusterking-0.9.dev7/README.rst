.. note: Always use full path to image, because it won't render on
   pypi and others otherwise

.. image:: https://raw.githubusercontent.com/clusterking/clusterking/master/readme_assets/logo/logo.png
    :align: right

Clustering of Kinematic Graphs
==============================

|Build Status| |Coveralls| |Doc Status| |Pypi status| |Binder| |Chat| |License|

.. |Build Status| image:: https://travis-ci.org/clusterking/clusterking.svg?branch=master
   :target: https://travis-ci.org/clusterking/clusterking

.. |Coveralls| image:: https://coveralls.io/repos/github/clusterking/clusterking/badge.svg?branch=master
   :target: https://coveralls.io/github/clusterking/clusterking?branch=master

.. |Doc Status| image:: https://readthedocs.org/projects/clusterking/badge/?version=latest
   :target: https://clusterking.readthedocs.io/
   :alt: Documentation Status

.. |Pypi Status| image:: https://badge.fury.io/py/clusterking.svg
    :target: https://badge.fury.io/py/clusterking
    :alt: Pypi status

.. |Binder| image:: https://mybinder.org/badge_logo.svg
   :target: https://mybinder.org/v2/gh/clusterking/clusterking/master?filepath=examples%2Fjupyter_notebooks
   :alt: Binder

.. |Chat| image:: https://img.shields.io/gitter/room/clusterking/community.svg   
   :target: https://gitter.im/clusterking/community
   :alt: Gitter

.. |License| image:: https://img.shields.io/github/license/clusterking/clusterking.svg
   :target: https://github.com/clusterking/clusterking/blob/master/LICENSE.txt
   :alt: License

.. start-body

Description
-----------

This package provides a flexible yet easy to use framework to cluster sets of histograms (or other higher dimensional data) and to select benchmark points representing each cluster. The package particularly focuses on use cases in high energy physics.

Physics Case
------------

While most of this package is very general and can be applied to a broad variety of use cases, we have been focusing on applications in high energy physics (particle physics) so far and provide additional convenience methods for this use case. In particular, most of the current tutorials are in this context.

Though very successful, the Standard Model of Particle Physics is believed to be uncomplete, prompting the search for New Physics (NP).
The phenomenology of NP models typically depends on a number of free parameters, sometimes strongly influencing the shape of distributions of kinematic variables. Besides being an obvious challenge when presenting exclusion limits on such models, this also is an issue for experimental analyses that need to make assumptions on kinematic distributions in order to extract features of interest, but still want to publish their results in a very general way.

By clustering the NP parameter space based on a metric that quantifies the similarity of the resulting kinematic distributions, a small number of NP benchmark points can be chosen in such a way that they can together represent the whole parameter space. Experiments (and theorists) can then report exclusion limits and measurements for these benchmark points without sacrificing generality.  

Installation
------------

``clusterking`` can be installed with the python package installer:

.. code:: sh

    pip3 install clusterking

For a local installation, you might want to use the ``--user`` switch of ``pip``.
You can also update your current installation with ``pip3 install --upgrade clusterking``.  

For the latest development version type:

.. code:: sh

    git clone https://github.com/clusterking/clusterking/
    cd clusterking
    pip3 install --user .

Usage and Documentation
-----------------------

Good starting point: **Jupyter notebooks** in the ``examples/jupyter_notebook`` directory (|binder2|_).

.. |binder2| replace:: **run online using binder**
.. _binder2: https://mybinder.org/v2/gh/clusterking/clusterking/master?filepath=examples%2Fjupyter_notebooks

.. _run online using binder: https://mybinder.org/v2/gh/clusterking/clusterking/master?filepath=examples%2Fjupyter_notebooks

For a documentation of the classes and functions in this package, **read the docs on** |readthedocs.io|_.

.. |readthedocs.io| replace:: **readthedocs.io**
.. _readthedocs.io: https://clusterking.readthedocs.io/

Example
-------

Sample and cluster
~~~~~~~~~~~~~~~~~~

Being a condensed version of the basic tutorial, the following code is all that is needed to cluster the shape of the ``q^2`` distribution of ``B-> D* tau nu`` in the space of Wilson coefficients:

.. code:: python

   import flavio
   import numpy as np
   import clusterking as ck

   s = ck.scan.WilsonScanner(scale=5, eft='WET', basis='flavio')

   # Set up kinematic function

   def dBrdq2(w, q):
       return flavio.np_prediction("dBR/dq2(B+->Dtaunu)", w, q)

   s.set_dfunction(
       dBrdq2,
       binning=np.linspace(3.2, 11.6, 10),
       normalize=True
   )

   # Set sampling points in Wilson space

   s.set_spoints_equidist({
       "CVL_bctaunutau": (-1, 1, 10),
       "CSL_bctaunutau": (-1, 1, 10),
       "CT_bctaunutau": (-1, 1, 10)
   })

   # Create data object to write to and run

   d = ck.DataWithErrors()
   s.run(d)

   # Use hierarchical clustering

   c = ck.cluster.HierarchyCluster(d)
   c.set_metric()         # Use default metric (Euclidean)
   c.build_hierarchy()    # Build up clustering hierarchy
   c.cluster(max_d=0.15)  # "Cut off" hierarchy
   c.write()              # Write results to d

Benchmark points
~~~~~~~~~~~~~~~~

.. code:: python

   b = ck.Benchmark(d) # Initialize benchmarker for data d
   b.set_metric()      # Use default metric (Euclidean)
   b.select_bpoints()  # Select benchmark points based on metric
   b.write()           # Write results back to d

Plotting
~~~~~~~~

.. code:: python

    d.plot_clusters_scatter(
        ['CVL_bctaunutau', 'CSL_bctaunutau', 'CT_bctaunutau'],
        clusters=[1,2]  # Only plot 2 clusters for better visibility
    )

.. image:: https://raw.githubusercontent.com/clusterking/clusterking/master/readme_assets/plots/scatter_3d_02.png
 
.. code:: python

    d.plot_clusters_fill(['CVL_bctaunutau', 'CSL_bctaunutau'])

.. image:: https://raw.githubusercontent.com/clusterking/clusterking/master/readme_assets/plots/fill_2d.png

Plotting all benchmark points:

.. code:: python

    d.plot_dist()

.. image:: https://raw.githubusercontent.com/clusterking/clusterking/master/readme_assets/plots/all_bcurves.png

Plotting minima and maxima of bin contents for all histograms in a cluster (+benchmark histogram):

.. code:: python

    d.plot_dist_minmax(clusters=[0, 2])

.. image:: https://raw.githubusercontent.com/clusterking/clusterking/master/readme_assets/plots/minmax_02.png

Similarly with box plots:

.. code:: python

   d.plot_dist_box()

.. image:: https://raw.githubusercontent.com/clusterking/clusterking/master/readme_assets/plots/box_plot.png

License & Contributing
----------------------

This project is ongoing work and questions_, comments, `bug reports`_ or `pull requests`_ are most welcome. You can also use the chat room on gitter_ or contact us via email_.  We are also working on a paper, so please make sure to cite us once we publish.

.. _email: mailto:clusterkinematics@gmail.com
.. _gitter: https://gitter.im/clusterking/community
.. _questions: https://github.com/clusterking/clusterking/issues
.. _bug reports: https://github.com/clusterking/clusterking/issues
.. _pull requests: https://github.com/clusterking/clusterking/pulls

This software is lienced under the `MIT license`_.

.. _MIT  license: https://github.com/clusterking/clusterking/blob/master/LICENSE.txt

.. end-body
