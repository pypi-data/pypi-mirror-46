## Build from sources

```
pipenv run python setup.py clean build bdist bdist_wheel bdist_pex --pex-args="--disable-cache" --bdist-all
docker run -v "$(pwd):/src/" cdrx/pyinstaller-linux "pyinstaller --clean -y --dist ./dist --workpath /tmp *.spec"
docker run -v "$(pwd):/src/" cdrx/pyinstaller-windows "pip install --upgrade setuptools && pyinstaller --clean -y --dist ./dist --workpath /tmp *.spec"
```

## Release

```
pipenv shell

prerelease

pipenv run python setup.py clean build bdist bdist_wheel &&\
docker run -v "$(pwd):/src/" cdrx/pyinstaller-linux "pyinstaller --clean -y --dist ./dist --workpath /tmp *.spec" &&\
docker run -v "$(pwd):/src/" cdrx/pyinstaller-windows "pip install --upgrade setuptools && pyinstaller --clean -y --dist ./dist --workpath /tmp *.spec"

release

githubrelease release Toilal/python-cfssl-cli create $(python -m cfsslcli --version | cut -d ' ' -f 3-) --publish "dist/*"

postrelease
```