[![PyPI status](https://img.shields.io/pypi/status/ting.svg)](https://pypi.python.org/pypi/ting/)
[![PyPI version](https://img.shields.io/pypi/v/ting.svg)](https://pypi.python.org/pypi/ting/)
[![Pipeline status](https://gitlab.com/frkl/ting/badges/develop/pipeline.svg)](https://gitlab.com/frkl/ting/pipelines)
[![Code style](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)

# ting

*Create Python objects out of data*


## Description

Documentation still to be done.

# Development

Assuming you use [pyenv](https://github.com/pyenv/pyenv) and [pyenv-virtualenv](https://github.com/pyenv/pyenv-virtualenv) for development, here's how to setup a 'ting' development environment manually:

    pyenv install 3.7.3
    pyenv virtualenv 3.7.3 ting
    git clone https://gitlab.com/frkl/ting
    cd <ting_dir>
    pyenv local ting
    pip install -e .[develop,testing,docs]
    pre-commit install


## Copyright & license

[Parity Public License 6.0.0](https://licensezero.com/licenses/parity)


Please check the [LICENSE](/LICENSE) file in this repository (it's a short license!), also check out the [*freckles* license page](https://freckles.io/license) for more details.

### frkl product ids

Versions:

  - 0.9:
    - 97de2bf5-0fbb-4884-9d26-488217e1477c
  - 1.x.x:  
    - 97de2bf5-0fbb-4884-9d26-488217e1477c

[Copyright (c) 2019 frkl OÜ](https://frkl.io)
