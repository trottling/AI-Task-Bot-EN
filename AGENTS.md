# Developer Guidelines

- Use PEP8 code style. Before committing, run a syntax check:
```bash
python -m py_compile $(git ls-files '*.py')
```
- There are no tests in the project. If they appear, run them with the `pytest` command.
- Write commits in English and try to make them atomic.
- To install dependencies, use:
```bash
pip install -r requirements.txt
```