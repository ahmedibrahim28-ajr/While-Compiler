# =========================
# USER INPUT
# =========================

print("Enter program (END to finish):")

code = ""

while True:
    line = input()

    if line == "END":
        break

    code += line + "\n"


# =========================
# LEXICAL ANALYZER + CFG
# =========================

keywords = ["int", "float", "while", "printf"]
operators = ["+", "-", "*", "/", "=", "<", ">", "==", "!=", "++"]
separators = ["(", ")", "{", "}", ";", ","]

CFG = {
    "program": "statement_list",
    "statement": "declaration | assignment | increment | while_stmt | printf_stmt | block",
    "declaration": "type IDENTIFIER ;",
    "assignment": "IDENTIFIER = expression ;", # =
    "increment": "IDENTIFIER ++ ;",
    "while_stmt": "while ( condition ) statement",
    "printf_stmt": "printf ( STRING , IDENTIFIER ) ;",
    "block": "{ statement_list }", # group of statements inside {}
    "condition": "expression relop expression", # compare 2 expression
    "expression": "term (+|- term)*",  # addition or sub
    "term": "factor (*|/ factor)*", # multiplication or division
    "factor": "IDENTIFIER | NUMBER"
}

tokens = []
i = 0

while i < len(code):

    ch = code[i]

    if ch in " \n\t": # skips empty spaces and lines
        i += 1
        continue

    # STRING
    if ch == '"':

        s = '"'
        i += 1

        while i < len(code) and code[i] != '"':
            s += code[i]
            i += 1

        s += '"'
        i += 1

        tokens.append((s, "STRING"))
        continue

    # WORD
    if ch.isalpha():

        word = ""

        while i < len(code) and code[i].isalnum():
            word += code[i]
            i += 1

        t = "KEYWORD" if word in keywords else "IDENTIFIER"

        tokens.append((word, t))
        continue

    # NUMBER
    if ch.isdigit():

        num = ""

        while i < len(code) and code[i].isdigit():
            num += code[i]
            i += 1

        tokens.append((num, "NUMBER"))
        continue

    # DOUBLE OPERATOR
    if i + 1 < len(code) and code[i:i+2] in operators:

        tokens.append((code[i:i+2], "OPERATOR"))
        i += 2
        continue

    # SINGLE OPERATOR
    if ch in operators:

        tokens.append((ch, "OPERATOR"))
        i += 1
        continue

    # SEPARATOR
    if ch in separators:

        tokens.append((ch, "SEPARATOR"))
        i += 1
        continue

    tokens.append((ch, "UNKNOWN"))
    i += 1


# =========================
# SHOW LEXICAL ANALYSIS
# =========================

print("\n===== LEXICAL ANALYSIS =====")

for x in tokens:
    print(x[0], "->", x[1])

print("\n===== CFG =====")

for x in CFG:
    print(x, "->", CFG[x])


# =========================
# SYNTAX ANALYZER
# =========================

index = 0
tree = []

def current():
    return tokens[index] if index < len(tokens) else ("EOF", "EOF") # EOF-(end of file)(no tokens)

def add(name, level):
    tree.append("|   " * level + "|-- " + name)

def error(msg):
    print("\nSyntax Error:", msg)
    print("Found:", current())
    exit()

def match(x, level):
    global index
    if current()[0] == x:
        add("match " + x, level)
        index += 1
    else:
        error(x)

def match_type(t, level):
    global index
    if current()[1] == t:
        add("match " + current()[0], level)
        index += 1
    else:
        error(t)


# =========================
# PARSER FUNCTIONS
# =========================

def program(level=0):

    add("Program", level)

    while current()[0] != "EOF":
        statement(level + 1)


def statement(level):

    add("Statement", level)

    tok = current()[0]

    if tok in ["int", "float"]:
        declaration(level + 1)

    elif tok == "while":
        while_stmt(level + 1)

    elif tok == "printf":
        printf_stmt(level + 1)

    elif tok == "{":
        block(level + 1)

    elif current()[1] == "IDENTIFIER":

        if index + 1 < len(tokens) and tokens[index + 1][0] == "++":
            increment(level + 1)

        else:
            assignment(level + 1)

    else:
        error("statement")


def declaration(level):

    add("Declaration", level)

    match(current()[0], level + 1)
    match_type("IDENTIFIER", level + 1)
    match(";", level + 1)


def assignment(level):

    add("Assignment", level)

    match_type("IDENTIFIER", level + 1)
    match("=", level + 1)
    expression(level + 1)
    match(";", level + 1)


def increment(level):

    add("Increment", level)

    match_type("IDENTIFIER", level + 1)
    match("++", level + 1)
    match(";", level + 1)


