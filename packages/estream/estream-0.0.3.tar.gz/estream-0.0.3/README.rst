.. image:: https://img.shields.io/pypi/v/estream.svg
    :target: https://pypi.python.org/pypi/estream
    :alt: PyPI Version
.. image:: https://img.shields.io/pypi/l/estream.svg
    :target: https://github.com/mickeycj/estream/blob/master/LICENSE
    :alt: License
.. image:: https://travis-ci.org/mickeycj/estream.svg
    :target: https://travis-ci.org/mickeycj/estream
    :alt: Travis CI Build Status

====================================
An E-Stream implementation in Python
====================================

E-Stream is an evolution-based technique for stream clustering which supports
five behaviors:

1. Appearance
2. Disappearance
3. Self-evolution
4. Merge
5. Split

These behaviors are achieved by representing each cluster as a *Fading Cluster
Structure with Histogram (FCH)*, utilizing a histogram for each feature of the
data.

The details for the underlying concepts can be found `here <https://www.researchgate.net/publication/221571035_E-Stream_Evolution-Based_Technique_for_Stream_Clustering>`_:

Udommanetanakit, K, Rakthanmanon, T, Waiyamai, K, *E-Stream: Evolution-Based
Technique for Stream Clustering*, Advanced Data Mining and Applications: Third
International Conference, 2007

-------------------
How to use E-Stream
-------------------

The ``estream`` package aims to be substibutable with ``sklearn`` classes so it
can be used interchangably with other transformers with similar API.

.. code-block:: python

    from estream import EStream
    from sklearn.datasets.samples_generator import make_blobs

    estream = EStream()
    data, _ = make_blobs()

    estream.fit(data)

E-Stream contains a number of parameters that can be set; the major ones are as
follows:

- ``max_clusters``: This limits the number of clusters the clustering can have
  before the existing clusters have to be merged. The default is set to
  *10*.
- ``stream_speed/decay_rate``: These determine the fading factor of the
  clusters. In this implementation, the fading function is constant derived
  from the default values of *10* and *0.1*, respectively.
- ``remove_threshold``: This sets the lower bound for each cluster's weight
  before they are considered to be removed. The default is set to *0.1*.
- ``merge_threshold``: This determines whether two close clusters can be merged
  togther. The default is set to *1.25*.
- ``radius_threshold``: This determines the minimum range from an existing
  cluster that a new data must be in order to be merged into one. The default
  is set to *3.0*.
- ``active_threshold``: This sets the minimum weight of each cluster before
  they are considered active. The default is set to *5.0*.

An example of setting these parameters:

.. code-block:: python

    from estream import EStream
    from sklearn.datasets.samples_generator import make_blobs

    estream = EStream(max_clusters=5,
                      merge_threshold=0.5,
                      radius_threshold=1.5,
                      active_threshold=3.0)
    data, _ = make_blobs()

    estream.fit(data)

------------
Installation
------------

Currently, the package is only available through either ``PyPI``:

.. code-block:: bash

    pip install estream

or a manual install:

.. code-block:: bash

    wget https://github.com/mickeycj/estream/archive/master.zip
    unzip master.zip
    rm master.zip
    cd estream-master
    python setup.py install

--------------
Help & Support
--------------

Currently, there is no dedicated documentation available, so any questions or
issues can be asked via my `email <chanonjenakom@gmail.com>`_.

--------
Citation
--------

If you make use of this software for your work, please cite the paper from the
Advanced Data Mining and Applications: Third International Conference:

.. code-block:: bibtex

    @inproceedings{inproceedings,
        author = {Udommanetanakit, Komkrit, and Rakthanmanon, Thanawin and Waiyamai, Kitsana},
        year = {2007},
        month = {08},
        pages = {605-615},
        title = {E-Stream: Evolution-Based Technique for Stream Clustering},
        volume = {4632},
        doi = {10.1007/978-3-540-73871}
    }

Moreover, this implementation is based on a MOA implementaion of E-Stream (and
other related algorithms) by `David Ratier <https://gitub.com/ratierd>`_. The
original source code can be found in this `repository <https://gitub.com/ratierd/MOA>`_.

-------
License
-------

The ``estream`` package is under the GNU General Public License.

------------
Contributing
------------

Contributions are always welcome! Everything ranging from code to notebooks and
examples/documentation will be very valuable to the growth of this project. To
contribute, please `fork this project <https://github.com/mickeycj/estream/issues#fork-destination-box>`_
, make your changes and submit a pull request. I will do my best to fix any
issues and merge your code into the main branch.

:Author: Chanon Jenakom
:Version: 0.0.3
:Dedicated: To DAKDL, Kasetsart University
