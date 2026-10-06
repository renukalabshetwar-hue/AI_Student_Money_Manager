import streamlit as st
from datetime import date
from collections import defaultdict
from ollama import chat
import os


# --------------------------------------------------
# PAGE SETTINGS
# --------------------------------------------------

st.set_page_config(
    page_title="AI Student Money Manager",
    page_icon="💰",
    layout="wide"
)


# --------------------------------------------------
# FILE
# --------------------------------------------------

FILE_NAME = "student_money.txt"

if not os.path.exists(FILE_NAME):
    open(FILE_NAME, "w", encoding="utf-8").close()


# --------------------------------------------------
# CUSTOM CSS
# --------------------------------------------------

st.markdown("""
<style>

.main-title {
    text-align: center;
    font-size: 38px;
    font-weight: bold;
}

.subtitle {
    text-align: center;
    font-size: 18px;
    margin-bottom: 25px;
}

.card {
    padding: 20px;
    border-radius: 15px;
    border: 1px solid #ddd;
    text-align: center;
    margin-bottom: 15px;
}

.ai-box {
    padding: 20px;
    border-radius: 15px;
    background-color: #f0f8ff;
    border: 1px solid #b8d8ff;
    margin-top: 10px;
}

</style>
""", unsafe_allow_html=True)


# --------------------------------------------------
# READ DATA
# --------------------------------------------------

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


# --------------------------------------------------
# SAVE DATA
# --------------------------------------------------

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


# --------------------------------------------------
# AI ANALYSIS
# --------------------------------------------------

