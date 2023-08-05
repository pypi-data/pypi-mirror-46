#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
from typing import List
from pathlib import Path


def rmdawn(filenames: List[str]) -> str:
    """Create an R markdown file from markdown and code files."""
    return "\n\n".join([
        # YAML files
        "---\n" + Path(name).read_text() + "\n---"
        if name.endswith((".yaml", "yml"))

        # Code files that start with knitr spin comments
        else re.sub("#\+ (.*?)\n", r"```{\1}\n",
                    Path(name).read_text()) + "\n```"
        if Path(name).read_text().startswith("#+")
           and name.endswith((".py", ".r", ".R"))

        # R files that do not start with knitr spin comments
        else "```{r}\n" + Path(name).read_text().strip() + "\n```"
        if name.endswith((".r", ".R"))

        # Python files that do not start with knitr spin comments
        else "```{python}\n" + Path(name).read_text().strip() + "\n```"
        if name.endswith(".py", )

        # All other files (markdown, txt, etc.)
        else Path(name).read_text()
        for name in filenames
    ])
