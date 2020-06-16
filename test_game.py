from game import Bot, Game, Human, NRG, Player

import pytest


players = [Bot('Botik'), Human('Pavlik'), Bot('Bot'), Bot()]


@pytest.fixture(scope='module')
def game():
    game = Game()

    for player in players:
        game.add_player(player)

    return game


class Gamer(Player):

    def __init__(self):
        super().__init__()


class TestGamePlayers:

    def test_game_players(self, game):
        assert players == game.players

    def test_game_len_players(self, game):
        assert len(players) == len(game.players)

    def test_player_name(self, game):
        assert players[0].name == game.players[0].name

    def test_player_card_creation(self, game):
        for player, game_player in zip(players, game.players):
            assert player.card_game == game_player.card_game

    def test_base_instance(self, game):
        for game_player in game.players:
            assert isinstance(game_player, Player)

    def test_game_player_instance(self, game):
        for player, game_player in zip(players, game.players):
            assert isinstance(game_player, player.__class__)

    def test_player_abstract_class(self):
        with pytest.raises(TypeError):
            Player()

    def test_player_abstract_method(self):
        with pytest.raises(TypeError):
            gamer = Gamer()
            gamer.update_card()


class TestNRG:

    def test_nrg_singleton(self, game):
        for player, game_player in zip(players, game.players):
            assert NRG.nrg == player.nrg == game_player.nrg == game.nrg

    def test_len_numbers(self):
        assert len(NRG.nrg.numbers) == 89

    def test_custom_len_numbers(self):
        for i in range(9):
            NRG.nrg.numbers.pop()

        assert len(NRG.nrg.numbers) == 80

    def test_number_exist(self):
        assert isinstance(NRG.nrg.number, int)
