from PyInquirer import prompt
from examples import custom_style_2
from expense import new_expense
from status import calculate_owe_balance_from_csv, printbalance
from user import add_user

users = []
expenses = []


def ask_option():
    main_option = {
        "type":"list",
        "name":"main_options",
        "message":"Expense Tracker v0.1",
        "choices": ["New Expense","Show Status","New User"]
    }


    option = prompt(main_option)
    if (option['main_options']) == "New Expense":
        new_expense(users, expenses)
        ask_option()
    elif (option['main_options']) == "Show Status":
        printbalance()
        ask_option()
    else:
        add_user(users)
        ask_option()

def main():
    ask_option()

main()