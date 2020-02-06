from blackjack import *


def game(deck, table, players, dealer):
    for round in range(2):
        for player in players:
            player.add_card(deck.draw())
            if round == 1:
                dealer.add_card(deck.draw())
                dealer.hand[0].flip()
            else:
                dealer.add_card(deck.draw())
    print(table)

    for player in players:
        while player.keep_playing:
            player.play()
            print(table)

    dealer.play()
    print(table)
    return


def player_names():
    names = []
    more_players = True
    print("Add players by name. Type '0' to Stop Entering")
    while more_players:
        name = input("Player Name: ")
        if not name:
            more_players = False
        else:
            names.append(name)
    return names


def create_gamblers(deck):
    names = player_names()
    gamblers = []
    for name in names:
        gamblers.append(Player(deck, name))
    return gamblers
