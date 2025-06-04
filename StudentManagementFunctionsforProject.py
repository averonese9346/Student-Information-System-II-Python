#Description: This is where the student management functions for the student management
#system program are stored. per the project directions these needed to be stored in
#separate files.

import mysql.connector #importing mysqlconnector to connect with the database files
import re #we need this module for the pattern recognition
import os #importing os for reading json file
import hashlib #importing hashlib for the password hashing
import json #importing json to read whatever we have stored in json files for the program
from BasicOperationsFunctionsforProject import *  #importing all files from the other
#project file just in case something is called there and needed

##############################PROGRAM FUNCTIONS - BASIC OPS################################################
def connectDB(): #defining the connection function that actually connects to the sql database with my unique information
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="melkor22",
        database="student_records"
    )
######################################################################################
def displayUser(): #defining the display user function. this will prompt users to display
    #students in several different ways
    conn = connectDB() #opening the connection to the database
    cursor = conn.cursor()

#while loop to ensure we keep going here if something is incorrect
    while True:
        cursor.execute("SELECT COUNT(*) FROM students") #the execute function to begin iterating through
        #the student database
        student_count = cursor.fetchone()[0] #passing through this argument and finding the
        #correct student

        if student_count == 0: #if there are no students in the database then this error message
            #will print and the connectionw ill close
            print(f"\u274C No existing students to display.")
            cursor.close()
            conn.close()
            return

#this is the general menu that will print when the user picks display user function.
        #users will pick one of these and those functions are called below.
        print(f"======================Show Student======================\n"
              "\t \u25c6 1. Show All Students\n"
              "\t \u25c6 2. Show Students by Name\n"
              "\t \u25c6 3. Show Students by ID\n"
              "\t \u25c6 Other: Return")
        operationCode = input("Please Select 1-3: ").strip() #again using the operation code function

        if operationCode == '1':
            displayAll(cursor) #passing through the argument cursor that connects to the database, calling the display all function
            return #return to the secondmain menu
        elif operationCode == '2':
            displayByName(cursor) #passing through the argument cursor that connects to the database, calling the display by name function
            return #return to the secondmain menu
        elif operationCode == '3':
            displayByID(cursor) #passing through the argument cursor that connects to the database, calling the display by id function
            return #return to the secondmain menu
        else:
            return #return to the secondmain menu

    cursor.close() #closing the database connection
    conn.close()
######################################################################################
def addUser(): #defining the adduser function to add a new student to the system.
    conn = connectDB() #opening the database connection.
    cursor = conn.cursor()

    print("======================Add Student======================\n"  #showing the rules first
          "1. The first letter of firstname and lastname must be capitalized.\n"
          "2. Firstname and lastname must each have at least two letters.\n"
          "3. No digit allowed in the name.\n"
          "4. Age must be betwen 0 and 100.\n"
          "5. Gender can be M (Male), F (Female), or O (Other)\n"
          "6. Phone must be in the (xxx-xxx-xxxx) format.")

    studentName = getStudentName()  # making sure to call all of our functions that will be used
    #to set the student information
    age = getStudentAge()
    gender = getStudentGender()
    studentMajor = getStudentMajor()
    phoneNumber = getPhoneNumber()

#try and except block to connect to database
    try:
        #Insert new student record into the MySQL database with the try block and saving the record
        cursor.execute("""
            INSERT INTO students (name, age, gender, major, phone) 
            VALUES (%s, %s, %s, %s, %s)
        """, (studentName, age, gender, studentMajor, phoneNumber))

        conn.commit()  #Save the changes (no rollback)
        print(f"\u2714 New student record has been added successfully!") #print success message if all works

    except Exception as e:
        print(f"\u274C Error adding student: {e}") #error message will print if except is hit
        conn.rollback()  #Rollback if an error occurs

    finally:
        cursor.close() #close connection
        conn.close()

    continueMenu() #go back to the secondmain menu
######################################################################################
def getStudentName(): #defining the getstudent name function which checks the student name
    #to make sure it fits parameters.
    while True: #while loop to ensure we keep getting looped back if something doesnt work out
        studentName = input("Please Enter the Student Name (Firstname Lastname): ").strip()
        #prompting user to enter the name
        if re.fullmatch(r"[A-Z][a-zA-Z]{1,} [A-Z][a-zA-Z]{1,}", studentName): #this means that we can only
            #have a name that starts with a uppercase letter and then either an upper or lower
            #case after that and it needs at least one other digit
            #both of these rules apply to first and last name
            return studentName
        else:
            print(f"\u274C {studentName} is an invalid name.") #if it doesnt fit parameters error message will print
