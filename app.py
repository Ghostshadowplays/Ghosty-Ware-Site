import os
from flask import Flask, render_template, request, redirect, url_for, session, send_from_directory, flash
from flask_sqlalchemy import SQLAlchemy  # type: ignore
from datetime import datetime
from flask_migrate import Migrate  # type: ignore

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_unique_secret_key'  # Set your secret key here
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///feedback.db'  # Path to the SQLite database
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the SQLAlchemy object and migration
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Define the Feedback model
class Feedback(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    message = db.Column(db.Text, nullable=False)
    date_submitted = db.Column(db.DateTime, default=datetime.utcnow)

# Create database tables if they don't exist
with app.app_context():
    db.create_all()

# Home page
@app.route('/')
def home():
    return render_template('index.html')

# Other routes
@app.route('/downloads/<path:filename>')
def download_file(filename):
    return send_from_directory('downloads', filename)

@app.route('/projects')
def projects():
    return render_template('projects.html')

@app.route('/tutorials')
def tutorials():
    return render_template('tutorials.html')

@app.route('/feedback')
def feedback():
    all_feedback = Feedback.query.all()  # Retrieve all feedback entries from the database
    return render_template('feedback.html', feedback=all_feedback)

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/view-feedback')
def view_feedback():
    all_feedback = Feedback.query.all()
    print(all_feedback)  # Debugging line to check retrieved feedback
    return render_template('view_feedback.html', feedback=all_feedback)

@app.route('/submit-feedback', methods=['POST'])
def submit_feedback():
    name = request.form.get('name', '').strip()  # Get the name and strip whitespace
    message = request.form.get('message', '').strip()  # Get the message and strip whitespace

    print(f"Received feedback - Name: {name}, Message: {message}")  # Debugging line

    # Check if the name and message are not empty
    if not name or not message:
        flash("Name and message cannot be empty.", "danger")
        return redirect(url_for('feedback'))

    # Create a new feedback entry
    feedback_entry = Feedback(name=name, message=message)

    # Save the feedback entry to the database
    try:
        db.session.add(feedback_entry)
        db.session.commit()
        flash("Thank you for your feedback!", "success")
    except Exception as e:
        db.session.rollback()
        flash("Error saving feedback. Please try again.", "danger")
        print(f"Error: {e}")  # Print the error for debugging

    return redirect(url_for('feedback'))  # Redirect to feedback page


if __name__ == '__main__':
    app.run(debug=True)  # Run the app in debug mode
