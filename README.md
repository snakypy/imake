# iMake

[![Tests](https://github.com/snakypy/imake/actions/workflows/tests.yml/badge.svg)](https://github.com/snakypy/imake/actions/workflows/tests.yml)
[![Python Versions](https://img.shields.io/pypi/pyversions/imake)](https://pyup.io/repos/github/snakypy/imake/)
[![Python Whell](https://img.shields.io/pypi/wheel/imake)](https://pypi.org/project/wheel/)
[![PyPI](https://img.shields.io/pypi/v/imake)](https://pypi.org/project/imake/#history)
[![PyPI - Implementation](https://img.shields.io/pypi/implementation/imake)](https://pypi.org/project/imake)
[![Isort](https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=ef8336)](https://pycqa.github.io/isort/)
[![Mypy](http://www.mypy-lang.org/static/mypy_badge.svg)](http://mypy-lang.org/)
[![Code style: Black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![PyPI - Downloads](https://img.shields.io/pypi/dm/imake)](https://pypi.org/project/imake/#files)
[![GitHub license](https://img.shields.io/github/license/snakypy/imake)](https://github.com/snakypy/imake/blob/master/LICENSE)

----------------
<div align="center">
  <h4>
    <a href="#requirements">Requirements</a> |
    <a href="#installing">Install</a> |
    <a href="#configuration">Configuration</a> |
    <a href="#using">Using</a> |
    <a href="#donation">Donation</a> |
  </h4>
  <h5>
    | <a href="#more-commands">More Commands</a> |
  </h5>
</div>

<div align="center">
  <sub>Built with ❤︎ by:
  <a href="https://williamcanin.github.io" target="_blank">William Canin</a> in free time,
  to the sound of the playlist: <a href="https://open.spotify.com/playlist/48brJJZdVifY79QAFmEImq?si=GmsvfKqATpG4p72ZeVClIQ" target="_blank">Bursting Of The Tympanum</a></sub>
</div>
<br>
<br>

**iMake** is a command line tool to simplify commands in [Python](https://python.org) projects, discarding the usability of a [Makefile](https://www.gnu.org/software/make/) file.
As **iMake** saves on typed commands, passing them a configuration file.

## Requirements

To work correctly, you will first need:

- [`Python`](https://python.org) (v3.9 or recent);
- [`Pip`](https://pip.pypa.io/en/stable/) (v21.0.1 or recent) must be installed;

## Installing

```shell
$ pip install imake --user
```

## Configuration

The configuration file must exist at the location where **imake** will be called. The file must be named **.imake **, that is, a file hidden on Unix systems.

To create the file use `touch`:

```shell
$ touch .imake
```

After creating the file, you should leave it with the following structure. Example:

```toml
[build]
commands = ["python setup.py sdist"]
```

The key with the name **commands** is an Array and must be mandatory for **iMake**. In this key you must inform the commands you want to execute using the primary key, in this case, the **build**.

Option with multiple commands:

```toml
[build]
commands = ["rm -rf build", "rm -rf docs/_build;", "python setup.py sdist"]
```

You can also execute commands in blocks instead of a list, as follows using triple quotes:

```toml
[clean]
commands = ["""
            if [[ -d "build" ]]; then
              rm -r build;
            fi
            rm -rf docs/_build;
            rm -rf .pytest_cache;
"""]
```

**iMake** settings still have 3 other keys, which are **description**, **header**, and **footer**. All optional.

The key **description** you must put only a description for a given command. Example:

```toml
[build]
description = "This command compiles the project."
commands = ["rm -rf build", "rm -rf docs/_build;", "python setup.py sdist"]
```

The **header** key is a message that will appear before the commands start. Example:

```toml
[build]
description = "This command compiles the project."
header = "Starting the build ..."
commands = ["rm -rf build", "rm -rf docs/_build;", "python setup.py sdist"]
```

The **footer** key is a message that will appear after the commands are finished. Example:

```toml
[build]
description = "This command compiles the project."
header = "Starting the build ..."
commands = ["rm -rf build", "rm -rf docs/_build;", "python setup.py sdist"]
footer = "Build command finished!"
```

> Note: The position of the keys does not imply anything, but the values do. The command that you put first in the **commands** key will be the first to be executed.

Another interesting option is that you can call the execution of a command within another one using **imake**. Would be like this:

```toml
[build]
description = "This command compiles the project."
header = "Starting the build ..."
commands = ["imake clean -q", "python setup.py sdist"]
footer = "Build command finished!"
```

Notice that the command **imake clean -q** is inside **commands**. Where the `-q` option means to silence verbose mode.

## Using

After making the settings in the file **.imake**, execute the command **imake** followed by the primary key, which in our example is **build**. It will look like this:

```shell
$ imake build
```

You can run the help command, `imake -h` to show which commands are available to you. Any configuration that is in the **.imake** file will be shown in `help`, minus the description of each command, which will be shown only if you run the `--desc` or `-d` option, for example:

```shell
$ imake build --desc 
```

 ## More Commands

For more command information, use:

```shell
$ imake -h
```

## Donation

If you liked my work, buy me a coffee :coffee: :smiley:

[![paypal](https://www.paypalobjects.com/en_US/i/btn/btn_donateCC_LG.gif)](https://www.paypal.com/cgi-bin/webscr?cmd=_s-xclick&hosted_button_id=YBK2HEEYG8V5W&source)

## License

The project is available as open source under the terms of the [MIT License](https://github.com/snakypy/imake/blob/master/LICENSE) ©

## Credits

See, [AUTHORS](https://github.com/snakypy/imake/blob/master/AUTHORS.rst).
