#Making updates to the rudimentary student database system from project 1 that include
#logging in, registering, exiting in the new main menu, adding new student details
#to student information pages and a new sql database system to house
#student files. this is the file that houses the main program and imports from the other program files.

#importing any modules we may need
import re  #we need this module for the pattern recognition
import os #importing os for reading json file
import json  #we need this module to have all student records saved in the json file
import mysql.connector #importing mysqlconnector to connect with the database files
from BasicOperationsFunctionsforProject import * #importing all functions from the basic ops program file
from StudentManagementFunctionsforProject import * #importing all functions from the student management functions file

#Defining the main function (the "start" function as labeled in the project directions)
def main():
    while True: #while this is all true, this will appear on the screen as the main welcome screen
        #in a while loop because we want this to keep looping back to after certain functions
        openReadWelcome() #calling the readwelcome function that defines the
        #function that reads and displays the welcome text from a .txt file

        openOperationCode = input(f"\nPlease select (1 - 3): ").strip() #making sure to strip of anything else
        #so this can be read as a string
        #the user selects 1 of the 3 options (login, register, exit)

        openCusInput(openOperationCode) #calling the customer input function that will run the
        #user input for the entire main menu

######################################################################################

#Invoking the main function so that the program will run
main()