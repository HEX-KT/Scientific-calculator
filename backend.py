#Import needed library
import math
import re
import sqlite3
from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np
import sympy

#Path to resource folder
absolute_path = Path(__file__).resolve().parent
resource_path = absolute_path/ "resources"

def calculate(equation, ans):
    try:
        #Replace inputted symbols to math programmable syntax
        eq = equation.replace('÷', '/').replace('×', '*').replace('−', '-').replace('^', '**').replace('log(', 'math.log(')
        eq = eq.replace('π', '(22/7)').replace('Ans', ans)
        eq = eq.replace('sin(', 'math.sin(').replace('cos(', 'math.cos(').replace('tan(', 'math.tan(').replace('³√', 'p')
        eq = eq.replace('sinh(', 'math.sinh(').replace('cosh(', 'math.cosh(').replace('tanh(', 'math.tanh(').replace('ln(', 'math.log(')

        #Auto close all brackets
        open_brackets = eq.count('(')
        close_brackets = eq.count(')')
        if open_brackets > close_brackets:
            eq += ')' * (open_brackets - close_brackets)

        # Handle e^x and e constant
        eq = re.sub(r'e\^(\(?[^)]+\)?)', r'math.exp(\1)', eq)  # e^2 → math.exp(2)
        eq = eq.replace('e', 'math.e')

        # Handle square root and cube root
        eq = re.sub(r'√(\(?[^)]+\)?)', r'math.sqrt(\1)', eq)   # √9 → math.sqrt(9)
        eq = re.sub(r'p(\(?[^)]+\)?)', r'(\1**(1/3))', eq)   # ³√8 → (8**(1/3))

        # Handle log and ln
        eq = re.sub(r'log(\d+(\.\d+)?)', r'math.log10(\1)', eq)  # log5 → math.log10(5)
        eq = re.sub(r'ln(\d+(\.\d+)?)', r'math.log(\1)', eq)     # ln2 → math.log(2)

        # Handle factorial
        eq = re.sub(r'(\d+)!', r'math.factorial(\1)', eq)

        # Insert multiplication where implied: number before function or parenthesis
        eq = re.sub(r'(\d)(?=math\.)', r'\1*', eq)
        eq = re.sub(r'(\d)(?=\()', r'\1*', eq)
        eq = re.sub(r'(\))(?=\d)', r')*', eq)
        eq = re.sub(r'(\))(?=math\.)', r')*', eq)

        # Auto-close brackets
        open_brackets = eq.count('(')
        close_brackets = eq.count(')')
        if open_brackets > close_brackets:
            eq += ')' * (open_brackets - close_brackets)

        # Evaluate safely
        result = eval(eq, {"__builtins__": None}, {"math": math})
        return str(result) #Returns the answer as a string
    except:
        return "Error" #Return error if process goes wrong


try:
    from scipy.interpolate import make_interp_spline
    SPLINE_AVAILABLE = True
except:
    SPLINE_AVAILABLE = False


def plot(val):
    x = np.array(val[0], dtype=float)
    y = np.array(val[1], dtype=float)

    # if not enough points for smoothing OR SciPy missing → regular plot
    if not SPLINE_AVAILABLE or len(x) < 4:
        plt.plot(x, y)
    else:
        # smooth X
        x_new = np.linspace(x.min(), x.max(), 300)
        # spline curve
        spline = make_interp_spline(x, y, k=3)
        y_new = spline(x_new)
        plt.plot(x_new, y_new)

    plt.xlabel("X")
    plt.ylabel("Y")
    plt.title("Scientific Computation Graph")
    plt.grid(True)
    plt.show()

def fx(func_str, x_values):
    import numpy as np
    import math
    import re

    try:
        eq = func_str.replace(" ", "").lower()

        # ----------- replace math symbols safely -----------
        eq = eq.replace("π", "np.pi")
        eq = eq.replace("^", "**")
        eq = eq.replace("√", "np.sqrt")

        # ----------- replace functions -----------
        func_map = {
            "sin(": "np.sin(",
            "cos(": "np.cos(",
            "tan(": "np.tan(",
            "sinh(": "np.sinh(",
            "cosh(": "np.cosh(",
            "tanh(": "np.tanh(",
            "ln(": "np.log(",
            "log(": "np.log10(",
            "log2(": "np.log2(",
            "exp(": "np.exp(",
        }

        for k, v in func_map.items():
            eq = eq.replace(k, v)

        # ----------- e CONSTANT (correct way) -----------
        # Replace e only when NOT part of a number or identifier
        eq = re.sub(r'(?<![\w\d])e(?![\w\d])', 'np.e', eq)

        # ----------- IMPLIED MULTIPLICATION -----------

        # 2x → 2*x
        eq = re.sub(r'(\d)(?=x)', r'\1*', eq)

        # x2 → x*2
        eq = re.sub(r'x(?=\d)', r'x*', eq)

        # )x → )*x
        eq = re.sub(r'\)(?=x)', r')*', eq)

        # x( → x*(
        eq = re.sub(r'x(?=\()', r'x*', eq)

        # 2( → 2*(
        eq = re.sub(r'(\d)(?=\()', r'\1*', eq)

        # )( → )*(
        eq = re.sub(r'\)(?=\()', r')*(', eq)

        # function sticking: 2np.sin(x) → 2*np.sin(x)
        eq = re.sub(r'(\d)(?=np\.)', r'\1*', eq)

        # xnp.sin(x) → x*np.sin(x)
        eq = re.sub(r'x(?=np\.)', r'x*', eq)

        # ----------- evaluate safely -----------
        y_values = []
        for x in x_values:
            try:
                y = eval(eq, {"__builtins__": None, "np": np, "math": math, "x": x})
            except:
                y = float('nan')
            y_values.append(y)

        return (x_values, y_values)

    except:
        return None


conn = sqlite3.connect(resource_path / "database.db")
cur = conn.cursor()

# Create history table
cur.execute("""
CREATE TABLE IF NOT EXISTS history (
    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    equation TEXT NOT NULL
)
""")
conn.commit()

# Create theme table
cur.execute("""
CREATE TABLE IF NOT EXISTS theme (
    theme TEXT NOT NULL
)
""")
conn.commit()

cur.execute("""
CREATE TABLE IF NOT EXISTS kill (
    kill TEXT NOT NULL
)
""")
conn.commit()

def get_history():
    r = cur.execute("SELECT equation FROM history ORDER BY id DESC")
    return [row[0] for row in r]

def write_history(history: str):
    cur.execute("INSERT INTO history (equation) VALUES (?)", (history,))
    conn.commit()

def del_history():
    cur.execute("DELETE FROM history")

def write_theme(theme: str):
    cur.execute("DELETE FROM theme")  # remove old theme
    cur.execute("INSERT INTO theme (theme) VALUES (?)", (theme,))
    conn.commit()

def read_theme():
    r = cur.execute("SELECT theme FROM theme LIMIT 1").fetchone()
    return r[0] if r else None

def write_kill(val: str = "1"):
    cur.execute("DELETE FROM kill")  # remove old theme
    cur.execute("INSERT INTO kill (kill) VALUES (?)", (val,))
    conn.commit()

def read_kill():
    r = cur.execute("SELECT kill FROM kill LIMIT 1").fetchone()
    return r[0] if r else None

def delete_kill():
    cur.execute("DELETE FROM kill")  # remove all entries
    conn.commit()
