class Student:

    def __init__(self, FirstName, LastName, GPA, Major, FacultyAdvisor, IsDeleted):
        self.FirstName = str(FirstName)
        self.LastName = str(LastName)
        self.GPA = float(GPA)
        self.Major = str(Major)
        self.FacultyAdvisor = str(FacultyAdvisor)
        self.IsDeleted = int(IsDeleted)

    # accessors
    def getVals(self):
        return (self.FirstName, self.LastName, self.GPA, self.Major, self.FacultyAdvisor)

    def getFirstName(self):
        return self.FirstName

    def getLastName(self):
        return self.LastName

    def getGPA(self):
        return self.GPA

    def getMajor(self):
        return self.Major

    def getFacultyAdvisor(self):
        return self.FacultyAdvisor

    # mutators
    def setFirstName(self, name):
        self.FirstName = str(name)

    def setLastName(self, name):
        self.LastName = str(name)

    def setGPA(self, GPA):
        self.GPA = float(GPA)

    def setMajor(self, Major):
        self.Major = str(Major)

    def setFacultyAdvisor(self, Advisor):
        self.FacultyAdvisor = str(Advisor)

    def setIsDeleted(self, IsDeleted):
        self.IsDeleted = int(IsDeleted)