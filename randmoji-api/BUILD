python_library(
    sources=[
        "src/**/*.py"
    ]
)

pex_binary(
    name="pex_binary",
    entry_point="src/main.py",
    dependencies=[
        "randmoji-api"
    ],
)

# You need `python_requirements` to teach pants that this project has third-party requirements
# Without this, no requirements will be bundled. By including this directive, pants
# will try to find the `requirements.txt` file for this project (by default assumed
# to be at /apple-pie-api/requirements.txt)
python_requirements()
