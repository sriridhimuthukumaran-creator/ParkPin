from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# This is your fake database for now — just a dictionary
# Format: plate number → zone
parking_data = {
    "TN09AB1234": "A2",
    "TN22CD5678": "B1",
    "TN01EF9999": "C3",
}

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/find", methods=["POST"])
def find_vehicle():
    plate = request.json.get("plate", "").strip().upper()
    if plate in parking_data:
        zone = parking_data[plate]
        return jsonify({"found": True, "plate": plate, "zone": zone})
    else:
        return jsonify({"found": False, "plate": plate})

if __name__ == "__main__":
    app.run(debug=True)