from random import shuffle as rshuffle

class Card():
    def __init__(self, face, value, suit):
        self.face = face
        self.value = value
        self.suit = suit
        self.card = face+suit
        self.front = f"[{self.card}]"
        self.back = "[**]"
        self.facedown = False
        return 

    def __str__(self):
        return self.show()
    
    def flip(self):
        self.facedown = ~self.facedown
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

class Deck():
    def __init__(self, cards, num_cards=52):
        self.cards = cards
        self.num_cards = len(cards)
        return

    def shuffle(self):
        rshuffle(self.cards)
        return
    
    def draw(self):
        top_card = None
        if len(self.cards) >0:
            top_card = self.cards.pop()
        else:
            print("NO MORE CARDS")
        return top_card
    
    def cards_left(self):
        print([card.card for card in self.cards])


class Player():
    def __init__(self, deck, name="Player"):
        self.hand = [] 
        self.name = name
        self.deck = deck
        self.blackjack = False
        self.bust = False
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
        pass

    def score(self):
        score = 0
        for card in self.hand:
            if card.face == "A":
                if score + card.value[1] > 21:
                    score += card.value[0]  
                else: 
                    score += card.value[1]
            else:
                score+=card.value
        return score
        
    def play(self):
        keep_playing = True
        while keep_playing and not self.bust and not self.blackjack:
            choice = input("(H)it or (S)tay: ")
            if choice in {"H", "h", "Hit", "hit"}:
                self.hit(self.deck.draw())
            elif choice in {"S", "s", "Stay", "stay"}:
                self.stay()
                keep_playing = False
            # elif split:
            # elif double:
            else:
                print("Invalid Selection! Select Again")
            print(self.show_hand())
            if self.blackjack:
                print("21!")
                keep_playing = False
        
        return
    
    def show_hand(self):
        hand_str = ""
        for card in self.hand:
            hand_str += card.front
        return hand_str

class Dealer(Player):
    def __init__(self, deck):
        super().__init__(deck, "Dealer")
        return

    def show_hidden(self):
        for card in self.hand:
            if card.facedown==True:
                return card.flip_show()

    def play(self):
        bust = False
        if self.score() > 21:
            bust = True
        elif self.score() < 16:
            while self.score() < 17:
                self.hit(self.deck.draw())
        else:
            self.stay()

        return bust

    
    


