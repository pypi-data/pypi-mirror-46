# Orion Framework

Python library companion for the Orion Framework

## How to build from source

```bash
git clone ...
cd orionframework
python3 -m venv .python-env
source .python-env/bin/activate
pip install -r requirements.txt

#
# at least once to set up all your libraries needed to build
#
source scripts/pre-build.sh

#
# actually build the local package
#
source scripts/build.sh

```