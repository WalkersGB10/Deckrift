import random
import time

hands = 5
discards = 3
table = 1
basedealers = [100, 300, 600, 1000, 2400, 6000]
handvalues = {
  4: [5, 1],
  5: [5, 1],
  6: [5, 1],
  7: [5, 1],
  8: [5, 1],
  9: [10, 2],
  10: [10, 2],
  11: [10, 2],
  12: [20, 2],
  13: [30, 3],
  14: [30, 3],
  15: [30, 3],
  16: [30, 3],
  17: [30, 4],
  18: [35, 4],
  19: [40, 4],
  20: [60, 5],
  21:  [60, 7],
  "bj":  [100, 8]
}

suits = ["S", "H", "C", "D"]
values = ["A"] + [str(n) for n in range(2, 10)] + ["T", "J", "Q", "K"]
decks = {
  "standard": [value+suit for suit in suits for value in values],

  "noface": [value+suit for suit in suits for value in values if value not in ["J", "Q", "K"]],

  "even": [value+suit for suit in suits for value in values if value not in [3, 5, 7, 9]],

  "odd": [value+suit for suit in suits for value in values if value not in [2, 4, 6, 8]],

  "prime": [str(value)+suit for suit in suits for value in ["A", 2, 3, 5, 7]],

  "red": [value+suit for suit in ["H", "D"] for value in values],

  "black": [value+suit for suit in ["S", "C"] for value in values],

  "low": [str(value)+suit for suit in suits for value in ["A", 1, 2, 3, 4, 5]],

  "high": [str(value)+suit for suit in suits for value in ["A", 9, "T", "J", "Q", "K"]],

  "mirror": [value+suit for suit in suits for value in values] * 2,

  "countless": [str(value)+suit for suit in suits for value in [7, 8, 9]]*2
}

jokers = [
  ["Jeweler", "+3 Multiplier per Diamond Played", 3],
  
  ["Miner", "+3 Multiplier per Spade Played", 3],
  
  ["Lover", "+3 Multiplier per Heart Played", 3],
  
  ["Botanist", "+3 Multiplier per Club Played", 3],

  ["Lifeguard", "Survive if you get 50% requireed score", 6],

  ["Wasteful", "+1 Discard per Dealer", 4],

  ["Quickdraw", "+1 Hand per Dealer", 4],

  ["Phantom Joker", "Allows You to See Both of the Dealer's Starting Hand", 4],

  ["Jimbo", "+4 Multiplier", 4]
  
]

bossdealers = {
  "Ruby": "Disables Diamonds",

  "Heartless": "Disables Hearts",

  "Spadebane": "Disables Spades",

  "Golfer": "Disables Clubs",

  "Jack": "Disables Aces",

  "The Void": "Disables all cards under 5",

  "The Collector": "No Discards",

  "Final Reckoning": "Play only one Hand"
  }





def playdeckrift():
  pldeck = choosedeck()

def choosedeck(decks):
  for deck in decks.keys():
      print(deck)
  while True:
    try:
      deck = input("Which deck would you like?").lower()
      return decks[deck]
    except:
      print("Deck not Found")

def drawcard(deck, hand, value):
  card = deck[0]
  hand.append(card)
  deck.pop(0)
  if card[0] in ["T", "J", "Q", "K"]:
      value += 10
  elif card[0] == "A":
    if value <11:
      value += 11
    else:
      value += 1
  else:
    value += int(card[0])
  return deck, hand, value

def discard(hand, value):
  selected = input("Enter the cards you would like to discard separated by a space")
  selected = selected.split()

  if len(selected) > 3:
    for selection in range(0, 3):
      if selected[selection] in hand:
        hand.remove(selected[selection])
        if selected[selection][0] == "A":
          if value > 10:
            value -= 11
          else:
            value -= 1
        elif selected[selection][0] in ["T", "J", "Q", "K"]:
          value -= 10
        else:
          value -= int(selected[selection[0]])
  else:
    for selection in selected:
      if selection in hand:
        hand.remove(selection)
        if selection[0] == "A":
          if value > 10:
            value -= 11
          else:
            value -= 1
        elif selection[0] in ["T", "J", "Q", "K"]:
          value -= 10
        else:
          value -= int(selection[0])
  return hand, value

