const form = document.getElementById('transaction-form');
const transactionsTable = document.getElementById('transactions');
const totalIncomeElement = document.getElementById('total-income');
const totalExpensesElement = document.getElementById('total-expenses');

// Fetch all transactions from the backend
async function loadTransactions() {
    try {
        const response = await fetch('/transactions');
        if (!response.ok) throw new Error('Failed to fetch transactions.');

        const transactions = await response.json();
        console.log('Fetched transactions:', transactions);

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
                    <a href="#" class="delete-btn" data-id="${transaction.id}">Delete</a>
                </td>
            `;
            transactionsTable.appendChild(row);

            // Calculate totals
            if (transaction.type === 'income') {
                totalIncome += transaction.amount;
            } else if (transaction.type === 'expense') {
                totalExpenses += transaction.amount;
            }
        });

        // Update total income and expenses
        totalIncomeElement.textContent = `$${totalIncome.toFixed(2)}`;
        totalExpensesElement.textContent = `$${totalExpenses.toFixed(2)}`;

        // Add event listeners for delete buttons
        document.querySelectorAll('.delete-btn').forEach(button => {
            button.addEventListener('click', async (event) => {
                event.preventDefault();
                const transactionId = button.getAttribute('data-id');
                await deleteTransaction(transactionId);
            });
        });

    } catch (error) {
        console.error('Error loading transactions:', error);
    }
}

// Add a new transaction
form.addEventListener('submit', async (event) => {
    event.preventDefault();

    const amount = parseFloat(document.getElementById('amount').value);
    const category = document.getElementById('category').value;
    const type = document.getElementById('type').value;

    if (isNaN(amount) || amount <= 0) {
        alert('Please enter a valid amount.');
        return;
    }

    const transaction = { amount, category, type };

    try {
        const response = await fetch('/add-transaction', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(transaction),
        });

        if (!response.ok) throw new Error('Failed to add transaction.');

        console.log('Transaction added successfully.');
        form.reset();
        loadTransactions();

    } catch (error) {
        console.error('Error adding transaction:', error);
        alert('An error occurred while adding the transaction. Please try again.');
    }
});

// Delete a transaction
async function deleteTransaction(id) {
    try {
        const response = await fetch(`/delete-transaction/${id}`, { method: 'GET' });
        if (!response.ok) throw new Error('Failed to delete transaction.');

        console.log('Transaction deleted successfully.');
        loadTransactions();

    } catch (error) {
        console.error('Error deleting transaction:', error);
    }
}

// Initial load
loadTransactions();
