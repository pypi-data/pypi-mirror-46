# -*- coding: utf-8 -*-
from distutils.core import setup

modules = \
['project_template']
extras_require = \
{'docs': ['sphinx>=1.8,<2.0',
          'sphinx_rtd_theme>=0.4.3,<0.5.0',
          'toml>=0.10.0,<0.11.0']}

setup_kwargs = {
    'name': 'project-template',
    'version': '0.1.0',
    'description': '',
    'long_description': '.. start-include\n\n================\nproject_template\n================\n\n.. image:: https://travis-ci.org/thejohnfreeman/project-template-python.svg?branch=master\n   :target: https://travis-ci.org/thejohnfreeman/project-template-python\n   :alt: Build status\n\n.. image:: https://readthedocs.org/projects/project-template-python/badge/?version=latest\n   :target: https://project-template-python.readthedocs.io/\n   :alt: Documentation status\n\n.. image:: https://img.shields.io/pypi/v/project_template.py.svg\n   :target: https://pypi.org/project/project_template.py/\n   :alt: Latest PyPI version\n\n.. image:: https://img.shields.io/pypi/pyversions/project_template.py.svg\n   :target: https://pypi.org/project/project_template.py/\n   :alt: Python versions supported\n\nThis is a sample project generated by generator-python_ for Yeoman_. [#]_ It has\na number of features, each with its own chapter in the documentation_:\n\n.. _generator-python: https://github.com/thejohnfreeman/generator-python\n.. _Yeoman: https://yeoman.io/\n.. _documentation: https://project-template-python.readthedocs.io/\n\n- ISC_ license\n- All package metadata in ``pyproject.toml``\n  (reaching standardization in `PEP 518`_)\n- Scripts for common development tasks (linting, testing, building\n  documentation)\n- Testing with pytest_, doctests_, and coverage\n- Continuous integration on Linux and OSX with `Travis CI`_\n- Documentation with Sphinx_ and `Read the Docs`_\n\n.. _ISC: https://tldrlegal.com/license/-isc-license\n.. _PEP 518: https://www.python.org/dev/peps/pep-0518/\n.. _pytest: https://docs.pytest.org/\n.. _doctests: https://pymotw.com/2/doctest/\n.. _Travis CI: https://travis-ci.org/\n.. _Sphinx: https://www.sphinx-doc.org/\n.. _Read the Docs: https://docs.readthedocs.io/\n\n.. [#] With the exception of a few additions. Most notably, the content of\n   this documentation is not generated (but its boilerplate is).\n\n.. end-include\n',
    'author': 'John Freeman',
    'author_email': 'jfreeman08@gmail.com',
    'url': 'https://github.com/thejohnfreeman/project-template-python/',
    'py_modules': modules,
    'extras_require': extras_require,
    'python_requires': '>=3.6-dev,<4.0',
}


setup(**setup_kwargs)
