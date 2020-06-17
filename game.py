import random
from abc import ABC, abstractmethod
from typing import List


class Singleton(type):

    _instances = {}

    def __init__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super().__init__(*args, **kwargs)
        return cls._instances[cls]


class NumbersRandomGenerator(metaclass=Singleton):

    def __init__(self):
        # init list random numbers between 1 and 90
        self.numbers = random.sample(range(1, 90+1), k=90)
        self.number = self.numbers.pop()

    @staticmethod
    def get_card_numbers() -> List[int]:
        return random.sample(range(1, 90+1), k=15)

    @staticmethod
    def get_number_positions() -> List[int]:
        size = 3 * 9  # 3 - rows, 9 - columns
        count_number = 15  # need only 15 numbers on board
        return random.sample(range(0, size+1), k=count_number)


class NRG:

    nrg = NumbersRandomGenerator()


class Player(ABC, NRG):

    def __init__(self):
        self.card = self._card_init()
        self.card_game = self.card.copy()

    def _card_init(self) -> List[int]:
        numbers = self.nrg.get_card_numbers()
        positions = self.nrg.get_number_positions()
        card = dict(zip(positions, numbers))
        size = 27
        return [card[i] if i in card else 0 for i in range(size+1)]

    @abstractmethod
    def update_card(self, *args, **kwargs) -> None:
        raise NotImplementedError

    def __str__(self):
        return f"{self.name}"

    def __repr__(self):
        return f"{self.__class__.__name__.lower()}"


class Human(Player):

    def __init__(self, name: str = 'Player'):
        super().__init__()
        self.name = name

    def update_card(self, choice: bool = False) -> None:
        number_on_card = self.nrg.number in self.card_game
        if choice != number_on_card:
            raise GameOver(f"{self.name} your Game is Over")
        if number_on_card:
            self.card_game = [0 if n == self.nrg.number else n
                              for n in self.card_game]


class Bot(Player):

    def __init__(self, name: str = 'Bot'):
        super().__init__()
        self.name = name

    def update_card(self, *args, **kwargs) -> None:
        self.card_game = [0 if n == self.nrg.number else n
                          for n in self.card_game]


class GameOver(Exception):
    ...


class Game(NRG):

    def __init__(self):
        self.players = []
        self.winner = None

    def add_player(self, player: Player) -> None:
        self.players.append(player)

    def _check_winer(self, player: Player) -> None:
        print(player.card_game)
        if not sum(player.card_game):
            self.winner = player

        if len(self.players) == 1:
            self.winner = self.players[0]

    def one_cycle(self, player: Player, *args, **kwargs) -> None:
        try:
            player.update_card(*args, **kwargs)
            self._check_winer(player)
        except GameOver as e:
            print(e)
            self.players.remove(player)
