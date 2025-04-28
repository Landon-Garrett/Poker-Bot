import random 
from itertools import combinations

def main():
    print("Welcome to the poker game!")

    chips = int(input("Enter your chips: "))
    again = 'y'
    while again.lower() != 'n' and chips > 0:
        print(f"Chips equal: {chips}")
        pot = 0
        player_cards = input("Enter your cards: ").split()

        #handles preflop betting
        bet,opponent_bet = preflop(player_cards, chips)
        if bet == -1:
            print(f"You folded. Opponent wins the pot of {opponent_bet} .")
            again = input("Do you want to play again? (y/n): ")
            continue
        if opponent_bet == -1:
            print(f"Opponent folded.I win pot of {bet} chips!")
            chips += bet
            again = input("Do you want to play again? (y/n): ")
            continue
        chips -= bet
        print(f"Chips left: {chips}")
        pot += bet + opponent_bet
        print(f"Pot is: {pot}")

        #handles flop betting
        flop = input("Enter flop cards: ").split()
        bet,opponent_bet = flop_betting(player_cards, flop,chips)
        if bet == -1:
            print(f"You folded. Opponent wins the pot of {pot} .")
            again = input("Do you want to play again? (y/n): ")
            continue
        if opponent_bet == -1:
            print(f"Opponent folded.I win pot of {pot} chips!")
            chips += pot
            again = input("Do you want to play again? (y/n): ")
            continue
        chips -= bet
        print(f"Chips left: {chips}")
        pot += bet + opponent_bet
        print(f"Pot is: {pot}")

        #handles turn betting
        turn = input("Enter turn card: ").split()
        bet,opponent_bet = turn_betting(player_cards, flop + turn,chips)
        if bet == -1:
            print(f"You folded. Opponent wins the pot of {pot} .")
            again = input("Do you want to play again? (y/n): ")
            continue
        if opponent_bet == -1:
            print(f"Opponent folded.I win pot of {pot} chips!")
            chips += pot
            again = input("Do you want to play again? (y/n): ")
            continue
        chips -= bet
        print(f"Chips left: {chips}")
        pot += bet + opponent_bet
        print(f"Pot is: {pot}")

        #handles river betting
        river = input("Enter river card: ").split()
        bet,opponent_bet = river_betting(player_cards, flop + turn + river,chips)
        if bet == -1:
            print(f"You folded. Opponent wins the pot of {pot} .")
            again = input("Do you want to play again? (y/n): ")
            continue
        if opponent_bet == -1:
            print(f"Opponent folded.I win pot of {pot} chips!")
            chips += pot
            again = input("Do you want to play again? (y/n): ")
            continue
        chips -= bet
        print(f"Chips left: {chips}")
        pot += bet + opponent_bet
        print(f"Pot is: {pot}")

        print("Winner is: ")
        opponent_cards = input("Enter opponent's cards: ").split()
        community_cards = flop + turn + river
        winner_index = determine_winner(player_cards, opponent_cards, community_cards)
        if winner_index == 0:
            print(f"I win the pot of {pot} chips!")
            chips += pot
        elif winner_index == 1:
            print(f"Opponent wins the pot of {pot} chips!")
        else:
            print("It's a tie! Both players win half the pot.")
            print(f"Each player wins {pot//2} chips!")
            chips += pot // 2

        again = input("Do you want to play again? (y/n): ")

# Preflop Betting
def preflop(player_cards, chips):
    preflop_strength = evaluate_preflop(player_cards)
    print("Preflop evaluation:", preflop_strength)

    strength_to_bet = {
        "strong": 0.2,
        "Moderate": 0.1,
        "High card": 0.05,
        "Weak": 0
    }

    first = input("Is it your turn? (y/n): ")

    if first.lower() == 'y':
        initial_bet = int(chips * strength_to_bet.get(preflop_strength, 0))
        print(f"Raised {initial_bet} chips")
        return initial_bet,0
    
    else:
        opponent_bet = int(input("Enter opponent's raise value: "))

        if opponent_bet == -1:
            print("Opponent folded.")
            return 0,-1 #because he is folding we return -1 to indicate that the game is over

        if preflop_strength == "Weak":
            if opponent_bet > chips * 0.2:
                print("Folded")
                return -1,opponent_bet #because we are folding, we return -1 to indicate that the game is over
            else:
                print(f"Called {opponent_bet} chips")
                bet = opponent_bet
                return bet,opponent_bet

        target_bet = int(chips * strength_to_bet.get(preflop_strength, 0))

    if opponent_bet == 0:
        print(f"Raised {target_bet} chips")
        return target_bet,opponent_bet
    elif opponent_bet < target_bet:
        if preflop_strength == "strong":
            raise_amount = opponent_bet * 2
        elif preflop_strength == "Moderate":
            raise_amount = opponent_bet * 1.5
        else:
            raise_amount = opponent_bet * 1.2
        print(f"Raised {raise_amount} chips")
        return raise_amount,opponent_bet
    elif opponent_bet > target_bet:
        #if opponent bets more than chips and we have a strong or moderate hand, we go all in
        if opponent_bet > chips and preflop_strength == "moderate" or preflop_strength =="strong":
            print("All in")
            bet = chips
        #if opponent bets more than chips and we have a weak hand, we fold
        elif opponent_bet > chips and preflop_strength != "moderate" or preflop_strength != "strong":
            print("Folded")
            return -1,opponent_bet
        #else if opponents bets less than chips, we call the bet
        else:
            print(f"Called {opponent_bet} chips")
            bet = opponent_bet
        return bet,opponent_bet


