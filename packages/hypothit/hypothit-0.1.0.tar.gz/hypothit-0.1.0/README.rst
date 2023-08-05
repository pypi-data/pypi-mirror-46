========
hypothit
========

|PyPI badge| |Docs badge| |CI badge|

Command line interface for Hypothesis property based tests

::

    $ hypothit trial --given "a=integers()" --assume 'a!=0' "assert a==42"
    from hypothesis import given, assume
    from hypothesis.strategies import integers


    @given(a=integers())
    def inner(a):
        assume(a!=0)
        assert a==42

    inner()

    Falsifying example: inner(a=1)
    Traceback (most recent call last):
    File ".../hypothit/cli.py", line 90, in trial
        exec(src, g)
    File "<string>", line 10, in <module>
    File "<string>", line 6, in inner
    File ".../hypothesis/core.py", line 1024, in wrapped_test
        raise the_error_hypothesis_found
    File "<string>", line 8, in inner
    AssertionError

* Free software: MPL v2
* Documentation: https://hypothit.readthedocs.io.

Credits
-------

This package was cut with Cookiecutter_, & `audreyr/cookiecutter-pypackage`_.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage

.. |PyPI badge| image:: https://img.shields.io/pypi/v/hypothit.svg
        :target: https://pypi.python.org/pypi/hypothit

.. |CI badge| image:: https://img.shields.io/travis/moreati/hypothit.svg
        :target: https://travis-ci.org/moreati/hypothit

.. |Docs badge| image:: https://readthedocs.org/projects/hypothit/badge/?version=latest
        :target: https://hypothit.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status
