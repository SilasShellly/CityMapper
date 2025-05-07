from flask import Flask, request, jsonify
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)  # Enable CORS to allow frontend requests

GOOGLE_MAPS_API_KEY = "GOOGLE KEY"

# Function to get travel details from Google Maps API
def get_routes(origin, destination, mode):
    url = f"https://maps.googleapis.com/maps/api/directions/json?origin={origin}&destination={destination}&mode={mode}&key={GOOGLE_MAPS_API_KEY}"
    response = requests.get(url)
    data = response.json()

    if "routes" not in data or not data["routes"]:
        return None

    route = data["routes"][0]["legs"][0]
    
    distance_km = route["distance"]["value"] / 1000
    duration_mins = route["duration"]["value"] / 60

    return {
        "distance": round(distance_km, 2),
        "time": round(duration_mins, 2)
    }

# Function to calculate fares
def calculate_fare(distance_km, mode):
    base_fares = {
        "taxi": 30 + (distance_km * 15),  # Taxi: ₹30 base + ₹15 per km
        "bus": 10 + (distance_km * 5),   # Bus: ₹10 base + ₹5 per km
        "bike": 10 + (distance_km * 8),  # Bike: ₹10 base + ₹8 per km
        "mixed": 15 + (distance_km * 6)  # Mixed: ₹15 base + ₹6 per km
    }
    return f"₹{round(base_fares.get(mode, 0), 2)}"

@app.route("/getRoutes", methods=["GET"])
def get_routes_api():
    origin = request.args.get("origin")
    destination = request.args.get("destination")

    if not origin or not destination:
        return jsonify({"error": "Missing parameters"}), 400

    taxi = get_routes(origin, destination, "driving")
    bus = get_routes(origin, destination, "transit")
    
    # Bike should have same distance as Taxi but slightly faster time
    bike = taxi.copy()
    bike["time"] = round(taxi["time"] * 0.8, 2)  # Bike is 20% faster

    # Mixed Transport: Best combination (Auto → Metro → Train → Bus)
    mixed = {
        "distance": round((bus["distance"] + bike["distance"]) / 2, 2),
        "time": round((bus["time"] + bike["time"]) / 2, 2)
    }

    # Add fares
    taxi["fare"] = calculate_fare(taxi["distance"], "taxi")
    bus["fare"] = calculate_fare(bus["distance"], "bus")
    bike["fare"] = calculate_fare(bike["distance"], "bike")
    mixed["fare"] = calculate_fare(mixed["distance"], "mixed")

    routes = {
        "taxi": taxi,
        "bus": bus,
        "bike": bike,
        "mixed": mixed
    }

    return jsonify(routes)

if __name__ == "__main__":
    app.run(debug=True)
