from sys import exit as sys_exit
from src.model.main import Model
from src.menu.main import Menu
from os import name as os_name

def main():
    if os_name != 'nt':
        print("Sorry, this is not available on this platform")
        sys_exit(1)

    model = Model()

    menu = Menu(model=model)
    menu.start()

if __name__ == "__main__":
    main()