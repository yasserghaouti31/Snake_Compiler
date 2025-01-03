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
    r"\bIf\b": "mot cle de conditionnel",
    r"\bElse\b": "mot cle de sinon",
    r"\bBegin\b": "mot cle de début de bloc",
    r"\bEnd\b": "mot cle de fin de bloc",
    r"\bSet\b": "mot cle de affectation d’une valeur",
    r"\bGet\b": "mot cle de Affectation de valeur entre 2 variables",
    r"\bfrom\b": "mot cle de transfere",
    r"\bSnk_Print\b": "mot cle de Affichage",
    r"##.*": "commentaire",
    r"\[": "début de condition",
    r"\]": "fin de condition",
    r"<|>|<=|>=|==|!=": "Opérateur de comparaison",
    r",": "séparateur",
    r"#": "fin d’instruction",
    r"\b\d+\.\d+\b": "nombre réel",
    r"\b\d+\b": "nombre entier",
    r"\b[a-zA-Z][a-zA-Z0-9]?\b": "identificateur", 
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

def syntax_analysis(source_code):
    lexique_result = lexique_analysis(source_code)  # Now tokens is a list, not a string
    tokens = []
    for line in lexique_result.splitlines():
        if ':' in line:
            match, description = line.split(" : ")
            tokens.append((description, match))

    current_token = 0  # Initialize the pointer

    print("Tokens:")
    for token in tokens:
        print(token)
    print("\nStarting syntax analysis...")

    # Check if Snk_Begin is at the start
    if current_token < len(tokens) and tokens[current_token][0] == "mot cle de début du programme":
        current_token += 1  # Move to the next token
        variables = D(tokens, current_token)  # Pass current_token
        current_token = variables[1]  # Update the current_token index after D()

        # Check for statements (if any)
        current_token = S(tokens, current_token)

        # Check for Snk_End at the end
        if current_token < len(tokens) and tokens[current_token][0] == "mot cle de fin du programme":
            return "No syntax errors"
        else:
            return "Syntax error: Missing Snk_End"
    else:
        return "Syntax error: Missing Snk_Begin"

# Syntax analysis (basic checks for Snk_Begin and Snk_End)
def D(tokens, current_token):
    print("Entering D:", current_token)
    variables = []  # List to collect declared variables
    while current_token < len(tokens) and tokens[current_token][0] in [
        "mot cle de déclaration de variables entières",
        "mot cle de déclaration d’une variable réelle"
    ]:
        print("D Token:", tokens[current_token])
        current_token += 1  # Move to the next token
        if current_token >= len(tokens) or tokens[current_token][0] != "identificateur":
            raise Exception("Syntax error: Expected an identifier.")
        var_name = tokens[current_token][1]  # Capture the variable name
        variables.append(var_name)  # Store the declared variable
        current_token += 1  # Move past identifier

        while current_token < len(tokens) and tokens[current_token][0] == "séparateur":
            current_token += 1
            if current_token >= len(tokens) or tokens[current_token][0] != "identificateur":
                raise Exception("Syntax error: Expected an identifier.")
            var_name = tokens[current_token][1]
            variables.append(var_name)
            current_token += 1  # Move past identifier

        if current_token >= len(tokens) or tokens[current_token][0] != "fin d’instruction":
            raise Exception("Syntax error: Expected # at the end of declaration.")
        current_token += 1  # Move past #

    return variables, current_token  # Return the list of declared variables

