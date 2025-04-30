from evaluating import evaluate_preflop, evaluate_hand

all_in = False

# Preflop Betting
def preflop(player_cards, chips):
    # Evaluate the strength of the player's hole cards
    preflop_strength = evaluate_preflop(player_cards)
    print("Preflop evaluation:", preflop_strength)

    # Define betting percentages based on hand strength
    strength_to_bet = {
        "strong": 0.2,       # Strong hands bet 20% of chips
        "Moderate": 0.1,     # Moderate hands bet 10% of chips
        "High card": 0.05,   # High card hands bet 5% of chips
        "Weak": 0            # Weak hands do not bet
    }

    # Ask the player if they go first
    first = input("Is it your turn? (y/n): ")

    # Calculate the target bet amount based on hand strength and available chips
    target_bet = int(chips * strength_to_bet.get(preflop_strength, 0))
    target_bet = min(target_bet, chips)  # Ensure the bet does not exceed available chips
    global all_in

    if first.lower() == 'y':
        # Player goes first
        print(f"Raised {target_bet} chips")
        opponent_bet = int(input("Enter opponent's value: "))
        if opponent_bet == -1:
            # Opponent folded
            print("Opponent folded.")
            return 0, -1
        elif opponent_bet == target_bet:
            # Opponent called your raise
            print(f"Opponent Called {target_bet} chips.")
            return target_bet, opponent_bet 

        # Handle opponent's initial raise and subsequent re-raises
        while True and all_in != True:
            #handels if the opponent went all in but was less the target_bet, stops the loop from keep going
            if opponent_bet == -2:
                all_in_amount = int(input("Enter the amount opponent went all-in for: "))
                print(f"Opponent went all-in for {all_in_amount} chips.")
                all_in = True  #global boolean flag to also tell street betting that opponent went all in in preflop
                return target_bet, all_in_amount
            # Fold if the opponent's bet exceeds 30% of chips and the hand is weak
            if preflop_strength == "Weak" or preflop_strength == "High card":
                if opponent_bet > chips * 0.3:
                    print("Folded")
                    return -1, opponent_bet
                else:
                    # Call the opponent's bet if it is manageable
                    print(f"Called {opponent_bet} chips")
                    return opponent_bet, opponent_bet

            # If the opponent bets 0, raise the target bet amount
            elif opponent_bet == 0:
                print(f"Raised {target_bet} chips")
                opponent_bet = int(input("Enter opponent's next raise value: "))
                if opponent_bet == -1:
                    # Opponent folded
                    print("Opponent folded.")
                    return target_bet, -1
                elif opponent_bet == target_bet:
                    # Opponent called your raise
                    print(f"Opponent called {target_bet} chips.")
                    return target_bet, opponent_bet

            # If the opponent bets less than the target bet amount
            elif opponent_bet < target_bet:
                print(f"Raised {target_bet} chips")
                opponent_bet = int(input("Enter opponent's next raise value: "))
                if opponent_bet == -1:
                    # Opponent folded
                    print("Opponent folded.")
                    return target_bet, -1
                elif opponent_bet == target_bet:
                    # Opponent called your raise
                    print(f"Opponent called {target_bet} chips.")
                    return target_bet, opponent_bet
                

            # If the opponent bets more than or equal to the target bet amount
            elif opponent_bet >= target_bet:
                if opponent_bet > chips and (preflop_strength == "moderate" or preflop_strength == "strong"):
                    # Go all-in if the opponent's bet exceeds available chips and the hand is strong or moderate
                    print("All in")
                    return chips, opponent_bet
                elif opponent_bet > chips and preflop_strength != "moderate" and preflop_strength != "strong":
                    # Fold if the opponent's bet exceeds available chips and the hand is weak
                    print("Folded")
                    return -1, opponent_bet
                else:
                    # Call the opponent's bet
                    print(f"Called {opponent_bet} chips")
                    return opponent_bet, opponent_bet
        return 0

    else:
        # Opponent goes first
        opponent_bet = int(input("Enter opponent's raise value: "))
        if opponent_bet == -1:
            # Opponent folded
            print("Opponent folded.")
            return 0, -1
        elif opponent_bet == target_bet:
            # Opponent called your raise
            print(f"called {target_bet} chips.")
            return target_bet, opponent_bet

        # Handle opponent's initial raise and subsequent re-raises
        while True and all_in != True:
        #handels if the opponent went all in, stops the loop from keep going
            if opponent_bet == -2:
                # Opponent went all-in
                all_in_amount = int(input("Enter the amount opponent went all-in for: "))
                print(f"Opponent went all-in for {all_in_amount} chips.")
                bet = min(chips,all_in_amount)  #Checks to see if the opponet went all in for was more than what is have
                if chips == bet:
                    print(f"I went all in for {bet}")
                if bet == all_in_amount:
                    print(f"Called opponets bet of {bet}")
                all_in = True
                return bet, all_in_amount
            # Fold if the opponent's bet exceeds 30% of chips and the hand is weak
            if preflop_strength == "Weak" or preflop_strength == "High card":
                if opponent_bet > chips * 0.3:
                    print("Folded")
                    return -1, opponent_bet
                else:
                    # Call the opponent's bet if it is manageable
                    print(f"Called {opponent_bet} chips")
                    return opponent_bet, opponent_bet

            # If the opponent bets 0, raise the target bet amount
            elif opponent_bet == 0:
                print(f"Raised {target_bet} chips")
                opponent_bet = int(input("Enter opponent's next raise value: "))
                if opponent_bet == -1:
                    # Opponent folded
                    print("Opponent folded.")
                    return target_bet, -1
                elif opponent_bet == target_bet:
                    # Opponent called your raise
                    print(f"Opponent called {target_bet} chips.")
                    return target_bet, opponent_bet

            # If the opponent bets less than the target bet amount, raise based on hand strength
            elif opponent_bet < target_bet:
                print(f"Raised {target_bet} chips")
                opponent_bet = int(input("Enter opponent's next raise value: "))
                if opponent_bet == -1:
                    # Opponent folded
                    print("Opponent folded.")
                    return target_bet, -1
                elif opponent_bet == target_bet:
                    # Opponent called your raise
                    print(f"Opponent called {target_bet} chips.")
                    return target_bet, opponent_bet
                

            # If the opponent bets more than or equal to the target bet amount
            elif opponent_bet >= target_bet:
                if opponent_bet > chips and (preflop_strength == "moderate" or preflop_strength == "strong"):
                    # Go all-in if the opponent's bet exceeds available chips and the hand is strong or moderate
                    print("All in")
                    return chips, opponent_bet
                elif opponent_bet > chips and preflop_strength not in ["moderate", "strong"]:
                    # Fold if the opponent's bet exceeds available chips and the hand is weak
                    print("Folded")
                    return -1, opponent_bet
                else:
                    # Call the opponent's bet
                    print(f"Called {opponent_bet} chips")
                    return opponent_bet, opponent_bet
        return 0,0



