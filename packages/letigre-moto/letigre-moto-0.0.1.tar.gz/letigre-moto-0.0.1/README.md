# Moto - Mock AWS Services

A version from https://github.com/spulec/moto for letigre.

# Build and hosting (Works only in Linux machine. Can use vaggrant linux vm)
0. Clone letigre-moto from Letigre project and make required chnages.
1. Update setup.py with updated version.
2. Run python setup.py sdist bdist_wheel to create a distribution.
3. Update ~/.pypirc with below details
```console
[server-login]
username:letigre
password:<pwd>
```
4. pip install twine
5. twine upload dist/*
6. View the dist in pypi https://pypi.org

## Install in your machine

```console
$ pip install "letigre-moto[server]"
```
