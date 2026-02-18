# Report issues

If you have any issue with **The Fuck** (Python 3.12.X version), we’ll do our best to fix it. First, try **updating the project** and see if the bug persists.

If the issue remains, check if it has already been reported. If not, open an issue on [GitHub](https://github.com/Radiump123/thefuck-py3.12.x) with the following information:

* Output of `thefuck --version` (e.g., `The Fuck 4.0 using Python 3.12.x`)
* Your shell and version (`bash`, `zsh`, *Windows PowerShell*, etc.)
* Your system (Debian 13, Arch Linux, Windows, macOS, etc.)
* Steps to reproduce the bug
* Output of The Fuck with debugging enabled:

```bash
export THEFUCK_DEBUG=true
thefuck
```

* If the bug is application-specific, include that app’s version and output
* Anything else you think might be relevant

The more information you provide, the easier it is to fix the problem.

---

# Make a pull request

We gladly accept pull requests for new rules, features, bug fixes, etc., on [GitHub](https://github.com/Radiump123/thefuck-py3.12.x).

---

# Developing

There are two ways to develop locally:

1. Using a local Python 3.12.x installation with a virtual environment
2. Using the included **VSCode Dev Container**

---

## Develop using local Python installation

[Create and activate a Python 3.12 virtual environment.](https://docs.python.org/3/tutorial/venv.html)

Install **The Fuck** for development:

```bash
pip install -r requirements.txt
python setup.py develop
```

Run code style checks:

```bash
flake8
```

Run unit tests:

```bash
pytest
```

Run unit and functional tests (requires Docker):

```bash
pytest --enable-functional
```

For packaging and publishing to PyPI:

```bash
sudo apt-get install pandoc
./release.py
```

---

## Develop using Dev Container

A [VSCode DevContainer](https://code.visualstudio.com/docs/remote/remote-overview) is included for a ready-to-go development environment. It comes with all prerequisites pre-installed, so you don’t need a local Python setup.

### Prerequisites

* [Docker](https://www.docker.com/products/docker-desktop)
* [VSCode](https://code.visualstudio.com/)
* [VSCode Remote Development Extension](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.vscode-remote-extensionpack)
* Windows users: WSL2 + Docker configured for WSL2

Full installation notes [here](https://code.visualstudio.com/docs/remote/containers#_installation).

### Running the container

1. Open VSCode
2. Open the command palette (CMD+SHIFT+P on macOS, CTRL+SHIFT+P on Windows)
3. Select **Remote-Containers: Reopen in Container**
4. VSCode will build the container, install pip requirements, and mount your workspace automatically
5. Your VSCode + container environment is now fully ready for development
