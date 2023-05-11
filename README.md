# Ask My Texts


- Prepare several texts in Markdown format
- Ask questions about the texts using [Streamlit](https://www.streamlit.io/) UI


## How to prepare text

Put your text in `texts` folder.
The texts should be in [Markdown](https://en.wikipedia.org/wiki/Markdown) format.
In the beginning of each file include Markdown front matter with `url` and `title` fields.

```markdown
---
url: https://example.com
title: Example
---
Your text here
```


## How to launch

```sh
make run
```


## How to use

Navigate to [http://localhost:8501](http://localhost:8501) in your browser.
Ask questions about the text in the text box.