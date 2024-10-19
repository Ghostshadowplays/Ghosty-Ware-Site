from flask import Flask, render_template, redirect, request
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, render_template, request, redirect, url_for, send_from_directory


# Create the Flask application instance
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///feedback.db'  # Path to the SQLite database
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the SQLAlchemy object
db = SQLAlchemy(app)

# Define the Feedback model
class Feedback(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    message = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return f'<Feedback {self.name}>'

@app.route('/')
def home():
    return render_template('index.html')

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
    return render_template('feedback.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/view-feedback')
def view_feedback():
    all_feedback = Feedback.query.all()  # Retrieve all feedback entries from the database
    return render_template('view_feedback.html', feedback=all_feedback)

@app.route('/submit-feedback', methods=['POST'])
def submit_feedback():
    name = request.form['name']
    message = request.form['message']

    # Create a new feedback entry and save it to the database
    new_feedback = Feedback(name=name, message=message)
    db.session.add(new_feedback)
    db.session.commit()

    return redirect('/feedback')  # Redirect back to the feedback page

if __name__ == '__main__':
    with app.app_context():  # Create an application context
        db.create_all()  # Create the database tables
    app.run(debug=True)  # Run the app in debug mode
