from flask import Flask, render_template, request, redirect, url_for
from .database import users_collection

def register_routes(app):
    @app.route('/')
    def home():
        return render_template('index.html')

    @app.route('/booking')
    def form():
        return render_template('booking.html')
    
    @app.route('/report')
    def report():
        return render_template('report.html')
    
    @app.route('/submit', methods=['POST'])
    def submit():
        name = request.form.get('name')
        email = request.form.get('email')

        if name and email:
            users_collection.insert_one({"name": name, "email": email})  # Insert into "users"

        return redirect(url_for('home'))