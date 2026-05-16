# ⚙️ While Compiler

An interactive compiler for a subset of C-like code (focused on `while` loops), built as a Computer Science project. It features a full compilation pipeline — from lexical analysis all the way to assembly code generation — with a modern web-based visualizer.

---

## ✨ Features

| Stage | What it does |
|-------|-------------|
| **Lexical Analysis** | Tokenizes source code into keywords, identifiers, numbers, operators, separators, and strings |
| **CFG Visualization** | Displays the Context-Free Grammar rules and highlights which rules were actually used |
| **Syntax Analysis** | Recursive-descent parser that validates code structure |
| **Parse Tree** | Visual, collapsible tree showing how the program was parsed |
| **Semantic Analysis** | Detects duplicate declarations and undeclared variable usage |
| **Symbol Table** | Lists all declared variables and their types |
| **Assembly Generation** | Produces simple pseudo-assembly for `while` loop constructs |
| **Error Reporting** | Inline syntax and semantic error messages |

---

## 📁 Project Structure

```
Final_Project/
├── compiler.py       # Backend: full compiler pipeline (CLI version)
└── compiler.html     # Frontend: interactive web-based visualizer
```

---

## 🚀 Getting Started

### Option 1 — Web Visualizer (Recommended)

Just open `compiler.html` in any modern browser. No installation needed.

- Type your program line by line in the terminal input
- Click **▶ Run Compiler** to see all stages instantly
- Click nodes in the Parse Tree to expand/collapse them

### Option 2 — Python CLI

Requires Python 3.

```bash
python compiler.py
```

Enter your program line by line and type `END` when done. Results are printed to the terminal.

---

## 🗣️ Supported Language

The compiler supports a small but complete subset of C:

```c
int i;
i = 0;
while (i < 5) {
    printf("%d\n", i);
    i++;
}
```

### Supported Constructs

- **Types:** `int`, `float`
- **Statements:** variable declaration, assignment, increment (`++`), `while` loops, `printf`, blocks (`{}`)
- **Expressions:** arithmetic (`+`, `-`, `*`, `/`)
- **Conditions:** relational operators (`<`, `>`, `==`, `!=`)
- **Output:** `printf` with `%d` and `\n` format specifiers

---

## 🧠 How It Works

### 1. Lexical Analysis
The lexer scans the source character by character and produces a flat list of tokens, each labeled with its type (KEYWORD, IDENTIFIER, NUMBER, OPERATOR, SEPARATOR, STRING, UNKNOWN).

### 2. CFG
A Context-Free Grammar defines the legal structure of the language. The web visualizer highlights which grammar rules were actually exercised during parsing.

### 3. Syntax Analysis (Parser)
A hand-written recursive-descent parser validates that the token stream matches the grammar. It builds a parse tree as it goes, and recovers from errors to continue parsing.

### 4. Semantic Analysis
After parsing, the compiler checks for:
- **Duplicate declarations** — the same variable declared more than once
- **Undeclared variables** — using a variable before declaring it

### 5. Symbol Table
All declared variables are recorded with their types and displayed as a lookup table.

### 6. Assembly Code Generation
For `while` loop constructs, the compiler emits pseudo-assembly instructions:

```
L1:
    LOAD i
    CMP  5
    JGE  L2
    PRINT_INT i
    PRINT_NEWLINE
    INC  i
    JMP  L1
L2:
```

Supported assembly ops: `LOAD`, `CMP`, `JGE`, `JLE`, `INC`, `ADD`, `SUB`, `MUL`, `DIV`, `STORE`, `PRINT_INT`, `PRINT_NEWLINE`, `JMP`

---

## 🖥️ Web Visualizer Panels

| Panel | Color | Description |
|-------|-------|-------------|
| CFG Rules | Blue | Grammar rules; used rules highlighted |
| Symbol Table | Green | Declared variables and types |
| Lexeme Table | Yellow | Full token list with types |
| Errors | Red | Syntax and semantic errors |
| Syntax Tree | Purple | Interactive collapsible parse tree |
| Assembly Code | Orange | Generated pseudo-assembly |

---

## 🛠️ Tech Stack

- **Python 3** — compiler backend (lexer, parser, semantic analyzer, code generator)
- **HTML / CSS / JavaScript** — self-contained web visualizer (no frameworks, no dependencies)
- **Fonts** — JetBrains Mono, Outfit (via Google Fonts)

---

## 📌 Limitations

- Only `while` loops generate assembly output; standalone declarations and assignments are analyzed but not code-generated
- `printf` supports `%d` and `\n` format specifiers only
- No support for nested `while` loops in assembly generation
- Float variables are declared but treated the same as int at the assembly level

---

## 👤 Author

**Ahmed Ibrahim**  
Computer Science — Compiler Design Project
