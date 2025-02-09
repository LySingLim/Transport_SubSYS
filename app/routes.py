from flask import Flask, render_template, request, redirect, url_for, jsonify
from .database import booking_collection, users_collection, prices_collection

def register_routes(app):
    @app.route('/')
    def home():
        users = list(users_collection.find().sort("_id", -1)) # Get all bookings in ascending order
        return render_template('index.html', users=users)


    @app.route('/booking')
    def booking():
        return render_template('booking.html')
    
    @app.route('/report')
    def report():
        # Aggregate data to count how many times each person booked
        booking_counts = booking_collection.aggregate([
            {"$group": {"_id": "$name", "booking_count": {"$sum": 1}}},  # Group by name and count
            {"$sort": {"booking_count": -1}}  # Sort by most bookings
        ])

        # Convert to list
        bookings = [{"name": b["_id"], "count": b["booking_count"]} for b in booking_counts]

        return render_template('report.html', bookings=bookings)
    
    @app.route('/submit', methods=['POST'])
    def submit():
        name = request.form.get('name')
        people = request.form.get('people')
        transport = request.form.get('transport')

        if not name or not people or not transport:
            return jsonify({"success": False, "message": "All fields are required"}), 400

        booking_collection.insert_one({
            "name": name,
            "people": int(people),  # Ensure people is stored as an integer
            "transport": transport
        })

        return redirect(url_for('home'))
    

    # 📌 API Route to Receive Data from Other Systems
    @app.route('/api/receive', methods=['POST'])
    def receive_booking():
        data = request.json

        # Validate incoming data
        if not data or "name" not in data or "people" not in data or "transport" not in data:
            return jsonify({"success": False, "message": "Invalid data format"}), 400

        # Insert into database
        users_collection.insert_one({
            "name": data["name"],
            "people": int(data["people"]),
            "transport": data["transport"]
        })

        return jsonify({"success": True, "message": "Booking received!"}), 201

    @app.route("/api/transports", methods=["GET"])
    def get_transports():
        transports = list(prices_collection.find({}, {"_id": 0, "id": 1, "transport": 1, "price": 1}))
        print(transports)
        return jsonify(transports)