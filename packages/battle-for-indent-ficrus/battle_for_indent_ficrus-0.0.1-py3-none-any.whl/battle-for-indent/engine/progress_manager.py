import memento
import pickle


class ProgressManager:
    def __init__(self, progress_file="../save_data/progress"):
        self.progress_file = progress_file
        try:
            with open(self.progress_file, "rb") as progress:
                self.restore(pickle.load(progress))
        except FileNotFoundError:
            self.wins = 0
            self.draws = 0
            self.loses = 0
            self.fraction = ""

    def save(self) -> memento.ProgressMemento:
        return memento.ProgressMemento([self.wins,
                                        self.draws,
                                        self.loses,
                                        self.fraction])

    def save_on_disk(self, memento: memento.ProgressMemento) -> None:
        with open(self.progress_file, "wb") as progress:
            pickle.dump(memento, progress)

    def restore(self, memento: memento.ProgressMemento) -> None:
        (self.wins,
        self.draws,
        self.loses,
        self.fraction) = memento.get_state()

    def add_win(self):
        self.wins += 1

        self.save_on_disk(self.save())

    def add_draw(self):
        self.draws += 1

        self.save_on_disk(self.save())

    def add_lose(self):
        self.loses += 1

        self.save_on_disk(self.save())

    def select_fraction(self, fraction):
        self.fraction = fraction

        self.save_on_disk(self.save())

    def reset(self):
        self.wins = 0
        self.draws = 0
        self.loses = 0
        self.fraction = ""

        self.save_on_disk(self.save())
