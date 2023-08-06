# AIConf
This project provides convenience functions to handle config files in HOCON, in particular for the selection of the use of implemented classes and their parameter orchestration.

## Installation
```bash
pip install AIconf
```

## Example

Say you have multiple implementations of `SomeInterface`
```python
class SomeInterface:
    ...

class SomeClass(SomeInterface):
    def __init__(self, arg1, arg2):
        ...
class SomeOtherClass(SomeInterface):
    def __init__(self, arg3, arg4):
        ...
```
You want to use a config file `sample.conf` to select appropriate implementations transparently and choose appropriate parameters.
```hocon
impl_1 = {
  '()' = somepackage.SomeClass
  arg1 = 3
  arg2 = 4
}
impl_2 = {
  '()': somepackage.SomeOtherClass
  arg3 = true
  arg4 = false
}
```
calling
```python
from aiconf import ConfigReader
from aiconf import construct_from_config
cfg = ConfigReader('sample.conf').read_config()
impl_1 = construct_from_config(cfg['impl_1'])
impl_2 = construct_from_config(cfg['impl_2'])

assert isinstance(impl_1, SomeClass)

assert isinstance(impl_1, SomeOtherClass)
```
## Config file backed Argument parser
With a config file `config.conf`
```hocon
foo = "bar"
d {
 y = 3
 z = 4
}

```

and a python script `test.py`
```python
from aiconf import get_arg_parser

parser = get_arg_parser("This is an example arg parser", 'config.conf')
# works like a usual parser
parser.add_argument("--wonk", type=int, default=0)
# get args as usual
args = parser.parse_args()
# get access to the config
conf = parser.conf
assert args.wonk == 3
assert conf['foo'] == "bar"
assert conf['d.y'] == 5
```
run
```bash
python test.py --wonk 3 -c foo=bar -c d.y = 5
```

marvel at its beauty and the merged configs.

For further information, refer to the documentation.
