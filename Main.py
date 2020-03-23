from DatabaseManager import Manager
from Menu import Menu

if __name__ == "__main__":
    manager = Manager("StudentDB.db")
    menu = Menu()

    while True:
        menu.show()
        select = menu.getOption()

        if select == 1:
            manager.display()
        elif select == 2:
            manager.insert()
        elif select == 3:
            manager.update()
        elif select == 4:
            manager.delete()
        elif select == 5:
            manager.search()
        elif select == 6:
            break