# Reportify

## Installation

Assuming you have pip installed, you can run

```bash
pip install reportify --user
```

Omit `--user` if you are running in a Python virtual environment, but otherwise keep it: don't use sudo, it's dangerous because it modifies the Python environment that your operating system may rely on.

If you aren't running in a Python virtual environment, you may need to add `~/.local/bin` to your `PATH` environment variable. This can be done by editing your shell initialization script, usually `~/.bashrc`. (The tilde character '~' will expand to the path to your home directory). Add the following line to the end of that file:

```bash
export PATH=~/.local/bin:$PATH
```

Now check that the `reportify` script is available by trying `reportify --help`. If you see usage information, everything went fine. If you get something like 'command not found', then everything went not fine.

## Usage

To see arguments, run `reportify --help`.

Inside the repository's `examples` directory is an example notebook, `example.ipynb`, on which you can try reportify:

```bash
reportify example.ipynb
```

this should output a file, `example.html`, in the current directory.
