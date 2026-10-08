import math
import re


# ==========================================
# DEGREE TO RADIAN
# ==========================================

def to_radians(value):

    return math.radians(value)


# ==========================================
# FACTORIAL
# ==========================================

def factorial(value):

    if value < 0:

        raise ValueError(
            "Factorial cannot be used with negative numbers."
        )


    if not float(value).is_integer():

        raise ValueError(
            "Factorial requires a whole number."
        )


    return math.factorial(int(value))


# ==========================================
# SIN
# ==========================================

def calculate_sin(value, mode):

    if mode == "DEG":

        value = math.radians(value)

    return math.sin(value)


# ==========================================
# COS
# ==========================================

def calculate_cos(value, mode):

    if mode == "DEG":

        value = math.radians(value)

    return math.cos(value)


# ==========================================
# TAN
# ==========================================

def calculate_tan(value, mode):

    if mode == "DEG":

        value = math.radians(value)

    return math.tan(value)


# ==========================================
# CREATE SAFE ENVIRONMENT
# ==========================================

def create_environment(mode):

    return {

        "sin": lambda x:
            calculate_sin(x, mode),

        "cos": lambda x:
            calculate_cos(x, mode),

        "tan": lambda x:
            calculate_tan(x, mode),

        "sqrt": math.sqrt,

        "log": math.log10,

        "ln": math.log,

        "abs": abs,

        "factorial": factorial,

        "pi": math.pi,

        "e": math.e,

        "pow": pow

    }


# ==========================================
# PREPARE EXPRESSION
# ==========================================

def prepare_expression(expression):

    expression = expression.strip()


    # Multiplication
    expression = expression.replace("×", "*")


    # Division
    expression = expression.replace("÷", "/")


    # Power
    expression = expression.replace("^", "**")


    # Pi
    expression = expression.replace("π", "pi")


    # Square root
    expression = expression.replace("√", "sqrt")


    # Percentage
    expression = re.sub(
        r"(\d+(?:\.\d+)?)%",
        r"(\1/100)",
        expression
    )


    # Factorial
    expression = re.sub(
        r"(\d+(?:\.\d+)?)!",
        r"factorial(\1)",
        expression
    )


    return expression


# ==========================================
# VALIDATE EXPRESSION
# ==========================================

def validate_expression(expression):

    pattern = r"^[0-9+\-*/().,\s_a-zA-Z]*$"

    if not re.match(pattern, expression):

        raise ValueError(
            "Invalid characters in expression."
        )


# ==========================================
# CALCULATE
# ==========================================

def calculate_expression(
    expression,
    mode="DEG"
):

    if not expression:

        raise ValueError(
            "Expression cannot be empty."
        )


    expression = prepare_expression(
        expression
    )


    validate_expression(
        expression
    )


    environment = create_environment(
        mode
    )


    try:

        result = eval(
            expression,
            {
                "__builtins__": {}
            },
            environment
        )


    except ZeroDivisionError:

        raise ValueError(
            "Cannot divide by zero."
        )


    except ValueError as error:

        raise ValueError(
            str(error)
        )


    except Exception:

        raise ValueError(
            "Invalid mathematical expression."
        )


    # Complex number check

    if isinstance(result, complex):

        raise ValueError(
            "Complex numbers are not supported."
        )


    # Infinite result check

    if not math.isfinite(
        float(result)
    ):

        raise ValueError(
            "Result is not finite."
        )


    # Remove .0

    if float(result).is_integer():

        return int(result)


    return round(
        float(result),
        10
    )