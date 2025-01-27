from flask import Flask, request, jsonify, render_template, flash, redirect, url_for
import csv
from io import StringIO
from flask import Response
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from sqlalchemy import func


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///finance.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'your_secret_key'  # Secret key for sessions
db = SQLAlchemy(app)

# Models
class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Float, nullable=False)
    category = db.Column(db.String(50), nullable=False)
    type = db.Column(db.String(10), nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)

# Initialize the database
with app.app_context():
    db.create_all()

# Routes
@app.route('/')
def home():
    return render_template('landing.html')  # Serve the landing page at root

@app.route('/app')
def app_page():
    return render_template('index.html')  # Serve the finance tracker app

@app.route('/add-transaction', methods=['POST'])
def add_transaction():
    data = request.json
    new_transaction = Transaction(
        amount=data['amount'],
        category=data['category'],
        type=data['type']
    )
    db.session.add(new_transaction)
    db.session.commit()
    return jsonify({'message': 'Transaction added successfully!'}), 201

@app.route('/transactions', methods=['GET'])
def get_transactions():
    transactions = Transaction.query.all()
    result = [
        {
            'id': t.id,
            'amount': t.amount,
            'category': t.category,
            'type': t.type,
            'date': t.date.strftime('%Y-%m-%d %H:%M:%S')
        } for t in transactions
    ]
    return jsonify(result)

@app.route('/delete-transaction/<int:id>', methods=['GET'])
def delete_transaction(id):
    transaction = Transaction.query.get(id)
    if transaction:
        db.session.delete(transaction)
        db.session.commit()
        flash('Transaction deleted successfully.')
    else:
        flash('Transaction not found.')
    return redirect(url_for('app_page'))  # Redirect to the main app page after deleting

@app.route('/export-transactions')
def export_transactions():
    transactions = Transaction.query.all()

    output = StringIO()
    writer = csv.writer(output)
    writer.writerow(['ID', 'Amount', 'Category', 'Type', 'Date'])

    for transaction in transactions:
        writer.writerow([transaction.id, transaction.amount, transaction.category, transaction.type, transaction.date.strftime('%Y-%m-%d')])

    output.seek(0)
    return Response(output, mimetype='text/csv', headers={'Content-Disposition': 'attachment; filename=transactions.csv'})

# Monthly Summary Route
@app.route('/summary')
def summary():
    # Get the current month and year
    current_month = datetime.utcnow().month
    current_year = datetime.utcnow().year
    
    # Query transactions for the current month and group by category
    transactions = db.session.query(
        func.sum(Transaction.amount).label('total_amount'),
        Transaction.category,
        func.strftime('%Y-%m', Transaction.date).label('month')
    ).filter(
        func.extract('month', Transaction.date) == current_month,
        func.extract('year', Transaction.date) == current_year
    ).group_by(Transaction.category).all()

    # Convert SQLAlchemy Row object to a list of dictionaries
    transactions_list = [{
        'category': t.category,
        'total_amount': t.total_amount
    } for t in transactions]

    # Calculate total amount
    total_amount = sum(t['total_amount'] for t in transactions_list)

    # Render the monthly summary page with the results
    return render_template('summary.html', 
                           transactions=transactions_list,
                           total_amount=total_amount,
                           current_year=current_year,
                           current_month=current_month)

if __name__ == '__main__':
    app.run(debug=True)
