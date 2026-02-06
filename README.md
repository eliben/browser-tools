# browser-tools

Client-side tools running entirely in the browser.

Availailable online at https://eliben.github.io/browser-tools/

## List of tools

* [Remove Background](https://eliben.github.io/browser-tools/remove-background) -
  remove background color from an image.

* [C AST Explorer](https://eliben.github.io/browser-tools/c-ast-explorer) -
  parse C code in the browser with pycparser and interactively explore its AST tree.

## Dependencies

This repository has no JavaScript or Python package manager manifests; tools are primarily
static HTML and load browser/runtime dependencies from CDNs.

* `remove-background.html`: Tailwind CSS via `https://cdn.tailwindcss.com`
* `c-ast-explorer.html`:
  * Pyodide via `https://cdn.jsdelivr.net/pyodide/v0.28.3/full/pyodide.mjs`
  * `micropip` (loaded in Pyodide) and `pycparser` (installed at runtime in the browser)
* `_tools/genindex/genindex.py`: Python standard library only (`html`, `re`, `pathlib`,
  `typing`)
