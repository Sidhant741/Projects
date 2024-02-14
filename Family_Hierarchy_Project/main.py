from helper import *
from Database_helper import *

db_engine = DB()
no_of_unique_nodes = db_engine.calculate_unique_person()[0][0]


def add_node_details():
    first_name = input("Enter First Name :")
    last_name = input("Enter Last Name :")
    gender = input("Enter Gender ('M' or 'F'):")
    dob = input("Enter Date Of Birth (in format 'YYYY-MM-DD') :")
    dod = input("Enter Date Of Birth (in format 'YYYY-MM-DD') :")
    father_name =

def what_to_do(choice):
    global no_of_unique_nodes
    if int(choice) == 1:
        print("Your Family Tree")
    elif int(choice) == 2:
        print("Enter details")
        no_of_unique_nodes += 1

        print(no_of_unique_nodes)
    elif int(choice) == 3:
        print("delete a node")
    elif int(choice) == 4:
        print("Updating a node")
    else:
        print("Wrong input, Try again")


while True:
    print("Welcome To your family Tree \nWhat do you want to do?")
    print("1. See your Family Tree \n2. Add a node \n3. Delete a node \n4. Update a node \n5. Quit")
    temp_input = input()
    if int(temp_input) == 5:
        break
    what_to_do(temp_input)
