import random

# Deck of cards
class Card:
    def __init__(self, suit, value):
        self.suit = suit
        self.value = value
    
    def __repr__(self):
        return " of ".join((self.value, self.suit))

class Deck:
    def __init__(self):
        self.cards = [Card(s, v) for s in ["Spades", "Clubs", "Hearts", "Diamonds"]
                      for v in ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]]

    def shuffle(self):
        if len(self.cards) > 1:
            random.shuffle(self.cards)
    
    def deal(self):
        if len(self.cards) > 1:
            return self.cards.pop(0)

class Hand:
    def __init__(self, dealer=False):
        self.dealer = dealer
        self.cards = []
        self.value = 0

    def add_card(self, card):
        self.cards.append(card)

    def calculate_value(self):
        self.value = 0
        ace_count = 0
        for card in self.cards:
            if card.value.isnumeric():
                self.value += int(card.value)
            elif card.value == "A":
                ace_count += 1
                self.value += 11  # Add Ace as 11 initially
            else:
                self.value += 10
        
        # Adjust for Aces if the value is over 21
        while self.value > 21 and ace_count:
            self.value -= 10  # Convert one Ace from 11 to 1
            ace_count -= 1
    
    def get_value(self):
        self.calculate_value()
        return self.value
    
    def display(self):
        if self.dealer:
            print("hidden")
            print(self.cards[1])
        else:
            for card in self.cards:
                print(card)
            print("Value:", self.get_value())

# This is how the game works
class Game:
    def __init__(self):
        pass

    def play(self):
        playing = True

        while playing:
            self.deck = Deck()
            self.deck.shuffle()

            self.player_hand = Hand()
            self.dealer_hand = Hand(dealer=True)

            # Initial deal: 2 cards to each player and dealer
            for i in range(2):
                self.player_hand.add_card(self.deck.deal())
                self.dealer_hand.add_card(self.deck.deal())
            
            print("Your hand is:")
            self.player_hand.display()
            print()
            print("Dealer's hand is: ")
            self.dealer_hand.display()

            game_over = False
            doubled_down = False

            while not game_over:
                player_has_blackjack, dealer_has_blackjack = self.check_for_blackjack()

                if player_has_blackjack or dealer_has_blackjack:
                    game_over = True
                    self.show_blackjack_results(player_has_blackjack, dealer_has_blackjack)
                    continue
                
                choice = input("Please choose [Hit/Stand/Double Down] ").lower()
                while choice not in ["h", "s", "d", "hit", "stand", "double"]:
                    choice = input("Please choose [Hit/Stand/Double Down] or (h/s/d)").lower()
                
                if choice in ['double', 'd'] and not doubled_down:
                    self.player_hand.add_card(self.deck.deal())
                    print("You doubled down and drew:")
                    self.player_hand.display()
                    doubled_down = True
                    if self.player_is_over():
                        print("You have lost!")
                        game_over = True
                    else:
                        choice = 'stand'  # Automatically stand after doubling down

                if choice in ['hit', 'h'] and not doubled_down:
                    self.player_hand.add_card(self.deck.deal())
                    self.player_hand.display()
                    if self.player_is_over():
                        print("You have lost!")
                        game_over = True
                elif choice in ['stand', 's'] or doubled_down:
                    # Dealer's turn: draw until 17 or above
                    while self.dealer_hand.get_value() < 17:
                        new_card = self.deck.deal()
                        self.dealer_hand.add_card(new_card)
                        print("Dealer draws:", new_card)
                        print("Dealer's hand value:", self.dealer_hand.get_value())

                    player_hand_value = self.player_hand.get_value()
                    dealer_hand_value = self.dealer_hand.get_value()

                    print("Final Results")
                    print("Your hand:", player_hand_value)
                    print("Dealer's hand:", dealer_hand_value)

                    if player_hand_value > 21:
                        print("You Bust! Dealer Wins!")
                    elif dealer_hand_value > 21:
                        print("Dealer Busts! You Win!")
                    elif player_hand_value > dealer_hand_value:
                        print("You Win!")
                    elif player_hand_value == dealer_hand_value:
                        print("Tie!")
                    else:
                        print("Dealer Wins!")

                    game_over = True

            again = input("Play Again? (Y/N) ")
            while again.lower() not in ["y", "n"]:
                again = input("Please enter Y or N ")
            if again.lower() == "n":
                print("Thanks for playing!")
                playing = False
            else:
                game_over = False

    def player_is_over(self):
        return self.player_hand.get_value() > 21

    def check_for_blackjack(self):
        player = False
        dealer = False
        if self.player_hand.get_value() == 21 and len(self.player_hand.cards) == 2:
            player = True
        if self.dealer_hand.get_value() == 21 and len(self.dealer_hand.cards) == 2:
            dealer = True

        return player, dealer

    def show_blackjack_results(self, player_has_blackjack, dealer_has_blackjack):
        if player_has_blackjack and dealer_has_blackjack:
            print("Both players have blackjack! Draw!")
        elif player_has_blackjack:
            print("Player has blackjack! Player wins!")
        elif dealer_has_blackjack:
            print("Dealer has blackjack! Dealer wins!")

if __name__ == "__main__":
    g = Game()
    g.play()
    