import os
import shutil
import json

def load_config(config_path="config.json"):
    """Load configuration from a JSON file."""
    if not os.path.isfile(config_path):
        raise FileNotFoundError(f"Configuration file '{config_path}' not found.")
    with open(config_path, "r") as file:
        return json.load(file)

def create_package(config_path="config.json"):
    """Create a Python package with an 'src' folder based on the provided config."""
    # Load configuration
    config = load_config(config_path)

    # Validate required config fields
    if "files" not in config or not isinstance(config["files"], list):
        raise ValueError("Config must include a 'files' key with a list of Python file paths.")
    if "name" not in config:
        raise ValueError("Config must include a 'name' key for the package name.")

    package_name = config["name"]
    file_paths = config["files"]

    # Create package directory
    if not os.path.exists(package_name):
        os.makedirs(package_name)
        print(f"Created package directory: {package_name}")

    # Create src folder within the package
    src_folder = os.path.join(package_name, "src")
    os.makedirs(src_folder, exist_ok=True)
    print(f"Created src folder: {src_folder}")

    # Copy Python files into the src folder
    module_names = []
    for file_path in file_paths:
        if not os.path.isfile(file_path) or not file_path.endswith('.py'):
            print(f"Skipping invalid Python file: {file_path}")
            continue
        file_name = os.path.basename(file_path)
        module_names.append(os.path.splitext(file_name)[0])
        shutil.copy(file_path, os.path.join(src_folder, file_name))
        print(f"Copied {file_path} to {src_folder}/{file_name}")

    # Generate __init__.py in the root of the package
    with open(os.path.join(package_name, "__init__.py"), 'w') as init_file:
        imports = "\n".join([f"from .src.{module} import *" for module in module_names])
        init_file.write(f"""# __init__.py
{imports}
""")
    print(f"Created {package_name}/__init__.py")

    # Generate README.md and pyproject.toml from config
    generate_readme(package_name, config)
    generate_pyproject(package_name, config)

    print(f"Package '{package_name}' created successfully!")

def generate_readme(package_name, config):
    """Generate a README.md file based on config."""
    readme_content = f"""# {config.get('name', package_name)}

{config.get('description', 'A Python package created with PyPackify.')}

## Author
{config.get('author', 'Unknown')}
"""
    with open(os.path.join(package_name, "README.md"), "w") as file:
        file.write(readme_content)
    print(f"Created {package_name}/README.md")

def generate_pyproject(package_name, config):
    """Generate a pyproject.toml file based on config."""
    pyproject_content = f"""[build-system]
requires = ["setuptools>=42", "wheel"]
build-backend = "setuptools.build_meta"

[project]
name = "{config.get('name', package_name)}"
version = "{config.get('version', '0.1.0')}"
description = "{config.get('description', 'A Python package created with PyPackify.')}"
authors = [
    {{ name = "{config.get('author', 'Unknown')}", email = "{config.get('author_email', 'unknown@example.com')}" }}
]
license = "{config.get('license', 'MIT')}"
readme = "README.md"
requires-python = ">=3.6"
classifiers = [
    "Programming Language :: Python :: 3",
    "License :: OSI Approved :: {config.get('license', 'MIT')} License",
    "Operating System :: OS Independent",
]

[tool.setuptools.packages.find]
where = ["src"]
"""
    with open(os.path.join(package_name, "pyproject.toml"), "w") as file:
        file.write(pyproject_content)
    print(f"Created {package_name}/pyproject.toml")

def main():
    import argparse
    parser = argparse.ArgumentParser(description="Convert multiple Python files into a package.")
    parser.add_argument('--config', default="config.json", help="Path to the config.json file.")
    args = parser.parse_args()

    create_package(args.config)

if __name__ == "__main__":
    main()
