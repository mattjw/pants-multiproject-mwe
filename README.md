# pants-multiproject-mwe

Minimal example of a multi-project set-up using pants.

This repo riffs off `https://github.com/pantsbuild/example-python`.

## Repo-wide things to try out

- `./pants lint ::` Lint all projects
- `./pants help goals` List all the pants goals; e.g., this will remind you you have `./pants fmt` available, which will black-format a project.
- `./pants help` Pants CLI help.
- `./pants list ::` List all targets that match the `::` pattern. The `::` arg can be replaced by any pants _Address_ (read docs [here](https://www.pantsbuild.org/v2.0/docs/targets#target-addresses)). `::` is a special _target selector_ that matches "everything", so this lists all targets in this repo. Notes on selectors:

  > Pants supports two globbing target selectors, as a convenience on the command-line. These forms are not allowed in BUILD files.
  > A trailing single colon specifies a glob of targets at the specified location
  > A trailing double colon specifies a recursive glob of targets at the specified location

## Understanding dependencies and dependency inference

Root level files: `BUILD`, `constraints.txt`, and `requirements.txt`; also, `requirement_constraints = "constraints.txt"` in `pants.toml`. To do: Clarify the role of these files.

See also https://www.pantsbuild.org/docs/python-third-party-dependencies

Get pants's view of what the dependencies for a given file are: `./pants dependencies apple-pie-api/src/main.py`.

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

Project that's a FastAPI HTTP service, with Pipenv as its packaging tool. The project-specific Pipenv tooling and the repo-wide pants tooling co-exist. Refer to `apple-pie-api/README.md` for the pretend "project-specific" documentation, which treats that as a project that's unaware that it sits inside a pants repo.

### Build

Full build pipeline...

```bash
bash -c "\
  cd apple-pie-api \
    && pipenv lock -r > requirements.txt \
"
./pants package apple-pie-api:pex_binary
```

Then run `./pants package apple-pie-api:pex_binary`.

Things to note about the build process...

- Inspect the output pex with `unzip -l dist/apple-pie-api/pex_binary.pex` or `unzip dist/apple-pie-api/pex_binary.pex -d dist/_unzip_apple-pie-api`.
- Inspect the resolved dependencies for the entry point, according to pants, with `./pants dependencies apple-pie-api/src/main.py`:

  ```text
  apple-pie-api/src/main.py:../apple-pie-api
  apple-pie-api/src/numerics/pi.py:../../apple-pie-api
  apple-pie-api:fastapi
  apple-pie-api:uvicorn
  ```

- Some things that end up in the pex's `.deps` (`unzip -l dist/apple-pie-api/pex_binary.pex`):

  ```text
  .deps/click-7.1.2-py2.py3-none-any.whl/
  .deps/fastapi-0.65.1-py3-none-any.whl/
  .deps/h11-0.12.0-py3-none-any.whl/
  .deps/pydantic-1.8.2-cp38-cp38-macosx_10_9_x86_64.whl/
  .deps/starlette-0.14.2-py3-none-any.whl/
  .deps/typing_extensions-3.10.0.0-py3-none-any.whl/
  .deps/uvicorn-0.13.4-py3-none-any.whl/
  ```

  Note that there is _no_ `pycountry` in the `.deps` directory, even though it is in the `Pipfile` and `requirements.txt`. Explanation as follows...

  - `pycountry` is not referenced in any of the project's source code. pants's dependency inference inspects the source code (i.e., `import` statements) and identifies dependencies that are genuinely required by the project. By running `./pants dependencies apple-pie-api:` you'll see that `apple-pie-api:pycountry` doesn't appear in the dependencies, whereas the dependencies we _would_ expect are listed, like `apple-pie-api:fastapi`.
  - For the sake of demonstration, we could add an `import pycountry` to `apple-pie-api/src/main.py`, and then we'd see that `apple-pie-api:pycountry` would appear in the dependencies list and will be vendored into the pex file.
  - What if we have a package that's imported by some magic but not referenced in an explicit `import`? You can use the `dependencies` arg of the `python_library` directive. This we force any explicitly listed dependencies into the build. More info [here](https://www.pantsbuild.org/docs/python-third-party-dependencies#basic-setup).
  - What if we have a package that has a different package name to its import statements? E.g. ,`bs4` vs `beautifulsoup4`.  Name mapping rules can be specified via [`module_mapping`](https://www.pantsbuild.org/docs/python-third-party-dependencies#basic-setup).

### Execute from pex

You can simply execute to pex file!

```bash
./dist/apple-pie-api/pex_binary.pex
```

And then send a request with `curl http://127.0.0.1:8096`.

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

## To be explored

- Additional FastAPI service with partially overlaping dependencies as the existing FastAPI service
- Library shared among multiple projects
- Introspection and git-diff-based changes
- Automated builds to docker images
- Within-project tests
- Cross-project tests
