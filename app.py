from flask import Flask, render_template, request, redirect, url_for, flash
import json
from pathlib import Path
from datetime import datetime, timedelta
from functools import wraps

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'  # Required for flash messages

# Add template filters
@app.template_filter('strptime')
def _jinja2_filter_strptime(date_string, format):
    if not date_string:
        return ''
    return datetime.strptime(date_string, '%Y-%m-%d')

@app.template_filter('strftime')
def _jinja2_filter_strftime(date, format):
    if not date:
        return ''
    return date.strftime(format)

# Add a decorator to handle JSON loading/saving
def with_expenses(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        expenses = load_expenses()
        return f(expenses, *args, **kwargs)
    return decorated_function

DATA_FILE = Path("data/expenses.json")


def init_data_file():
    DATA_FILE.parent.mkdir(exist_ok=True)
    if not DATA_FILE.exists():
        DATA_FILE.write_text("[]", encoding="utf-8")


def load_expenses():
    init_data_file()
    with DATA_FILE.open("r", encoding="utf-8") as f:
        return json.load(f)


def save_expenses(expenses):
    with DATA_FILE.open("w", encoding="utf-8") as f:
        json.dump(expenses, f, indent=2)


def add_expense_to_file(amount, category, description, date_str=None):
    expenses = load_expenses()

    if not date_str:
        date_str = datetime.today().strftime("%Y-%m-%d")

    new_id = max((e["id"] for e in expenses), default=0) + 1

    expense = {
        "id": new_id,
        "date": date_str,
        "category": category,
        "amount": float(amount),
        "description": description
    }

    expenses.append(expense)
    save_expenses(expenses)


def get_categories(expenses):
    """Get unique categories from expenses"""
    return sorted(set(expense["category"] for expense in expenses))

@app.route("/", methods=["GET"])
@with_expenses
def index(expenses):
    # Get all unique categories for dropdown
    categories = get_categories(expenses)
    
    # Get filter parameters with defaults
    category = request.args.get("category", "").strip()
    start_date = request.args.get("start_date", "").strip()
    end_date = request.args.get("end_date", "").strip()
    sort_by = request.args.get("sort_by", "date_desc")

    # Apply filters
    filtered = expenses

    # Filter by category
    if category and category != "all":
        filtered = [
            e for e in filtered
            if e["category"].lower() == category.lower()
        ]

    # Filter by date range
    if start_date:
        filtered = [e for e in filtered if e["date"] >= start_date]
    if end_date:
        filtered = [e for e in filtered if e["date"] <= end_date]

    # Apply sorting
    if sort_by == "date_asc":
        filtered_sorted = sorted(filtered, key=lambda x: x["date"])
    elif sort_by == "amount_asc":
        filtered_sorted = sorted(filtered, key=lambda x: x["amount"])
    elif sort_by == "amount_desc":
        filtered_sorted = sorted(filtered, key=lambda x: x["amount"], reverse=True)
    else:  # Default: date_desc
        filtered_sorted = sorted(filtered, key=lambda x: x["date"], reverse=True)

    # Calculate totals
    total_filtered = sum(e["amount"] for e in filtered_sorted)
    total_all = sum(e["amount"] for e in expenses)
    
    # Calculate expenses by category for the filtered view
    category_totals = {}
    for expense in filtered_sorted:
        cat = expense["category"]
        category_totals[cat] = category_totals.get(cat, 0) + expense["amount"]
    
    # Get top 3 categories by amount
    top_categories = sorted(category_totals.items(), key=lambda x: x[1], reverse=True)[:3]

    # Get current date for the form
    now = datetime.now()
    
    return render_template(
        "index.html",
        expenses=filtered_sorted,
        total=total_filtered,
        overall_total=total_all,
        categories=categories,
        selected_category=category,
        selected_start_date=start_date,
        selected_end_date=end_date,
        selected_sort=sort_by,
        top_categories=top_categories,
        now=now
    )


@app.route("/add", methods=["POST"])
@app.route("/add", methods=["POST"])
def add():
    try:
        # Get and validate amount
        amount_str = request.form.get("amount", "").strip()
        if not amount_str:
            flash("Amount is required", "error")
            return redirect(url_for("index"))
            
        try:
            amount = float(amount_str)
            if amount <= 0:
                flash("Amount must be greater than 0", "error")
                return redirect(url_for("index"))
        except ValueError:
            flash("Please enter a valid amount", "error")
            return redirect(url_for("index"))
        
        # Get and validate category
        category = request.form.get("category", "").strip()
        if not category:
            flash("Category is required", "error")
            return redirect(url_for("index"))
        
        # Get optional fields
        description = request.form.get("description", "").strip()
        date_str = request.form.get("date", "").strip()
        
        # Validate date if provided
        if date_str:
            try:
                # Try to parse the date to ensure it's valid
                datetime.strptime(date_str, "%Y-%m-%d")
            except ValueError:
                flash("Invalid date format. Please use YYYY-MM-DD", "error")
                return redirect(url_for("index"))
        else:
            # If no date provided, use today's date
            date_str = datetime.now().strftime("%Y-%m-%d")
        
        # Add the expense
        add_expense_to_file(amount, category, description, date_str)
        flash(f"Successfully added expense of ₹{amount:.2f} for {category}", "success")
        
    except Exception as e:
        app.logger.error(f"Error adding expense: {str(e)}")
        flash("An error occurred while adding the expense. Please try again.", "error")
    
    return redirect(url_for("index"))
    description = request.form.get("description", "").strip()
    date_str = request.form.get("date")  # can be empty

    if not amount or not category:
        return redirect(url_for("index"))

    try:
        float(amount)
    except ValueError:
        return redirect(url_for("index"))

    add_expense_to_file(amount, category, description, date_str)
    return redirect(url_for("index"))


if __name__ == "__main__":
    # Ensure the data directory exists
    data_dir = Path("data")
    data_dir.mkdir(exist_ok=True)
    
    # Initialize the data file if it doesn't exist
    if not DATA_FILE.exists():
        init_data_file()
    
    # Run the app
    app.run(debug=True, host='0.0.0.0', port=5000)
      