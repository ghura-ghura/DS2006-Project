from src.utils.sys import clear_screen_windows, flush_input_windows
from src.config.main import menu_config, train_model_options
from src.menu.options import OptionsMenu
from src.types.dataclass import Dataset
from src.menu.key import KeyHandler
from src.model.main import Model

class Menu:
    def __init__(self, model: Model) -> None:
        self.trained_models_options: list[str] = []
        self.dataset_to_load: str | None = None
        self.available_datasets: list[str] = []
        self.show_train_model_options = False
        self.dataset: Dataset | None = None
        self.isOptionSelected = False
        self.selected_option = 0
        self.exiting = False
        self.model = model

        self.options_menu = OptionsMenu(
            set_show_train_model_options=self.set_show_train_model_options,
            set_trained_models_options=self.set_trained_models_options,
            model=self.model,
        )
        self.key_handler = KeyHandler()

    def start(self, clear_screen: bool = True) -> None:
        if clear_screen:
            clear_screen_windows()
        
        self.render_title(menu_config["title"])

        if self.show_train_model_options:
            self.options = train_model_options
            self.instruction = "Select a model to train:"
        elif len(self.trained_models_options) > 0:
            self.options = self.trained_models_options
            self.instruction = "Select a model to evaluate:"
        else:
            self.options = menu_config["options"]
            self.instruction = "Select an option:"

        self.render_options(options=self.options, instruction=self.instruction)

        if not self.isOptionSelected:
            self.handle_input()

    def render_title(self, title: str) -> None:
        seperator = "=" * len(title)
        print(f"{seperator} {title} {seperator}")

    def render_options(self, options: list[str], instruction: str) -> None:
        print(instruction)

        for i, option in enumerate(options):
            arrow = " "
            if i == self.selected_option:
                arrow = "→" if not self.isOptionSelected else "✓"

            print(f"{arrow}  {i + 1}.  {option}")
        
        print("\nPress Esc to quit\n") 

    def handle_input(self) -> None:
        while not self.exiting:
            try:
                if self.exiting or self.isOptionSelected:
                    return

                key = self.key_handler.get_key_windows()
                if not key:
                    continue
                
                match key:
                    case 'w' | 'W':
                        self.selected_option = (self.selected_option - 1) % len(self.options)
                        clear_screen_windows()
                        self.start()
                    case 's' | 'S':
                        self.selected_option = (self.selected_option + 1) % len(self.options)
                        clear_screen_windows()
                        self.start()
                    case '\r':
                        self.select_option()
                        break
                    case '\x1b':
                        self.quit()
                        break
            except KeyboardInterrupt:
                self.quit()
                break

    def select_option(self) -> None:
        self.isOptionSelected = True
        clear_screen_windows()

        self.render_title(menu_config["title"])
        self.render_options(options=self.options, instruction=self.instruction)
        
        print(self.show_train_model_options)
        self.options_menu.on_option_click(options=self.options, selected_option=self.selected_option, is_evaluating=not self.show_train_model_options)
        
        self.isOptionSelected = False
        self.selected_option = 0
        
        self.start(clear_screen=False)

    def set_show_train_model_options(self, show: bool) -> None:
        self.show_train_model_options = show
        self.selected_option = 0

    def set_trained_models_options(self, options: list[str]) -> None:
        self.trained_models_options = options
        self.selected_option = 0

    def quit(self) -> None:
        self.exiting = True
        flush_input_windows()
        print("\nExiting...")
