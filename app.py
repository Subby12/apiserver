import json
from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import math

app = Flask(__name__)
CORS(app)

def is_armstrong(n):
    """Check if a number is an Armstrong number."""
    num_str = str(abs(n))
    power = len(num_str)
    return sum(int(digit) ** power for digit in num_str) == abs(n)

def is_even(n):
    """Check if a number is even."""
    return n % 2 == 0

def get_properties(n):
    """Get list of number properties based on specified combinations."""
    properties = []
    if is_armstrong(n):
        properties.append("armstrong")
    if is_even(n):
        properties.append("even")
    else:
        properties.append("odd")
    return properties

def digit_sum(n):
    """Calculate sum of digits."""
    return sum(int(digit) for digit in str(abs(n)))

def get_fun_fact(n):
    """Get mathematical fun fact about the number."""
    try:
        response = requests.get(f"http://numbersapi.com/{abs(n)}/math", timeout=5)
        return response.text if response.status_code == 200 else f"No fun fact available for {n}"
    except Exception as e:
        return f"No fun fact available for {n}"

@app.route('/api/classify-number', methods=['GET'])
def classify_number():
    # Default response structure
    response = {
        "number": None,
        "error": False,
        "digit_sum": None,
        "is_perfect": False,
        "is_prime": False,
        "properties": [],
        "fun_fact": "No fun fact available"
    }

    try:
        if 'number' not in request.args:
            response["error"] = True
            return jsonify(response), 400

        number = request.args.get('number').strip()
        num_float = float(number)
        num_int = int(num_float)

        response.update({
            "number": num_int,
            "digit_sum": digit_sum(num_int),
            "properties": get_properties(num_int),
            "fun_fact": get_fun_fact(num_int)
        })
        return jsonify(response), 200

    except (ValueError, TypeError):
        response.update({
            "number": request.args.get('number'),
            "error": True
        })
        return jsonify(response), 400

    except Exception as e:
        response["error"] = True
        return jsonify(response), 500

@app.after_request
def after_request(response):
    response.headers["Content-Type"] = "application/json"
    return response

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
