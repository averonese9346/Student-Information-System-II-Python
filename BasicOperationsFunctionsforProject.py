#Description: This is where the basic operation functions for the student management
#system program are stored. per the project directions these needed to be stored in
#separate files.

import mysql.connector #importing mysqlconnector to connect with the database files
import re #we need this module for the pattern recognition
import os #importing os for reading json file
import json #importing json to read whatever we have stored in json files for the program
import hashlib #importing hashlib for the password hashing
from StudentManagementFunctionsforProject import * #importing all files from the other
#project file just in case something is called there and needed

##############################PROGRAM FUNCTIONS - BASIC OPS################################################
def connectDB():  #defining the connection function that actually connects to the sql database with my unique information
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="melkor22",
        database="student_records"
    )
######################################################################################
def openReadWelcome(): #defining the readwelcome function that shows the welcome text from the .txt file
    try:
        with open("userWelcomeV2.txt", "r", encoding='utf-8') as openWelcomeText:  #naming the
            #name of the file, set to read, and setting the encoding so it displays properly
            text = openWelcomeText.read() #setting a new variable with our text and the readwelcome function
            #printing the results #using try and exception block to read with json formatting, it is
            #from a json file that this is being read.
            print(text, end = ' ')
    except FileNotFoundError:
        print("Welcome file not found. Please ensure 'userWelcomeV2.txt' exists.")
##############################################################################################################
def openCusInput(openOperationCode): #this is the customer input function that will take
    #any of the inputs the customer gives from the main menu and sends them
    #to the correct function from that menu option
    if openOperationCode == '1':    #if statements for each operation code making sure to use '' with the number so that
        #is read as a string and not as a literal integer
        logIn()  #then showing the function that is being called after the user inputs
        #the number choice selection, the login function will allow the user to login
    elif openOperationCode == '2':
        regUser()  #register function will allow user to register a username and password
    elif openOperationCode == '3':
        exitSystem() #exit system function will completely exit the system
    else:
        print("\u274C Please enter a valid operation code, 1 - 3.") #unicode for x to state that
        #this is invalid message please enter a different operation code
        #and it will loop back to show the main menu
##############################################################################################################
#defining the exit system function, used to exit the system altogether.
def exitSystem():
    while True: #while loop to make sure that if the user enters something other than
        #yes or no they will be asked again (else)
        exitConfirmation = input("Do you Want to Exit the System? Enter Y or N: ").strip().upper()
        #exitconfirmation is the user telling the program whether or not they want to exit
        #with stripping the white space and making sure that if the user inputs either
        #upper or lower case it will still work
        if exitConfirmation == 'Y':
            exit()  #if the user wants to exit they can press Y to exit and exit() will stop the program
        if exitConfirmation == 'N':  #if the user says no it will return to the main menu
            return
        else:  #if the user enters anything else it will make the user enter a valid option
            print(f"\u274C That is not a valid option. Please select Y or N.")
##############################################################################################################
def regUser(): #the register user function being defined here.
    #after pressing the button for registration the user is given the rules for the account name. the rest
    #is built into the username/account name function
    print(f"======================Registration======================\n" 
          "\t \u2666 1. Account name is between 3 and 6 letters long\n"
          "\t \u2666 2. Account name's first letter must be capitalized\n")

    usernameCheck() #calling the usernamecheck function to begin the registration process with username, acctname
##############################################################################################################
def usernameCheck(): #defining the username check function
    while True: #creating a while loop so that we loop back if the acctname is not following paramters
        conn = connectDB() #this is to open the connection for the database
        cursor = conn.cursor() #cursor is the argument to pass through to connect to database

        acctName = input("Please Enter Account Name: ").strip()  #user enters acct name

#below is the execute operation for the database argument to actually save the
#username to the passwords table in the sql database
        cursor.execute(""" 
            SELECT p.username FROM passwords p WHERE p.username = %s
        """, (acctName,))

        result = cursor.fetchone()  #gathering the result and checking the acctname to make sure
        #it isnt already in use

#these are the parameters and rules given to the user for acct name.
        #if the acct bname does pass it will continue
        #if the username is already taken (result) the error message will show.
        if len(acctName) >= 3 and len(acctName) <= 6 and (acctName[0]).isupper():
            if result:
                print(f"\u274C '{acctName}' is already taken. Please choose a different account name.")
                cursor.close() #closing db connection for this if statement
                conn.close()
                continue #if username is okay we move into password check.

            password = passwordCheck() #calling the password check function to check password creation
            #per parameters

            cursor.execute("INSERT INTO passwords (username, password) VALUES (%s, %s)",
                           (acctName, password))  # Insert the username and hashed password into the database
            conn.commit() #committing the change (no rollbacks)

            print("\u2714 Registration completed!")  #if all is good the success message will print
            #if everything is saved and good

            cursor.close() #closing the database connection
            conn.close()
            return

#elif statements for the username parameters in case the user tries an account name that
        #does not follow instructions. each will print the unique error message.
        elif len(acctName) < 3:
            print(f"\u274C This username is too short. Please enter another account name that is between 3 and 6 characters long.")
        elif len(acctName) > 6:
            print(f"\u274C This username is too long. Please enter another account name that is between 3 and 6 characters long.")
        elif (acctName[0]).islower():
            print(f"\u274C The username needs to begin with an uppercase letter. Please enter another account name that has a capitalized first letter.")
######################################################################################
def passwordCheck(): #defining the password check function.
    specialChars = ['!', '@', '#', '$', '%', '^', '&', '*'] #defining the special characters
    #in a list that the user is allowed to use in their password per project instructions.

