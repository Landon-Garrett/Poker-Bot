from betting import *
from evaluating import *

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

if __name__ == "__main__":
    main()