import re

# Lexical analysis (just detects integers, real numbers, and strings)
def lexique_analysis(source_code):
    tokens = []
    patterns = {
        "integer": r"\bSnk_Int\b\s+(\w+)\s*(,?\s*\w*)",  # Matches Snk_Int declarations
        "real": r"\bSnk_Real\b\s+(\w+)\s*(,?\s*\w*)",    # Matches Snk_Real declarations
        "string": r"\bSnk_Strg\b\s+\"([^\"]+)\"",         # Matches Snk_Strg declarations
        "number": r"\b\d+(\.\d+)?\b",                     # Matches numbers (integers and real)
    }

    # Tokenize the source code
    for name, pattern in patterns.items():
        matches = re.findall(pattern, source_code)
        for match in matches:
            tokens.append((name, match))
    
    return "\n".join([f"{name}: {match}" for name, match in tokens])


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