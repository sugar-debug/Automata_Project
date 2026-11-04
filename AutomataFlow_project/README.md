# AutomataFlow

Interactive Regular Expression → ε-NFA → NFA → DFA → Minimized DFA converter with string testing.

## Requirements
- Python 3.10+
- Graphviz system package
- Python dependencies in `requirements.txt`

## Setup (macOS)
```bash
brew install graphviz
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

## Windows
Install Graphviz and ensure its `bin` directory is on PATH, then:
```powershell
py -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
streamlit run app.py
```

## Supported syntax
- Union: `a|b`
- Concatenation: `ab` (implicit)
- Kleene star: `a*`
- One or more: `a+`
- Optional: `a?`
- Parentheses: `(a|b)`
- Empty string: `ε`
- Escape a metacharacter using backslash, e.g. `\*`

## Run tests
```bash
python -m unittest discover -s tests
```

## Note
This is a teaching implementation. It treats each ordinary character as one alphabet symbol and ignores whitespace in the regex itself.
