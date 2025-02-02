import os
import shutil
import json
import toml
import re
import argparse

def load_config(config_path="config.json"):
    """Load configuration from a JSON file."""
    if not os.path.isfile(config_path):
        raise FileNotFoundError(f"Configuration file '{config_path}' not found.")
    with open(config_path, "r") as file:
        return json.load(file)

def load_license_text(license_name):
    """Load the license text from licenses.json."""
    licenses_path = "licenses.json"
    if not os.path.isfile(licenses_path):
        raise FileNotFoundError(f"Licenses file '{licenses_path}' not found.")
    with open(licenses_path, "r") as file:
        licenses = json.load(file)
    return licenses.get(license_name, f"License text for '{license_name}' not found.")

def validate_version(version):
    """Validate that the version string follows semantic versioning."""
    semver_pattern = r"^\d+\.\d+\.\d+$"
    if not re.match(semver_pattern, version):
        raise ValueError(f"Invalid version format: '{version}'. Expected format: X.Y.Z (e.g., 1.0.0)")

def deep_merge_dicts(base, extra):
    """
    Recursively merge the extra dictionary into the base dictionary.
    If keys overlap and both values are dictionaries, merge them;
    otherwise, overwrite the base value with the extra value.
    """
    for key, value in extra.items():
        if key in base and isinstance(base[key], dict) and isinstance(value, dict):
            deep_merge_dicts(base[key], value)
        else:
            base[key] = value
    return base

def create_package(config_path="config.json"):
    """Create a Python package following the specified structure."""
    # Load configuration
    config = load_config(config_path)

    # Validate required config fields
    if "files" not in config or not isinstance(config["files"], list):
        raise ValueError("Config must include a 'files' key with a list of Python file paths.")
    if "name" not in config:
        raise ValueError("Config must include a 'name' key for the package name.")
    if "username" not in config:
        raise ValueError("Config must include a 'username' key for the package namespace.")

    validate_version(config.get("version", "0.1.0"))

    package_name = f"{config['name']}"
    root_dir = config["name"]
    src_folder = os.path.join(root_dir, "src", package_name)
    tests_folder = os.path.join(root_dir, "tests")
    os.makedirs(src_folder, exist_ok=True)
    os.makedirs(tests_folder, exist_ok=True)
    print(f"Created package directory: {src_folder}")

    # Copy Python files into the package directory
    for file_path in config["files"]:
        if not os.path.isfile(file_path) or not file_path.endswith('.py'):
            print(f"Skipping invalid Python file: {file_path}")
            continue
        file_name = os.path.basename(file_path)
        shutil.copy(file_path, os.path.join(src_folder, file_name))
        print(f"Copied {file_path} to {src_folder}/{file_name}")

    # Generate __init__.py in the package directory
    init_path = os.path.join(src_folder, "__init__.py")
    with open(init_path, 'w') as init_file:
        init_file.write(f"# Package: {package_name}\n")
    print(f"Created {init_path}")

    # Generate pyproject.toml in the root directory using the updated TOML format
    generate_pyproject(root_dir, package_name, config)

    # Generate README.md in the root directory
    generate_readme(root_dir, config)

    # # Generate LICENSE file in the root directory
    # generate_license(root_dir, config)

    # Generate MANIFEST.in in the root directory to include the LICENSE file
    # generate_manifest(root_dir, config)

    print(f"Package '{package_name}' created successfully!")

def generate_pyproject(root_dir, package_name, config):
    """Generate a pyproject.toml file in the root directory using the updated TOML format."""
    license_classifiers = {
        "MIT": "License :: OSI Approved :: MIT License",
        "Apache-2.0": "License :: OSI Approved :: Apache Software License",
        "GPL-3.0-or-later": "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
    }

    license_name = config.get("license", "MIT")
    license_classifier = license_classifiers.get(
        license_name, "License :: Other/Proprietary License"
    )

    pyproject_data = {
        "build-system": {
            "requires": ["setuptools>=42", "wheel"],
            "build-backend": "setuptools.build_meta",
        },
        "project": {
            "name": package_name,
            "version": config.get("version", "0.1.0"),
            "description": config.get("description", "A Python package created with PyPackify."),
            "authors": [
                {
                    "name": config.get("author", "Unknown"),
                    "email": config.get("author_email", "unknown@example.com"),
                }
            ],
            # Updated license field using the new TOML/PEP 621 format:
            "license": {"text": license_name},
            "readme": "README.md",
            "requires-python": ">=3.6",
            "classifiers": [
                "Programming Language :: Python :: 3",
                license_classifier,
                "Operating System :: OS Independent",
            ],
        },
        "tool": {
            "setuptools": {
                "packages": {
                    "find": {
                        "where": ["src"],
                    }
                }
            }
        },
    }

    # Merge custom entries from config.json (if provided) into pyproject_data.
    if "pyproject_extra" in config and isinstance(config["pyproject_extra"], dict):
        deep_merge_dicts(pyproject_data, config["pyproject_extra"])

    pyproject_path = os.path.join(root_dir, "pyproject.toml")
    try:
        with open(pyproject_path, "w") as file:
            toml.dump(pyproject_data, file)
        print(f"Created {pyproject_path}")
    except (OSError, IOError) as e:
        print(f"Error creating pyproject.toml: {e}")

def generate_readme(root_dir, config):
    """Generate a README.md file in the root directory."""
    readme_source = config.get("readme", "README.md")
    try:
        with open(readme_source, "r") as file:
            readme_content = file.read()
    except FileNotFoundError:
        readme_content = f"# {config.get('name', 'Package')}\n\nA Python package created with PyPackify."
    readme_content += "\n\nGenerated with [PyPackify](https://github.com/SpyC0der77/PyPackify). Package your python files, the easy way."
    readme_path = os.path.join(root_dir, "README.md")
    with open(readme_path, "w") as file:
        file.write(readme_content)
    print(f"Created {readme_path}")

def generate_license(root_dir, config):
    """Generate a LICENSE file in the root directory."""
    license_name = config.get("license", "Unlicensed")
    license_text = load_license_text(license_name)

    # Replace placeholders dynamically
    year = str(config.get("year", "2025"))
    author = config.get("author", "Unknown")
    license_text = license_text.replace("[YEAR]", year).replace("[AUTHOR]", author)

    license_path = os.path.join(root_dir, "LICENSE")
    try:
        with open(license_path, "w") as file:
            file.write(license_text)
        print(f"Created {license_path}")
    except (OSError, IOError) as e:
        print(f"Error creating LICENSE: {e}")

def generate_manifest(root_dir, config):
    """Generate a MANIFEST.in file in the root directory to include the LICENSE file."""
    manifest_path = os.path.join(root_dir, "MANIFEST.in")
    manifest_content = "include LICENSE\n"
    try:
        with open(manifest_path, "w") as file:
            file.write(manifest_content)
        print(f"Created {manifest_path}")
    except (OSError, IOError) as e:
        print(f"Error creating MANIFEST.in: {e}")

def main():
    parser = argparse.ArgumentParser(
        description="Package Python files into a structured package using config.json"
    )
    parser.add_argument('--config', default="config.json", help="Path to the config.json file.")
    args = parser.parse_args()

    create_package(args.config)

if __name__ == "__main__":
    main()
