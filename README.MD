
# PyPackify

PyPackify is a tool for converting multiple Python files into a structured Python package. It generates essential package files for easy usage and distribution.

## Features

* Converts multiple Python files into a Python package.
* Generates a `pyproject.toml` file for Python packaging.
* Creates a root-level `__init__.py` to expose package functionality.

## Installation

Use Python 3.6 or newer. The script uses only the Python standard library.

```bash
git clone https://github.com/SpyC0der77/PyPackify.git
cd PyPackify
```

## Usage

1. Create a `config.json` file specifying your package metadata and Python files to include.

### Example `config.json`:

```json
{
  "name": "example_package",
  "version": "0.1.0",
  "author": "John Doe",
  "author_email": "johndoe@example.com",
  "description": "An example package created with PyPackify.",
  "license": "MIT",
  "files": [
    "example1.py",
    "example2.py"
  ]
}
```

2. Run the script:

```bash
python pypackify.py --config config.json
```

3. Check the generated package directory:

```
example_package/
├── README.md
├── pyproject.toml
├── __init__.py
├── src/
│   ├── example1.py
│   ├── example2.py
```

## Current limitations

Paths in `files` resolve relative to the working directory. Invalid or missing Python files are skipped. Running the script again with the same package name overwrites generated metadata and copied files.

The generated layout is a starting point. It creates `__init__.py` at the root while setuptools discovery points at `src`, so review the package layout and imports before building or publishing it. The script does not build a wheel or publish to PyPI.

## License

This project is licensed under the MIT License.
