# pants-multiproject-mwe

Minimal example of a multi-project set-up using pants.

## Repo-wide things to try out


```bash
./pants lint ::  # lint all projects
```

## Build a single project

Build all outputs for the _helloworld_ project:

```bash
./pants package helloworld:
```

Inspect the pex:

```bash
unzip -l dist/helloworld/pex_binary.pex
```

Or unzip the contents with `unzip dist/helloworld/pex_binary.pex -d dist/_unzip_helloworld`.

Interesting things to note:

- `.deps/*`: Third party dependencies are vendored within the pex. E.g., `.deps/PyYAML-5.4.1-cp38-cp38-macosx_10_9_x86_64.whl/*`.
- `__main__.py`: Boilerplate entry point wrapper, by pex/pants.
- `helloworld/*` The project's first-party code.

## `apple-pie-api` The apple pie dummy project

Project that's a FastAPI HTTP service, with pipenv as its packaging tool.

## Issues encountered

### macOS Python 2.7

When running `./pants package helloworld:`, encounter:

```text
ERROR: Cannot install virtualenv because these package versions have conflicting dependencies.
ERROR: ResolutionImpossible: for help visit https://pip.pypa.io/en/latest/user_guide/#fixing-conflicting-dependencies
pid 39878 -> /System/Library/Frameworks/Python.framework/Versions/2.7/Resources/Python.app/Contents/MacOS/Python /Users/mattjw/.cache/pants/named_caches/pex_root/pip.pex/cf4106b4c7898b462f7c172dde686a9747103f1a --disable-pip-version-check --no-python-version-warning --exists-action a --use-feature 2020-resolver --isolated -q --cache-dir /Users/mattjw/.cache/pants/named_caches/pex_root --log /private/var/folders/67/0hshxfvn5m92fq48mj23ft2w0000gq/T/process-executiong3JbOb/.tmp/tmpsQKNN5/pip.log download --dest /private/var/folders/67/0hshxfvn5m92fq48mj23ft2w0000gq/T/process-executiong3JbOb/.tmp/tmpm1euDx/linux_x86_64-cp-37-cp37m --platform manylinux2014_x86_64 --platform linux_x86_64 --implementation cp --python-version 37 --abi cp37m --only-binary :all: --constraint constraints.txt protobuf>=3.11.3 setuptools<54.0,>=50.3.0 translate>=3.2.1 --index-url https://pypi.org/simple/ --retries 5 --timeout 15 exited with 1 and STDERR:
```

Cause: Unwanted interaction between Pants and macOS system Python

Solution: Drop `"<PATH>"` in `pants.toml`, see `interpreter_search_paths = ["<PYENV>"]`.

Recommendation: All devs exclusively use pyenv, across all platforms (linux, OS X).
