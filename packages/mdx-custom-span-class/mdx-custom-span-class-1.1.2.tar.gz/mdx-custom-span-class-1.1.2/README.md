## Custom Span Class Markdown Extension

This is a simple extension for Python-Markdown library, which allows adding span elements with custom class.

The original version was developed by [exaroth](https://github.com/exaroth/mdx_custom_span_class).

It was then improved by [plugboy](https://github.com/plugboy/mdx_custom_span_class).

This version allows easier installation via `pip install mdx-custom-span-class`.

## Syntax

The syntax is:
```
!!<class name>|<text to be wrapped>!!
```
For instance:

```shell
I love !!text-alert|spam!!
```
will return

```html
<p>I love <span class="text-alert">spam</span></p>
```

### Installation

```shell
pip install mdx-custom-span-class
```

### Usage

```python
import markdown

md = markdown.Markdown(extensions=["custom-span-class"])
md.convert("I love !!text-danger|spam!!")

```