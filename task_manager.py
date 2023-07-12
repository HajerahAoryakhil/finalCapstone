# Notes:
# 1. Use the following username and password to access the admin rights
# username: admin
# password: password
# 2. Ensure you open the whole folder for this task in VS Code otherwise the
# program will look in your root directory for the text files.

# =====importing libraries===========
import os
from datetime import datetime, date

# Creating a reg_user function 
def reg_user():
    '''Add a new user to the user.txt file'''
    # - Request input of a new username

    if curr_user == 'admin':   # only admin will be able to register a user 
        new_username = input("New Username: ")
        if new_username not in username_password:  
            print("Valid username.")
        else:
            print('Error, username already exists')
            return

            # - Request input of a new password
        new_password = input("New Password: ")

        # - Request input of password confirmation.
        confirm_password = input("Confirm Password: ")

        # - Check if the new password and confirmed password are the same.
        if new_password == confirm_password:
            # - If they are the same, add them to the user.txt file,
            print("New user added")
            username_password[new_username] = new_password

            try:  #using try-except for file not found error handling
            # writitng to user.txt file to update the username and password log in
                with open("user.txt", "w") as out_file:
                    user_data = []
                    for k in username_password:
                        user_data.append(f"{k};{username_password[k]}")
                    out_file.write("\n".join(user_data))
            except FileNotFoundError:
                print("File not found.")

            # - Otherwise you present a relevant message.
        else:
            print("Passwords do no match, Please try again")

    else:
        print("Only admin can add users")

# creating an add_task functions
def add_task():
    '''Allow a user to add a new task to task.txt file
            Prompt a user for the following:
            - A username of the person whom the task is assigned to,
            - A title of a task,
            - A description of the task and
            - the due date of the task.'''

    task_username = input("Name of person assigned to task: ")
    while task_username not in username_password.keys():
        task_username = input("User does not exist. Please enter a valid username or enter '-1' to return to main menu: ")  # ---------this doesnt work
        if task_username == '-1':
            return False

    task_title = input("Title of Task: ")
    task_description = input("Description of Task: ")
    while True:
        # using try-except for value error handling
        try: 
            task_due_date = input("Due date of task (YYYY-MM-DD): ")
            due_date_time = datetime.strptime(task_due_date, DATETIME_STRING_FORMAT)
            break

        except ValueError:
            print("Invalid datetime format. Please use the format specified. eg. 2023-07-01")

    # Then get the current date.
    curr_date = date.today()
    ''' Add the data to the file task.txt and
        Include 'No' to indicate if the task is complete.'''
    # dictionary for the new task created by user
    new_task = {
        "username": task_username,
        "title": task_title,
        "description": task_description,
        "due_date": due_date_time,
        "assigned_date": curr_date,
        "completed": 'No'
    }

    task_list.append(new_task)
    #Writing it to update tasks.txt file
    with open("tasks.txt", "w") as task_file:
        task_list_to_write = []
        for task in task_list:
            str_attrs = [
                task['username'],
                task['title'],
                task['description'],
                task['due_date'].strftime(DATETIME_STRING_FORMAT),
                task['assigned_date'].strftime(DATETIME_STRING_FORMAT),
                task['completed']
            ]
            task_list_to_write.append(";".join(str_attrs))
        task_file.write("\n".join(task_list_to_write))
    print("Task successfully added.")


# creating a view_all function
def view_all():
    '''Reads the task from task.txt file and prints to the console in the
            format of Output 2 presented in the task pdf (i.e. includes spacing
            and labelling)
            '''

    for task in task_list:
        disp_str = f"Task: \t\t {task['title']}\n"
        disp_str += f"Assigned to: \t {task['username']}\n"
        disp_str += f"Date Assigned: \t {task['assigned_date'].strftime(DATETIME_STRING_FORMAT)}\n"
        disp_str += f"Due Date: \t {task['due_date'].strftime(DATETIME_STRING_FORMAT)}\n"
        disp_str += f"Task Description: \n {task['description']}\n"
        print(disp_str)

