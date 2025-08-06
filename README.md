# -Project name-

## Information
We'll be using pyodide to work with the frontend

...

## Coding rules
Use `ruff check` to check your code style.
```shell
$ ruff check
```
### Naming
**Functions**: lowercase and use underscores
```py
def my_function():
    my_variable = "value"
```
**Classes and Variable names**: PascalCase style
```py
from typing import List

class MyClass:
    pass

ListOfMyClass = List[MyClass]
```
**Constants**: SCREAMING_SNAKE_CASE style
```py
MY_CONSTANT = 1
```
**Operators**: at the start of a newline
```py
# No
result = (
    1 +
    2 *
    3
)
# Yes
result = (
    1
    + 2
    * 3
)
```
**equivalent to None**: use `is`, `is not` instead of `==`
```py
if variable == None: # No
    print("Variable is None")
if variable is None: # Yes
    print("Variable is None")¨
```
**not** positioning:
```py
if not variable is None: # No
    print("Variable is not None")
if variable is not None: # Yes, easier to read
    print("Variable is not None")
```
**Imports**: do not import multiple modules on one line or everything from a module (*)
```py
# No
import pathlib, os
from pathlib import *

# Yes
import os
import pathlib
from pathlib import Path
```

## Setup
1. First we set up our python enviroment
```shell
$ python -m venv .venv
```
2. Entering it
```shell
# Linux, Bash
$ source .venv/bin/activate
# Linux, Fish
$ source .venv/bin/activate.fish
# Linux, Csh
$ source .venv/bin/activate.csh
# Linux, PowerShell Core
$ .venv/bin/Activate.ps1
# Windows, cmd.exe
> .venv\Scripts\activate.bat
# Windows, PowerShell
> .venv\Scripts\Activate.ps1
```
3. Installing development dependecies
```shell
$ pip install --group dev
```
4. If we want to exit our enviroment we do
```shell
$ deactivate
```
