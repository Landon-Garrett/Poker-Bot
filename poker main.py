from itertools import combinations

def main():
    print("Welcome to the poker game!")

    chips = int(input("Enter your chips: "))
    player_cards = input("Enter your cards: ").split()

    print("Are you first: ")
    first = input("Enter y/n: ")

    #handles preflop betting
    bet =preflop(player_cards, chips, first)
    chips -= bet
    print(f"Chips left: {chips}")

    #handles flop betting
    flop = input("Enter flop cards: ").split()
    bet = flop_betting(player_cards, flop,chips)
    chips -= bet
    print(f"Chips left: {chips}")

    #handles turn betting
    turn = input("Enter turn card: ").split()
    bet = turn_betting(player_cards, flop + turn,chips)
    chips -= bet
    print(f"Chips left: {chips}")

    #handles river betting
    river = input("Enter river card: ").split()
    bet = river_betting(player_cards, flop + turn + river,chips)
    chips -= bet
    print(f"Chips left: {chips}")

    print("Winner is: ")
    opponent_cards = input("Enter opponent's cards: ").split()
    community_cards = flop + turn + river
    winner = determine_winner(player_cards, opponent_cards, community_cards)

#handles preflop betting
def preflop(player_cards, chips, first):
   pass


#handles flop betting
def flop_betting(player_cards, flop, chips,):
   pass


#handles turn betting
def turn_betting(player_cards, turn, chips):
    pass


#handles river betting
def river_betting(player_cards, river, chips):
    pass


#handles preflop evaluation
def evaluate_preflop(hole_cards):
    """Evaluate the strength of the hole cards preflop."""
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

    # Special case: 5-high straight (A, 2, 3, 4, 5)
    if set(rank_values) == {12, 0, 1, 2, 3}:  # Ace is treated as low
        straight = True
        sorted_ranks = [3, 2, 1, 0, 12]

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


def poker(hands):
    
    scores = []
    for i, hand in enumerate(hands):
        # Evaluate the hand and get the score
        hand_score = evaluate_hand(hand.split())
        scores.append((i, hand_score))

    #x[1] sorts the scores by the second element of the tuple (the score)
    #sorted(scores, key=lambda x: x[1]) sorts the scores in ascending order
    #[-1] gets the last element of the sorted list, which is the highest score
    #Then [0] gets the index of the winning hand from the tuple (index, score)
    winner_index = sorted(scores, key=lambda x: x[1])[-1][0]

    # Get the winning hand using the index
    winning_hand = hands[winner_index]
    
    # used to outptut the best 5-card hand for the winner
    #needed because when given all 5 cards plus hole cards it will return all 7 cards
    #this instead shows the best 5-card hand that won
    #combinations(winning_hand.split(), 5 ) generates all possible combinations of 5 cards from the winning hand
    #key=score finds the best combination based on the score function
    #max() returns the combination with the highest score
    best_5_card_hand = max(combinations(winning_hand.split(), 5), key=score)
    best_5_card_hand_str= " ".join(best_5_card_hand) # Convert tuple to string for output

    # Determine the type of the winning hand
    hand_score, _ = score(best_5_card_hand)
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
    winning_hand_type = hand_types[hand_score[0]]

    return best_5_card_hand_str, winner_index,winning_hand_type


def determine_winner(player_cards, opponent_cards, community_cards):
    # Combine hole cards with community cards
    player_hand = player_cards + community_cards
    opponent_hand = opponent_cards + community_cards

    # Format hands as strings for the poker function
    hands = [" ".join(player_hand), " ".join(opponent_hand)]

    # Evaluate the hands and get their scores
    player_score = evaluate_hand(player_hand)
    opponent_score = evaluate_hand(opponent_hand)

    # Extract just the hand scores (e.g., 5 for a Straight)
    player_hand_score = player_score[0][0]
    opponent_hand_score = opponent_score[0][0]

    # Determine the winner
    if player_hand_score == opponent_hand_score & player_hand_score >=5:
        print("It's a tie!")
        return None
    winning_hand, winner_index,winning_hand_type = poker(hands)
    if winner_index == 0:
        print(f"The winning 5-card hand is mine: {winning_hand}, type: {winning_hand_type}")
    if winner_index == 1:
        print(f"The winning 5-card hand is the opponent: {winning_hand}, type: {winning_hand_type}")
    return winning_hand


if __name__ == "__main__":
    main()




