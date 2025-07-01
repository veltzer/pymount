""" python deps for this project """

import config.shared

build_requires: list[str] = config.shared.PBUILD
test_requires: list[str] = config.shared.PTEST
requires = build_requires + test_requires