def jokercheck(jokers, hand, chips, multiplier):
  for joker in jokers:
    if joker == "Jeweler":
      for card in hand:
        if card[1] == "D":
          multiplier += 3
          print("Chips:", chips, "Multiplier:", multiplier)
    
    elif joker == "Miner":
      for card in hand:
        if card[1] == "S":
          multiplier += 3
          print("Chips:", chips, "Multiplier:", multiplier)
    
    elif joker == "Lover":
      for card in hand:
        if card[1] == "H":
          multiplier += 3
          print("Chips:", chips, "Multiplier:", multiplier)
    
    elif joker == "Botanist":
      for card in hand:
        if card[1] == "C":
          multiplier += 3
          print("Chips:", chips, "Multiplier:", multiplier)
  
  return chips, multiplier

def dealer(pldeck, ddeck, scoretobeat, pljokers, hands, discards):
  global handvalues
  if "Wasteful" in pljokers:
    discards += 1
  elif "Quickdraw" in pljokers:
    hands += 1
  random.shuffle(pldeck)
  random.shuffle(ddeck)
  score = 0

  print("Target Score:", scoretobeat)
  
  while score < scoretobeat and hands > 0:
    ans = ""
    handscore = 0
    doubledown = 1
    chips, multiplier = 0, 0
    dhand, dvalue = [], 0
    plhand, plvalue = [], 0
  
    for i in range(0, 2):
      pldeck, plhand, plvalue = drawcard(pldeck, plhand, plvalue)

    for i in range(0, 2):
      ddeck, dhand, dvalue = drawcard(ddeck, dhand, dvalue)
    
    print("Your cards:")
    for card in plhand:
      print(card, end = " ")
    print("\nValue:", plvalue)

    print("\n\nDealer Upcard:")
    if dhand[0][0] == "A":
      print(dhand[0], "\nValue:", 11)
    elif dhand[0][0] in ["T", "J", "Q", "K"]:
      print(dhand[0], "\nValue:", 10)
    else:
      print(dhand[0], "\nValue:", dhand[0][0])

    while ans != "stick" and plvalue < 22:
      ans = input("Would you like to: hit, stick, double down, or discard?")
      if ans == "hit":
        pldeck, plhand, plvalue = drawcard(pldeck, plhand, plvalue)
      elif ans == "double down":
        pldeck, plhand, plvalue = drawcard(pldeck, plhand, plvalue)
        doubledown = 2
        ans = "stick"
      elif ans == "discard":
        discards -= 1
        print("Discards remaining:", discards)
        plhand, plvalue = discard(plhand, plvalue)
      elif ans != "stick":
        continue
      print("Your cards:")
      for card in plhand:
        print(card, end = " ")
      print("\nValue:", plvalue)
      hands -= 1

    if plvalue > 21:
      print("You Went Bust!")

    while dvalue < 17:
      ddeck, dhand, dvalue = drawcard(ddeck, dhand, dvalue)
      print("\nDealer cards:")
      for card in dhand:
        print(card, end = " ")
      print("\nValue:", dvalue)
      print()
      time.sleep(1)

    if plvalue > 21:
      print("Score:", score)
      print("Hands Remaining:", hands)
      print("Discards Remaining:", discards)
      continue
    
    if plvalue == 21 and len(plhand) == 2:
      chips, multiplier = handvalues["bj"][0], handvalues["bj"][1]
    else:
      chips, multiplier = handvalues[plvalue][0], handvalues[plvalue][1]   

    for card in plhand:
      print("Chips:", chips, "Multiplier:", multiplier)
      if card[0] == "A":
        chips += 11
      elif card[0] in ["T", "J", "Q", "K"]:
        chips += 10
      else:
        chips += int(card[0])
      time.sleep(1)

    chips, multiplier = jokercheck(pljokers, plhand, chips, multiplier)

    handscore = chips * multiplier * doubledown

    if dvalue > 21:
      print(chips, "*", multiplier, "*", doubledown, "=", handscore)
      score += handscore
    elif dvalue == plvalue:
      print(chips, "*", multiplier//2, "*", doubledown, "=", handscore//2)
      score += handscore // 2
    elif plvalue > dvalue:
      print(chips, "*", multiplier, "*", doubledown, "=", handscore)
      score += handscore
  
    print("Score:", score)

    print("Hands Remaining:", hands)
    print("Discards Remaining:", discards, "\n\n")

  if score > scoretobeat:
    print("You WIN!")
  else:
    print("You LOSE!")

dealer(decks["standard"], decks["standard"], basedealers[table], ["Botanist"], hands, discards)
  
