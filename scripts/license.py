# -*- coding: utf-8 -*-
import subprocess

import toml

# Ouverture du fichier pyproject.toml
with open("pyproject.toml", "r") as file:
    # Parsing du fichier TOML
    pyproject = toml.loads(file.read())

# Récupération des dépendances de développement
dev_dependencies = pyproject["tool"]["poetry"]["dependencies"]

# Boucle pour extraire les noms des packages sans la version
packages = []
for package in dev_dependencies:
    package_name = package.split("=")[0].strip()
    packages.append(package_name)

subprocess.run(
    [
        "pip-licenses",
        "--from",
        "meta",
        "-f",
        "rst",
        "-a",
        "-u",
        "-d",
        "--output-file",
        "third_party.rst",
        "-p",
    ]
    + packages
)
