from blackjack import *


def game(deck, table, players, dealer):
    for round in range(2):
        for i, player in enumerate(players):
            player.add_card(deck.draw())
            if i == 0:
                if round == 1:
                    dealer.add_card(deck.draw())
                    dealer.hand[0].flip()
                else:
                    dealer.add_card(deck.draw())
    print(table.create_table(players, dealer))

    for player in players:
        while player.keep_playing:
            player.play()
            print(table.create_table(players, dealer))

    dealer.play()
    print(table.create_table(players, dealer))
    return


def player_names():
    names = []
    more_players = True
    print("Add players by name. Type '0' to Stop Entering")
    while more_players:
        name = input("Player Name: ")
        if name == str(0):
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

def winners(players, dealer):
    winners = []
    for player in players:
        if dealer.blackjack:
            winners.append(dealer)
            break
        if player.blackjack:
            winners.append(player)
    else:
        winners.append(dealer)

    return winners

# def display_winners():

