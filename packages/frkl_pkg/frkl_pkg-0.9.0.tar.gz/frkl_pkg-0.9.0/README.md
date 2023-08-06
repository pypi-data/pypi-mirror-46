[![PyPI status](https://img.shields.io/pypi/status/frkl-pkg.svg)](https://pypi.python.org/pypi/frkl-pkg/)
[![PyPI version](https://img.shields.io/pypi/v/frkl-pkg.svg)](https://pypi.python.org/pypi/frkl-pkg/)
[![PyPI pyversions](https://img.shields.io/pypi/pyversions/frkl-pkg.svg)](https://pypi.python.org/pypi/frkl-pkg/)
[![Pipeline status](https://gitlab.com/frkl/frkl-pkg/badges/develop/pipeline.svg)](https://gitlab.com/frkl/frkl-pkg/pipelines)
[![Code style](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)

# frkl-pkg

*Runtime package and environment management.*


## Description

Documentation still to be done.

# Development

Assuming you use [pyenv](https://github.com/pyenv/pyenv) and [pyenv-virtualenv](https://github.com/pyenv/pyenv-virtualenv) for development, here's how to setup a 'frkl-pkg' development environment manually:

    pyenv install 3.7.3
    pyenv virtualenv 3.7.3 frkl_pkg
    git clone https://gitlab.com/frkl/frkl_pkg
    cd <frkl_pkg_dir>
    pyenv local frkl_pkg
    pip install -e .[develop,testing,docs]
    pre-commit install


## Copyright & license

Please check the [LICENSE](/LICENSE) file in this repository (it's a short license!), also check out the [*freckles* license page](https://freckles.io/license) for more details.

[Parity Public License 6.0.0](https://licensezero.com/licenses/parity)

[Copyright (c) 2019 frkl OÜ](https://frkl.io)
