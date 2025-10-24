from src.model.main import Model
from src.menu.main import Menu

def main():
    model = Model()

    menu = Menu(model=model)
    menu.start()

if __name__ == "__main__":
    main()