# creating a view_mine function
def view_mine():
    '''Reads the task from task.txt file and prints to the console in the
        format of Output 2 presented in the task pdf (i.e. includes spacing
        and labelling)
        '''
    user_count = 0  # count current user's tasks
    task_dict = {} # creating a new dictonary to append new task information    
    write_str = ""
    for task in task_list:
        user_count += 1 
        task_dict[user_count] = task
        if task['username'] == curr_user:
            print(f"Task No. ({user_count})\n")
            disp_str = f"Task: \t\t {task['title']}\n"
            disp_str += f"Assigned to: \t {task['username']}\n"
            disp_str += f"Date Assigned: \t {task['assigned_date'].strftime(DATETIME_STRING_FORMAT)}\n"
            disp_str += f"Due Date: \t {task['due_date'].strftime(DATETIME_STRING_FORMAT)}\n"
            disp_str += f"Task Description: \n {task['description']}\n"
            print(disp_str)
    
    user_task_choice = ''
    while True:
        # getting users input to choose task they want or -1 to return to main menu
        user_task_choice = int(input("Please select the task you want, or enter -1 return to the main menu: ")) 
        if user_task_choice not in task_dict and user_task_choice != -1:
            continue

        elif user_task_choice == -1:
            return False
        
        else:
            user_choice = ''
            chosen_task = task_dict[user_task_choice]
            while user_choice != 'a' and user_choice != 'b':
                #getting user input to wither mark chosen task as completed or to edit task
                user_choice = input("Please select either (a) - mark as complete or (b) - edit task: ").lower()

                if user_choice == 'a':
                    #if chosen mark as completed
                    chosen_task['completed'] = "Yes"  #updating task_dict 
                    task_dict[user_task_choice] = chosen_task
                    print(f"Task {user_task_choice} is marked as completed!")
                    #writing into tasks.txt and updating information
                    for task in task_dict.values():  # updating the values in the dictionary not the key
                        write_str += f"{task['username']};{task['title']};{task['description']};{task['due_date'].strftime(DATETIME_STRING_FORMAT)};{task['assigned_date'].strftime(DATETIME_STRING_FORMAT)};{task['completed']}\n"
                    with open('tasks.txt', 'w') as task_file:
                        task_file.write(write_str)  
                        return menu()
                elif user_choice == 'b':
                    #if chosen to edit the selected task
                    if chosen_task['completed'] == 'No':  # making sure task in not marked as complete so its able to edit.
                        # getting users input to edit chosen task -- either to change who its assigned to or change the due date
                        edit_choice = input('Enter (1) - edit who the task is assigned to or (2) - edit the due date:\n ')
                        
                        if edit_choice == '1':
                            # if chosen to change the assignee get input to whom they want to change it too
                            new_assignee = input('Which user would you like to assign this task too?')
                            if new_assignee in username_password:  # checking if the username they want to assign it to exist
                                    task_dict[user_task_choice]['username'] = new_assignee # updating new_assignee to task_dict
                                    
                                    #writing into the tasks.txt file and updating the given information with .write so it doesnt overwrite
                                    for task in task_dict.values():
                                        write_str += f"{task['username']};{task['title']};{task['description']};{task['due_date'].strftime(DATETIME_STRING_FORMAT)};{task['assigned_date'].strftime(DATETIME_STRING_FORMAT)};{task['completed']}\n"
                                    with open('tasks.txt','w') as task_file:
                                        task_file.write(write_str)
                                        print(f"Task {user_task_choice} is successfully assigned to another user.")
                                        return menu()

                        elif edit_choice == '2':
                            #if chosen to edit the due date for the selected task
                            while True:
                                #using try-except for value error handling
                                try:
                                    #getting input from user for new due date.
                                    new_due_date = input("Due date of task (YYYY-MM-DD: ) ")
                                    new_due_date = datetime.strptime(new_due_date, DATETIME_STRING_FORMAT)
                                    task_dict[user_task_choice]['due_date'] = new_due_date
                                    
                                    #writing into tasks.txt and updating the given information
                                    for task in task_dict.values():
                                        write_str += f"{task['username']};{task['title']};{task['description']};{task['due_date'].strftime(DATETIME_STRING_FORMAT)};{task['assigned_date'].strftime(DATETIME_STRING_FORMAT)};{task['completed']}\n"
                                    with open('tasks.txt','w') as task_file:
                                        task_file.write(write_str)
                                        print(f"Task {user_task_choice} due date is successfully updated.")
                                        return menu()
                                        
                                except ValueError:
                                    print("Invalid datetime format. Please use the format specified")

                    else:
                        print("Task selected is already marked as complete and cannot be edited, please select another task.")

