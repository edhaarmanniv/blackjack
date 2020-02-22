from random import shuffle as rshuffle
from terminaltables import SingleTable


class Card:
    def __init__(self, face, value, suit):
        self.face = face
        self.value = value
        self.suit = suit
        self.card = face + suit
        self.front = f"[{self.card}]"
        self.back = "[**]"
        self.facedown = False
        return

    def __str__(self):
        return self.show()

    def flip(self):
        self.facedown = not self.facedown
        return

    def show(self):
        display = None
        if self.facedown:
            display = self.back
        else:
            display = self.front
        return display

    def flip_show(self):
        self.flip()
        return self.show()


class Deck:
    def __init__(self, cards, num_cards=52):
        self.cards = cards
        self.num_cards = len(cards)
        return

    def shuffle(self):
        rshuffle(self.cards)
        return

    def draw(self):
        top_card = None
        if len(self.cards) > 0:
            top_card = self.cards.pop()
        else:
            print("NO MORE CARDS")
        return top_card

    def cards_left(self):
        print([card.card for card in self.cards])


class Player:
    def __init__(self, deck, name="Player"):
        self.hand = []
        self.name = name
        self.deck = deck
        self.blackjack = False
        self.bust = False
        self.keep_playing = True
        return

    def __str__(self):
        return f"{self.name} || {self.score()} || {self.show_hand()}"

    def add_card(self, card):
        self.hand.append(card)
        return

    def hit(self, card):
        self.add_card(card)
        if self.score() > 21:
            self.bust = True
        if self.score() == 21:
            self.blackjack = True
        return

    def stay(self):
        self.keep_playing = False
        return

    def score(self):
        score = 0
        for card in self.hand:
            if card.face == "A":
                if score + card.value[1] > 21:
                    score += card.value[0]
                else:
                    score += card.value[1]
            else:
                score += card.value
        return score

    def play(self):
        while self.keep_playing and not self.bust and not self.blackjack:
            choice = input(f"Player {self.name}:\n(H)it or (S)tay: ")
            if choice in {"H", "h", "Hit", "hit"}:
                self.hit(self.deck.draw())
                print(self)
            elif choice in {"S", "s", "Stay", "stay"}:
                self.stay()
            # elif split:
            # elif double: 
            else:
                print("Invalid Selection! Select Again")
            
            if self.blackjack:
                print("21!")
                self.keep_playing = False
            
            if self.bust:
                print("Busted!")
                self.keep_playing = False
        return

    def show_hand(self):
        hand_str = ""
        for card in self.hand:
            if card.facedown == True:
                hand_str += card.back
            else:
                hand_str += card.front
        return hand_str


class Dealer(Player):
    def __init__(self, deck):
        super().__init__(deck, "Dealer")
        return

    def show_hidden(self):
        for card in self.hand:
            if card.facedown == True:
                card.flip()

    def play(self):
        print("Dealer's Turn:")
        if self.score() > 21:
            bust = True
        elif self.score() < 16:
            while self.score() < 17:
                self.hit(self.deck.draw())
        else:
            self.stay()
        self.show_hidden()
        return

    def score(self):
        score = 0
        for card in self.hand:
            if card.face == "A":
                if score + card.value[1] > 21:
                    score += card.value[0]
                else:
                    score += card.value[1]
            else:
                score += card.value
        return score


class Table:
    def __init__(self, players, dealer):
        self.players = players
        self.dealer = dealer
        self.table = self.create_table(players, dealer)
        return

    def __str__(self):
        return self.show_table()

    def create_table(self, players, dealer):
        column_headers = ["Player", "Score", "Hand"]
        table_data = [column_headers]
        players_done_playing = {player.keep_playing for player in players}
        if len(players_done_playing) == 1 and False in players_done_playing:
            table_data.append([self.dealer.name, self.dealer.score(), self.dealer.show_hand()])
        else:
            table_data.append(
            [self.dealer.name, "??", self.dealer.show_hand()]
            )
        table_data.extend(
            [
                [player.name, player.score(), player.show_hand()]
                for player in self.players
            ]
        )

        single_table = SingleTable(table_data, title="Blackjack")
        for column in range(len(column_headers)):
            single_table.justify_columns[column] = "center"
        return single_table.table

    def show_table(self):
        return self.table
