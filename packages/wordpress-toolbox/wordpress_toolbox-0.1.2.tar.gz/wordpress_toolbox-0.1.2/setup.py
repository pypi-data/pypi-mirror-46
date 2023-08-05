#!/usr/bin/env python
# -*- encoding: utf-8 -*-
from package_controller.utils import package_setup

package_setup(
    description=(
        "A collection of CLI commands to use for a wordpress website through "
        "it's REST API"
    ),
    author="Alex Seitsinger",
    author_email="contact@alexseitsinger.com",
    base_url="https://github.com/alexseitsinger",
    setup_requires=["package_controller"],
    install_requires=["requests", "click", "python-slugify"],
    console_scripts={"wpt": "cli:main"}
)
