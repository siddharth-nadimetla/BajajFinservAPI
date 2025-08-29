from flask import Flask, request, jsonify
import re

app = Flask(__name__)

# Change these three variables to your details before deploying/submission
FULL_NAME = "Siddharth_nadimetla"
ROLL_NUMBER = "22BCI0303"
EMAIL_ID = "nadimetla.siddharth2022@vitstudent.ac.in"
DOB = "28092004"  # for user_id, use ddmmyyyy

# Helper functions
def process_array(data):
    odd_numbers = []
    even_numbers = []
    alphabets = []
    special_characters = []
    sum_numbers = 0
    concat_str = ""

    for item in data:
        # Handle string numbers
        if re.fullmatch(r'[0-9]+', item):
            num = int(item)
            if num % 2 == 0:
                even_numbers.append(item)
            else:
                odd_numbers.append(item)
            sum_numbers += num
        # Handle pure alphabets
        elif re.fullmatch(r'[a-zA-Z]+', item):
            alphabets.append(item.upper())
            concat_str += item
        # Handle alphanumeric with only alphabets (e.g., “ABcD”, “DOE”)
        elif any(c.isalpha() for c in item) and item.isalnum():
            alphabets.append(item.upper())
            concat_str += item
        # Special characters (including symbols, etc.)
        else:
            special_characters.append(item)

    # Alternating caps: reverse the concatenated string, alternating upper/lower, starting with upper
    concat_str_rev = ""
    chars = list(concat_str[::-1])
    for idx, c in enumerate(chars):
        if idx % 2 == 0:
            concat_str_rev += c.upper()
        else:
            concat_str_rev += c.lower()

    return {
        "odd_numbers": odd_numbers,
        "even_numbers": even_numbers,
        "alphabets": alphabets,
        "special_characters": special_characters,
        "sum": str(sum_numbers),
        "concat_string": concat_str_rev
    }

@app.route("/bfhl", methods=["POST"])
def bfhl():
    try:
        req = request.get_json()
        data = req.get("data", [])
        processed = process_array(data)

        response = {
            "is_success": True,
            "user_id": f"{FULL_NAME.lower()}_{DOB}",
            "email": EMAIL_ID,
            "roll_number": ROLL_NUMBER,
            "odd_numbers": processed["odd_numbers"],
            "even_numbers": processed["even_numbers"],
            "alphabets": processed["alphabets"],
            "special_characters": processed["special_characters"],
            "sum": processed["sum"],
            "concat_string": processed["concat_string"]
        }
        return jsonify(response), 200
    except Exception as e:
        # Graceful error handling
        return jsonify({
            "is_success": False,
            "user_id": f"{FULL_NAME.lower()}_{DOB}",
            "message": str(e)
        }), 400

if __name__ == "__main__":
    app.run()
