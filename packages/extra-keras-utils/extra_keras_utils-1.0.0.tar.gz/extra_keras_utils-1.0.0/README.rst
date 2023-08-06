extra_keras_utils
======================================================================================================
|travis| |sonar_quality| |sonar_maintainability| |sonar_coverage| |code_climate_maintainability| |pip|

Python package collecting commonly used snippets for the Keras library.

How do I get this package?
-------------------------------------
As usual, just instal it using pip:

.. code:: bash

    pip install extra_keras_utils


is_gpu_available
--------------------------------------
Method that returns a boolean if a GPU is detected or not.

.. code:: python

    from extra_keras_utils import is_gpu_available

    if is_gpu_available():
        print("Using gpu!")

set_seed
--------------------------------------
Method to get reproducible results.

.. code:: python

    from extra_keras_utils import set_seed

    set_seed(42) # set as seed 42, the results are nearly reproducible.
    set_seed(42, kill_parallelism=true) # set as seed 42, the results are fully reproducible.


.. |travis| image:: https://travis-ci.org/LucaCappelletti94/extra_keras_utils.png
   :target: https://travis-ci.org/LucaCappelletti94/extra_keras_utils

.. |sonar_quality| image:: https://sonarcloud.io/api/project_badges/measure?project=LucaCappelletti94_extra_keras_utils&metric=alert_status
    :target: https://sonarcloud.io/dashboard/index/LucaCappelletti94_extra_keras_utils

.. |sonar_maintainability| image:: https://sonarcloud.io/api/project_badges/measure?project=LucaCappelletti94_extra_keras_utils&metric=sqale_rating
    :target: https://sonarcloud.io/dashboard/index/LucaCappelletti94_extra_keras_utils

.. |sonar_coverage| image:: https://sonarcloud.io/api/project_badges/measure?project=LucaCappelletti94_extra_keras_utils&metric=coverage
    :target: https://sonarcloud.io/dashboard/index/LucaCappelletti94_extra_keras_utils

.. |code_climate_maintainability| image:: https://api.codeclimate.com/v1/badges/25fb7c6119e188dbd12c/maintainability
   :target: https://codeclimate.com/github/LucaCappelletti94/extra_keras_utils/maintainability
   :alt: Maintainability

.. |pip| image:: https://badge.fury.io/py/extra_keras_utils.svg
    :target: https://badge.fury.io/py/extra_keras_utils