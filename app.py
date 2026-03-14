from flask import Flask, render_template, request, jsonify
import sympy as sp
import numpy as np

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/solve', methods=['POST'])
def solve():
    try:
        data = request.json
        print(f"Received data: {data}")
        expression = data.get('expression', '')
        
        if not expression:
            print("Error: No expression provided")
            return jsonify({'error': 'No expression provided'}), 400
            
        # Preprocess expression (convert ^ to ** and handle equations)
        expression = expression.replace('^', '**')
        if '=' in expression:
            lhs, rhs = expression.split('=', 1)
            expression = f"({lhs}) - ({rhs})"
        print(f"Processing: {expression}")
        
        # Parse the expression with implicit multiplication support
        from sympy.parsing.sympy_parser import parse_expr, standard_transformations, implicit_multiplication_application
        transformations = (standard_transformations + (implicit_multiplication_application,))
        expr = parse_expr(expression, transformations=transformations)
        
        # Determine the operation (default to simplify)
        result = sp.simplify(expr)
        
        # Identify variables for possible solving/calculus
        vars = list(expr.free_symbols)
        x = vars[0] if vars else sp.Symbol('x')
        
        # Try to provide more details (derivative, integral, solutions)
        solutions = None
        if vars:
            try:
                sol = sp.solve(expr, x)
                solutions = sp.latex(sol)
            except:
                pass

        detail = {
            'simplified': str(result),
            'latex': sp.latex(result),
            'derivative': sp.latex(sp.diff(expr, x)) if vars else None,
            'integral': sp.latex(sp.integrate(expr, x)) if vars else None,
            'solutions': solutions
        }
        
        return jsonify({
            'answer': str(result),
            'latex': sp.latex(result),
            'details': detail
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True, port=5000)