######################################################################################
def getPhoneNumber(): #defining the getphone number function.
    while True: #we keep looping back if something isnt working
        #using pattern recongition to ensure the phone number is valid and follows the pattern for phone numbers
        #prompting user to enter phone number
        phoneNumber = input("Please Enter the Student Phone \u260E: ").strip() #added the unicode for phone icon per directions
        if re.fullmatch(r"\d{3}-\d{3}-\d{4}", phoneNumber): #pattern here is
            #3 digits, - , 3 digits, - , 4 digits
            return phoneNumber
        else: #if it is anything other than above it is invalid
            print(f"\u274C {phoneNumber} is an invalid phone number.")
######################################################################################
def getStudentMajor(): #defining the get studentmajor function
    while True:  #while loop bc although while this project does not have parameters on major
        #there would be in a real scenario
        studentMajor = input("Please Enter the Student Major: ").strip() #prompting user
        #to input the student major
        studentMajor = studentMajor.upper() #we need to make sure that even if the user
        #inputs a lowercase major it is saved properly in the database
        return studentMajor
######################################################################################
def getStudentAge(): #defining the get student age function
    while True: #while loop in case the user enters an invalid age so it keeps getting looped back
        age = int(input("Please Enter Student's Age: ")) #prompting the user to enter student age
        if age >= 0 and age <= 100: #student age parameters
            return age #return age if it fits in parameters
        else: #else if the user enters in invalid age
            print(f"\u274C {age} is an age. Please add an age between 0 - 100.")
######################################################################################
def getStudentGender(): #defining the get student gender function.
    while True: #while loop in case the parameters does not fit one of the 3 allowed genders
        gender = input("Please Enter Student's Gender: ").strip().upper() #making sure to save it in uppercase
        if gender == 'M' or gender == 'F' or gender == 'O':
            return gender
        else: #if anything other than the 3 choices this error message will print.
            print(f"{gender} is not a valid gender. Please enter 'M' for male, 'F' for female, or 'O' for other.")
######################################################################################
#defining the display all students user function
def displayAll(cursor): #passing through the argument cursor to connect to database
    cursor.execute("SELECT ID, Name, Age, Gender, Major, Phone FROM students") #execute function
    #to iterate through the database
    students = cursor.fetchall() #students is what is found from the database execute above
#printing the titles with proper formatting for alignment
    print("==================================Student Record==================================")
    print(f"{'ID':<18} {'Name':<18} {'Age':<8} {'Gender':<10} {'Major':<11} {'\u260E'}")
#if there are no students this error message will print
    if not students:
        print("\u274C No existing students to display.")
    else: #if anything else other than no students we will print thei information as per below
        for student in students:
            studentID, name, age, gender, major, phone = student  #unpacking the tuple from the database
            print(f"{studentID:<18} {name:<18} {age:<8} {gender:<10} {major:<11} {phone}") #also ensuring proper formatting

    cursor.close() #connection closed
    return #returns back to secondmain menu
######################################################################################
def displayByName(cursor): #defining display by name function
    conn = connectDB() #opening database connection
    cursor = conn.cursor()

#while loop to ensure we get looped back if something is incorrect
    while True:
        studentName = input("Please Enter Student Name to Display: ") #prompting user to enter name to display
        #the execute function searches through the database to find requested information
        cursor.execute("SELECT id, name, age, gender, major, phone FROM students WHERE name = %s", (studentName,))
        matchedStudents = cursor.fetchall()  #storing the found information
#if the name is found in students then display the title
        if matchedStudents:
            print("==================================Student Record==================================")
            print(f"{"ID":<18} {"Name":<18} {"Age":<8}{"Gender":<10}{"Major":<11}{"\u260E"}")
            # if the name is found in students then display the requested student information
            for student in matchedStudents:
                studentID, name, age, gender, major, phone = student  #unpacking the tuple from the database
                print(f"{studentID:<18} {name:<18} {age:<8} {gender:<8} {major:<10} {phone}") #also ensuring proper formatting

            return #return to secondmain menu

#if the name is not found then state that this student is not an existing student.
        else:
            print("=====================================Student Record====================================")
            print(f"\u274C {studentName} is not an exisiting student. Please enter a valid student name to continue.")
            print("=======================================================================================")
            continue

    cursor.close() #close connection
    conn.close()
    return #return to secondmain menu
