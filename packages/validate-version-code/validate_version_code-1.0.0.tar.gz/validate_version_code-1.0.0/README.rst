validate_version_code
==================================================
|travis| |sonar_quality| |sonar_maintainability| |sonar_coverage| |code_climate_maintainability| |pip|

Python package to validate version code.

How do I get this package?
--------------------------------------------
As usual, just use pip:

.. code:: bash

    pip install validate_version_code


Usage example
--------------------------------------------
He's a basic how to:

.. code:: python

    from validate_version_code import validate_version_code

    valid_version_code = "1.2.3"
    invalid_version_code = "beta.3"

    assert validate_version_code(valid_version_code)
    assert not validate_version_code(invalid_version_code)


.. |travis| image:: https://travis-ci.org/LucaCappelletti94/validate_version_code.png
   :target: https://travis-ci.org/LucaCappelletti94/validate_version_code

.. |sonar_quality| image:: https://sonarcloud.io/api/project_badges/measure?project=LucaCappelletti94_validate_version_code&metric=alert_status
    :target: https://sonarcloud.io/dashboard/index/LucaCappelletti94_validate_version_code

.. |sonar_maintainability| image:: https://sonarcloud.io/api/project_badges/measure?project=LucaCappelletti94_validate_version_code&metric=sqale_rating
    :target: https://sonarcloud.io/dashboard/index/LucaCappelletti94_validate_version_code

.. |sonar_coverage| image:: https://sonarcloud.io/api/project_badges/measure?project=LucaCappelletti94_validate_version_code&metric=coverage
    :target: https://sonarcloud.io/dashboard/index/LucaCappelletti94_validate_version_code

.. |code_climate_maintainability| image:: https://api.codeclimate.com/v1/badges/25fb7c6119e188dbd12c/maintainability
   :target: https://codeclimate.com/github/LucaCappelletti94/validate_version_code/maintainability
   :alt: Maintainability

.. |pip| image:: https://badge.fury.io/py/validate_version_code.svg
    :target: https://badge.fury.io/py/validate_version_code