#creating a generate_task_overview function
def generate_task_overview():
    #the amount/length in the task list is the total task for all users
    num_task_total = len(task_list)
    #assigning variables to 0 to update everytime the for-loop is iterating 
    completed_task = 0
    uncompleted_task = 0
    over_due_task = 0
    #using for loop to update counter
    for task in task_list:
        if task['completed'] == 'Yes':     #if task is completed update the complete task counter
            completed_task += 1
        else:
            uncompleted_task += 1          # else if its uncomplete then update the uncompleted task counter

            if task['due_date'] < datetime.now():    #checking if the given duedate is older than current date, 
                over_due_task += 1                   #if so updates the over due date counter

    #calculating the percentages for incompleted task and overdue task by dividing it by the total of task number and times it by 100
    perc_incomp = round((uncompleted_task / num_task_total) * 100, 2)  # and rounded it up to 2 decimal places
    perc_overdue = round((over_due_task / num_task_total) * 100, 2)

    #writing eveything to a new text file called task_overview
    #entering them in new lines so its easier to read and user friendly
    with open('task_overview.txt', 'w') as file:
        if num_task_total != 0:
            file.write("------------------------------------------------------------------------------------------- \n")
            file.write("Task Overview \n")
            file.write(f"Total number of task(s): \t{num_task_total}\n")
            file.write(f"Total number of completed task(s): \t{completed_task}\n")
            file.write(f"Total number of uncompleted task(s): \t{uncompleted_task}\n")
            file.write(f"Total number of overdue task(s): \t{over_due_task}\n")
            file.write(f"Total percentage of uncompleted task(s): \t{perc_incomp}%\n")
            file.write(f"Total percentage of overdue task(s): \t{perc_overdue}%\n")
            file.write("------------------------------------------------------------------------------------------- \n")
            

        else:
            file.write("------------------------------------------------------------------------------------------- \n")
            file.write("Task Overview \n")
            file.write("Currently there are no existing task(s)")
            file.write("------------------------------------------------------------------------------------------- \n")

