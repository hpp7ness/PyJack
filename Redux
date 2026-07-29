import json
from random import shuffle

try:
    with open("caps.json", "r") as f:
        caps = json.load(f)
except (FileNotFoundError, KeyError):
    caps = 5

def game(caps):
    print("Caps:", caps)
    
    card_values = ["A", 2, 3, 4, 5, 6, 7, 8, 9, 10, "J", "Q", "K"]
    deck = []
    for value in card_values:
        for i in range(4):
            deck.append(value)
    
    while True:
        try:
            num_decks = int(input("How many decks would you like to use? "))
            if num_decks < 1:
                print("Please use a positive number!")
            else:
                deck *= num_decks
                break
        except ValueError:
            print("Please use numbers!")
    shuffle(deck)
    
    bet = 0
    while bet > caps or bet <= 0: # Makes sure bet is a valid numerical value (needs upgrading to refuse non-numbers)
        try:
            bet = int(input("What is your bet? ")) 
            if bet > caps:
                print("You can not bet more caps than you have!")
            if bet == 0:
                print("You can not bet nothing!")
            if bet < 0:
                print("You can not bet less than nothing!")
        except ValueError:
            print("Please bet with numbers, not letters!")
    player_hand = []
    
    for i in range(2):
        player_hand.append(deck.pop(-1))
    
    def hand_value(hand):
        hand_copy = sorted(hand, key=lambda x: card_values.index(x), reverse=True)
        value = 0
        for card in hand_copy:
            if card in ['J', 'Q', 'K']:
                value += 10
            elif not card == 'A':
                value += int(card)
            if card == 'A':
                if value + 11 > 21:
                    value += 1  
                else:                
                    value += 11
        return value
    
    player_hand_value = hand_value(player_hand)
    if player_hand_value == 21 and len(player_hand) == 2: # Player has blackjack
        print("Blackjack!")
        caps += bet*1.5
        return(caps)
        
    while True:
        player_hand_value = hand_value(player_hand)
        
        print(" ")
        print("Hand:", player_hand)
        print("Hand value:", player_hand_value)
        print(" ")
        
        move = str(input("Hit, stand, or double? h/s/d "))
        
        if move == "h":
            player_hand.append(deck.pop(-1))
        elif move == "s":
            break
        elif move == "d":
            bet *= 2
            player_hand.append(deck.pop(-1))
            break
        else:
            print("Invalid move!")
    player_hand_value = hand_value(player_hand)
    print(" ")
    
    bot_hand = []
    while hand_value(bot_hand) < 17:
        bot_hand.append(deck.pop(-1))
        
    bot_hand_value = hand_value(bot_hand)
    
    print("Hand:", player_hand)
    print("Hand value:", player_hand_value)
    print(" ")
    print("Bot hand:", bot_hand)
    print("Bot hand value:", bot_hand_value)
    print(" ")
    
    if player_hand_value > 21: # Player busts
        if not bot_hand_value > 21:
            print("Bust!")
            if caps - bet < 5:
                caps = 5
            else:
                caps -= bet
        else: # Both bust
             print("Tie!")
    else:
        if bot_hand_value > 21: # Bot busts
            print("Bot busted! You win!")
            caps += bet
        else: # Neither busts
            if player_hand_value > bot_hand_value: # Player has higher hand value
                print("You win!")
                caps += bet
            elif bot_hand_value > player_hand_value: # Bot has higher hand value
                print("Bot wins!")
                if caps - bet < 5:
                    caps = 5
                else:
                    caps -= bet
            elif bot_hand_value == player_hand_value: # Tie / Push
                print("Push!")
                
    print("Caps:", caps)
    return(caps)

while True:
    caps = game(caps)
    play_again = input("Play again? Y/n ")
    
    with open("caps.json", "w") as f:
        json.dump(caps, f)

    if play_again == "Y":
        continue
    else:
        break