######################################################################################
def displayByID(cursor): #defining display by id function
    conn = connectDB() #opening database connection
    cursor = conn.cursor()
    # while loop to ensure we get looped back if something is incorrect
    while True:
        studentID = input( #prompting user to input the id to display
            "Please enter the student ID to display: ").strip()  # stripping of any thing the user might have added

        if not re.fullmatch(r"7003\d{5}", studentID):  # if it is not a full match to
            # match our pattern of a valid student id then we tell the user this is an
            # invalid id and go back to the main menu, error message prints
            print("======================Student Record=====================")
            print(f"\u274C {studentID} is an invalid Student ID.")
            print("=========================================================")
            continue

#the execute block to find the student in the database
        cursor.execute("SELECT id, name, age, gender, major, phone FROM students WHERE id = %s", (int(studentID),))
        student = cursor.fetchone()
#if the student is found then print the title
        if student:
            print("==================================Student Record==================================")
            print(f"{"ID":<18} {"Name":<18} {"Age":<8}{"Gender":<10}{"Major":<11}{"\u260E"}")
            # if the student is found then print the student requested information
            studentID, name, age, gender, major, phone = student
            print(f"{studentID:<18} {name:<18} {age:<8} {gender:<8} {major:<10} {phone}")
            return  # ✅ Exits after displaying the student

        else: #if anything else then the student id does not exist and is not in the system
            print("======================Student Record=====================")
            print(f"\u274C The Student ID {studentID} Record Does Not Exist.")
            print("=========================================================")
            return  # we return to the main menu after

    cursor.close() #close the connection
    conn.close()
######################################################################################
def queryScores(): #defining the query scores function
    print(f"\u25c6 1. Display Student Score by Name\n" #teh user has the choice to display by id or name
            f"\u25c6 2. Update Student Score by ID")
    operationCode = input("Please Select 1 or 2: ").strip() #again calling operation code function for selections

    if operationCode == '1':
        displayStudentScoreName() #calling the display student score by name function
    elif operationCode == '2':
        updateScoreByID() #calling the update student score by id function
    else:
        return #returning to the secondmain menu
######################################################################################
def displayStudentScoreName(): #defining the display student score by name function
    conn = connectDB() #opening the database connection
    cursor = conn.cursor()

    while True: #while looop to ensure we are getting looped back
        studentName = input("Please Enter Student Name to Display the Score: ").strip() #stripping of anything the user added

#execute block below to find the requested information from the database
        cursor.execute("""
            SELECT s.id, s.name, 
                   COALESCE(sc.cs1030, 0), 
                   COALESCE(sc.cs1100, 0), 
                   COALESCE(sc.cs2030, 0)
            FROM students s
            LEFT JOIN scores sc ON s.id = sc.id
            WHERE s.name = %s
        """, (studentName,))

#the matched students variable is what is found from the student database
        matchedStudents = cursor.fetchall()
#if the information is found then print the title with proper formatting
        if matchedStudents:
            print("\n==================== Student Scores ====================")
            print(f"{'ID':<12} {'Name':<15} {'CS1030':<8} {'CS1100':<8} {'CS2030':<8}")
            print("=" * 60)
            # if the information is found then print the requested information with proper formatting
            for student in matchedStudents:
                print(f"{student[0]:<12} {student[1]:<15} {student[2]:<8} {student[3]:<8} {student[4]:<8}")
            print('')
            return #return back to the secondmain menu

        else:
            print(f"\u274C No student records found for '{studentName}'. Please enter a valid student name.")
            continue #if the student name is not found it is not valid and not in the system.

    cursor.close() #close the database connection
    conn.close()
######################################################################################
def updateScoreByID(): #defining the update student score by id function
    conn = connectDB() #opening the database connection
    cursor = conn.cursor()

    while True: #while loop to ensure we are looped back
        studentID = input("Please Enter Student ID to update the Score: ").strip() #prompting user
        #to enter the student id for the student they wish to change grades for

        if not re.fullmatch(r"7003\d{5}", studentID):  # Check for valid student ID
            print("======================Student Record=====================")
            print(f"\u274C {studentID} is an invalid Student ID.") #if it is not a match then print error message
            print("=========================================================")
            return #go back to secondmain menu

        # Check if the student exists in the scores table
        #and we have a trigger to ensure that when a new student is added to the database it also
        #gets added to scores table
        #execute block to find
        cursor.execute("SELECT id, cs1030, cs1100, cs2030 FROM scores WHERE id = %s", (studentID,))
        student = cursor.fetchone()
        #the student is stored in this variable if found

#if student found then print the scores, ditionary to store key value pairs 'test' and 'score'
        if student:
            print("\nCurrent Scores:")
            print(f"CS1030: {student[1] if student[1] is not None else 0}")
            print(f"CS1100: {student[2] if student[2] is not None else 0}")
            print(f"CS2030: {student[3] if student[3] is not None else 0}")
