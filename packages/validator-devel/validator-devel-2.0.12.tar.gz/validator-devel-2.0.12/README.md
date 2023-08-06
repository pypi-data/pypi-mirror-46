# Validator Devel

this is the frontend dashboard for build module with GLOBO SRL technologies.

Is built with Python and React for the frontend.

## Requirements

* Python >= 3.7.2
* for the frontend only: Node 10.x
* yarn

## Build the project

The project has two different method of build, the first one is use Node for build the frontend and put the result where python can find for serve it.

#### Frontend build

```bash
cd frontend
yarn build
```

#### Python environment

Please consider use virtual environents for the installation:
```bash
pip install -r requirements.txt
python validator_devel/main.py
```
