# AutomataFlow

### Regular Expression to Finite Automata Converter

AutomataFlow is an interactive Python application that transforms regular expressions into finite automata through a sequence of computational steps.

It demonstrates fundamental concepts of **Theory of Computation**, allowing users to explore automata construction, conversion, minimization, and string recognition.

---

## Overview

AutomataFlow takes a regular expression as input and converts it into different representations of finite automata.

```text
Regular Expression
        |
        v
 Infix to Postfix
        |
        v
      ε-NFA
        |
        v
       NFA
        |
        v
       DFA
        |
        v
  Minimized DFA
        |
        v
  String Validation
```

The application also allows users to check whether a particular string belongs to the language represented by the given regular expression.

---

## Key Features

- **Regular Expression Processing** – Accepts regular expressions as input.
- **Postfix Conversion** – Converts infix expressions into postfix notation.
- **ε-NFA Generation** – Constructs an ε-NFA using Thompson's Construction.
- **NFA Conversion** – Eliminates epsilon transitions.
- **DFA Generation** – Uses the Subset Construction algorithm.
- **DFA Minimization** – Minimizes the generated DFA.
- **String Validation** – Determines whether an input string is accepted or rejected.
- **Automata Visualization** – Provides visual representations of automata.

---

## Supported Operators

| Operator | Description | Example |
|:---:|---|---|
| `+` | Union | `a+b` |
| `*` | Kleene Star | `a*` |
| `·` | Concatenation | `a·b` |
| `?` | Optional | `a?` |
| `ε` | Empty String | `ε` |
| `( )` | Grouping | `(a+b)*` |

---

## Example

Consider the regular expression:

```text
(a+b)*
```

Its postfix representation is:

```text
ab+*
```

This expression represents all possible strings containing any combination of `a` and `b`, including the empty string.

### String Testing

| Input | Result |
|---|---|
| `abbaaabbb` | Accepted |
| `aaaa` | Accepted |
| `bbbb` | Accepted |
| `ababab` | Accepted |
| Empty String | Accepted |
| `abc` | Rejected |

---

## Algorithms Used

| Algorithm | Purpose |
|---|---|
| Infix to Postfix Conversion | Converts expressions into postfix notation |
| Thompson's Construction | Generates ε-NFA |
| Epsilon Closure | Finds states reachable through epsilon transitions |
| Subset Construction | Converts NFA into DFA |
| DFA Minimization | Reduces equivalent DFA states |

---

## Technology Stack

- **Python** – Core implementation
- **Streamlit** – Interactive web interface
- **Graph Visualization Libraries** – Automata visualization (as configured in the project dependencies)

---

## Project Structure

```text
AutomataFlow_project/
│
├── app.py
├── requirements.txt
├── automata/
│   ├── __init__.py
│   ├── regex_parser.py
│   ├── enfa.py
│   ├── nfa.py
│   ├── dfa.py
│   └── minimizer.py
│
├── utils/
│   ├── __init__.py
│   └── visualization.py
│
└── tests/
    └── test_automata.py

```

---

## Installation and Setup

### 1. Clone the Repository

```bash
git clone <https://github.com/sugar-debug/Automata_Project.git>
```

### 2. Navigate to the Project

```bash
cd AutomataFlow_project
```

### 3. Create a Virtual Environment

```bash
python -m venv venv
```

Activate the environment:

**macOS / Linux**

```bash
source venv/bin/activate
```

**Windows**

```bash
venv\Scripts\activate
```

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

### 5. Run the Application

```bash
streamlit run app.py
```

The application will open in your browser.

---

## Learning Outcomes

This project provides practical experience with:

- Regular Expressions and Formal Languages
- Finite Automata and State Transitions
- Epsilon Transitions and Epsilon Closure
- NFA and DFA Construction
- Automata Conversion Algorithms
- DFA Minimization
- Language Recognition and String Validation
- Python-based implementation of theoretical concepts

---

## Future Improvements

- Step-by-step visualization of automata conversion.
- Interactive state-transition exploration.
- Export automata diagrams as images.
- Support for additional regular-expression operators.
- Improved user interface and testing capabilities.

---

## References

1. Hopcroft, Motwani & Ullman – *Introduction to Automata Theory, Languages, and Computation*.
2. Michael Sipser – *Introduction to the Theory of Computation*.
3. [Python Documentation](https://docs.python.org/3/)
4. [Streamlit Documentation](https://docs.streamlit.io/)

---

## Project Information

**Project:** AutomataFlow  
**Course:** Theory of Computation  
**Department:** Artificial Intelligence and Data Engineering  
**Institution:** Malaviya National Institute of Technology Jaipur  
**Academic Session:** 2026–27