#updated/new scores getting stored here in thsi dictionary
            updatedScores = {"CS1030": student[1], "CS1100": student[2], "CS2030": student[3]}

            # Get new scores for each course
            for course in ["CS1030", "CS1100", "CS2030"]:
                while True: #while loop to ensure we are looped back each time
                    newScore = input(f"New grade for {course} (press enter without modification): ")
                    if not newScore:  #if no new score then break loop (press enter)
                        break
                    if newScore.isdigit() and 0 <= int(newScore) <= 100: #if score is valid
                        #then update the new score and replace and break the loop
                        updatedScores[course] = int(newScore)
                        break
                    else: #if anything else then error message prints if invalid score
                        print(f"\u274C Invalid input! Score must be a number between 0 and 100.")

            # Update the scores in the database with the execute statement
            cursor.execute("""
                UPDATE scores 
                SET cs1030 = %s, cs1100 = %s, cs2030 = %s 
                WHERE id = %s
            """, (updatedScores["CS1030"], updatedScores["CS1100"], updatedScores["CS2030"], studentID))

            conn.commit() #commit the changes and save them to database
            print(f"\u2714 Record Updated Successfully!") #success statement prints
            return #return back to secondmenu

        else: #else if there is not a student record found for that id it is not in the system
            print("======================Student Record=====================")
            print(f"\u274C No record found for Student ID: {studentID}. Please enter a valid ID.")
            print("=========================================================")

    cursor.close() #close the database connection
    conn.close()
#################################################################
def modifyUser(): #defining the  modify user function
    conn = connectDB() #opening the connection to the database
    cursor = conn.cursor()

    while True:  #while loop to ensure we are brought back
        studentID = input("Please enter the Student ID to Modify: ").strip() #prompting the user to
        #enter the id of the student information they wish to modify
        #stripping of anything the user added
#the execute blocek actually goes to find this student and the requsted information
        cursor.execute("SELECT id, name, age, gender, major, phone FROM students WHERE id = %s", (studentID,))
        student = cursor.fetchone() #requsted information is stored in this variable
#if the studnet is found then we print the title and requested information with proper formatting
        if student:
            print("================================== Modify Student ==================================")
            print(f"{'ID':<18} {'Name':<18} {'Age':<8}{'Gender':<10}{'Major':<11}{'Phone':<15}")
            print(f"{student[0]:<18} {student[1]:<18} {student[2]:<8} {student[3]:<10} {student[4]:<11} {student[5]}")

            #storing original values
            originalAge, originalMajor, originalPhone = student[2], student[4], student[5]

            #while loop to modify the age
            while True:
                newAge = input("New age (press enter without modification): ").strip()
                #prompting the user to enter a new age
                if not newAge:  # If Enter is pressed, keep the old age, per above directions
                    newAge = originalAge #storing the new age
                    break #break the loop
                if newAge.isdigit() and 0 <= int(newAge) <= 100: #checking to make sure age is valid
                    newAge = int(newAge)  #storing new age as integer and not string
                    break #break the loop
                print(f"\u274C {newAge} is an invalid age. Please enter a number between 0 - 100.")
                #if it is not valid then error message prints

                #while loop to modify the major
            newMajor = input("New major (press enter without modification): ").strip().upper()
            #prompting the user to enter their new major, stripping of anything else and
            #making sure it is stored in uppercase
            if not newMajor: #if the major is not updated then keep the original major
                newMajor = originalMajor

                #while loop to modify the phone number
            while True:
                newPhone = input(f"New phone \u2709 (press enter without modification): ").strip()
                #prompting the user to enter the new phone numbe or press enter to keep
                #stripping of anything else they may have added
                if not newPhone:  # Keep the old number
                    newPhone = originalPhone
                    break #break the loop
                if re.fullmatch(r"\d{3}-\d{3}-\d{4}", newPhone):  # Validate phone format to match
                    #the pattern
                    break #break the loop
                print(f"\u274C {newPhone} is an invalid phone number.") #this will print if it does
                #not match the pattern

#if nothing new was given then the record was not modified and will print this message
            if (newAge, newMajor, newPhone) == (originalAge, originalMajor, originalPhone):
                print("\u274C Record not modified!")
            else: #if anything else than update everything in the database system and store
                #new updates
                cursor.execute("""
                    UPDATE students 
                    SET age = %s, major = %s, phone = %s
                    WHERE id = %s
                """, (newAge, newMajor, newPhone, studentID))

                conn.commit() #commit and save to the database
                print("\u2714 Student record updated successfully!") #print success message

            break #break the loop

        else: #if it is not found in datbaase then print error message
            print(f"\u274C No record found!")
            break

    cursor.close() #close the database connection
    conn.close()
