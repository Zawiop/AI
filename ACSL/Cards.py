def match2(cardA, cardB):
   
    matches = sum(cardA[i] == cardB[i] for i in range(3))
    return (matches == 2)

def simulate_pile(face_up, hand):
    
    final_pile = [face_up]  
    top = face_up           

    temp_hand = hand[:]     

    while True:
        found_index = None
        
        for i, card in enumerate(temp_hand):
            if match2(top, card):
                found_index = i
                break

        if found_index is None:
            
            break
        else:
            
            card_to_place = temp_hand.pop(found_index)
            final_pile.append(card_to_place)
            top = card_to_place

    cards_placed = len(final_pile) - 1  
    return final_pile, cards_placed

def solve(face_up1, face_up2, hand):

    pile1, placed1 = simulate_pile(face_up1, hand)
    pile2, placed2 = simulate_pile(face_up2, hand)

    if placed2 > placed1:
        return pile2
    else:
        return pile1

def main():
    
    with open("test.txt", "r") as f:
        lines = [line.strip() for line in f]

    
    
    
    
    puzzle_count = 6
    for i in range(puzzle_count):
        
        face_up_line = lines[2*i]      
        hand_line    = lines[2*i + 1]  

        
        face_up_cards = face_up_line.split()  
        hand_cards = hand_line.split()        

        
        face_up1, face_up2 = face_up_cards
        final_pile = solve(face_up1, face_up2, hand_cards)

        
        
        print(f"{i+1}.", " ".join(final_pile))

if __name__ == "__main__": main()
