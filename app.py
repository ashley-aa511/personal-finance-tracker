from flask import Flask, request, jsonify, render_template, flash, redirect, url_for, Response
import csv
from io import StringIO
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
    try:
        # Parse JSON data from the request
        data = request.get_json()
        amount = data.get('amount')
        category = data.get('category')
        transaction_type = data.get('type')

        # Validate required fields
        if amount is None or category is None or transaction_type is None:
            return jsonify({'error': 'All fields are required!'}), 400

        # Create the transaction object and save to the database
        transaction = Transaction(
            amount=float(amount),
            category=category,
            type=transaction_type
        )
        db.session.add(transaction)
        db.session.commit()

        return jsonify({'message': 'Transaction added successfully'}), 201

    except Exception as e:
        return jsonify({'error': str(e)}), 500

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

@app.route('/delete-transaction/<int:id>', methods=['DELETE'])
def delete_transaction(id):
    try:
        transaction = Transaction.query.get(id)
        if not transaction:
            return jsonify({'error': 'Transaction not found'}), 404

        db.session.delete(transaction)
        db.session.commit()
        return jsonify({'message': 'Transaction deleted successfully'}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

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

@app.route('/summary')
def summary():
    current_month = datetime.utcnow().month
    current_year = datetime.utcnow().year

    # Query transactions for the current month and group by category
    transactions = db.session.query(
        func.sum(Transaction.amount).label('total_amount'),
        Transaction.category
    ).filter(
        func.extract('month', Transaction.date) == current_month,
        func.extract('year', Transaction.date) == current_year
    ).group_by(Transaction.category).all()

    # Convert to a list of dictionaries
    transactions_list = [{'category': t.category, 'total_amount': t.total_amount} for t in transactions]
    total_amount = sum(t['total_amount'] for t in transactions_list)

    return render_template('summary.html', 
                           transactions=transactions_list,
                           total_amount=total_amount,
                           current_year=current_year,
                           current_month=current_month)

if __name__ == '__main__':
    app.run(debug=True)
