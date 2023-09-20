from PyInquirer import prompt
import csv


def add_user(users):
    while True:
        name = input("What is your name?\n")
        if not name.isalpha():
            print("Invalid input. Please enter a valid name containing only letters.")
        else:
            if name in users:
                print("User already exists.")
            else:
                users.append(name)
                with open('users.csv', 'w', newline='') as f:
                    writer = csv.writer(f)
                    writer.writerow(users)
                print("User added! Current users are:", ", ".join(users))
            break
    return