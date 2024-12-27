import re

# Lexical analysis (just detects integers, real numbers, and strings)
def lexique_analysis(source_code):
    tokens = []
    patterns = {
        r"\bSnk_Begin\b": "début du programme",
        r"\bSnk_End\b": "fin du programme",
        r"\bSnk_Int\b\s+(\w+(?:\s*,\s*\w+)*)": "déclaration de variables entières",  # Matches 'Snk_Int' with multiple variables
        r"\bSnk_Real\b\s+(\w+)": "déclaration d’une variable réelle",  # Matches 'Snk_Real' with a single variable
        r"\bSet\b\s+(\w+)\s*(\d+(\.\d+)?)": "affectation d’une valeur à",  # Matches 'Set' with variable and value assignment
        r"\bIf\b": "conditionnel",  # Matches 'If'
        r"\bElse\b": "sinon",  # Matches 'Else'
        r"\bBegin\b": "début de bloc",  # Matches 'Begin'
        r"\bEnd\b": "fin de bloc",  # Matches 'End'
        r"\bSnk_Print\b": "Affichage",  # Matches 'Snk_Print'
        r"\bGet\b": "Affectation de valeur entre 2 variables",  # Matches 'Get' for assignment
        r"##.*": "commentaire",  # Matches comments starting with ##
        r"\[|\]": "début/fin de condition",  # Matches square brackets for condition start/end
        r"\b\d+(\.\d+)?\b": "nombre entier ou réel",  # Matches numbers (integer or real)
        r"<|>|<=|>=|==|!=": "Opérateur de comparaison",  # Matches comparison operators
        r"[#,]": "séparateur",  # Matches separators like ',' or '#'
        r"\w+": "identificateur",  # Matches variable names or identifiers
    }

    # Tokenize the source code
    for pattern, description in patterns.items():
        matches = re.findall(pattern, source_code)
        for match in matches:
            if isinstance(match, tuple):  # If it's a tuple (for patterns with multiple groups), join them
                tokens.append((description, " ".join(match)))
            else:
                tokens.append((description, match))

    return "\n".join([f"{description}: {match}" for description, match in tokens])
# Syntax analysis (basic checks for Snk_Begin and Snk_End)
def syntax_analysis(source_code):
    if "Snk_Begin" not in source_code or "Snk_End" not in source_code:
        return "Syntax error: Missing Snk_Begin or Snk_End"
    
    # Check for one instruction per line
    lines = source_code.splitlines()
    for line in lines:
        if line and line.strip()[-1] != '#':  # Instructions must end with #
            return f"Syntax error: Missing '#' at the end of instruction in line: {line}"
    
    return "Syntax analysis complete.\nNo syntax errors detected."


# Semantic analysis (checks for undefined variables and type mismatches)
def semantic_analysis(source_code):
    variables = {}
    errors = []

    # Simple implementation of variable declaration
    for line in source_code.splitlines():
        if line.startswith("Snk_Int"):
            vars_declared = re.findall(r"Snk_Int\s+([\w, ]+)", line)
            if vars_declared:
                for var in vars_declared[0].split(","):
                    variables[var.strip()] = "int"
        elif line.startswith("Snk_Real"):
            vars_declared = re.findall(r"Snk_Real\s+([\w, ]+)", line)
            if vars_declared:
                for var in vars_declared[0].split(","):
                    variables[var.strip()] = "real"
        elif line.startswith("Snk_Strg"):
            vars_declared = re.findall(r"Snk_Strg\s+([\w, ]+)", line)
            if vars_declared:
                for var in vars_declared[0].split(","):
                    variables[var.strip()] = "string"
        elif line.startswith("Set"):
            parts = line.split()
            var_name = parts[1]
            if var_name not in variables:
                errors.append(f"Semantic error: Variable {var_name} is not declared.")
    
    if errors:
        return "\n".join(errors)
    return "Semantic analysis complete.\nNo semantic errors found."
