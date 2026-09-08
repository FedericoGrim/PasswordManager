# Generating documentation — Password Manager Backend

How to generate the Python code documentation automatically with Sphinx.

## 1. Preparation

- Make sure **every folder containing `.py` files has an `__init__.py` file** (can be empty).
- Write **docstrings** (explanations of functions, classes and methods) using `''' ... '''` or `""" ... """`, right after their definition.

## 2. Generating the `.rst` files

From the `docs` folder, run:

```bash
sphinx-apidoc -o . ../
```

This generates one `.rst` file per module, based on the docstrings in the `.py` files.

## 3. Build and live preview of the documentation

Move the generated `.rst` files into `docs/source/`, then make sure they're listed in the `toctree` in `index.rst`:

```rst
.. toctree::
   :maxdepth: 2
   :caption: Contents

   modules
```

Finally, from the `docs/source` folder, start the preview server:

```bash
sphinx-autobuild . _build/html
```

The documentation will be available at http://127.0.0.1:8000 and will rebuild automatically on every change to the code or docstrings.