def S(tokens, current_token):
    """
    Analyzes statements in the program.
    """
    print("Entering S:", current_token)
    while current_token < len(tokens) and tokens[current_token][0] in [
        "mot cle de déclaration de variables entières",
        "mot cle de déclaration d’une variable réelle",
        "mot cle de affectation d’une valeur",
        "mot cle de conditionnel",
        "mot cle de début de bloc",
        "mot cle de Affichage"
        ,"mot cle de Affectation de valeur entre 2 variables"
        ,"mot cle de transfere"
        ,"commentaire"
    ]:
        print("S Token:", tokens[current_token])
        if tokens[current_token][0] == "mot cle de conditionnel":
            current_token = condition(tokens, current_token)
        elif tokens[current_token][0] == "mot cle de début de bloc":
            current_token = block(tokens, current_token)
        elif tokens[current_token][0] == "mot cle de Affectation de valeur entre 2 variables":
            current_token = get_statement(tokens, current_token)
        elif tokens[current_token][0] == "mot cle de affectation d’une valeur":
            current_token = assignment(tokens, current_token)
        elif tokens[current_token][0] == "mot cle de Affichage":
            current_token = print_statement(tokens, current_token)
        elif tokens[current_token][0] =="commentaire" :
            current_token +=1
        elif tokens[current_token][0] == "mot cle de déclaration de variables entières" or \
             tokens[current_token][0] == "mot cle de déclaration d’une variable réelle":
            current_token = D(tokens, current_token)[1]  # Skip over variable declarations
        else:
            # Handle any unexpected tokens (optional)
            current_token += 1

    return current_token  # Return updated current_token
def get_statement(tokens, current_token):
    print("Entering get_statement:", current_token)
    current_token += 1
    if current_token >= len(tokens) or tokens[current_token][0] != "identificateur":
        raise Exception("Syntax error: Expected an identifier 1 .")
    current_token += 1
    if current_token >=len(tokens) or tokens[current_token][0] !="mot cle de transfere":
        raise Exception("Syntax error : Expected a from.")
    current_token +=1
    if current_token >= len(tokens) or tokens[current_token][0] != "identificateur":
        raise Exception("Syntax error: Expected an identifier 2 .")
    current_token += 1

    if current_token >= len(tokens) or tokens[current_token][0] != "fin d’instruction":
        raise Exception("Syntax error: Expected # at the end of statement.")
    current_token += 1

    return current_token
def condition(tokens, current_token):
    """
    Analyzes an If-Else condition.
    """
    print("Entering condition:", current_token)
    current_token += 1  # Move past the 'If' keyword
    if current_token >= len(tokens) or tokens[current_token][0] != "début de condition":
        raise Exception("Syntax error: Expected '[' for condition start.")
    current_token += 1  # Move past '['

    # Handle condition expression (we assume it's a simple identifier or operator for now)
    if current_token >= len(tokens) or (tokens[current_token][0] != "identificateur" and 
       tokens[current_token][0] != "Opérateur de comparaison"):
        raise Exception("Syntax error: Expected a condition expression.")
    print("Condition expression:", tokens[current_token])
    current_token += 1  # Move past condition expression (identifier)

    # Handle the comparison operator and value
    if current_token >= len(tokens) or tokens[current_token][0] != "Opérateur de comparaison":
        raise Exception("Syntax error: Expected a comparison operator.")
    print("Comparison operator:", tokens[current_token])
    current_token += 1  # Move past operator

    if current_token >= len(tokens) or tokens[current_token][0] != "nombre entier":
        raise Exception("Syntax error: Expected a numeric value.")
    print("Condition value:", tokens[current_token])
    current_token += 1  # Move past numeric value

    if current_token >= len(tokens) or tokens[current_token][0] != "fin de condition":
        raise Exception("Syntax error: Expected ']' for condition end.")
    print("Condition end:", tokens[current_token])
    current_token += 1  # Move past ']'

    # Handle the block for the 'If' condition
    current_token = block(tokens, current_token)

    # Handle the optional 'Else' part
    if current_token < len(tokens) and tokens[current_token][0] == "mot cle de sinon":
        current_token += 1  # Move past 'Else'
        current_token = block(tokens, current_token)

    return current_token  # Return updated current_token

def block(tokens, current_token):
    """
    Analyzes a block of statements.
    """
    print("Entering block:", current_token)
    current_token += 1  # Move past the 'Begin' keyword

    # Analyze statements within the block
    while current_token < len(tokens) and tokens[current_token][0] != "mot cle de fin de bloc":
        current_token = S(tokens, current_token)
    
    if current_token >= len(tokens) or tokens[current_token][0] != "mot cle de fin de bloc":
        raise Exception("Syntax error: Expected 'End' for block end.")
    print("Block end:", tokens[current_token])
    current_token += 1  # Move past 'End'
    
    return current_token  # Return updated current_token

