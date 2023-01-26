# Notes: 
# 1. Use the following username and password to access the admin rights 
# username: admin
# password: password
# 2. Ensure you open the whole folder for this task in VS Code otherwise the 
# program will look in your root directory for the text files.

#=====importing libraries===========
import os
from datetime import datetime, date

DATETIME_STRING_FORMAT = "%Y-%m-%d"


def write_task_file(tasks):
    # - Function to write tasks from the add task funciton
    with open("tasks.txt", "w") as file:
        task_list_to_write = []
        for i in tasks:
            str_attrs = [i['username'],i['title'],i['description'],i['due_date'].strftime(DATETIME_STRING_FORMAT),i['assigned_date'].strftime(DATETIME_STRING_FORMAT),"Yes" if i['completed'] else "No"]
            task_list_to_write.append(";".join(str_attrs))
        file.write("\n".join(task_list_to_write))

def reg_user(username_password):
        
     # - Request input of a new username
        new_username = input("New Username: ")
        # - Loops if it detects a duplicate username and requests a new one
        while new_username in username_password.keys():
            new_username = input("That user is already registered, please try another name: ")

        # - Request input of a new password
        new_password = input("New Password: ")

        # - Request input of password confirmation.
        confirm_password = input("Confirm Password: ")

        # - Check if the new password and confirmed password are the same.
        if new_password == confirm_password:
            # - If they are the same, add them to the user.txt file,
            print("New user added")
            username_password[new_username] = new_password

            with open("user.txt", "w") as out_file:
                user_data = []
                for k in username_password:
                    user_data.append(f"{k};{username_password[k]}")
                out_file.write("\n".join(user_data))
        else:
            print("Passwords do not match")

def add_task(username_password):
    task_username = input("Name of person assigned to task: ")
    # - Check is user is registered
    if task_username not in username_password.keys():
        print("User does not exist. Please enter a valid username")
    task_title = input("Title of Task: ")
    task_description = input("Description of Task: ")
    task_completed="No"
    task_start_date=date.today()
    task_due_date = input("Due date of task (YYYY-MM-DD): ")
    # - Write the user inputs into the file 
    with open("tasks.txt", "a") as task_file:
        task_file.write(f"\n{task_username};{task_title};{task_description};{task_due_date};{task_start_date};{task_completed}")
    print("Task successfully added.")

def view_all_tasks(task_list):
    #- Print all tasks in the task list
        for t in task_list:
            disp_str = f"Task: \t\t\t {t['title']}\n"
            disp_str += f"Task Description: \t {t['description']}\n"
            disp_str += f"Assigned to: \t\t {t['username']}\n"
            disp_str += f"Date Assigned: \t\t {t['assigned_date'].strftime(DATETIME_STRING_FORMAT)}\n"
            disp_str += f"Due Date: \t\t {t['due_date'].strftime(DATETIME_STRING_FORMAT)}\n"
            print(disp_str)

def view_my_tasks():
    # - Loop through the task list and print any tasks that has the same user as the current user logged in
    for i,t in enumerate(task_list):
        if t['username'] == curr_user:
            disp_str = f"Task number: \t\t {i}\n"
            disp_str += f"Task: \t\t\t {t['title']}\n"
            disp_str += f"Task Description: \t {t['description']}\n"
            disp_str += f"Assigned to: \t\t {t['username']}\n"
            disp_str += f"Date Assigned: \t\t {t['assigned_date'].strftime(DATETIME_STRING_FORMAT)}\n"
            disp_str += f"Due Date: \t\t {t['due_date'].strftime(DATETIME_STRING_FORMAT)}\n"
            print(disp_str)
    edit_task_selector=int(input("Select a task number or return to the main menu with -1: "))
    if edit_task_selector == "-1":
        return
    # - Ensure value is valid
    elif edit_task_selector>len(task_list)-1:
        print("That was not a value task number, sorry.")
        return
    else:
        edit_task_option=input(f"\nEnter the option you would like to edit \n c - Mark the task as complete \n n - Change the user that is assigned to the task \n d - Change the due date of the task \n")
         # - Updates the task_list variable to then call the write task function to edit the original file
        if edit_task_option=="c":
            if task_list[edit_task_selector]["completed"] == True:
                print("This task is already marked as complete")
            # - Set task completion to true
            else:
                task_list[edit_task_selector]["completed"] = True
                print(f"Task {edit_task_selector} has been marked as complete.")
        # - Replace new name aslong as it has been registered
        elif edit_task_option=="n":
            new_name=input("What would you like the new name on the task to be? ")
            if new_name not in username_password.keys():
                print("This user is not registered.")
            else:
                task_list[edit_task_selector]["username"]=new_name
                print(f"The user for {edit_task_selector} has been changed to {new_name}")
        # - Set new due date
        elif edit_task_option=="d":
            new_date=input("What is the new due date for the task? (YYYY-MM-DD): ")
            due_date = datetime.strptime(new_date, DATETIME_STRING_FORMAT)
            task_list[edit_task_selector]["due_date"]=due_date
            print(f"The due date for Task:{edit_task_selector} has been changed to {new_date}")
        write_task_file(task_list)
    
