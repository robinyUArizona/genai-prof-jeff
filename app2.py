import streamlit as st
import re

def evaluate_expression(expression):
    # Allow only numbers, operators, and parentheses
    if re.match(r'^[0-9+\-*/(). ]+$', expression):
        try:
            # Evaluate the expression
            result = eval(expression)
            return result
        except Exception as e:
            return f"Error: {str(e)}"
    else:
        return "Invalid input: Only numbers and mathematical operators are allowed."

# Streamlit app
st.title("Simple Expression Evaluator")

# User input
expression = st.text_input("Enter a mathematical expression:", "")

# Evaluate and display result
if expression:
    result = evaluate_expression(expression)
    st.write(f"Result: {result}")
