# Expense Tracker Web Application

This project is a **modern, responsive web application** for tracking personal expenses. It provides an intuitive interface for managing your finances, with features like expense categorization, filtering, and data visualization.

## Problem Statement

Managing personal finances can be challenging without the right tools. Traditional spreadsheets are often cumbersome, and existing expense tracking apps may lack flexibility or require subscriptions.

This project addresses these challenges by providing a **free, open-source, and user-friendly** expense tracking solution that runs entirely in your browser with local data storage.

## Features

- 📊 **Dashboard Overview**
  - Total spending summary
  - Transaction count
  - Top spending categories

- ➕ **Easy Expense Tracking**
  - Add expenses with amount, category, date, and description
  - Auto-suggest for categories
  - Form validation

- 🔍 **Smart Filtering**
  - Filter by category
  - Date range filtering
  - Multiple sorting options

- 📱 **Responsive Design**
  - Works on desktop, tablet, and mobile devices
  - Clean, modern interface

- 📂 **Data Management**
  - Persistent storage with JSON file (`data/expenses.json`)
  - Simple file-based storage with automatic backup on write

## Tech Stack

- **Backend**: Python 3.8+
- **Web Framework**: Flask 2.3.3
- **Frontend**: 
  - HTML5, CSS3
  - Bootstrap 5.3.0
  - JavaScript (vanilla)
- **Data Storage**: JSON file
- **Dependency Management**: pip/requirements.txt

## Screenshots

> 📂 Screenshots of the application in action will be added to the `screenshots/` directory.


## Getting Started

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/buhariroshan/expense-tracker.git
   cd expense-tracker
   ```

2. **Create and activate a virtual environment (recommended)**
   ```bash
   # On Windows
   python -m venv venv
   .\venv\Scripts\activate
   
   # On macOS/Linux
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Initialize the data directory**
   ```bash
   # The application will automatically create the data directory and expenses.json file
   # when you first run the application
   ```

### Running the Application

```bash
# Start the development server
python app.py
```

Then open your browser and navigate to:
```
http://localhost:5000
```

## Project Structure

```
expense-tracker/
├── app.py                # Main application file
├── requirements.txt      # Project dependencies
├── README.md             # This file
├── screenshots/          # Screenshots of the application
├── templates/            # HTML templates
│   └── index.html
└── data/                 # Data storage
    └── expenses.json     # Stores all expense data
```

## Usage Guide

### Adding an Expense
1. Click the "Add New Expense" button
2. Fill in the amount, category, date, and description
3. Click "Add Expense" to save

### Filtering Expenses
- Use the filter section to view specific expenses
- Select a category from the dropdown
- Set date ranges using the date pickers
- Click "Apply Filters" to update the view

### Sorting Expenses
- Use the "Sort By" dropdown to change the sort order
- Options include:
  - Newest First (default)
  - Oldest First
  - Amount (High to Low)
  - Amount (Low to High)

## Acknowledgments

- Built with [Flask](https://flask.palletsprojects.com/)
- Styled with [Bootstrap 5](https://getbootstrap.com/)
- Icons by [Bootstrap Icons](https://icons.getbootstrap.com/)

---

<div align="center">
  Made with ❤️ by [@buhariroshan](https://github.com/buhariroshan)
</div>
