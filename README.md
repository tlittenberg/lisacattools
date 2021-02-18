# lisacattools

Python module for interacting with example LISA catalogs

## 1 - Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and
testing purposes.

### 1.1 - Prerequisites

You will need python3 to run this program.

### 1.2 - Installing

First, we need to clone the repository

#### 1.2.2 - By pip (for users)

To install the package for non-root users:
```
make user
```

To install the package on the root system:
```
make
```

#### 1.2.3 - By pip (for developpers)

Create a virtualenv

```
make prepare-dev
source .lisacattools-env
```

Install the sotfware and the external libraries for development purpose

```
make install-dev
```

## 2 - Development

Install the software by PIP (developpers version)

Then, develop your code and commit
```
git commit
```
The tests and code style formater will be run automatically. To ignore the
checks, do
```
git commit --no-verify
```

## Versioning

We use [SemVer](http://semver.org/) for versioning. For the versions available, see the [tags on this repository](https://github.com/your/project/tags).

## Authors

* **James I. Thorpe**, **Tyson B. Littenberg** - Initial work
* **Jean-Christophe Malapert**

## License

This project is licensed under the LGPLV3 License - see the [LICENSE](LICENSE) file for details