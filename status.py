from PyInquirer import prompt
import csv

def calculate_owe_balance_from_csv():
    # Create a dictionary to track the balances for each user
    user_balances = {}

    # Read data from the CSV file
    with open('expense_report.csv', 'r', newline='') as f:
        reader = csv.reader(f)
        for row in reader:
            amount = float(row[0])
            label = row[1]
            spender = row[2]
            cospender = eval(row[3])  # Assumes cospender is stored as a string list in the CSV

            # Update the balance for the spender
            if spender not in user_balances:
                user_balances[spender] = 0
            user_balances[spender] -= amount

            # Split the expense among the cospenders
            num_cospenders = len(cospender)
            if num_cospenders > 0:
                split_amount = amount / (num_cospenders + 1)  # Including the spender
                for c in cospender:
                    if c not in user_balances:
                        user_balances[c] = 0
                    user_balances[c] += split_amount

    # Identify who owes whom
    owes_data = []
    for debtor, balance in user_balances.items():
        if balance > 0:
            for creditor, creditor_balance in user_balances.items():
                if creditor_balance < 0:
                    # Calculate the amount debtor owes to creditor
                    amount_owed = min(abs(balance), abs(creditor_balance))
                    owes_data.append((debtor, creditor, amount_owed))
                    # Update balances
                    user_balances[debtor] -= amount_owed
                    user_balances[creditor] += amount_owed

    return owes_data


def printbalance():
    # Calculate who owes whom and how much
    owe_data = calculate_owe_balance_from_csv()
    paid_debts = []  # List to track paid debts

    while True:
        print("paid debt")
        print(paid_debts)

        print("owe_data")
        print(owe_data)
        # Filter out paid debts from the report
        filtered_owe_data = [debt for debt in owe_data if debt not in paid_debts]

        # Display the status report
        print("Status Report:")
        for debtor, creditor, amount in filtered_owe_data:
            print(f"{debtor} owes {amount} to {creditor}")

        # Add an option to mark a debt as paid
        mark_debt_choices = [f"{debtor} owes {amount} to {creditor}" for debtor, creditor, amount in filtered_owe_data]
        if not mark_debt_choices:
            print("No more debts to mark as paid.")
            break

        mark_debt_choices.append('Exit')

        mark_debt_choice = {
            'type': 'list',
            'name': 'mark_debt',
            'message': 'Select a debt to mark as paid (or exit):',
            'choices': mark_debt_choices,
        }

        option = prompt(mark_debt_choice)

        if option['mark_debt'] == 'Exit':
            break

        selected_debt = option['mark_debt']
        debtor, creditor, amount = selected_debt.split(" owes ")[0], selected_debt.split(" to ")[1], float(
            selected_debt.split(" owes ")[1].split(" to ")[0])
        paid_debts.append((debtor, creditor, amount))
        print(f"Debt marked as paid: {selected_debt}")