# Generalized Betting for Flop, Turn, and river
def street_betting(player_cards, board_cards, chips, street_name):
    is_turn = input(f"Is it your turn on the {street_name}? (y/n): ")
    all_cards = player_cards + board_cards
    evaluation, _ = evaluate_hand(all_cards)
    street_score = evaluation[0]

    print(f"{street_name} evaluation:", street_score)

    # Base percentages depending on hand strength
    score_to_base = {
        1: 0.1,    # High card
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

    # Different aggressiveness based on street
    street_multiplier = {
        "Flop": 1.0,
        "Turn": 1.5,
        "River": 2.0
    }

    #used to determine the bet amount based on the street score and street name
    base_bet_percentage = score_to_base.get(street_score, 0)
    multiplier = street_multiplier.get(street_name, 1.0)
    bet_amount = int(chips * base_bet_percentage * multiplier)

    if is_turn.lower() == 'y':
        if bet_amount == 0:
            print("Checked 0 chips")
        else:
            print(f"Raised {bet_amount} chips")
        return bet_amount,0
    
    else:
        opponent_bet = int(input(f"Enter opponent's raise value on the {street_name}: "))

        if opponent_bet == -1:
            print("Opponent folded.")
            return 0,-1 #because he is folding we return -1 to indicate that the game is over
            
        # Only activates when deciding to fold based on preflop or weak postflop hand, does not fold on strong hand during preflop
        if (street_name == "Preflop" and evaluate_preflop(player_cards) != "strong") or (street_name != "Preflop" and street_score == 1):
            if opponent_bet > chips * 0.3:
                print("Folded")
                return -1, opponent_bet  # Return -1 to indicate fold
            else:
                print(f"Called {opponent_bet} chips")
                bet = opponent_bet
                return bet, opponent_bet


        if opponent_bet == 0:
            print(f"Raised {bet_amount} chips")
            return bet_amount,opponent_bet
        elif opponent_bet < bet_amount:
            raise_amount = int(opponent_bet * street_multiplier.get(street_name, 1.0))
            print(f"Raised {raise_amount} chips")
            return raise_amount,opponent_bet
        elif opponent_bet > bet_amount:
            #if opponent bets more than chips and we have a hand stronger than 2 (one pair), we go all in
            if opponent_bet > chips and street_score >= 2:
                print("All in")
                bet = chips
            #if opponent bets more than chips and we have a hand weaker than 2 (one pair), we fold
            elif opponent_bet > chips and street_score < 2:
                print("Folded because of weak hand")
                return -1,opponent_bet
            #else if opponents bets less than chips, we call the bet
            else:
                print(f"Called else {opponent_bet} chips")
                bet = opponent_bet
            return bet,opponent_bet
 


# Flop, Turn and river betting call street_betting with appropriate names
def flop_betting(player_cards, flop, chips):
    return street_betting(player_cards, flop, chips, "Flop")

def turn_betting(player_cards, turn, chips):
    return street_betting(player_cards, turn, chips, "Turn")

def river_betting(player_cards, river, chips):
    return street_betting(player_cards, river, chips, "River")

#handles preflop evaluation
def evaluate_preflop(hole_cards):
    #Evaluate the strength of the hole cards preflop.
    ranks = '23456789TJQKA'

    #Extracts the suits from the hole cards
    suits = []
    for card in hole_cards:
        suits.append(card[1])

    #Extracts the rank values from the hole cards
    rank_values = []
    for card in hole_cards:
        rank_values.append(ranks.index(card[0]))

    # Check for pocket pairs
    if rank_values[0] == rank_values[1]:
        return "strong"                         #pocket pair

    # Check for suited cards
    if suits[0] == suits[1]:
        if abs(rank_values[0] - rank_values[1]) == 1:  
            return "strong"                     #suited connectors
        return "Moderate"                       #suited cards
    
    #Check for offsuit cards
    if abs(rank_values[0] - rank_values[1]) == 1:
        return "Moderate"                       #offsuit connectors
    
    #Check for multiple face cards (T, J, Q, K, A), by checking if all ranks are >= T
    if all(rank >= ranks.index('T') for rank in rank_values):
        return "strong"  # multiple face cards

    # Check for high cards, by finding the max rank value and checking if it is >= T
    if max(rank_values) >= ranks.index('T'):
        return "High card"                      #high cards

    # Default case
    return "Weak"                                #low cards

def score(hand):
    ranks = '23456789TJQKA'

    # Convert card ranks to numerical values for comparison
    rank_values = []
    for card in hand:
        r = card[0]  # Extract the rank (first character of the card)
        rank_index = ranks.find(r)  # Find the index of the rank in the ranks string
        rank_values.append(rank_index)

    #counts the occurrences of each rank in the hand, needed for hand evaluation
    # Dictionary to store the counts of each rank,keys are the unique ranks(e.g, 1,2,3,12) 
    # and values is their frequency
    rank_counts = {} 
    unique_ranks = set(rank_values)  # Get unique ranks from rank_values by converting it to a set
    for rank in unique_ranks:
        count = rank_values.count(rank)  # Count occurrences of the rank in rank_values
        rank_counts[rank] = count  # Add the rank and its count to the dictionary   

    # Sorts only the frequency of each rank in descending order,by retrieving the values from the dictionary
    #reversing ensures that the highest counts come first
    #used to determine the type of hand (e.g., pair, two pair, three of a kind, etc.)
    counts = sorted(rank_counts.values(), reverse=True) 

    # Sorts only the unique ranks based on the frequency of their occurrences and then by their rank value
    #key=lambda specifies a function to be called on each element before comparison
    #-rank_counts[x] is used to sort the ranks first by their frequency in descending order (higher counts first)
    #-x is is used if two ranks have the same count, sorts rank value in descending order
    sorted_ranks = sorted(rank_counts, key=lambda x: (-rank_counts[x], -x)) 
    #e.g, rank_counts = {12: 1, 1: 2, 2: 3} => sorted_ranks = [2, 1, 12]

    # Check for flush (all cards have the same suit)
    suits = []
    for card in hand:
        suits.append(card[1]) # Extract the suit (second character of the card)
    #checks if all suits are the same, by converting the list of suits to a set which removes duplicates 
    # and checking its length
    flush = len(set(suits)) == 1 #(T/F)

    # Check for straight (5 consecutive ranks)
    rank_range = max(rank_values) - min(rank_values)
    #checks if the number of unique ranks is 5 since a straight requires 5 unique ranks
    #and the difference between the highest and lowest rank is 4
    straight = len(rank_counts) == 5 and rank_range == 4

    # Special case: 5-high straight (A, 2, 3, 4, 5), and also check for 5 high straight flush
    if set(rank_values) == {12, 0, 1, 2, 3}:  # Ace is treated as 
        straight = True
        sorted_ranks = [3, 2, 1, 0, 12]
        if flush:
            return (9,), sorted_ranks # Straight flush
    
    # Royal flush
    if flush and straight and max(rank_values) == ranks.find('A'):
        return (10,), sorted_ranks

    # Straight flush
    if flush and straight:
        return (9,), sorted_ranks

    # Four of a kind
    if counts == [4, 1]:
        return (8,), sorted_ranks

    # Full house
    if counts == [3, 2]:
        return (7,), sorted_ranks

    # Flush
    if flush:
        return (6,), sorted_ranks

    # Straight
    if straight:
        return (5,), sorted_ranks

    # Three of a kind
    if counts == [3, 1, 1]:
        return (4,), sorted_ranks

    # Two pair
    if counts == [2, 2, 1]:
        return (3,), sorted_ranks

    # One pair
    if counts == [2, 1, 1, 1]:
        return (2,), sorted_ranks

    # High card
    return (1,), sorted_ranks

def evaluate_hand(hand):
    best_hand = None
    best_score = None

    # Iterate through all 5-card combinations
    for hand in combinations(hand, 5):
        hand_score = score(hand)  # Evaluate the score of the current hand
        if best_score is None or hand_score > best_score:
            best_hand = hand  # Update the best hand
            best_score = hand_score  # Update the best score

    return score(best_hand)  # Return the score of the best hand

def determine_winner(player_cards, opponent_cards, community_cards):
    # Combine hole cards with community cards
    player_hand = player_cards + community_cards
    opponent_hand = opponent_cards + community_cards

    # Format hands as strings for the poker function
    hands = [" ".join(player_hand), " ".join(opponent_hand)]

    # Evaluate the hands
    player_score = evaluate_hand(player_hand)
    opponent_score = evaluate_hand(opponent_hand)

    # Compare full scores directly
    if player_score > opponent_score:
        winner_index = 0
    elif player_score < opponent_score:
        winner_index = 1
    else:
        winner_index = -1  # Tie

    # Find the best 5-card hand for display
    if winner_index != -1:
        # Get the best 5-card hand from the winner's cards by comparing all combinations
        # and using the score function to determine the best hand 
        best_5_card_hand = max(combinations(hands[winner_index].split(), 5), key=score)    
        best_5_card_hand_str = " ".join(best_5_card_hand) # Convert to string for display

        # Get the score of the best 5-card hand by calling the score function
        #,_ means that we are not interested in the second element of the tuple returned by the score function
        hand_score, _ = score(best_5_card_hand)

        #create a dictionary to map hand scores to their types
        hand_types = {
            10: "Royal Flush",
            9: "Straight Flush",
            8: "Four of a Kind",
            7: "Full House",
            6: "Flush",
            5: "Straight",
            4: "Three of a Kind",
            3: "Two Pair",
            2: "One Pair",
            1: "High Card"
        }
        # Get the type of hand based on the score
        #hand_score[0] is used to get the first element of the tuple returned by the score function
        winning_hand_type = hand_types[hand_score[0]]

        if winner_index == 0:
            print(f"The winning 5-card hand is mine: {best_5_card_hand_str}, type: {winning_hand_type}")
        elif winner_index ==1:
            print(f"The winning 5-card hand is the opponent: {best_5_card_hand_str}, type: {winning_hand_type}")
    else:
        print("It's a tie!")

    return winner_index

def decide_action(player_hand_strength, oppenent_hand_strength, opponent_bet, round_stage):
    # Player's decision 
    if round_stage == "pre-flop":
        #Pre-flop decision based on hand strength
        if player_hand_strength >= 8: #Strong hand 
            return "bet"
        elif player_hand_strength >= 5: # Moderate hand  
            return "call" # Call if hand is not too weak
        else:
            return "fold" #Weak hand, fold 
            
    elif round_stage in ["flop", "turn", "river"]:
        #Post-flop, turn, or river, decisions based on hand strength and opponent's actions
        if player_hand_strength >= 8: #Strong hand 
            if oppenent_bet > 0:
                return "raise"    #Raise if opponent bet
            return "bet" #Otherwise, bet 
        elif player_hand_strength >= 5:    #moderate hand 
            if oppenent_bet > 0:
                return "call" #Call if opponent bet 
            return "check"    #Otherwise, check 
        else:
            return "fold"    #Weak hand, fold 

def simulate_hand():
    #Create a deck of cards 
    deck = [f"{rank}{suit}" for rank in "23456789TJQKA" for suit in "cdhs"]

    #Shuffle deck 
    random.shuffle(deck)

    #Deal 2 cards each 
    player_cards = [deck.pop(), deck.pop()]
    oppenent_cards = [deck.pop(), deck.pop]

    #Deal community cards (5 cards: flop, turn, and river)
    community_cards = [deck.pop() for _ in range(5)]

    print(f"Player's Cards: {player_cards}") 
    print(f"Oppenent's Cards: {oppenent_cards}")
    print(f"Community Cards: {community_cards}")

    #Simulate pre-flop action (before community cards are revealed)
    player_hand_strength = evaluate_hand(player_cards)
    oppenent_hand_strength = evaluate_hand(opponent_cards)
    round_stage = "pre-flop"
    
    #Simulate opponent's action (random for now)
    opponent_actions = ["bet", "check", "fold"]
    opponent_action = random.choice(oppenent_actions)
    print(f"Opppnent's action pre-flop: {opponent_action}")

    player_action = decide_action(player_hand_strength, opponent_hand_strength, 0, round_stage)
    print(f"Player's action pre-flop: {player_action}") 

    #Proceed to flop, turn, and river betting rounds
    for stage in ["flop", "turn", "river"]:
        if stage == "flop":
            community_cards = community_cards[:3]
        elif stage == "turn":
            community_cards = community_cards[:4]
        else:
            community_cards = community_cards[:5]

        print(f"\nStage: {stage}")
        print(f"Community Cards: {community_cards}")

        #Hand strength after stage cards are revealed 
        player_hand_strength = evaluate_hand(player_cards + community_cards)
        opponent_hand_strength = evaluate_hand(opponent_cards + community_cards)

        #Opponent's action 
        opponent_action = random.choice(opponent_actions)
        print(f"Opponent's action {stage}: {opponent_action}")

        #Player's action 
        player_action = decide_action(player_hand_strength, opponent_hand_strength, 0, stage)
        print(f"\nPlayer's action {stage}: {player_action}")

        #After river, determine the winner 
        winner = determine_winner(player_cards, opponent_cards, community_cards)
        print(f"\nWinner: {'Player' if winner == 0 else 'Opponent' if winner == 1 else 'Tie'}")
    
        
    

if __name__ == "__main__":
    main()
