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
            player.play(deck)
            print(table.create_table(players, dealer))

    dealer.play(deck)
    print(table.create_table(players, dealer))
    display_winners(winners(players, dealer))
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


def create_gamblers():
    names = player_names()
    gamblers = [Player(name) for name in names]
    return gamblers


def winners(players, dealer):
    winners = []
    scores = [player.score() for player in players]
    if dealer.blackjack:
        winners.append(dealer)
    elif any(player.blackjack for player in players):
        winners = [player for player in players if player.blackjack]
    elif all(dealer.score() >= score for score in scores) and not dealer.bust:
            winners = [dealer]
    else:
        winners = [player for player in players if player.score == max(scores)]

    for winner in winners:
        winner.num_wins += 1

    return winners


def display_winners(winners):
    win = "Winners:" if len(winners) > 1 else "Winner:"
    if len(winners) == 1 and winners[0].name == "Dealer":
        print("Dealer Wins! :(")
    else:
        print(win)
        print(*winners, sep=", ")


def reset_hands(players, dealer):
    dealer.reset_hand()
    for player in players:
        player.reset_hand()
    return
