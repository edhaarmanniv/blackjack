from blackjack import *
from cards import *

cards = []
for _, suit in suits["solid"].items():
    for face, face_value in faces.items():
        cards.append(Card(face, face_value, suit))

deck = Deck(cards)
deck.shuffle()

ed = Player(deck, "Ed")
ed.play()
# run thru starting scenario:
# cycle thru players and dealer drawing one card face up
# cycle again leaving second up except for dealer
# show the current status of the table
def game(deck, players, dealer):
    for round in range(1):
        for player in players:
            player.add_card(deck.draw())
        dealer.add_card(deck.draw())
        if round == 1:
            dealer.hand[-1].flip()



