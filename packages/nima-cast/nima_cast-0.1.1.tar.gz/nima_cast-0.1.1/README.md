# nima_cast


# Installation

Install using pip:
```bash
$ pip install nima_cast
```

Upgrading:
```bash
pip install nima_cast --upgrade
```

# Minio Configuration

On windows: 

```bash
set ACCESS_KEY=XXXXXXXXXXXXXXXXX
set SECRET_KEY=XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
set MINIO_SERVER=YOUR_MINIO_SERVER:9000
```

On ubuntu:

```bash
export ACCESS_KEY=XXXXXXXXXXXXXXXXX
export SECRET_KEY=XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
export MINIO_SERVER=YOUR_MINIO_SERVER:9000
```

# Running the app

```bash
$ nima_cast
```

# Options

- use `--no-minio` for streaming purposes (no need to connect to minio).
- use `--show-debug` to see debug messages from the cast.

# Publishing

Install dependencies:
```bash
pip install twine
```

Update the version in `nima_cast/__init__.py`, create a source distribution and upload them:
```bash
nano nima_cast/__init__.py
python setup.py sdist
twine upload dist/*
```
