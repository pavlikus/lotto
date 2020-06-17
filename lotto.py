#!/usr/bin/env python

from typing import List

from game import Bot, Game, Human, Player


def add_players(game: Game) -> None:
    players = {'bot': Bot,
               'human': Human}
    choice = input("Add player? (y/n) ")
    while choice.lower() in ('y', 'yes'):
        i = input("Possible type(human, bot), example: Alex bot: ")
        name, player, *_ = i.split()
        if player.lower() in players:
            game.add_player(players[player](name))
            print(f"Added {name} in game")
        choice = input("Add more player? (y/n) ")


def card_formater(player: Player) -> List[str]:
    diff = list(set(player.card) - set(player.card_game))
    card = []
    for i in player.card:
        if not i:
            card.append('  ')
        elif i in diff:
            card.append(' X')
        else:
            card.append(f' {i}' if i < 10 else f'{i}')
    return card


def print_card(card: List[str]) -> None:
    print("-" * 30)
    j = 0
    for i in range(9, 28, 9):
        row = ' '.join(card[j:i])
        print('|', f"{row}", '|')
        j = i
    print("-" * 30)


def player_choice(name: str) -> bool:
    choice = input(f"{name} cross out the number? (y/n) ")
    if choice.lower() in ('y', 'yes'):
        choice = True
    else:
        choice = False
    print(f"Your choice {choice}")
    return choice


def game_process(game: Game):
    winner = None
    choice = False

    while game.nrg.numbers:
        for player in game.players.copy():
            if isinstance(player, Human):
                choice = player_choice(player.name)
            game.one_cycle(player, choice=choice)
            print(f"{player.name:*^30}")
            card = card_formater(player)
            print_card(card)
        print(f"Number was - {game.nrg.number}")
        game.nrg.number = game.nrg.numbers.pop()

        if game.winner:
            winner = game.winner
            break
    else:
        winner = game.players[0]
    print(f"{winner} you win")


if __name__ == '__main__':
    game = Game()
    add_players(game)

    if not game.players:
        game.add_player(Bot())
        game.add_player(Human())

    game_process(game)
