from PyInquirer import prompt
import csv

def new_expense(users, expenses):
    expense_questions = [
        {
            "type": "input",
            "name": "amount",
            "message": "New Expense - Amount: ",
            "validate": lambda val: val.replace('.', '', 1).isdigit() or "Amount must be a valid number"
        },
        {
            "type": "input",
            "name": "label",
            "message": "New Expense - Label: ",
            "validate": lambda val: len(val.strip()) > 0 or "Label cannot be empty"
        },
        {
            "type": "list",
            "name": "spender",
            "message": "New Expense - Spender: ",
            "choices": users,
        }
    ]


    if not users:
        print("Add User First")
        return False

    infos = prompt(expense_questions)
    spender = infos["spender"]
    if spender not in users:
        print("User does not exist")
        return False
    elif (len(users) == 1):
        print("There is only one user. To add an expense you need at least two users")
        return False
    else:
        choices = [{"name": choice, "value": choice} for choice in users if choice != spender]

        usersquestions = {
            "type": "checkbox",
            "name": "cospender",
            "message": "New Expense - Persons involved: ",
            "choices": choices,
        }
        users = prompt(usersquestions)

        while not users["cospender"]:
            print("Please select at least one entry")
            users = prompt(usersquestions)

        infos["cospender"] = users["cospender"]
        expenses.append(infos)

        with open('expense_report.csv', 'w', newline='') as f:
            writer = csv.writer(f)
            for expense in expenses:
                writer.writerow(expense.values())

        print("Expense Added !")
    return True