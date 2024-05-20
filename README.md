# Arma Reforger Dedicated Server Mod Manager (ardsmm)

## Installation

### Using Virtualenv

```
python -m venv venv 

# If on Windows:
.\venv\Scripts\activate

# If on Linux/Unix:
source venv/bin/activate

pip install git+https://github.com/jhunkeler/ardsmm
```

## Using Conda

```
conda create -n "ardsmm" python
conda activate ardsmm
pip install  git+https://github.com/jhunkeler/ardsmm
```

## Usage

```
usage: ardsmm [-h] [-i] [-o OUTPUT_FILE] [-m MOD_FILE] [-I INDENT] [-V] [configfile]

positional arguments:
  configfile            An Arma Reforger dedicated server JSON config

options:
  -h, --help            show this help message and exit
  -i, --in-place        modify JSON config file in-place
  -o OUTPUT_FILE, --output-file OUTPUT_FILE
                        write JSON output to file (default: stdout)
  -m MOD_FILE, --mod-file MOD_FILE
                        read mods from file (default: stdin)
  -I INDENT, --indent INDENT
                        set JSON indentation level (default: 4)
  -V, --version         display version number and exit

```

## Examples

Create a new configuration file with your `config.json` as the baseline. Mod definitions are appended to `{ "game": { "mods": [] } }`:

```
ardsmm -o test.json -m examples/mods.txt examples/config.json
```

Or add mods to an existing configuration file:

```
ardsmm -i -m examples/mods.txt examples/config.json
```
