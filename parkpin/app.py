from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

parking_data = {
    "TN09AB1234": "A2",
    "TN22CD5678": "B1",
    "TN01EF9999": "C3",
}

# Every zone's position on the grid
# Format: zone → (row, col)
zone_positions = {
    "A1": (0, 0), "A2": (0, 1), "A3": (0, 2), "A4": (0, 3),
    "B1": (1, 0), "B2": (1, 1), "B3": (1, 2), "B4": (1, 3),
    "C1": (2, 0), "C2": (2, 1), "C3": (2, 2), "C4": (2, 3),
}

def get_directions(from_zone, to_zone):
    if from_zone not in zone_positions or to_zone not in zone_positions:
        return []

    from_row, from_col = zone_positions[from_zone]
    to_row, to_col = zone_positions[to_zone]

    row_diff = to_row - from_row  # negative = move up, positive = move down
    col_diff = to_col - from_col  # negative = move left, positive = move right

    steps = []

    if from_zone == to_zone:
        steps.append("You are already at your vehicle's zone!")
        return steps

    # Vertical movement first
    if row_diff < 0:
        steps.append(f"Walk forward {abs(row_diff)} row(s) toward the entrance")
    elif row_diff > 0:
        steps.append(f"Walk back {abs(row_diff)} row(s) away from the entrance")

    # Horizontal movement
    if col_diff < 0:
        steps.append(f"Turn left and walk {abs(col_diff)} zone(s)")
    elif col_diff > 0:
        steps.append(f"Turn right and walk {abs(col_diff)} zone(s)")

    steps.append(f"Zone {to_zone} is right there — your vehicle is parked here!")

    return steps

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/find", methods=["POST"])
def find_vehicle():
    plate = request.json.get("plate", "").strip().upper()
    current_zone = request.json.get("current_zone", "").strip().upper()

    if plate in parking_data:
        to_zone = parking_data[plate]
        directions = get_directions(current_zone, to_zone) if current_zone else []
        return jsonify({
            "found": True,
            "plate": plate,
            "zone": to_zone,
            "directions": directions,
            "from_zone": current_zone
        })
    else:
        return jsonify({"found": False, "plate": plate})

if __name__ == "__main__":
    app.run(debug=True)