def task_overview(task_list,user_data):
    curr_date=datetime.today()
    total_tasks=len(task_list)
    total_users=len(user_data)
    # - Creating dictionary to hold all the values for the file
    final_rep_dict={"total_tasks":total_tasks,
                    "total_users":total_users,
                    "total_completed":0,
                    "total_uncompleted":0,
                    "total_overdue":0,
                    }
    # - Itterating over each task and updating dictionary values based on the conditions for each stat
    for task in task_list:
        if task["completed"]:
            final_rep_dict["total_completed"]+=1
        if task["completed"]==False:
            final_rep_dict["total_uncompleted"]+=1
        if task["due_date"] < curr_date and task["completed"]==False:
            final_rep_dict["total_overdue"]+=1
    with open ("task_overview.txt", "w") as task_overview_file:
        task_overview_file.write(f"""
*********************************************************************************
Total Tasks Generated:              {final_rep_dict["total_tasks"]}
Total Completed Tasks:              {final_rep_dict["total_completed"]}
Total Uncomplete Tasks:             {final_rep_dict["total_uncompleted"]}
Total Overdue Tasks:                {final_rep_dict["total_overdue"]}
Percentage of incomplete tasks:     {round((final_rep_dict["total_uncompleted"]/final_rep_dict["total_tasks"])*100)}%
Percentage of overdue tasks:        {round((final_rep_dict["total_overdue"]/final_rep_dict["total_tasks"])*100)}%
*********************************************************************************
        """)

def user_overview(task_list,user_data):
    curr_date=datetime.today()
    total_tasks=len(task_list)
    total_users=len(user_data)
    # - Creating dictionary with users as a nested dictionary containing each unique user
    final_rep_dict={"total_tasks":total_tasks,
                    "total_users":total_users,
                    "users":{}
                    }
    # - Itterating over every task in the list, update values for the corresponding user
    for task in task_list:
        if task["username"] not in final_rep_dict["users"]:
            final_rep_dict["users"][task["username"]]=  {"number_of_tasks":0,
                                                         "number_of_completed":0,
                                                         "number_of_uncompleted":0,
                                                         "number_of_overdue":0
                                                        }
        final_rep_dict["users"][task["username"]]["number_of_tasks"]+=1
        if task["completed"]:
            final_rep_dict["users"][task["username"]]["number_of_completed"]+=1
        if task["completed"]==False:
            final_rep_dict["users"][task["username"]]["number_of_uncompleted"]+=1
        if task["due_date"]<curr_date and task["completed"]==False:
            final_rep_dict["users"][task["username"]]["number_of_overdue"]+=1
        with open ("user_overview.txt", "w") as user_overview_file:
            user_overview_file.write(f"""
*********************************************************************************
        Total Tasks Generated:              {final_rep_dict["total_tasks"]}
        Total Users Registered:             {final_rep_dict["total_users"]}
*********************************************************************************
        """)
        # - For each user in the nested dictionary, calculate the required values as it itterates through each task, i believe due to indentation, 
        # - it is rewriting the file with new values each itteration which may be unnessesary but i didnt want to mess with it
            for user in final_rep_dict["users"]:
                try:
                    user_overview_file.write(f""" 
*********************************************************************************
Total Tasks Asigned to {user}:                              {final_rep_dict["users"][user]["number_of_tasks"]}
Percentage of total tasks assigned to {user}:               {round((final_rep_dict["users"][user]["number_of_tasks"]/final_rep_dict["total_tasks"])*100)}
Percentage of tasks assigned to {user} that are complete:   {round((final_rep_dict["users"][user]["number_of_completed"]/final_rep_dict["users"][user]["number_of_tasks"])*100)}
Percentage of tasks assigned to {user} that are incomplete: {round((final_rep_dict["users"][user]["number_of_uncompleted"]/final_rep_dict["users"][user]["number_of_tasks"])*100)}
Percentage of tasks assigned to {user} that are overdue:    {round((final_rep_dict["users"][user]["number_of_overdue"]/final_rep_dict["users"][user]["number_of_tasks"])*100)}
*********************************************************************************
                    """)
                except ZeroDivisionError:
                    user_overview_file.write(f""" 
*********************************************************************************
Total Tasks Asigned to {user}:                              0
Percentage of total tasks assigned to {user}:               0
Percentage of tasks assigned to {user} that are complete:   0
Percentage of tasks assigned to {user} that are incomplete: 0
Percentage of tasks assigned to {user} that are overdue:    0
*********************************************************************************
""")
    print("The new reports have been generated.")

