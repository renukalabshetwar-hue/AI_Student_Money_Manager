import streamlit as st
from datetime import date
from collections import defaultdict
import os

st.set_page_config(
    page_title="AI Student Money Manager",
    page_icon="💰",
    layout="wide"
)

FILE_NAME = "student_money.txt"


# ==============================
# CREATE FILE
# ==============================

if not os.path.exists(FILE_NAME):
    open(FILE_NAME, "w", encoding="utf-8").close()


# ==============================
# READ DATA
# ==============================

def read_data():

    money = 0
    expenses = []

    with open(FILE_NAME, "r", encoding="utf-8") as file:
        lines = file.readlines()

    section = ""

    for line in lines:

        line = line.strip()

        if line == "MONEY":
            section = "money"

        elif line == "EXPENSES":
            section = "expenses"

        elif line and section:

            parts = line.split("|")

            try:

                if section == "money" and len(parts) == 1:

                    money = float(parts[0].strip())

                elif section == "expenses" and len(parts) == 4:

                    expenses.append({
                        "expense": parts[0].strip(),
                        "category": parts[1].strip(),
                        "amount": float(parts[2].strip()),
                        "date": parts[3].strip()
                    })

            except ValueError:
                pass

    return money, expenses


# ==============================
# SAVE DATA
# ==============================

def save_data(money, expenses):

    with open(FILE_NAME, "w", encoding="utf-8") as file:

        file.write("MONEY\n")
        file.write(f"{money}\n\n")

        file.write("EXPENSES\n")

        for item in expenses:

            file.write(
                f"{item['expense']} | "
                f"{item['category']} | "
                f"{item['amount']} | "
                f"{item['date']}\n"
            )


money, expenses = read_data()


# ==============================
# TITLE
# ==============================

st.title("💰 AI Student Money Manager")

st.write(
    "Track your money and find where you can save."
)

st.divider()


# ==============================
# CALCULATIONS
# ==============================

total_expenses = sum(
    item["amount"] for item in expenses
)

available_money = max(
    0,
    money - total_expenses
)


# ==============================
# SUMMARY
# ==============================

if not expenses:

    st.metric(
        "💰 Available Money",
        f"₹{money:,.2f}"
    )

else:

    col1, col2 = st.columns(2)

    with col1:

        st.metric(
            "💰 Available Money",
            f"₹{available_money:,.2f}"
        )

    with col2:

        st.metric(
            "💸 Total Expenses",
            f"₹{total_expenses:,.2f}"
        )


st.divider()


# ==============================
# ADD MONEY
# ==============================

st.header("💰 Add Money")

money_amount = st.number_input(
    "Enter Amount",
    min_value=0.0,
    step=100.0,
    value=0.0,
    key="money_amount"
)


if st.button(
    "➕ Add Money",
    key="add_money_button"
):

    if money_amount <= 0:

        st.error(
            "Please enter an amount greater than ₹0."
        )

    else:

        money = money + money_amount

        save_data(
            money,
            expenses
        )

        st.success(
            f"₹{money_amount:,.2f} added successfully!"
        )

        st.rerun()


st.divider()


# ==============================
# MULTIPLE EXPENSES
# ==============================

st.header("💸 Add Multiple Expenses")

st.write(
    "Add Food, Travel, Education, Shopping and other expenses at once."
)


expense_date = st.date_input(
    "Expense Date",
    value=date.today(),
    key="expense_date"
)


# ==============================
# FIRST ROW
# ==============================

col1, col2, col3 = st.columns(3)

with col1:

    food = st.number_input(
        "🍔 Food",
        min_value=0.0,
        step=50.0,
        key="food"
    )

with col2:

    travel = st.number_input(
        "🚌 Travel",
        min_value=0.0,
        step=50.0,
        key="travel"
    )

with col3:

    education = st.number_input(
        "📚 Education",
        min_value=0.0,
        step=50.0,
        key="education"
    )


# ==============================
# SECOND ROW
# ==============================

col1, col2, col3 = st.columns(3)

with col1:

    shopping = st.number_input(
        "🛍️ Shopping",
        min_value=0.0,
        step=50.0,
        key="shopping"
    )

with col2:

    entertainment = st.number_input(
        "🎬 Entertainment",
        min_value=0.0,
        step=50.0,
        key="entertainment"
    )

with col3:

    personal = st.number_input(
        "👤 Personal",
        min_value=0.0,
        step=50.0,
        key="personal"
    )


# ==============================
# OTHER
# ==============================

other = st.number_input(
    "📌 Other",
    min_value=0.0,
    step=50.0,
    key="other"
)


# ==============================
# ADD ALL EXPENSES
# ==============================

if st.button(
    "➕ Add All Expenses",
    key="add_all_expenses"
):

    expense_list = [
        ("Food", food),
        ("Travel", travel),
        ("Education", education),
        ("Shopping", shopping),
        ("Entertainment", entertainment),
        ("Personal", personal),
        ("Other", other)
    ]

    new_total = sum(
        amount
        for category, amount in expense_list
    )


    if money == 0:

        st.error(
            "Please add money first."
        )

    elif new_total == 0:

        st.warning(
            "Please enter at least one expense."
        )

    elif new_total > available_money:

        st.error(
            f"You only have ₹{available_money:,.2f} available."
        )

    else:

        for category, amount in expense_list:

            if amount > 0:

                expenses.append({
                    "expense": category,
                    "category": category,
                    "amount": amount,
                    "date": str(expense_date)
                })

        save_data(
            money,
            expenses
        )

        st.success(
            "All expenses added successfully!"
        )

        st.rerun()


# ==============================
# SAVING SUGGESTION
# ==============================

if expenses:

    st.divider()

    st.header("💡 Saving Suggestion")

    category_totals = defaultdict(float)

    for item in expenses:

        category_totals[
            item["category"]
        ] += item["amount"]


    if available_money == 0:

        st.info(
            "You have ₹0 available. "
            "Try to reduce your expenses."
        )

    else:

        highest = max(
            category_totals,
            key=category_totals.get
        )

        st.success(
            f"💡 Try to reduce your {highest} expenses."
        )


# ==============================
# EXPENSE RECORDS
# ==============================

if expenses:

    st.divider()

    st.header("📋 All Expenses")

    for item in expenses:

        st.write(
            f"💸 {item['category']} | "
            f"₹{item['amount']:,.2f} | "
            f"{item['date']}"
        )


# ==============================
# DOWNLOAD REPORT
# ==============================

if expenses:

    st.divider()

    st.header("📥 Download Your Money Report")

    report = ""

    report += "========================================\n"
    report += "       AI STUDENT MONEY MANAGER\n"
    report += "========================================\n\n"

    report += (
        f"TOTAL MONEY ADDED: ₹{money:,.2f}\n\n"
    )

    report += "EXPENSES\n"
    report += "--------\n"

    for item in expenses:

        report += (
            f"{item['category']} | "
            f"₹{item['amount']:,.2f} | "
            f"{item['date']}\n"
        )

    report += "\nSUMMARY\n"
    report += "-------\n"

    report += (
        f"Total Money Added: ₹{money:,.2f}\n"
    )

    report += (
        f"Total Expenses: ₹{total_expenses:,.2f}\n"
    )

    report += (
        f"Available Money: ₹{available_money:,.2f}\n"
    )

    st.download_button(
        "⬇️ Download Money Report",
        report,
        "student_money_report.txt",
        mime="text/plain",
        key="download_report"
    )
    