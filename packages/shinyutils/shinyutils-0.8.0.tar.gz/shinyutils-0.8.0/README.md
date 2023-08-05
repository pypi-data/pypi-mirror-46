# shinyutils
Various utilities for common tasks. :sparkles: :sparkles: :sparkles:

## Setup
Install with `pip`.

```bash
pip install shinyutils
```

## `matwrap`
Wrapper around `matplotlib` and `seaborn`.
### Usage
```python
from shinyutils import MatWrap as mw  # do not import `matplotlib`, `seaborn`

mw.configure()  # this should be called before importing any packages that import matplotlib

fig = mw.plt().figure()
ax = fig.add_subplot(111)  # `ax` can be used normally now

# Use class methods in `MatWrap` to access `matplotlib`/`seaborn` functions.
mw.mpl()  # returns `matplotlib` module
mw.plt()  # returns `matplotlib.pyplot` module
mw.sns()  # returns `seaborn` module
```

### Configuration
Use `mw.configure` to configure plots. Arguments (defaults indicated with []) are:
```python
context: seaborn context ([paper]/poster/talk/notebook)
style: seaborn style (white/whitegrid/dark/darkgrid/[ticks])
font: any font available to fontspec (default [Latin Modern Roman])
latex_pkgs: additional latex packages to be included before defaults
**rc_extra: matplotlib rc parameters to override defaults
```

## `subcls`
Utility functions for dealing with subclasses.
### Functions
* __`get_subclasses(cls)`__: returns a list of all the subclasses of `cls`.
* __`get_subclass_names(cls)`__: returns a list of names of all subclasses of `cls`.
* __`get_subclass_from_name(base_cls, cls_name)`__: return the subclass of `base_cls` named `cls_name`.
* __`build_subclass_object(base_cls, cls_name, kwargs)`__: return an instance of `get_subclass_from_name` initialized using `kwargs`.

## `argp`
Utilities for argument parsing.
### `LazyHelpFormatter`
`HelpFormatter` with sane defaults, and colors (courtesy of `crayons`)! To use, simply pass `formatter_class=LazyHelpFormatter` when creating `ArgumentParser` instances.
```python
arg_parser = ArgumentParser(formatter_class=LazyHelpFormatter)
sub_parsers = arg_parser.add_subparsers(dest="cmd")
sub_parsers.required = True
# `formatter_class` needs to be set for sub parsers as well.
cmd1_parser = sub_parsers.add_parser("cmd1", formatter_class=LazyHelpFormatter)
```

### `comma_separated_ints`
`ArgumentParser` type representing a comma separated list of ints (example `1,2,3,4`).
```python    
arg_parser.add_argument("--csi", type=comma_separated_ints)
```

### `OutputFileType`
`ArgumentParser` type representing an output file. The file's base directory is created if needed. The returned value is a file object.

### `OutputDirectoryType`
`ArgumentParser` type representing an output directory. The directory is created if it doesn't exist.

### `ClassType`
`ArgumentParser` type representing sub-classes of a given base class. The returned value is a class.
```python
class Base:
    pass

class A(Base):
    pass

class B(Base):
    pass

arg_parser.add_argument("--cls", type=ClassType(Base), default=A)
```

### `shiny_arg_parser`
`ArgumentParser` object with LazyHelpFormatter, and logging argument.

## `logng`
Utilities for logging.
### `build_log_argp`
Creates an argument group with logging arguments.
```
>>> arg_parser = ArgumentParser()
>>> build_log_argp(arg_parser)
>>> arg_parser.print_help()
usage: test.py [-h] [--log-level {DEBUG,INFO,WARNING,ERROR,CRITICAL}]

optional arguments:
  -h, --help            show this help message and exit
  --log-level {DEBUG,INFO,WARNING,ERROR,CRITICAL}
```

### `conf_logging`
Configures global logging (and adds colors!) using arguments returned by `ArgumentParser.parse_args`. `log_level` can be over-ridden with the keyword argument. Colors are not enabled if output isn't a tty.
```python
args = arg_parser.parse_args()
conf_logging(args)
conf_logging(args, log_level="INFO")  # override `log_level`
```
By default, the package configures logging at INFO level.
