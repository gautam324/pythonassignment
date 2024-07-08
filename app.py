from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///submissions.db'
db = SQLAlchemy(app)

class Submission(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    date_submitted = db.Column(db.DateTime, default=datetime.utcnow)

@app.route('/')
def home():
    current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return render_template('index.html', current_datetime=current_datetime)

@app.route('/submit', methods=['POST'])
def submit():
    name = request.form['name']
    email = request.form['email']
    new_submission = Submission(name=name, email=email)
    try:
        db.session.add(new_submission)
        db.session.commit()
        return redirect(url_for('submitted', name=name, email=email))
    except:
        return 'There was an issue adding your submission'

@app.route('/submitted')
def submitted():
    name = request.args.get('name')
    email = request.args.get('email')
    return render_template('submitted.html', name=name, email=email)


@app.route('/submissions')
def submissions():
    all_submissions = Submission.query.order_by(Submission.date_submitted).all()
    return render_template('submissions.html', submissions=all_submissions)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)