def assignment(tokens, current_token):
    """
    Analyzes an assignment statement.
    """
    print("Entering assignment:", current_token)
    current_token += 1  # Move past 'Set' keyword
    if current_token >= len(tokens) or tokens[current_token][0] != "identificateur":
        raise Exception("Syntax error: Expected an identifier.")
    current_token += 1  # Move past identifier
    if current_token >= len(tokens) or (tokens[current_token][0] != "nombre entier" and 
       tokens[current_token][0] != "nombre réel"):
        raise Exception("Syntax error: Expected a number.")
    current_token += 1  # Move past number

    if current_token >= len(tokens) or tokens[current_token][0] != "fin d’instruction":
        raise Exception("Syntax error: Expected # at the end of assignment.")
    current_token += 1  # Move past '#'
    
    return current_token  # Return updated current_token

def print_statement(tokens, current_token):
    """
    Analyzes a print statement.
    """
    print("Entering print_statement:", current_token)
    current_token += 1  # Move past 'Snk_Print' keyword
    while current_token < len(tokens) and (tokens[current_token][0] == "identificateur" or 
           tokens[current_token][0] == "chaine de caractère"):
        current_token += 1  # Move past identifier or string
        if current_token < len(tokens) and tokens[current_token][0] == "séparateur":
            current_token += 1  # Move past separator

    if current_token >= len(tokens) or tokens[current_token][0] != "fin d’instruction":
        raise Exception("Syntax error: Expected # at the end of print statement.")
    current_token += 1  # Move past '#'
    
    return current_token  # Return updated current_token



# Semantic analysis (checks for undefined variables and type mismatches)
def semantic_analysis(source_code):
    lexique_result = lexique_analysis(source_code)
    tokens = []
    for line in lexique_result.splitlines():
        if ':' in line:
            match, description = line.split(" : ")
            tokens.append((description, match))
    
    declared_variables = {}  # To track declared variables and their types
    current_token = 0

    while current_token < len(tokens):
        description, match = tokens[current_token]
        if description == "mot cle de début du programme":
            current_token += 1
        elif description in ["mot cle de déclaration de variables entières", "mot cle de déclaration d’une variable réelle"]:
            var_type = "int" if description == "mot cle de déclaration de variables entières" else "real"
            current_token += 1
            while tokens[current_token][0] == "identificateur":
                var_name = tokens[current_token][1]
                declared_variables[var_name] = var_type
                current_token += 1
                if tokens[current_token][0] == "séparateur":
                    current_token += 1
            if tokens[current_token][0] != "fin d’instruction":
                raise Exception("Semantic error: Expected # at the end of declaration.")
            current_token += 1
        elif description == "mot cle de affectation d’une valeur":
            current_token += 1
            var_name = tokens[current_token][1]
            if var_name not in declared_variables:
                raise Exception(f"Semantic error: Variable '{var_name}' not declared.")
            current_token += 1
            if tokens[current_token][0] == "nombre entier":
                if declared_variables[var_name] != "int":
                    raise Exception(f"Semantic error: Type mismatch for variable '{var_name}', expected int.")
            elif tokens[current_token][0] == "nombre réel":
                if declared_variables[var_name] != "real":
                    raise Exception(f"Semantic error: Type mismatch for variable '{var_name}', expected real.")
            current_token += 1
            if tokens[current_token][0] != "fin d’instruction":
                raise Exception("Semantic error: Expected # at the end of assignment.")
            current_token += 1
        elif description == "mot cle de Affichage":
            current_token += 1
            while tokens[current_token][0] in ["identificateur", "chaine de caractère"]:
                var_name = tokens[current_token][1]
                if tokens[current_token][0] == "identificateur" and var_name not in declared_variables:
                    raise Exception(f"Semantic error: Variable '{var_name}' not declared.")
                current_token += 1
                if tokens[current_token][0] == "séparateur":
                    current_token += 1
            if tokens[current_token][0] != "fin d’instruction":
                raise Exception("Semantic error: Expected # at the end of print statement.")
            current_token += 1
        elif description == "mot cle de fin du programme":
            return "No semantic errors"
        else:
            current_token += 1  # Move to the next token
    
    return "Semantic error: Missing Snk_End"