# Generalized Betting for Flop, Turn, and river
def street_betting(player_cards, board_cards, chips, street_name):
    is_turn = input(f"Is it your turn on the {street_name}? (y/n): ")

    all_cards = player_cards + board_cards
    evaluation, _ = evaluate_hand(all_cards)
    street_score = evaluation[0]

    print(f"{street_name} evaluation:", street_score)

    score_to_base = {
        1: 0.1,  # High card
        2: 0.2,  # One pair
        3: 0.3,  # Two pair
        4: 0.4,  # Three of a kind
        5: 0.5,  # Straight
        6: 0.6,  # Flush
        7: 0.7,  # Full house
        8: 0.8,  # Four of a kind
        9: 0.9,  # Straight flush
        10: 1.0  # Royal flush
    }

    street_multiplier = {
        "Flop": 1.0,
        "Turn": 1.2,
        "River": 1.5
    }

    #caculates bet amount based of stree score and name
    base_bet_percentage = score_to_base.get(street_score, 0)
    multiplier = street_multiplier.get(street_name, 1.0)
    bet_amount = int(chips * base_bet_percentage * multiplier)
    bet_amount = min(bet_amount, chips)
    global all_in

    #if I am first
    if is_turn.lower() == 'y':
        print(f"Raised {bet_amount} chips")
        #Gets opponets input
        opponent_bet = int(input(f"Enter opponent's raise value on the {street_name}: "))
        if opponent_bet == -1: #If they folded
            print("Opponent folded.")
            return 0, -1
        elif opponent_bet == bet_amount:
            # Opponent called your raise
            print(f"Opponent called {bet_amount} chips.")
            return bet_amount, opponent_bet 

        #Need loop to handel rerasing
        while True and all_in != True:
            #handels if the opponent went all in but was less the target_bet, stops the loop from keep going
            if opponent_bet == -2:
                # Opponent went all-in
                all_in_amount = int(input("Enter the amount opponent went all-in for: "))
                print(f"Opponent went all-in for {all_in_amount} chips.")
                all_in = True
                return bet_amount, all_in_amount
            #if my score is low then either fold or call based on opponent bet
            if street_score == 1:
                if opponent_bet > chips * 0.3:
                    print("Folded")
                    return -1, opponent_bet
                else:
                    print(f"Called {opponent_bet} chips")
                    return opponent_bet, opponent_bet
                
            #If opponenet bet 0 then I will raise and ask them again for the new value since I reraised
            elif opponent_bet == 0:
                print(f"Raised {bet_amount} chips")
                opponent_bet = int(input("Enter opponent's next raise value: "))
                if opponent_bet == -1:
                    print("Opponent folded.")
                    return bet_amount, -1
                elif opponent_bet == bet_amount:
                    # Opponent called your raise
                    print(f"Opponent called {bet_amount} chips.")
                    return bet_amount, opponent_bet

            #if the opponent bet was less than my bet amount then I will raise my bet and ask them what their new value is
            elif opponent_bet < bet_amount:
                print(f"Raised {bet_amount} chips")
                opponent_bet = int(input("Enter opponent's next raise value: "))
                if opponent_bet == -1:
                    print("Opponent folded.")
                    return bet_amount, -1
                elif opponent_bet == bet_amount:
                    # Opponent called your raise
                    print(f"Opponent called {bet_amount} chips.")
                    return bet_amount, opponent_bet

            #if they bet more than my bet amount
            elif opponent_bet >= bet_amount:
                #if the bet was more than my chips and i have a high score go all in
                if opponent_bet > chips and street_score >= 3:
                    print("All in")
                    return chips, opponent_bet
                #if low score fold
                elif opponent_bet > chips and street_score < 3:
                    print("Folded because of weak hand")
                    return -1, opponent_bet
                #else they bet less than my total chips i will just call
                else:
                    print(f"Called {opponent_bet} chips")
                    return opponent_bet, opponent_bet
        return 0,0

    #I am second
    else:
        #Get the value that the opponent raised
        opponent_bet = int(input(f"Enter opponent's raise value on the {street_name}: "))
        if opponent_bet == -1:
            print("Opponent folded.")
            return 0, -1
        #if their amount they raised is equal to my bet amount then just call
        elif opponent_bet == bet_amount:
            # Opponent called your raise
            print(f"called {bet_amount} chips.")
            return bet_amount, opponent_bet      

        while True and all_in != True:
            #handels if the opponent went all in, stops the loop from keep going
            if opponent_bet == -2:
                all_in_amount = int(input("Enter the amount opponent went all-in for: "))
                print(f"Opponent went all-in for {all_in_amount} chips.")
                all_in = True
                bet = min(chips,all_in_amount) #Checks to see if opponent went all in for more than what i have
                if chips == bet:
                    print(f"I went all in for {bet}")
                if bet == all_in_amount:
                    print(f"Called opponets bet of {bet}")
                return bet, all_in_amount
            
            #if low score then either fold or call
            if street_score == 1:
                if opponent_bet > chips * 0.3:
                    print("Folded")
                    return -1, opponent_bet
                else:
                    print(f"Called {opponent_bet} chips")
                    return opponent_bet, opponent_bet

            #If they bet zero then I will raise and ask them for their new value
            elif opponent_bet == 0:
                print(f"Raised {bet_amount} chips")
                opponent_bet = int(input("Enter opponent's next raise value: "))
                if opponent_bet == -1:
                    print("Opponent folded.")
                    return bet_amount, -1
                elif opponent_bet == bet_amount:
                    # Opponent called my raise
                    print(f"Opponent called {bet_amount} chips.")
                    return bet_amount, opponent_bet

            #if opponenet bet is less than my bet amount then I will raise and ask them for their new bet
            elif opponent_bet < bet_amount:
                print(f"Raised {bet_amount} chips")
                opponent_bet = int(input("Enter opponent's next raise value: "))
                if opponent_bet == -1:
                    print("Opponent folded.")
                    return bet_amount, -1
                elif opponent_bet == bet_amount:
                    # Opponent called my raise
                    print(f"Opponent called {bet_amount} chips.")
                    return bet_amount, opponent_bet

            #if the opponenet bet was greater than my bet amount
            elif opponent_bet >= bet_amount:
                #if greater than my total chips and have a high score go all in
                if opponent_bet > chips and street_score >= 3:
                    print("All in")
                    return chips, opponent_bet
                #low score fold
                elif opponent_bet > chips and street_score < 3:
                    print("Folded because of weak hand")
                    return -1, opponent_bet
                #else they bet less than by max chips and I just call
                else:
                    print(f"Called {opponent_bet} chips")
                    return opponent_bet, opponent_bet
        return 0,0
 


# Flop, Turn and river betting call street_betting with appropriate names
def flop_betting(player_cards, flop, chips):
    return street_betting(player_cards, flop, chips, "Flop")

def turn_betting(player_cards, turn, chips):
    return street_betting(player_cards, turn, chips, "Turn")

def river_betting(player_cards, river, chips):
    return street_betting(player_cards, river, chips, "River")
