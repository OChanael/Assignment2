import sqlite3
import pandas as pd
from Student import Student


class Manager:

    def __init__(self, db):
        # create sqlite connection
        self.conn = sqlite3.connect(db)
        self.cursor = self.conn.cursor()
        print("Connect to sqlite3")

        # create students table if none currently exists
        self.cursor.execute("CREATE TABLE IF NOT EXISTS Students ("
                        "StudentId INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,"
                        "FirstName VARCHAR(32) NOT NULL,"
                        "LastName VARCHAR(32) NOT NULL,"
                        "GPA NUMERIC NOT NULL,"
                        "Major VARCHAR(16) NOT NULL,"
                        "FacultyAdvisor VARCHAR(32),"
                        "IsDeleted INTEGER "
                        ");")
        self.conn.commit()

    # option 1
    def display(self):
        self.select("*")

    # option 2
    def insert(self):
        print()
        # loop until user confirms correct data
        isCorrect = False
        while not isCorrect:
            # Get user inputs to use as data
            FirstName = input("Enter First Name: ")
            LastName = input("Enter Last Name: ")
            GPA = self.getFloatInput("Enter GPA: ", 0)
            Major = input("Enter Major: ")
            FacultyAdvisor = input("Enter Faculty Advisor: ")
            IsDeleted = 0

            # ask user if data is correct
            print()
            print("First Name:", FirstName,"\nLast Name:", LastName,
             "\nGPA:", GPA, "\nMajor:", Major, "\nFaculty Advisor:", FacultyAdvisor,)
            # since IsDeleted is always entered as 0 it does not ask for it
            print()
            while True:
                valid = input("Are these values correct? ('Y' / 'N') ")
                if valid.upper() == "Y":
                    isCorrect = True
                    break
                elif valid.upper() == "N":
                    print()
                    print("Please re-enter values.")
                    break
                else:
                    print("Invalid option.")

        # Write to database
        student = Student(FirstName, LastName, GPA, Major, FacultyAdvisor, IsDeleted)
        self.cursor.execute("INSERT INTO Students(FirstName, LastName, GPA, Major, FacultyAdvisor, IsDeleted) "
                        "VALUES(?,?,?,?,?,0);", student.getVals())
        self.conn.commit()
        print("Student record entered successfully.")

    # option 3
    def update(self):
        # check if student is in database
        print()
        id = int(self.getFloatInput("Enter the StudentId of the student: ", 1))
        if not self.validStudent(id):
            print("Update failed. Please try again.")
        else:
            attr = ''
            while True:
                attr = input("Are you updating Major or Advisor? (Please enter 'Major' or 'Advisor') ")
                if attr.upper() == 'MAJOR':
                    attr = attr.capitalize()
                    break
                elif attr.upper() == 'ADVISOR':
                    attr = "FacultyAdvisor"
                    break
                else:
                    print("Invalid option.")
            val = input("Please enter the new value: ")

            # Write to database
            self.cursor.execute("UPDATE Students SET {0} = '{1}' WHERE StudentId = {2};"
                .format(attr, val, id)) # insert values into sql command
            self.conn.commit()
            print("Student record updated successfully.")

    # option 4
    def delete(self):
        # check if student is in database
        print()
        id = int(self.getFloatInput("Please enter the StudentId of the student: ", 1))
        if not self.validStudent(id):
            print("Deletion Failed. Please try again.")
        else:
            self.cursor.execute("UPDATE Students SET IsDeleted = 1 WHERE StudentId = {0};".format(id))
            self.conn.commit()
            print("Student record deletion successful.")

    # option 5
    def search(self):
        print()
        # select by major
        while True:
            major = input("Are you searching by Major? (Please enter 'Y' or 'N') ")
            if major.upper() == 'Y':
                data = input("Please enter the major you would like to search: ")
                self.select("Major", data)
                return
            elif major.upper() == 'N':
                break
            else:
                print("Invalid option. Please try again.")
        # select by GPA
        while True:
            GPA = input("Are you searching by GPA? (Please enter 'Y' or 'N') ")
            if GPA.upper() == 'Y':
                data = self.getFloatInput("Please enter the GPA you would like to search: ", 0)
                self.select("GPA", data)
                return
            elif GPA.upper() == 'N':
                break
            else:
                print("Invalid option. Please try again.")
        # select by FacultyAdvisor
        while True:
            advisor = input("Are you searching by FacultyAdvisor? (Please enter 'Y' or 'N') ")
            if advisor.upper() == 'Y':
                data = input("Please enter the FacultyAdvisor you would like to search: ")
                self.select("FacultyAdvisor", data)
                return
            elif advisor.upper() == 'N':
                break
            else:
                print("Invalid option. Please try again.")

        # If user says N to all options
        print("Search canceled.")

    # error checking functions, and a dynamic select

    # simplify error checking for floats
    def getFloatInput(self, message, option):
        data = 0
        while True:
            try:
                data = float(input(message))
                # if input is GPA
                if option == 0:
                    # don't allow GPA > 4.0
                    if data > 4.0 or data < 0.0:
                        raise SyntaxError()
                break
            except ValueError:
                print("Invalid Input. Must be numeric.")
            except SyntaxError:
                print("Invalid Input. GPA cannot be over 4.0 or under 0.")
        return data

    # returns whether a student is in the database given the ID
    def validStudent(self, id):
        self.cursor.execute("SELECT FirstName, LastName, GPA, Major, FacultyAdvisor, IsDeleted from Students WHERE StudentId = " + str(id))
        try:
            data = self.cursor.fetchall()[0] # get tuple from list
            student = Student(data[0], data[1], data[2], data[3], data[4], data[5]) # try to init a student with vals
            return True
        except Exception as e:
            print("Student not found.")
            return False

    # dynamically use select statement
    def select(self, col, data=None):
        print()
        dataFields = None

        # will not show deleted students, though they remain in the database
        if data == None:
            dataFields = pd.read_sql_query("SELECT StudentID, FirstName, LastName, Major, GPA FROM Students WHERE IsDeleted = 0;"
                                           .format(col), self.conn)
        elif isinstance(data, (int, float)):
            dataFields = pd.read_sql_query("SELECT StudentID, FirstName, LastName, Major, GPA FROM Students WHERE {0} = {1} AND IsDeleted = 0;"
                                           .format(col, data), self.conn)
        else:
            dataFields = pd.read_sql_query("SELECT StudentID, FirstName, LastName, Major, GPA FROM Students WHERE {0} = '{1}' AND IsDeleted = 0;"
                                           .format(col, data), self.conn)

        if dataFields.empty:
            print("No results found.")
        else:
            print(dataFields)