def get_ai_analysis(category_totals, total_expenses, available_money):

    spending = "\n".join(
        f"{category}: ₹{amount:.2f}"
        for category, amount in category_totals.items()
    )

    prompt = f"""
You are an AI financial assistant for a college student.

Analyze the student's expenses.

Expenses by category:
{spending}

Total expenses: ₹{total_expenses:.2f}
Available money: ₹{available_money:.2f}

Give a short analysis with exactly these three parts:

1. Spending Level:
Say whether the spending is Low, Moderate, or High.

2. Category to Reduce:
Identify ONE category the student should reduce.
Do not mention a saving amount.

3. Advice:
Give one simple and practical money-saving tip.

Rules:
- Use simple English.
- Keep the complete answer within 4 sentences.
- Do not tell the student how much money they should save.
- Do not use complicated financial terms.
"""

    response = chat(
        model="llama3.2",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return response["message"]["content"]


# --------------------------------------------------
# LOAD DATA
# --------------------------------------------------

money, expenses = read_data()


# --------------------------------------------------
# CALCULATIONS
# --------------------------------------------------

total_expenses = sum(
    item["amount"]
    for item in expenses
)

available_money = max(
    0,
    money - total_expenses
)


# --------------------------------------------------
# TITLE
# --------------------------------------------------

st.markdown(
    '<div class="main-title">💰 AI Student Money Manager</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'Manage your student expenses and get AI-powered money-saving suggestions.'
    '</div>',
    unsafe_allow_html=True
)


st.divider()


# --------------------------------------------------
# MONEY SUMMARY
# --------------------------------------------------

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


# --------------------------------------------------
# ADD MONEY
# --------------------------------------------------

st.header("💰 Add Money")

st.write(
    "Enter the amount of money currently available to you."
)

money_amount = st.number_input(
    "Amount",
    min_value=0.0,
    step=100.0,
    value=0.0,
    key="money_amount"
)


if st.button(
    "➕ Add Money",
    key="add_money_button",
    use_container_width=True
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


# --------------------------------------------------
# ADD EXPENSES
# --------------------------------------------------

st.header("💸 Add Your Expenses")

st.write(
    "Enter your expenses for different categories."
)


expense_date = st.date_input(
    "Expense Date",
    value=date.today()
)


# First row
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


# Second row
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


other = st.number_input(
    "📌 Other",
    min_value=0.0,
    step=50.0,
    key="other"
)


# --------------------------------------------------
# ADD ALL EXPENSES
# --------------------------------------------------

if st.button(
    "➕ Add All Expenses",
    key="add_all_expenses",
    use_container_width=True
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


    # No money
    if money <= 0:

        st.error(
            "Please add money first."
        )


    # No expense
    elif new_total == 0:

        st.warning(
            "Please enter at least one expense."
        )


    # Expense greater than available money
    elif new_total > available_money:

        st.error(
            f"You only have ₹{available_money:,.2f} available. "
            f"Your expenses total ₹{new_total:,.2f}."
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
            "All expenses added successfully! 🎉"
        )

        st.rerun()


# --------------------------------------------------
# EXPENSE ANALYSIS
# --------------------------------------------------

if expenses:

    st.divider()

    st.header("📊 Expense Overview")


    category_totals = defaultdict(float)


    for item in expenses:

        category_totals[
            item["category"]
        ] += item["amount"]


    # Highest category
    highest_category = max(
        category_totals,
        key=category_totals.get
    )


    highest_amount = category_totals[
        highest_category
    ]


    col1, col2 = st.columns(2)


    with col1:

        st.info(
            f"🏆 Highest Spending Category\n\n"
            f"**{highest_category}**"
        )


    with col2:

        st.info(
            f"💸 Highest Category Expense\n\n"
            f"**₹{highest_amount:,.2f}**"
        )


    # Chart
    st.subheader("📈 Spending by Category")

    chart_data = dict(category_totals)

    st.bar_chart(chart_data)


# --------------------------------------------------
# AI ANALYSIS
# --------------------------------------------------

if expenses:

    st.divider()

    st.header("🤖 AI Money Analysis")

    st.write(
        "Let AI analyze your spending and give you a personalized suggestion."
    )


    if st.button(
        "🤖 Analyze My Expenses",
        use_container_width=True,
        key="ai_analysis_button"
    ):

        with st.spinner(
            "🤖 AI is analyzing your expenses..."
        ):

            try:

                ai_result = get_ai_analysis(
                    category_totals,
                    total_expenses,
                    available_money
                )


                st.markdown(
                    '<div class="ai-box">',
                    unsafe_allow_html=True
                )

                st.write(
                    ai_result
                )

                st.markdown(
                    '</div>',
                    unsafe_allow_html=True
                )


            except Exception as error:

                st.error(
                    "AI could not analyze your expenses."
                )

                st.info(
                    "Make sure Ollama is running and the llama3.2 model is installed."
                )


# --------------------------------------------------
# FRIENDLY SPENDING MESSAGE
# --------------------------------------------------

if expenses:

    st.divider()

    st.header("💡 Money Status")


    if available_money == 0:

        st.error(
            "⚠️ You have used all your available money. "
            "Try to reduce unnecessary expenses."
        )

    elif total_expenses < money * 0.30:

        st.success(
            "🟢 Your spending is currently low. "
            "Good job managing your money!"
        )

    elif total_expenses < money * 0.70:

        st.warning(
            "🟡 Your spending is moderate. "
            "Keep an eye on your expenses."
        )

    else:

        st.error(
            "🔴 Your spending is high. "
            "Consider reducing unnecessary expenses."
        )


# --------------------------------------------------
# ALL EXPENSES
# --------------------------------------------------

if expenses:

    st.divider()

    st.header("📋 All Expenses")


    for item in expenses:

        st.write(
            f"💸 **{item['category']}**  |  "
            f"₹{item['amount']:,.2f}  |  "
            f"{item['date']}"
        )


# --------------------------------------------------
# DOWNLOAD REPORT
# --------------------------------------------------

if expenses:

    st.divider()

    st.header("📥 Download Your Money Report")


    report = ""

    report += "========================================\n"

    report += "       AI STUDENT MONEY MANAGER\n"

    report += "========================================\n\n"


    report += (
        f"TOTAL MONEY ADDED: "
        f"₹{money:,.2f}\n\n"
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
        f"Total Money Added: "
        f"₹{money:,.2f}\n"
    )


    report += (
        f"Total Expenses: "
        f"₹{total_expenses:,.2f}\n"
    )


    report += (
        f"Available Money: "
        f"₹{available_money:,.2f}\n"
    )


    report += (
        f"Highest Spending Category: "
        f"{highest_category}\n"
    )


    report += (
        f"Highest Category Expense: "
        f"₹{highest_amount:,.2f}\n"
    )


    st.download_button(

        "⬇️ Download Money Report",

        report,

        "student_money_report.txt",

        mime="text/plain",

        key="download_report",

        use_container_width=True
    )

    