# Getting Started with conda
- move to DCM folder
- `$ conda env create -f environment.yml -p .\venv`
- `$ conda activate .\venv`
- `$ python -m PySimpleGUI.PySimpleGUI`
# Export Environment
- `$ conda env export > environment.yml` 
- delete `name` and `prefix` entries in `environment.yml` after exporting
# Update Env
- `$ conda env update --prefix .\venv --file environment.yml  --prune`
