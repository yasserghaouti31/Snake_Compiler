import re

# Lexical analysis (just detects integers, real numbers, and strings

def lexique_analysis(source_code):
    # Define patterns
    tokens = []
    patterns = {
        r"\bSnk_Begin\b": "mot cle de début du programme",
        r"\bSnk_End\b": "mot cle de fin du programme",
        r"\bSnk_Int\b": "mot cle de déclaration de variables entières",
        r"\bSnk_Real\b": "mot cle de déclaration d’une variable réelle",
        r"\bSnk_Strg\b": "mot cle de déclaration d’une chaine de caractere",
        r"\s[a-zA-Z][a-zA-Z0-9]{0,1}\b": "identificateur" ,
        r"\bSet\b": "mot cle de affectation d’une valeur",
        r"\bIf\b": "mot cle de conditionnel",
        r"\bElse\b": "mot cle de sinon",
        r"\bBegin\b": "mot cle de début de bloc",
        r"\bEnd\b": "mot cle de fin de bloc",
        r"\bSnk_Print\b": "mot cle de Affichage",
        r"\bGet\b": "mot cle de Affectation de valeur entre 2 variables",
        r"##.*": "commentaire",
        r"\[": "début de condition",
        r"\]": "fin de condition",
        r"<|>|<=|>=|==|!=": "Opérateur de comparaison",
        r",": "séparateur",
        r"#": "fin d’instruction",
        r"\s+\d+\s+": "nombre entier",  
        r"\s+\d+\.\d+\b": "nombre réel",
    }

    position = 0  # Start position in the source code
    while position < len(source_code):
        matched = False  # Flag to track if any pattern was matched
        for pattern, description in patterns.items():
            match = re.match(pattern, source_code[position:])  # Match from current position
            if match:
                matched_string = match.group()
                tokens.append((description, matched_string))
                position += len(matched_string)  # Move forward by the length of the match
                matched = True
                break  # Move to the next pattern check after a match
        if not matched:
            position += 1  # No match found, just move to the next character

    return "\n".join([f"{match} : {description}" for description, match in tokens])

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
