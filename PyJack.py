import random
from pynput import keyboard
import json
import msvcrt

# I did this shit in two days bro :skull emoji:

def save_game(tokens): # Game info save logic
     with open("save.json", "w") as f:
         json.dump({"tokens": tokens},
f)
         
def load_game(): # Game info load logic
     try:
         with open("save.json", "r") as f:
             data = json.load(f)
             return data["tokens"]
     except FileNotFoundError:
         return 5

def IsFace(card): # Returns true on face cards
     return card in ("K", "Q", "J") 

def IsAce(card): # Returns true on ace
     if card == "A":
         return True
     else:
         return False
     
def Value(cards): # Calculates calue of hand
         total = 0
         aces = 0
         for card in cards:
             if IsFace(card): # Adds all face cards (worth 10 each)
                 total = total + 10
             elif IsAce(card): # Adds up ace amount
                 aces = aces + 1
             else:
                 total = total + card # Add numerical cards
         for card in range(aces): # Decides if aces should be valued at 11 or 1
             if total + 11 <= 21: 
                 total = total + 11
             else: 
                 total = total + 1 
         return total

def Bust(input): # Returns true if value of hand is more than 21 (a bust)
     if input > 21:
         return True
     else:
         return False 

def flush_input(): # Clears the stdin, so that the last round's pynput keystrokes don't clog the input()'s for "bet" or "Keep playing? y/n"
    while msvcrt.kbhit():
        msvcrt.getch()

def play_game(tokens): # Per round process
     
     flush_input()
     print(f"You have {tokens} tokens to bet!")
     bet = 0
     while bet > tokens or bet <= 0: # Makes sure bet is a valid numerical value (needs upgrading to refuse non-numbers)
         try:
             bet = int(input("What is your bet? ")) 
             if bet > tokens:
                 print("You can not bet more tokens than you have!")
             if bet == 0:
                 print("You can not bet nothing!")
             if bet < 0:
                 print("You can not bet less than nothing!")
         except ValueError:
             print("Please bet with numbers, not letters!")


     def BustInform(cards): # Tells player if they or dealer has busted, along with hands and values of the busted person
         if cards == Hand:
             print(f"Your hand is worth: {Value(cards)}, with cards {Hand} and HAS BUSTED! You lose!")
         else:
             print(f"Dealer hand is worth: {Value(cards)}, with shown cards: {DealerHand} and HAS BUSTED! You WIN!")

     def ValueInform(cards):  # Tells player value of cards and shows their hand, also shows dealer's
         if cards == Hand:
             print(f"Your hand is worth: {Value(cards)}, with cards {cards}")
         else:
             print(f"Dealer hand is worth: {Value(cards)}, with cards: {cards}")

     Deck = []
     while len(Deck) < 52: # Makes a deck 52 cards in length
         Deck.append(random.randint(1,13)) # 11, 12, and 13 are place holders for face cards
         if Deck.count(Deck[-1]) == 5: # Makes sure their are only 4 duplicates per card
             Deck.pop(-1)
     
     for i in range(len(Deck)): # Changes place holders to faces
         if Deck[i] == 13:
             Deck[i] = "K"
         if Deck[i] == 12:
             Deck[i] = "Q"
         if Deck[i] == 11:
             Deck[i] = "J"
         if Deck[i] == 1:
             Deck[i] = "A"
     random.shuffle(Deck) # Shuffles deck

     Hand = []
     for i in range(2): # Deals player 2 cards
        Hand.append(Deck.pop(0))
     ValueInform(Hand)

     DealerHand = [] # Deals dealer 2 cards
     for i in range(2):
        DealerHand.append(Deck.pop(0))
     print(f"Dealer has a shown card of: {DealerHand[0]}")
     
     def Dealer(hand): # Dealer's turn logic
         while Value(hand) < 17: 
             hand.append(Deck.pop(0))
         if Value(hand) >= 17:
             ValueInform(hand)

     def win(): # Win logic
         nonlocal tokens, bet
         tokens = tokens + bet
         bet = 0
         print(f"You WIN! You now have {tokens} tokens!")
         save_game(tokens)
         listener.stop()

     def lose(): # Lose logic
         nonlocal tokens, bet
         tokens = tokens - bet
         if tokens <= 0:
             tokens = 1
         bet = 0
         print(f"You Lose! You now have {tokens} tokens!")
         save_game(tokens)
         listener.stop()

     def tie(): # Tie logic
         nonlocal tokens, bet
         print(f"You have tied! You now have {tokens} tokens!")
         listener.stop()

     def on_press(key): # Key press listener for player actions
         nonlocal tokens, bet
         if key == keyboard.Key.space: # Stand
             print("Dealer will now start their turn!")
             Dealer(DealerHand)
             if Bust(Value(DealerHand)):
                 win()
             else:
                 if Value(Hand) > Value(DealerHand):
                     win()
                 elif Value(Hand) < Value(DealerHand):
                      lose()
                 elif Value(Hand) == Value(DealerHand):
                     tie()    
        
         elif key.char == 'e': # Hit
             Hand.append(Deck.pop(0))
             if Value(Hand) == 21:
                 win()
             elif Bust(Value(Hand)):
                 BustInform(Hand)
                 lose()  
             else:
                 ValueInform(Hand)

         elif key.char == 'q': # Double down
             bet = bet*2
             print(f"Bet doubled to: {bet}")
             Hand.append(Deck.pop(0))
             if Bust(Value(Hand)):
                 BustInform(Hand)
                 lose()
             elif Value(Hand) == 21:
                 win()
             else:
                 ValueInform(Hand)
                 print("Dealer will now start their turn!")
                 Dealer(DealerHand)
                 if Bust(Value(DealerHand)):
                     BustInform(DealerHand) 
                     win()
                 else:
                     if Value(Hand) > Value(DealerHand):
                         win()
                     elif Value(Hand) < Value(DealerHand):
                         lose()
                     elif Value(Hand) == Value(DealerHand):
                         tie()
             save_game(tokens)

     with keyboard.Listener(on_press=on_press,) as listener:
         listener.join()
    
     return tokens # Return updated token count



tokens = load_game() # Load saved tokens or start with 5
while True: # Game repeat
     tokens = play_game(tokens) # Updates token value
     save_game(tokens) # Saves token value for next game
    
     flush_input()
     choice = input("Play again? (y/n) ") # Prompts for next round
     if choice != 'y':
         break