#creating a while loop so that the user can be looped back if something is not correct.
    while True: #printing the password instruction parameters for the user.
        print(f"\n ====================================PASSWORD CREATION====================================\n"
            f"\t \u2666 1. Password must start with one of the following special characters: !@#$%^&*\n"
            f"\t \u2666 2. Password must contain at least one digit, one lowercase letter and one uppercase letter\n"
            f"\t \u2666 3. Password is between 6 and 12 letters long")
        password = input("Please enter your password: ").strip() #the password the user enters here.
        #stripping of anything they may have added.

        if len(password) == 0: #ensuring that the user does not enter an empty password.
            print(f"\u274C Password cannot be empty. Please enter a valid password.")
            continue
        if (password[0] in specialChars and  #an if statement to show that if the password
        #follows all of these given parameters it is good and will hash the password
                len(password) >= 6 and len(password) <= 12 and
                any(char.isdigit() for char in password) and
                any(char.isupper() for char in password) and
                any(char.islower() for char in password)):

#creating the instructions to hash the password.
            hashedPassword = hashlib.md5(password.encode()).hexdigest()
            return hashedPassword #returning hashed password instead of regular password
        #input that the user gives as that is not safe.

#elif statements for all of the things that could go wrong here if the user does not follow the given parameters.
        elif (password[0]) not in specialChars:
            print(f"\u274C This password is not valid. Please enter a password that begins with one of the following special characters: !@#$%^&*")
        elif len(password) < 6:
            print(f"\u274C This password is too short. Please enter a password that is between 6 - 12 characters long.")
        elif len(password) > 12:
            print(f"\u274C This password is too long. Please enter a password that is between 6 - 12 characters long.")
        elif not any(char.isdigit() for char in password):
            print(f"\u274C The password should have at least one digit. Please enter a password with at least one digit betweeen 0 - 9.")
        elif not any(char.islower() for char in password):
            print(f"\u274C The password should have at least one lowercase letter. Please enter a password with at least one lowercase letter.")
        elif not any(char.isupper() for char in password):
            print(f"\u274C The password should have at least one uppercase letter. Please enter a password with at least one uppercase letter.")
######################################################################################
def logIn(): #defining the login function.
    while True:
        print(f"======================Login======================") #this prints for the title.
        userAcctName = input("Please Enter Your Account: ") #prompting the user to enter their acct for login

        conn = connectDB() #opening the database connection.
        cursor = conn.cursor()
        cursor.execute("""
            SELECT p.password FROM passwords p WHERE p.username = %s
        """, (userAcctName,))
        #the execute block is here to find the password and username for what the user entered

        result = cursor.fetchone() #result is what is found in the database

        if not result: #if the acctname is found in the databse then all is good and logs in and moves to password
            #if not in result then it is not a valid acct name because it is not in the system.
            print(f"\u274C '{userAcctName}' is not a valid account name. Please enter a valid account name.")
            cursor.close()
            conn.close() #closing the connection to the database
            continue

        storedPassword = result[0] #the stored password should be the first result in result

        while True:  #while loop to enter the password after entering the
            #username
            userPassword = input("Please Enter Your Password: ")
            hashedPassword = hashlib.md5(userPassword.encode()).hexdigest()  #Hash entered password
            #after users enters the password

            if storedPassword == hashedPassword: #if the sotredpassword is the same as the hashed password
                #that the user entered then they can login and success message is printed
                print("\u2714 Login successful!")
                cursor.close() #closing connection
                conn.close()
                openSecondWelcome(userAcctName) #calling the welcome screen to show that when user
                #logs in properly
                return
#error message prints if user does not enter correct password
            print(f"\u274C That is not the correct password. Please enter a valid password to continue.")
######################################################################################
def openSecondWelcome(userAcctName): #defining the readwelcome function that shows the welcome text from the .txt file
    while True: #while loop to loop back here from returns
        #personalized welcome menu so that the user can see their name when they login
        print(f"================================================================\n"
                  f"\t \t \u273d\u273d\u273d Welcome {userAcctName} \u273d\u273d\u273d \n"
                "\t to the Student Management System\n"

             "\t \u25c6 1. Add a student\n"
             "\t \u25c6 2. Show a student\n"
             "\t \u25c6 3. Modify a student\n"
             "\t \u25c6 4. Delete a student\n"
             "\t \u25c6 5. Query student scores\n"
             "\t \u25c6 6. Return to the previous menu\n"
        "================================================================")

        operationCode = input(f"\nPlease select (1 - 6): ").strip() #making sure to strip of anything else
        #so this can be read as a string

        cusInput(operationCode) #calling the customer input function that will run the
        #user input for the entire program
######################################################################################
def cusInput(operationCode): #this is the customer input for each menu item selection
    if operationCode == '1':
        addUser() #calling the adduser function
    elif operationCode == '2':
        displayUser() #calling the display user function
    elif operationCode == '3':
        modifyUser() #calling the modify user function
    elif operationCode == '4':
        delUser() #calling the delete user function
    elif operationCode == '5':
        queryScores() #calling the query scores function
    elif operationCode == '6':
        main() #calling main to go back to the main menu
######################################################################################
def main():
    while True: #while this is all true, this will appear on the screen as the main welcome screen
        #in a while loop because we want this to keep looping back to after certain functions
        openReadWelcome() #calling the readwelcome function (below) that defines the
        #function that reads and displays the welcome text from a .txt file

        openOperationCode = input(f"\nPlease select (1 - 3): ").strip() #making sure to strip of anything else
        #so this can be read as a string

        openCusInput(openOperationCode) #calling the customer input function that will run the
        #user input for the entire main menu