def display_statistics():
    # - Read the 2 files containing the reports and print them line by line
    with open("task_overview.txt", "r") as task_overview_file, open("user_overview.txt", "r") as user_overview_file:
        print("****************Report****************")
        for line in task_overview_file:
            print("Start of Task Overview Report:")
            print(line)
        for line in user_overview_file:
            print("Start of User Overview Report:")
            print(line)

# Create tasks.txt if it doesn't exist
if not os.path.exists("tasks.txt"):
    with open("tasks.txt", "w") as default_file:
        pass

with open("tasks.txt", 'r') as task_file:
    task_data = task_file.read().split("\n")
    task_data = [t for t in task_data if t != ""]


task_list = []
for t_str in task_data:
    curr_t = {}

    # Split by semicolon and manually add each component
    task_components = t_str.split(";")
    curr_t['username'] = task_components[0]
    curr_t['title'] = task_components[1]
    curr_t['description'] = task_components[2]
    curr_t['due_date'] = datetime.strptime(task_components[3], DATETIME_STRING_FORMAT)
    curr_t['assigned_date'] = datetime.strptime(task_components[4], DATETIME_STRING_FORMAT)
    curr_t['completed'] = True if task_components[5] == "Yes" else False

    task_list.append(curr_t)

#====Login Section====
'''This code reads usernames and password from the user.txt file to 
    allow a user to login.
'''
# If no user.txt file, write one with a default account
if not os.path.exists("user.txt"):
    with open("user.txt", "w") as default_file:
        default_file.write("admin;password")

# Read in user_data
with open("user.txt", 'r') as user_file:
    user_data = user_file.read().split("\n")

# Convert to a dictionary
username_password = {}
for user in user_data:
    username, password = user.split(';')
    username_password[username] = password

logged_in = False
while not logged_in:

    print("LOGIN")
    curr_user = input("Username: ")
    curr_pass = input("Password: ")
    if curr_user not in username_password.keys():
        print("User does not exist")
        continue
    elif username_password[curr_user] != curr_pass:
        print("Wrong password")
        continue
    else:
        print("Login Successful!")
        logged_in = True


while True:
    # presenting the menu to the user and 
    # making sure that the user input is converted to lower case.
    print()
    menu = input('''Select one of the following Options below:
r - Registering a user
a - Adding a task
va - View all tasks
vm - View my task
gr - Generate Reports
ds - Display statistics
e - Exit
: ''').lower()

    if menu == 'r':
        reg_user(username_password)
        '''Add a new user to the user.txt file'''  

    elif menu == 'a':
        add_task(username_password)
        '''Allow a user to add a new task to task.txt file
            Prompt a user for the following: 
             - A username of the person whom the task is assigned to,
             - A title of a task,
             - A description of the task and 
             - the due date of the task.'''

    elif menu == 'va':
        view_all_tasks(task_list)
        '''Reads the task from task.txt file and prints to the console in the 
           format of Output 2 presented in the task pdf (i.e. includes spacing
           and labelling) 
        '''

    elif menu == 'vm':
        view_my_tasks()
        '''Reads the task from task.txt file and prints to the console in the 
           format of Output 2 presented in the task pdf (i.e. includes spacing
           and labelling)
        '''
    
    elif menu == 'ds' and curr_user == 'admin': 
        '''If the user is an admin they can display statistics about number of users
            and tasks.'''
        display_statistics()

    elif menu == "gr" and curr_user == "admin":
        # - Create files if they do not exist and then call the 2 functions for writing the overviews to the files
        if not os.path.exists("task_overview.txt"):
            with open("task_overview.txt", "w") as to_file:
                to_file.write("")   
        if not os.path.exists("user_overview.txt"):
            with open("user_overview.txt", "w") as uo_file:
                uo_file.write("")      
        task_overview(task_list,username_password)
        user_overview(task_list,username_password)

    elif menu == 'e':
        print('Goodbye!!!')
        exit()

    else:
        print("You have made a wrong choice, Please Try again")