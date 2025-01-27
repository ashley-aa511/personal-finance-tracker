---

# **Finance Tracker Application**

A simple web-based application built using Flask and JavaScript that allows users to track their income and expenses. This application enables users to add, view, and delete transactions, as well as export them to a CSV file or view a monthly summary.

---

## **Features**
- **Add Transactions:** Add income or expense transactions with category and type.
- **View Transactions:** Display all transactions in a tabular format.
- **Delete Transactions:** Remove transactions easily.
- **Export Transactions:** Download all transactions as a CSV file.
- **Monthly Summary:** View a summarized report of transactions grouped by category for the current month.

---

## **Technologies Used**
- **Frontend:**
  - HTML, CSS, JavaScript
- **Backend:**
  - Python with Flask
  - SQLite database
- **Other Libraries:**
  - SQLAlchemy for ORM
  - Bootstrap (optional) for styling

---

## **Setup Instructions**

### **1. Clone the Repository**
```bash
git clone https://github.com/your-username/finance-tracker.git
cd finance-tracker
```

### **2. Set Up a Virtual Environment**
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### **3. Install Dependencies**
```bash
pip install -r requirements.txt
```

### **4. Initialize the Database**
Run the following commands in Python to create the database:
```bash
python
>>> from app import db
>>> db.create_all()
>>> exit()
```

### **5. Run the Application**
```bash
python app.py
```
The application will run locally on `http://127.0.0.1:5000`.

---

## **Usage**
1. Navigate to the `/app` route to access the finance tracker interface.
2. Use the form to add transactions by specifying:
   - Amount
   - Category
   - Type (income or expense)
3. View transactions in the table.
4. Delete unwanted transactions by clicking "Delete."
5. Export transactions as a CSV file by clicking the "Export" button.
6. Check the monthly summary at the `/summary` route.

---

## **File Structure**
```
finance-tracker/
├── app.py                 # Main Flask application
├── templates/
│   ├── landing.html       # Landing page
│   ├── index.html         # Main tracker UI
│   └── summary.html       # Monthly summary page
├── static/
│   ├── styles.css         # Custom CSS
│   ├── script.js          # Frontend JavaScript
├── finance.db             # SQLite database file (generated after running the app)
├── requirements.txt       # Python dependencies
└── README.md              # Project README file
```

---

## **Screenshots**
### **1. Main Interface**
_Display the form and table for adding and viewing transactions._

### **2. Monthly Summary**
_View the categorized summary of income and expenses._

---

## **Future Improvements**
- Add user authentication for personalized data.
- Add chart/graph visualizations for better insights.
- Implement mobile-friendly design.
- Deploy the application using services like Heroku or Vercel.

---

## **License**
This project is licensed under the MIT License. Feel free to use and modify it for personal or educational purposes.

---