def printf_stmt(level):

    add("Printf", level)

    match("printf", level + 1)
    match("(", level + 1)

    if current()[1] == "STRING":
        match_type("STRING", level + 1)
        match(",", level + 1)

    match_type("IDENTIFIER", level + 1)

    match(")", level + 1)
    match(";", level + 1)


def while_stmt(level):

    add("WhileStmt", level)

    match("while", level + 1)
    match("(", level + 1)
    condition(level + 1)
    match(")", level + 1)

    if current()[0] == "{":
        block(level + 1)

    else:
        statement(level + 1)


def block(level):

    add("Block", level)

    match("{", level + 1)

    while current()[0] != "}":
        statement(level + 1)

    match("}", level + 1)


def condition(level):

    add("Condition", level)

    expression(level + 1)

    if current()[0] in ["<", ">", "==", "!="]:
        match(current()[0], level + 1)
    else:
        error("relational operator")

    expression(level + 1)


def expression(level):

    add("Expression", level)

    term(level + 1)

    while current()[0] in ["+", "-"]:
        match(current()[0], level + 1)
        term(level + 1)


def term(level):

    add("Term", level)

    factor(level + 1)

    while current()[0] in ["*", "/"]:
        match(current()[0], level + 1)
        factor(level + 1)


def factor(level):

    add("Factor", level)

    if current()[1] == "IDENTIFIER":
        match_type("IDENTIFIER", level + 1)

    elif current()[1] == "NUMBER":
        match_type("NUMBER", level + 1)

    else:
        error("IDENTIFIER or NUMBER")


# =========================
# START PARSER
# =========================

program() #start syntax analysis


# =========================
# PARSE TREE
# =========================

print("\n===== PARSE TREE =====")

for x in tree:
    print(x)


# =========================
# SEMANTIC ANALYZER
# =========================

table = {}

# detect duplicate variables
for i in range(len(tokens)):
    if tokens[i][0] in ["int", "float"]:
        var = tokens[i + 1][0]
        if var in table:
            print("\nSemantic Error:", var, "already declared")
            exit()
        table[var] = tokens[i][0]

# detect undeclared variables
for lex, tok in tokens:
    if tok == "IDENTIFIER" and lex != "printf":
        if lex not in table:
            print("\nSemantic Error:", lex, "not declared")
            exit()


print("\n===== SYMBOL TABLE =====")

for x in table:
    print(x, ":", table[x])


# =========================
# ASSEMBLY CODE
# =========================

assembly = []
label = 1
i = 0

while i < len(tokens):

    if tokens[i][0] == "while":

        start = "L" + str(label)
        label += 1

        end = "L" + str(label)
        label += 1

        left = tokens[i + 2][0]
        op = tokens[i + 3][0]
        right = tokens[i + 4][0]

        assembly += [
            start + ":", #l1:
            "LOAD " + left,
            "CMP " + right #compare
        ]

        # exit if condition become false
        if op == "<":
            assembly.append("JGE " + end) # jump if greater or equal

        elif op == ">":
            assembly.append("JLE " + end) # jump if less or equal

        body = i + 7

        while tokens[body][0] != "}":

            # printf
            if tokens[body][0] == "printf":

                format_str = tokens[body + 2][0]  # STRING token
                value = tokens[body + 4][0]       # IDENTIFIER

                # handle %d
                if "%d" in format_str:
                    assembly.append("PRINT_INT " + value)

                # handle newline \n
                if "\\n" in format_str:
                    assembly.append("PRINT_NEWLINE")

                # fallback (if unknown format)
                if "%d" not in format_str and "\\n" not in format_str:
                    assembly.append("PRINT " + value)

            # i++
            elif body + 1 < len(tokens) and tokens[body + 1][0] == "++":
                assembly.append("INC " + tokens[body][0])

            # assignment
            elif body + 4 < len(tokens) and tokens[body + 1][0] == "=":

                var = tokens[body][0]
                left_side = tokens[body + 2][0]
                op2 = tokens[body + 3][0]
                right_side = tokens[body + 4][0]

                assembly.append("LOAD " + left_side)

                if op2 == "+":
                    assembly.append("ADD " + right_side)

                elif op2 == "-":
                    assembly.append("SUB " + right_side)

                elif op2 == "*":
                    assembly.append("MUL " + right_side)

                elif op2 == "/":
                    assembly.append("DIV " + right_side)

                assembly.append("STORE " + var) #final result
            body += 1

        assembly += [
            "JMP " + start,
            end + ":"
        ]
    i += 1

# =========================
# SHOW ASSEMBLY
# =========================

print("\n===== ASSEMBLY CODE =====")

for x in assembly:
    print(x)

print("\nCompilation Finished Successfully!")