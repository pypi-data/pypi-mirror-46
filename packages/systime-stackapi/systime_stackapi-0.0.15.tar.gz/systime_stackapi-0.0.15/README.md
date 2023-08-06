# systime_stackapi

An API for accessing systimes infrastructure services.

# python environment

    pyenv virtualenv 3.7.1 stack-api
    echo "stack-api" > .python-version
    pip install --upgrade pip
    pyenv activate stack-api
    pip install -r requirements.txt

# package (handled by bitbucket)

    sudo python setup.py sdist bdist_wheel

# local test

    python test.py