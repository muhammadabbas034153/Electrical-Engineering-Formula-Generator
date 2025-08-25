import gradio as gr
import sympy as sp

# Dictionary of electrical engineering formulas
formulas = {
    "Ohm's Law": "V = I * R",
    "Power": "P = V * I",
    "Energy Stored in Capacitor": "E = 1/2 * C * V**2",
    "Energy Stored in Inductor": "E = 1/2 * L * I**2",
    "Resonant Frequency (LC Circuit)": "f = 1 / (2 * pi * sqrt(L * C))",
    "Impedance (RLC series circuit)": "Z = sqrt(R**2 + (X_L - X_C)**2)",
    "Capacitive Reactance": "X_C = 1 / (2 * pi * f * C)",
    "Inductive Reactance": "X_L = 2 * pi * f * L"
}

# Function to get formula by name
def get_formula_by_name(name: str):
    if not name:
        return "Please enter a formula name."
    name_lower = name.lower()
    for key in formulas:
        if name_lower in key.lower():
            return f"{key}: {formulas[key]}"
    return "Formula not found. Try again."

# Function to solve a formula if variables are given
def solve_formula(formula_name: str, **kwargs):
    if formula_name not in formulas:
        return "Formula not found."
    try:
        expr = sp.sympify(formulas[formula_name].split("=")[1])
        symbols = expr.free_symbols
        subs = {sp.Symbol(k): float(v) for k, v in kwargs.items() if v not in (None, "")}
        result = expr.evalf(subs=subs)
        return f"{formula_name}: {formulas[formula_name]} → {result}"
    except Exception as e:
        return f"Error solving formula: {str(e)}"

# Gradio interface
def formula_app(name, V=None, I=None, R=None, C=None, L=None, f=None):
    response = get_formula_by_name(name)
    if "not found" in response or "Please" in response:
        return response
    return solve_formula(name, V=V, I=I, R=R, C=C, L=L, f=f)

iface = gr.Interface(
    fn=formula_app,
    inputs=[
        gr.Textbox(label="Enter Formula Name (e.g., Ohm's Law, Power)"),
        gr.Number(label="Voltage (V)", value=None),
        gr.Number(label="Current (I)", value=None),
        gr.Number(label="Resistance (R)", value=None),
        gr.Number(label="Capacitance (C)", value=None),
        gr.Number(label="Inductance (L)", value=None),
        gr.Number(label="Frequency (f)", value=None)
    ],
    outputs="text",
    title="Electrical Engineering Formula Generator",
    description="Created by Muhammad Abbas — Enter a formula name and known values to calculate results."
)

if __name__ == "__main__":
    iface.launch()
