import random
import time

hands = 5
discards = 3
table = 0
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

def smalldealer(pldeck, ddeck, scoretobeat, pljokers, hands, discards):
  random.shuffle(pldeck)
  random.shuffle(ddeck)
  chips, multiplier = 0, 0
  score = 0
  dhand, dvalue = [], 0
  plhand, plvalue = [], 0

  for i in range(0, 2):
    pldeck, plhand, plvalue = drawcard(pldeck, plhand, plvalue)
  
  

smalldealer(decks["standard"], decks["standard"], basedealers[table], [], hands, discards)
  