#creating a generate_user_overview function
def generate_user_overview():
    #setting 2 variables for lengthn of user registered and length of tasks added
    all_user_total = len(user_data)
    num_task_total = len(task_list)
    #writing eveything to a new text file called user_overview      
    with open('user_overview.txt', 'w') as file:
        if all_user_total != 0:
            file.write("------------------------------------------------------------------------------------------- \n")
            file.write("User Overview \n")
            file.write(f"Total number of user(s) registered: \t{all_user_total}\n")
            file.write(f"Total number of task(s): \t{num_task_total}\n")
            file.write("------------------------------------------------------------------------------------------- \n")

            #creating a for loop to loop through all the user and create a file info log for each user
            for username in username_password:
                file.write(f"User: {username}\n")
                #setting variable as counters so once for loops runs it +1 each time it iterates.
                user_completed_task = 0
                user_uncompleted_task = 0
                user_over_due_task = 0
                user_total_task = 0

                #using a for loop to update counters
                for task in task_list:
                    if task['username'] == username:  # for each username if username matches in the task list
                        user_total_task += 1          # updates counter for amount user has task in tasklist
                        if task['completed'] == 'Yes': 
                            user_completed_task += 1   #if task is completed update the complete task counter
                        else:
                            user_uncompleted_task += 1  # else if its uncomplete then update the uncompleted task counter

                        if task['due_date'] < datetime.now():   #checking if the given duedate is older than current date, 
                            user_over_due_task += 1              #if so updates the over due date counter
                #calculating the percentage for each user's task-assigned, incompleted, completed, overdue, tasks.
                perc_user_incomp = round((user_uncompleted_task / num_task_total) * 100, 2) # by dividing it by the total of task number and times it by 100
                perc_user_overdue = round((user_over_due_task / num_task_total) * 100, 2)  #and rounded it up to 2 decimal places
                perc_user_comp = round((user_completed_task / num_task_total) * 100, 2)
                perc_user_task = round((user_total_task / num_task_total) * 100, 2)


                #entering them in new lines so its easier to read and user friendly
                file.write(f"Total number of task(s) assigned to this user: \t{user_total_task}\n")
                file.write(f"Total number of completed task(s) assigned to this user: \t{user_completed_task}\n")
                file.write(f"Total number of incompleted task(s) assigned to this user: \t{user_uncompleted_task}\n")
                file.write(f"Total number of overdue task(s) assigned to this user: \t{user_over_due_task}\n")
                file.write(f"Total percentage of task(s) assigned to this user: \t{perc_user_task}%\n")
                file.write(f"Total percentage of completed task(s) assigned to this user: \t{perc_user_comp}%\n")
                file.write(f"Total percentage of incompleted task(s) assigned to this user: \t{perc_user_incomp}%\n")
                file.write(f"Total percentage of overdue task(s) assigned to this user: \t{perc_user_overdue}%\n")
                file.write("------------------------------------------------------------------------------------------- \n")
        else:
            file.write("------------------------------------------------------------------------------------------- \n")
            file.write("User Overview \n")
            file.write("Currently there are no existing user's overview(s)")
            file.write("------------------------------------------------------------------------------------------- \n")
                

# ======================================

DATETIME_STRING_FORMAT = "%Y-%m-%d"

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
    curr_t['completed'] = task_components[5]

    task_list.append(curr_t)
# ====Login Section====
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


def menu():

    menu = " "
    while menu != "e":     #another way of while True
        #admin main menu options
        if curr_user == 'admin':

        # presenting the menu to the user and
        # making sure that the user input is converted to lower case.
            print()
            menu = input('''Select one of the following Options below:
    r - Registering a user
    a - Adding a task
    va - View all tasks
    vm - View my task
    gr - Generate reports
    ds - Display statistics
    e - Exit
    : ''').lower()
        else:
            #other user who is not admin main menu options
            menu = input('''Select one of the following Options below:
    a - Adding a task
    va - View all tasks
    vm - View my task
    e - Exit
    : ''').lower()

        if menu == 'r':
            reg_user()   #calling the reg_user function

        elif menu == 'a':
            add_task()   #calling the add_task function

        elif menu == 'va':
            view_all()   #calling the view_all function

        elif menu == 'vm':
            view_mine()  #calling the view_mine function

        elif menu == 'gr':
            generate_task_overview()  #calling both user and task generate overview function
            generate_user_overview()

        elif menu == 'ds' and curr_user == 'admin':
            generate_task_overview()
            generate_user_overview()
            with open("task_overview.txt", "r") as overview_file:  #calling the task_overview file as read so it can be displayed to admin
                print(overview_file.read())

            with open("user_overview.txt", "r") as overview_file:  #calling the user_overview file as read so it can be displayed to admin
                print(overview_file.read())

            '''If the user is an admin they can display statistics about number of users
                and tasks.'''
            num_users = len(username_password.keys())
            num_tasks = len(task_list)

            print("-----------------------------------")
            print(f"Number of users: \t\t {num_users}")
            print(f"Number of tasks: \t\t {num_tasks}")
            print("-----------------------------------")

        elif menu == 'e':
            print('Goodbye!!!')
            exit()

        else:
            print("You have made a wrong choice, Please Try again")

menu()