######################################################################################
def delUser(): #defining the delete user function
    while True: #while loop to ensure we are looped back
        #printing the menu options
        print("================================== Modify Student ==================================")
        print(f"\u25c6 1. Delete Students by Name\n"
              f"\u25c6 2. Delete Students by ID\n"
              f"\u25c6 Other Return")
        operationCode = input("Please Select: ").strip()
        print("===================================================================================")
#prompting the user to enter their selection again calling the operation code function
        if operationCode == '1':
            delStuName() #calling the delete by student name function
        elif operationCode == '2':
            delStuID() #calling the delete by student id function
        else: #if anything else then return to secondmain menu
            return
######################################################################################
def delStuName(): #defining the delete by student name function
    conn = connectDB() #opening the database connection
    cursor = conn.cursor()

#prompting the user to enter studentname to delete, stripping of anything they may have entered
    studentName = input("Please enter the Student Name to Delete: ").strip()
#execute block that executes the name and tries to find it in database
    cursor.execute("SELECT id, name, phone, major FROM students WHERE name = %s", (studentName,))
    student = cursor.fetchone() #if found it is stored in this variable
#if found in database then print the student record and confirmation message
    if student:
        print("======================Student Record=====================")
        print(f"\u2709 ID: {student[0]}, Name: {student[1]}, Phone: {student[2]}, Major: {student[3]}")
        confirmation = input("Are you sure you want to delete this record? (Y/N): ").strip().upper()
#confirming that the user wants or does not want to delete
        #if yes then record is deleted and changes are saved (committed) to database
        #if not then the deletion is canceled.
        if confirmation == 'Y':
            cursor.execute("DELETE FROM students WHERE name = %s", (studentName,))
            conn.commit()
            print(f"\u2714 Student {studentName} has been deleted successfully.")
            return #return to secondmain menu
        else:
            print("\u2139 Deletion canceled.")
            return #return to secondmain menu
    else:
        print(f"\u274C No student records found for '{studentName}'.")
        return #return to secondmain menu

    cursor.close() #closing the database connection
    conn.close()
######################################################################################
def delStuID(): #defining the delete by student id function
    conn = connectDB() #opening the database connection
    cursor = conn.cursor()
    # prompting the user to enter id to delete, stripping of anything they may have entered
    studentID = input("Please enter the Student ID to Delete: ").strip()
    # execute block that executes the name and tries to find it in database
    cursor.execute("SELECT id, name, phone, major FROM students WHERE id = %s", (studentID,))
    student = cursor.fetchone() #if found storing in this variable
    # if found in database then print the student record and confirmation message
    if student:
        print("======================Student Record=====================")
        print(f"\u2709 ID: {student[0]}, Name: {student[1]}, Phone: {student[2]}, Major: {student[3]}")
        confirmation = input("Are you sure you want to delete this record? (Y/N): ").strip().upper()
        # confirming that the user wants or does not want to delete
        # if yes then record is deleted and changes are saved (committed) to database
        # if not then the deletion is canceled.
        if confirmation == 'Y':
            cursor.execute("DELETE FROM students WHERE id = %s", (studentID,))
            conn.commit()
            print(f"\u2714 Student with ID {studentID} has been deleted successfully.")
            return #returning back to delete menu
        else:
            print("\u2139 Deletion canceled.")
            return #returning back to delete menu
    else:
        print(f"\u274C No student records found for ID {studentID}.")
        return #returning back to delete menu

    cursor.close() #closing the database connection
    conn.close()
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
#####################################################################################################
def continueMenu(): #defining the continue menu function. this is before the user adds another new student after adding one.
    while True: #while loop to ensure we are looped back when needed
        print(f"\u25c6 1. Continue \n" 
              f"\u25c6 2. Exit")

        operationCode = input("Please Select 1 or 2: ").strip() #calling the operation code function
        #so the user can input their selection

        if operationCode == '1':
            addUser()  #continue to adduser i fhtey wish to continue adding more users
        elif operationCode == '2':
            return  #return to secondmain menu
        else: #if anything else state that is not valid
            print("That is not a valid operation code. Please enter a valid selection.")
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

        operationCode = input(f"\nPlease select (1 - 6): ").strip() ##making sure to strip of anything else
        #so this can be read as a string

        cusInput(operationCode) #calling the customer input function that will run the
        #user input for the entire program
######################################################################################