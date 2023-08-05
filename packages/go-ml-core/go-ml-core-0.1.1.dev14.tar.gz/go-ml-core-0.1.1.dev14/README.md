# go-ml-core

Some share utilities in Gogoro Machine Learning Team.

## Release instructions

- To install essential packages

```
pip3 install setuptools wheel twine
```

- To prepare a ~/.pypirc

```
[distutils]
index-servers = pypi

[pypi]
repository:https://upload.pypi.org/legacy/
username:<username>
password:<password>
```

- To revision new version in setup.py


- To compile and upload

```
python3 setup.py sdist bdist_wheel
twine upload --skip-existing dist/*
```

## Config Setting

### Reference

```
config.yml
```

### Optional configs

- mlcore.datahelper.s3.write

```
default: mlcore.datahelper.s3.read
```

- mlcore.datahelper.s3.read.s3baseprefix

```
default: "ml/"
```

- mlcore.datahelper.s3.read.aws-access-key-id & mlcore.datahelper.s3.read.aws-secret-access-key

```
login using key or not
```

- mlcore.datahelper.s3.read.role-arn & mlcore.datahelper.s3.read.role-session-name

```
assume role or not
```
 

