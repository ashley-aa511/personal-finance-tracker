const form = document.getElementById('transaction-form');
const transactionsTable = document.getElementById('transactions');
const totalIncomeElement = document.getElementById('total-income');
const totalExpensesElement = document.getElementById('total-expenses');


// Fetch all transactions from the backend
async function loadTransactions() {
    try {
        const response = await fetch('/transactions');
        if (!response.ok) {
            throw new Error('Failed to fetch transactions.');
        }

        const transactions = await response.json();
        console.log('Fetched transactions:', transactions); // Debugging log

        // Clear existing rows in the table
        transactionsTable.innerHTML = '';

        let totalIncome = 0;
        let totalExpenses = 0;

        // Render transactions in the table
transactions.forEach(transaction => {
    const row = document.createElement('tr');
    row.innerHTML = `
        <td>${transaction.amount}</td>
        <td>${transaction.category}</td>
        <td>${transaction.type}</td>
        <td>${new Date(transaction.date).toLocaleString()}</td>
        <td>
            <a href="/delete-transaction/${transaction.id}" class="delete-btn" 
               onclick="return confirm('Are you sure you want to delete this transaction?');">
                Delete
            </a>
        </td>
    `;
    transactionsTable.appendChild(row);

    // Update the totals
    if (transaction.type === 'income') {
        totalIncome += transaction.amount;
    } else if (transaction.type === 'expense') {
        totalExpenses += transaction.amount;
    }
});

// Update total income and expenses
totalIncomeElement.textContent = `$${totalIncome.toFixed(2)}`;
totalExpensesElement.textContent = `$${totalExpenses.toFixed(2)}`;

} catch (error) {
console.error('Error loading transactions:', error);
}
}

// Add a new transaction
form.addEventListener('submit', async (event) => {
event.preventDefault();

// Get form data
const amount = parseFloat(document.getElementById('amount').value);
const category = document.getElementById('category').value;
const type = document.getElementById('type').value;

// Validate the form data
if (isNaN(amount) || amount <= 0) {
alert('Please enter a valid amount.');
return;
}

const transaction = { amount, category, type };
console.log('Submitting transaction:', transaction);

try {
const response = await fetch('/add-transaction', {
method: 'POST',
headers: { 'Content-Type': 'application/json' },
body: JSON.stringify(transaction),
});

if (!response.ok) {
throw new Error('Failed to add transaction.');
}

console.log('Transaction added successfully.');

// Clear form and reload transactions
form.reset();
loadTransactions();
} catch (error) {
console.error('Error adding transaction:', error);
alert('An error occurred while adding the transaction. Please try again.');
}
});

// Initial load of transactions
loadTransactions();