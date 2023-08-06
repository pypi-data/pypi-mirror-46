Holdouts generator
============================================================================
|travis| |sonar_quality| |sonar_maintainability| |sonar_coverage| |code_climate_maintainability| |pip|

Simple python package to generate and cache both random and chromosomal holdouts with arbitrary depth.

How do I get this package?
---------------------------------
As usual, just use pip:

.. code:: bash

    pip install holdouts_generator

Generating random holdouts
---------------------------------
Suppose you want to generate 3 layers of holdouts, respectively with 0.3, 0.2 and 0.1 as test size and 5, 3 and  2 as quantity:

.. code:: python

    from holdouts_generator import holdouts_generator, random_holdouts
    dataset = pd.read_csv("path/to/my/dataset.csv")
    generator = holdouts_generator(
        dataset,
        holdouts=random_holdouts(
            [0.3, 0.2, 0.1],
            [5, 3, 2]
        ),
        cache=False, # Set this parameter to True to enable automatic caching
        cache_dir=".holdouts_cache" # This is the default cache directory
    )


Generating chromosomal holdouts
---------------------------------
Suppose you want to generate 2 layers of holdouts, two outer ones with chromosomes 17 and 18 and 3 inner ones, with chromosomes 17/18, 20 and 21:

.. code:: python

    from holdouts_generator import holdouts_generator, chromosomal_holdouts
    dataset = pd.read_csv("path/to/my/genomic_dataset.csv")
    generator = holdouts_generator(
        dataset,
        holdouts=chromosomal_holdouts([
            ([17], [([18], None), ([20], None), ([21], None)])
            ([18], [([17], None), ([20], None), ([21], None)])
        ]),
        cache=False, # Set this parameter to True to enable automatic caching
        cache_dir=".holdouts_cache" # This is the default cache directory
    )

Clearing the holdouts cache
--------------------------------------
Just run the method `clear_holdouts_cache`:

.. code:: python

    from holdouts_generator import clear_holdouts_cache

    clear_holdouts_cache(
        cache_dir=".holdouts_cache" # This is the default cache directory
    )


.. |travis| image:: https://travis-ci.org/LucaCappelletti94/holdouts_generator.png
   :target: https://travis-ci.org/LucaCappelletti94/holdouts_generator

.. |sonar_quality| image:: https://sonarcloud.io/api/project_badges/measure?project=LucaCappelletti94_holdouts_generator&metric=alert_status
    :target: https://sonarcloud.io/dashboard/index/LucaCappelletti94_holdouts_generator

.. |sonar_maintainability| image:: https://sonarcloud.io/api/project_badges/measure?project=LucaCappelletti94_holdouts_generator&metric=sqale_rating
    :target: https://sonarcloud.io/dashboard/index/LucaCappelletti94_holdouts_generator

.. |sonar_coverage| image:: https://sonarcloud.io/api/project_badges/measure?project=LucaCappelletti94_holdouts_generator&metric=coverage
    :target: https://sonarcloud.io/dashboard/index/LucaCappelletti94_holdouts_generator

.. |code_climate_maintainability| image:: https://api.codeclimate.com/v1/badges/25fb7c6119e188dbd12c/maintainability
   :target: https://codeclimate.com/github/LucaCappelletti94/holdouts_generator/maintainability
   :alt: Maintainability

.. |pip| image:: https://badge.fury.io/py/holdouts_generator.svg
    :target: https://badge.fury.io/py/holdouts_generator