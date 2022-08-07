# Getting Started

Python Shiny app for handling Prodigy datasets.

## Installation instructions

Create a new virtual environment.

```bash
python -m venv venv
source venv/bin/activate
```

Install packages.

```bash
pip install --upgrade pip wheel
pip install -r requirements.txt
```

## Developer

Requirements for development are included in the `requirements-dev.txt` file. This includes requirements for building and serving the documentation.

There is also a `requirements-prodigy.txt` file, _not included in this repo_, for installing Prodigy. The file is only:

```txt
--extra-index-url https://XXXX-XXXX-XXXX-XXXX@download.prodi.gy/index 
prodigy>=1.11.0,<2.0.0
```

## Run shiny project

Run the python shiny app.

```bash
shiny run --reload 
```
