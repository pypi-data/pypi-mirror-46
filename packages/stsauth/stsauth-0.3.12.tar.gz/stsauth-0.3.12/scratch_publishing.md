# Publishing new versions

## ~/.pypirc

```ini
[distutils]
index-servers =
    pypi

[pypi]
username:phillip.jf
```

- Follow gitflow
- Once merged to develop, bump version in `setup.py`, update `CHANGELOG.md`
- Create PR from develop to master
- Once merged, perform the following:

```shell
git tag -a v0.0.0 -m "v0.0.0"
git push --tags
pip install -U pip setuptools wheel twine
rm -rf dist
python setup.py sdist bdist_wheel --universal
twine upload dist/*
```

- Create a Release in Github from the previously created Tag