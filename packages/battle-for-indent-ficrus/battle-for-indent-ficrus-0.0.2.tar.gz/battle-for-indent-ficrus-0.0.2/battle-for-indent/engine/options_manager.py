import memento
import pickle

class OptionsManager:
    def __init__(self, options_file="../save_data/options"):
        self.options_file = options_file
        try:
            with open(self.options_file, "rb") as options:
                self.restore(pickle.load(options))
        except FileNotFoundError:
            self.is_music_enabled = True
            self.is_sounds_enabled = True
            self.is_easter_egg_enabled = False

    def save(self) -> memento.OptionsMemento:
        return memento.OptionsMemento([self.is_music_enabled,
                                       self.is_sounds_enabled,
                                       self.is_easter_egg_enabled])

    def save_on_disk(self, memento: memento.OptionsMemento) -> None:
        with open(self.options_file, "wb") as options:
            pickle.dump(memento, options)

    def restore(self, memento: memento.OptionsMemento) -> None:
        (self.is_music_enabled,
        self.is_sounds_enabled,
        self.is_easter_egg_enabled) = memento.get_state()

    def change_music(self):
        self.is_music_enabled = not self.is_music_enabled

        self.save_on_disk(self.save())
    
    def change_sounds(self):
        self.is_sounds_enabled = not self.is_sounds_enabled

        self.save_on_disk(self.save())

    def change_egg(self):
        self.is_easter_egg_enabled = not self.is_easter_egg_enabled

        self.save_on_disk(self.save())
