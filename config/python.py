import config.project

package_name = config.project.project_name

dev_requires = [
    "pyclassifiers",
    "pypitools",
    "pydmt",
    "Sphinx",
    "pymakehelper",
]
test_requires = [
    "pylint",
    "pytest",
    "pytest-cov",
    "pyflakes",
    "flake8",
]

python_requires = ">=3.10"

test_os = ["ubuntu-22.04"]
test_python = ["3.10"]
