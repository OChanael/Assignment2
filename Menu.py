class Menu:

    def __init__(self):
        pass

    def show(self):
        print()
        print("Menu")
        print("1) Display Students\n"
              "2) Add Student\n"
              "3) Update Student\n"
              "4) Delete Student\n"
              "5) Search Student\n"
              "6) Quit")

    def getOption(self):
        while True:
            try:
                option = int(input("Please Enter Option: "))
                if option > 6 or option < 1:
                    raise Exception()
                break
            except Exception:
                print("Invalid Input.")
        return option
