# We set `module_mapping` for any requirements whose module names differ from the project's name so that dependency
# inference works.
python_requirements(
  module_mapping={
    "ansicolors": ["colors"],
    "setuptools": ["pkg_resources"],
  },
)

# Implicit from this BUILD file are `constraints.txt` and `requirements.txt` (TO BE CONFIRMED)
# See https://www.pantsbuild.org/docs/python-third-party-dependencies
