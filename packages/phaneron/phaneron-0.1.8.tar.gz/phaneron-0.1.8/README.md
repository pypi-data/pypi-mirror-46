# Phaneron

The phaneron package provides a extended python API for the Phaneron branch of Brayns

### 1. From the Python Package Index

```
(venv)$ pip install phaneron
```

### 2. From git repository

```
(venv)$ pip install git+https://github.com/favreau/pyPhaneron.git
```

### 3. From source

Clone the repository and install it:

```
(venv)$ git clone https://github.com/favreau/Phaneron.git
(venv)$ pip install -e ./pyPhaneron
```

## Connect to running Brayns instance

```python
>>> from brayns import Client
>>> from phaneron import CircuitExplorer

>>> brayns = Client('localhost:8200')
>>> circuit_explorer = CircuitExplorer(brayns)
```

# Upload to pypi

```bash
twine upload dist/*
```
