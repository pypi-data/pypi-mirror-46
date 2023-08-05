======
paraer
======


.. image:: https://img.shields.io/pypi/v/paraer.svg
        :target: https://pypi.python.org/pypi/paraer

.. image:: https://img.shields.io/travis/drinksober/paraer.svg
        :target: https://travis-ci.org/drinksober/paraer

.. image:: https://readthedocs.org/projects/paraer/badge/?version=latest
        :target: https://paraer.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status


.. image:: https://pyup.io/repos/github/drinksober/paraer/shield.svg
     :target: https://pyup.io/repos/github/drinksober/paraer/
     :alt: Updates



Python Boilerplate contains all the boilerplate you need to create a Python package.


* Free software: MIT license
* Documentation: https://paraer.readthedocs.io.


Features
--------

* 支持api参数校验,并且当多个参数输入不合法时，会收集多个参数的校验后的提示信息一并返回，而不是当有一个参数非法时立即返回
* 支持api导出为markdown文档，可通过pandoc转为其他格式
* 支持通过api直接生成swagger文档,完美对接django-restframework-swagger
* 支持根据ViewSet或者APIView中定义的serializer_class自动生成swagger的http code为200时的返回格式
* 支持ViewSet中的list方法自动生成分页参数
* 支持当参数为枚举值时，在description中定义枚举值的choices，可以自动生成swagger的表格

Credits
-------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
