# mdx-footnotes2

The official Python markdown "footnotes" extension, with additional options.

## Installation

Install the package with pip:

```
pip install mdx-footnotes2
```

## Usage

When using the extension, use "footnotes2" as the extension name instead of "footnotes".

```python
import markdown
md = markdown.Markdown(extensions=["footnotes2"])
```

For all other information, see the [official documentation](https://python-markdown.github.io/extensions/footnotes/).

## Options

Additional options:

`USE_LETTERS`: Use letters (a-z) instead of numbers as footnote markers. Defaults to `False`.

`SHOW_BACKLINKS`: Enable or disable backlinks from the footnote to the reader's place. Defaults to `True`.

For all other information, see the [official documentation](https://python-markdown.github.io/extensions/footnotes/).