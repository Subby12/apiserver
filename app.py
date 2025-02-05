from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import math
from collections import OrderedDict

app = Flask(__name__)
CORS(app)

def is_armstrong(n):
    """Check if a number is Armstrong number."""
    n = abs(n)  # Use absolute value
    str_n = str(n)
    power = len(str_n)
    
    # Single digit numbers are not Armstrong numbers
    if power == 1:
        return False
        
    sum_of_powers = sum(int(digit) ** power for digit in str_n)
    return sum_of_powers == n

def is_prime(n):
    """Check if a number is prime."""
    if abs(n) <= 1:
        return False
    for i in range(2, int(math.sqrt(abs(n))) + 1):
        if abs(n) % i == 0:
            return False
    return True

def is_perfect(n):
    """Check if a number is perfect."""
    if abs(n) <= 1:
        return False
    return sum(i for i in range(1, abs(n)) if abs(n) % i == 0) == abs(n)

def digit_sum(n):
    """Calculate sum of digits."""
    return sum(int(digit) for digit in str(abs(n)))

def get_fun_fact(n):
    """Get mathematical fun fact about the number."""
    try:
        response = requests.get(f"http://numbersapi.com/{abs(n)}/math")
        return response.text if response.status_code == 200 else f"{n} is a number"
    except:
        return f"{n} is a number"

def determine_properties(n):
    """Determine if number is armstrong and whether it's odd or even."""
    properties = []
    
    # Check if number is armstrong
    if is_armstrong(n):
        properties.append("armstrong")
    
    # Add odd/even property
    if abs(n) % 2 == 0:
        properties.append("even")
    else:
        properties.append("odd")
    
    return properties

@app.route('/api/classify-number', methods=['GET'])
def classify_number():
    # Get the number parameter
    number = request.args.get('number')
    
    # Check if number parameter exists
    if number is None:
        return jsonify(OrderedDict([
            ("number", None),
            ("error", True)
        ])), 400

    # Remove any additional query parameters and whitespace
    number = number.split('?')[0].strip()

    try:
        # Convert to float first to catch decimal points
        num_float = float(number)
        # Convert to int to ensure it's a whole number
        num_int = int(num_float)
        
        # Check if the number is actually an integer
        if num_float != num_int:
            return jsonify(OrderedDict([
                ("number", number),
                ("error", True)
            ])), 400

        response = {
            "number": num_int,
            "is_prime": is_prime(num_int),
            "is_perfect": is_perfect(num_int),
            "properties": determine_properties(num_int),
            "digit_sum": digit_sum(num_int),
            "fun_fact": get_fun_fact(num_int)
        }
        return jsonify(response), 200

    except (ValueError, TypeError):
        return jsonify(OrderedDict([
            ("number", number),
            ("error", True)
        ])), 400

@app.errorhandler(404)
def not_found(error):
    return jsonify(OrderedDict([
        ("number", None),
        ("error", True)
    ])), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify(OrderedDict([
        ("number", None),
        ("error", True)
    ])), 500

@app.after_request
def after_request(response):
    response.headers["Content-Type"] = "application/json"
    return response

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
