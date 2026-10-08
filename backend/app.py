from flask import Flask, request, jsonify
from flask_cors import CORS

from calculator import calculate_expression
from database import (
    create_database,
    add_history,
    get_history,
    clear_history
)


# Create Flask application
app = Flask(__name__)

# Allow frontend to communicate with backend
CORS(app)


# Create SQLite database
create_database()


# ==========================================
# HOME ROUTE
# ==========================================

@app.route("/", methods=["GET"])
def home():

    return jsonify({
        "success": True,
        "message": "Scientific Calculator API is running!"
    })


# ==========================================
# CALCULATE ROUTE
# ==========================================

@app.route("/api/calculate", methods=["POST"])
def calculate():

    try:

        data = request.get_json()

        if not data:

            return jsonify({
                "success": False,
                "error": "No data received."
            }), 400


        expression = data.get("expression", "").strip()

        mode = data.get("mode", "DEG").upper()


        if not expression:

            return jsonify({
                "success": False,
                "error": "Expression cannot be empty."
            }), 400


        if mode not in ["DEG", "RAD"]:

            return jsonify({
                "success": False,
                "error": "Mode must be DEG or RAD."
            }), 400


        # Calculate result
        result = calculate_expression(
            expression,
            mode
        )


        # Save calculation
        add_history(
            expression,
            result,
            mode
        )


        return jsonify({

            "success": True,

            "expression": expression,

            "result": result,

            "mode": mode

        })


    except ValueError as error:

        return jsonify({

            "success": False,

            "error": str(error)

        }), 400


    except Exception as error:

        print("Server Error:", error)

        return jsonify({

            "success": False,

            "error": "Internal server error."

        }), 500


# ==========================================
# GET HISTORY
# ==========================================

@app.route("/api/history", methods=["GET"])
def history():

    try:

        records = get_history()

        return jsonify({

            "success": True,

            "history": records

        })


    except Exception as error:

        print("History Error:", error)

        return jsonify({

            "success": False,

            "error": "Could not load history."

        }), 500


# ==========================================
# CLEAR HISTORY
# ==========================================

@app.route("/api/history", methods=["DELETE"])
def delete_history():

    try:

        clear_history()

        return jsonify({

            "success": True,

            "message": "History cleared successfully."

        })


    except Exception as error:

        print("Delete Error:", error)

        return jsonify({

            "success": False,

            "error": "Could not clear history."

        }), 500


# ==========================================
# START SERVER
# ==========================================

if __name__ == "__main__":

    app.run(
        host="127.0.0.1",
        port=5000,
        debug=True
    )