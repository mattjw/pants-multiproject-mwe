python_library(
    sources=[
        "src/**/*.py"
    ]
)

pex_binary(
    name="pex_binary",
    entry_point="src/main.py",
    dependencies=[
        "apple-pie-api"
    ],
)

# `poetry_requirements` (as an alternative to `python_requirements`) is used to
# teach pants that this project has third-party requirements Without this, no
# requirements will be bundled. By including this directive, pants will try to
# find the `pyproject.toml` file for this project (by default assumed to be at
# `/apple-pie-api/pyproject.toml`)
poetry_requirements()
