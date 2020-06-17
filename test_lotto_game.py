from game import Bot, Game, Human, NRG, Player

from lotto import add_players, game_process

import mock

import pytest


players = [Bot('Botik'), Human('Pavlik'), Bot('Bot'), Bot()]


@pytest.fixture()
def game():
    game = Game()

    for player in players:
        game.add_player(player)

    return game


class Gamer(Player):
    """Class for testing class Player"""


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


class TestLottoGame:

    def test_human_winner(self, game):
        for player in players:
            if isinstance(player, Human):
                break
        player.card = game.nrg.numbers[74:] + [game.nrg.number] + [0] * 11
        player.card_game = player.card.copy()
        with mock.patch('builtins.input', return_value="y"):
            game_process(game)
        assert player == game.winner

    def test_first_player_winner(self, game):
        player = game.players[0]
        player.card = [0] * 27
        player.card_game = player.card.copy()
        game_process(game)
        assert player == game.winner

    def test_one_player_winner(self, game):
        game.players = [Bot()]
        game_process(game)
        assert isinstance(game.winner, Bot)

    @pytest.mark.parametrize("game, players, game_players", [
        pytest.param(Game(),
                     ("Alex bot", "Pavlik human", "Botik bot"),
                     (Bot('Alex'), Human('Pavlik'), Bot('Botik')),
                     id="add bot - human - bot"),
        pytest.param(Game(),
                     ("First bot", "Second BOT", "Noname bOT"),
                     (Bot('First'), Bot('Second'), Bot('Noname')),
                     id="add bot with different name"),
        pytest.param(Game(),
                     ("Alex", "Pavlik human", "nam h", "Alex bot b b", "1 2 "),
                     (Human('Pavlik'), Bot('Alex')),
                     id="add only 2 players")

    ])
    def test_add_players(self, game, players, game_players):
        side_effect = []
        for player in players:
            side_effect.append('y')
            side_effect.append(player)
        else:
            side_effect.append('n')

        with mock.patch('builtins.input', side_effect=side_effect):
            add_players(game)

        assert len(game_players) == len(game.players)

        for player, game_player in zip(game_players, game.players):
            assert isinstance(player, game_player.__class__)
            assert str(player) == str(game_player)
