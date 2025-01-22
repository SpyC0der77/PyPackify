# PyPackify

PyPackify is a tool for converting multiple Python files into a structured Python package. It generates essential package files for easy usage and distribution.

## Features

* Converts multiple Python files into a Python package.
* Specify metadata

## Installation

Clone the repository or copy the `pypackify.py` script to your working directory.

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
├── setup.py
├── __init__.py
├── src/
│   ├── example1.py
│   ├── example2.py
```

## License

This project is licensed under the MIT License.
