import random
import time
import sys

hands = 5
discards = 3
table = 0
round = 1
money = 5
busts = 0
blackjacks = 0
packs_opened = 0
crystals_used = 0
fates_used = 0
destroyed_jokers = 0
pljokers = []
basedealers = [100, 300, 600, 1000, 2400, 6000, 12000, 25000, 50000]
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

  "noface": [str(value)+suit for suit in suits for value in ["A", 2, 3, 4, 5, 6, 7, 8, 9, "T"]],

  "even": [str(value)+suit for suit in suits for value in ["A", 2, 4, 6, 8, "T", "J", "Q", "K"]],

  "odd": [str(value)+suit for suit in suits for value in ["A", 3, 5, 7, 9, "J", "Q", "K"]],

  "prime": [str(value)+suit for suit in suits for value in ["A", 2, 3, 5, 7]] * 2,

  "red": [value+suit for suit in ["H", "D"] for value in values],

  "black": [value+suit for suit in ["S", "C"] for value in values],

  "low": [str(value)+suit for suit in suits for value in ["A", 1, 2, 3, 4, 5]],

  "high": [str(value)+suit for suit in suits for value in ["A", 9, "T", "J", "Q", "K"]],

  "mirror": [value+suit for suit in suits for value in values] * 2,

  "countless": [str(value)+suit for suit in suits for value in [7, 8, 9]]*4
}

jokers = [
  ["Jeweler", "+3 Multiplier per Diamond Played", 3],
  
  ["Miner", "+3 Multiplier per Spade Played", 3],
  
  ["Lover", "+3 Multiplier per Heart Played", 3],
  
  ["Botanist", "+3 Multiplier per Club Played", 3],

  ["Jimbo", "+4 Multiplier", 4],

  ["All Or Nothing", "+1 Multiplier per Bust This Run", 5],

  ["Fortune Teller", "+1 Multiplier per Fate Used This Run", 4],

  ["Broker", "+1 Multiplier per Crystal Used This Run", 4],

  ["Extrovert", "+3 Multiplier per Joker Owned (Extrovert Included)", 6],

  ["Backstabber", "Destroys a Random Joker Each Dealer. Adds 0.5X Multiplier to This Joker", 6],

  ["Introvert", "+0.5X Multiplier per Empty Joker Slot (Introvert Included)", 8],

  ["Mirror", "Copies Ability of Selected Joker", 6],
  
  ["Lifeguard", "Survive if you get 50% required score. Self Destructs on Use", 6],

  ["Wasteful", "+1 Discard per Dealer", 4],

  ["Quickdraw", "+1 Hand per Dealer", 4],

  ["Phantom Joker", "Allows You to See Both of the Dealer's Starting Hand", 4]
  
]

fates = [
  ["The Gambler", "1 in 4 chance of giving a joker. Must have space", 2],

  ["The Twist", "Gives $5 - $10", 2],

  ["The Reckoning", "Destroys a random joker. Gives $20", 2],
]

crystals = [
  ["Weak Crystal", "Upgrades Hand Totals 4-8", 2],
  
  ["Moderate Crystal", "Upgrades Hand Totals 9-12", 2],
  
  ["Strong Crystal", "Upgrades Hand Totals 13-16", 2],
  
  ["Power Crystal", "Upgrade Hand Totals 17-19", 2],
  
  ["Supreme Crystal", "Upgrade Hand Totals 20 and 21", 2],
  
  ["Ultimate Crystal", "Upgrades Blackjacks", 2]
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





def playdeckrift(decks, basedealers, table, hands, discards, round, money, handvalues, jokers):
  global pljokers
  deck = choosedeck(decks)
  while True:
    pldeck = []
    for card in deck:
      pldeck.append(card)
    if round % 3 == 1:
      table += 1
    if table == 9:
      print("You Beat My Game!\nThank You For Playing!")
      sys.exit()
    round, money = dealer(pldeck, decks["standard"], basedealers[table], pljokers, hands, discards, round, money, table)
    deck, money, pljokers, handvalues = shop(deck, money, pljokers, handvalues)

def usefate(fate, deck, money, pljokers):
  global jokers
  global fates_used
  fates_used += 1
  
  fate = fate[0]
  if fate == "The Gambler":
    chance = random.randint(0, 3)
    if chance == 3:
      if len(pljokers) < 5:
        print("You received a joker")
        index = random.randint(0, len(jokers)-1)
        pljokers.append(jokers[index][0])
        jokers.pop(index)
      else:
        print("No Space")
    else:
      print("NOPE")

  elif fate == "The Twist":
    chance = random.randint(5, 10)
    money += chance
    print("You gained $" + str(chance))

  elif fate == "The Reckoning":
    index = random.randint(0, len(pljokers))
    if len(pljokers) > 0:
      pljokers.pop(index)
    money += 20
    print("You gained $20")


  return deck, money, pljokers

def usecrystal(crystal, handvalues):
  global crystals_used
  crystals_used += 1
  
  crystal = crystal[0]
  if crystal == "Weak Crystal":
    for index in range(4, 9):
      handvalues[index][0] += 5
      handvalues[index][1] += 1
  elif crystal == "Moderate Crystal":
    for index in range(9, 13):
      handvalues[index][0] += 10
      handvalues[index][1] += 2
  elif crystal == "Strong Crystal":
    for index in range(13, 17):
      handvalues[index][0] += 20
      handvalues[index][1] += 2
  elif crystal == "Power Crystal":
    for index in range(17, 20):
      handvalues[index][0] += 20
      handvalues[index][1] += 3
  elif crystal == "Supreme Crystal":
    for index in range(20, 22):
      handvalues[index][0] += 30
      handvalues[index][1] += 3
  elif crystal == "Power Crystal":
    handvalues["bj"][18] += 40
    handvalues["bj"][18] += 4

  return handvalues
    

def choosedeck(decks):
  for deck in decks.keys():
      print(deck)
  while True:
    try:
      deck = input("Which deck would you like?").lower()
      return decks[deck]
    except:
      print("Deck not Found")

def countvalue(plhand):
  value = 0

  for card in plhand:
    if card[0] == "A":
      plhand.append(card)
      plhand.remove(card)
  
  for card in plhand:
    if card[0] in ["T", "J", "Q", "K"]:
        value += 10
    elif card[0] == "A":
      if value <11:
        value += 11
      else:
        value += 1
    else:
      value += int(card[0])
  return value

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
          value -= int(selected[selection][0])
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
  global busts
  global blackjacks
  global jokers_destroyed
  global fates_used
  global crystals_used
  global packs_opened
  
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

    elif joker == "Jimbo":
      multiplier += 4
      print("Chips:", chips, "Multiplier:", multiplier)
      
    elif joker == "All Or Nothing":
      muliplier += busts
      print("Chips:", chips, "Multiplier:", multiplier)
      
    elif joker == "Fortune Teller":
      multiplier += fates_used
      print("Chips:", chips, "Multiplier:", multiplier)

    elif joker == "Broker":
      multiplier += crystals_used
      print("Chips:", chips, "Multiplier:", multiplier)

    elif joker == "Extrovert":
      for item in jokers:
        multiplier += 3
        print("Chips:", chips, "Multiplier:", multiplier)

    elif joker == "Introvert":
      multiplier *= 1 + ((6-len(jokers)) * 0.5)
      print("Chips:", chips, "Multiplier:", multiplier)

    elif joker == "Backstabber":
      multiplier *= 1 + (jokers_destroyed * 0.5)
      print("Chips:", chips, "Multiplier:", multiplier)

    elif joker == "Mirror":
      if len(jokers) > 1:
        for item in jokers[1:]:
          print(item)
        copying = True
        while copying:
          ans = input("Which Joker will the Mirror Reflect?")
          if ans in jokers:
            chips, multiplier = jokercheck([ans], hand, chips, multiplier)
            copying = False
    
  
  return chips, multiplier

def dealer(pldeck, ddeck, scoretobeat, pljokers, 
hands, discards, round, money, table):
  global handvalues

  print("-"*15, f"Table:{table} Round:{round%3}", "-"*15)
  
  if "Wasteful" in pljokers:
    discards += 1
  elif "Quickdraw" in pljokers:
    hands += 1
  random.shuffle(pldeck)
  random.shuffle(ddeck)
  score = 0
  if round % 3 == 0:
    scoretobeat *= 2
  elif round % 3 == 2:
    scoretobeat *= 1.5
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

    if "Phantom Joker" not in pljokers:
      print("\n\nDealer Upcard:")
      if dhand[0][0] == "A":
        print(dhand[0], "\nValue:", 11)
      elif dhand[0][0] in ["T", "J", "Q", "K"]:
        print(dhand[0], "\nValue:", 10)
      else:
        print(dhand[0], "\nValue:", dhand[0][0])
    else:
      print("\n\nDealer Cards:")
      print(dhand[0], dhand[2], "\nValue:", dvalue)

    while ans != "stick" and ans != "stand":

      while len(plhand) < 2:
        pldeck, plhand, plvalue = drawcard(pldeck, plhand, plvalue)
        print("\nYou had less than two cards so were forced to draw")

      plvalue = countvalue(plhand)

      print("\nYour cards:")
      for card in plhand:
        print(card, end = " ")
      print("\nValue:", plvalue)

      if plvalue == 21:
        ans = "stick"
        continue

      ans = input("\nWould you like to: hit, stick, double down, or discard?")
      if ans == "hit":
        pldeck, plhand, plvalue = drawcard(pldeck, plhand, plvalue)
      elif ans == "double down":
        pldeck, plhand, plvalue = drawcard(pldeck, plhand, plvalue)
        doubledown = 2
        ans = "stick"
      elif ans == "discard":
        if discards > 0:
          discards -= 1
          print("Discards remaining:", discards)
          plhand, plvalue = discard(plhand, plvalue)
        else:
          print("0 Discards Remaining")
          continue
      elif ans != "stick":
        continue
      
      plvalue = countvalue(plhand)

      if plvalue > 21:
        break

    print("Your cards:")
    for card in plhand:
      print(card, end = " ")
    print("\nValue:", plvalue)

    hands -= 1

    if plvalue > 21:
      time.sleep(1)
      print("You Went Bust!")

    time.sleep(1)
    print("\nDealer cards:")
    for card in dhand:
      print(card, end = " ")
    print("\nValue:", dvalue)
    print()
    time.sleep(1)

    while dvalue < 17:
      ddeck, dhand, dvalue = drawcard(ddeck, dhand, dvalue)
      print("\nDealer cards:")
      for card in dhand:
        print(card, end = " ")
      print("\nValue:", dvalue)
      print()
      time.sleep(1)

    if plvalue > 21:
      time.sleep(1)
      print("Score:", score)
      time.sleep(1)
      print("Hands Remaining:", hands)
      time.sleep(1)
      print("Discards Remaining:", discards)
      time.sleep(1)
      continue
    
    if plvalue == 21 and len(plhand) == 2:
      chips, multiplier = handvalues["bj"][0], handvalues["bj"][1]
    else:
      chips, multiplier = handvalues[plvalue][0], handvalues[plvalue][1]   

    if plvalue > dvalue or dvalue > 21:
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
  
    time.sleep(1)
    print("Score:", score)

    time.sleep(1)
    print("Hands Remaining:", hands)
    time.sleep(1)
    print("Discards Remaining:", discards, "\n\n")
    time.sleep(1)

  if score >= scoretobeat:
    print("You WIN!")
    if round % 3 == 1:
      money += 3
    else:
      money += 5
    money += hands
    round += 1
    return round, money
  else:
    if "Lifeguard" in pljokers and score*2 >= scoretobeat:
      pljokers.remove("Lifeguard")
      print("Saved by lifeguard")
      round += 1
      return round, money
    else:
      print("You LOSE!")
      sys.exit()

def bossdealer(pldeck, ddeck, scoretobeat, pljokers, 
hands, discards, round, money, table):
  global handvalues

def shoproll(type, variants):
  global jokers
  global fates
  global crystals
  
  items = []
  variants = []
  for index in range(0, 2):
    items.append(random.randint(0,2))
  for slot in range(0, len(items)):
    if items[slot] == 0:
      variants.append("Joker")
      if type == "single":
        items.pop(slot)
        index = random.randint(0, len(jokers)-1)
        items.insert(slot, jokers[index])
        jokers.remove(jokers[index])
    elif items[slot] == 1:
      variants.append("Fate")
      if type == "single":
        items.pop(slot)
        index = random.randint(0, len(fates)-1)
        items.insert(slot, fates[index])
    else:
      variants.append("Crystal")
      if type == "single":
        items.pop(slot)
        index = random.randint(0, len(crystals)-1)
        items.insert(slot, crystals[index])

  if type == "single":
    return items, variants
  else:
    items = []
    for slot in range(0, len(variants)):
      size = random.randint(0, 2)
      if size == 0:
        name = "Standard " + variants[slot] + " Pack"
        items.append([name, "Choose One of Two Items", 4])
      elif size == 1:
        name = "Big " + variants[slot] + " Pack"
        items.append([name, "Choose One of Four Items", 6])
      else:
        name = "Supreme " + variants[slot] + " Pack"
        items.append([name, "Choose Two of Four Items", 8])
    return items, variants

def displayshop(singles, svariants, packs, pvariants, price):
  print("$"+str(price), "Reroll\n")
  print("Loose Items:")
  time.sleep(1)

  for card in singles:
    print("$"+str(card[2]), card[0], "("+svariants[singles.index(card)]+")")

  time.sleep(1)
  print("\nPacks:")
  time.sleep(1)

  for pack in packs:
    print("$"+str(pack[2]), pack[0])

def browse(item, singles, svariants, packs, pvariants, money):
  for card in singles:
    if item in card:
      print("$"+str(card[2]), card[0]+":", card[1])
      ans = input("Would you like to purchase " + card[0]+"?").lower()[0]
      if ans == "y":
        return True, singles.index(card)
      else:
        return False, 0
        

  for option in packs:
    if item in option:
      print("$"+str(option[2]), option[0]+":", option[1])
      ans = input("Would you like to purchase " + option[0]+"?").lower()[0]
      if ans == "y":
        return True, packs.index(option)
      else:
        return False

def openpack(pack, money):
  global handvalues
  global pljokers
  global deck
  global jokers

  name = pack[0]
  options = []
  indexes = []
  
  if "Standard" in name:
    size = 2
    choices = 1
  elif "Big" in name:
    size = 4
    choices = 1
  else:
    size = 4
    choices = 2

  if "Fate" in name:  
    for option in range(size):
      index = random.randint(0, len(fates)-1)
      options.append(fates[index])
      indexes.append(index)
     
    while choices > 0:
      for option in options:
        print(option[0] + ":", option[1])
      ans = input("Type the name of the fate you would like or 'Skip' if you wouldn't like any of them")
      if ans == "Skip":
        return
      for option in options:
        if ans in option:
          print(money)
          deck, money, pljokers = usefate(option, deck, money, pljokers)
          print(money)
          options.remove(option)
          choices -= 1
          break
    return money

  elif "Crystal" in name:  
    for option in range(size):
      index = random.randint(0, len(crystals)-1)
      options.append(crystals[index])
      indexes.append(index)
    while choices > 0:
      for option in options:
        print(option[0] + ":", option[1])
        
      print("You have", choices, "choices remaining")
      ans = input("Type the name of the crystal you would like or 'Skip' if you wouldn't like any of them")
      if ans == "Skip":
        return
      for option in options:
        if ans in option:
          handvalues = usecrystal(option, handvalues)
          options.remove(option)
          choices -= 1
          break
    return money

  elif "Joker" in name:  
    for option in range(size):
      index = random.randint(0, len(jokers)-1)
      options.append(jokers[index])
      indexes.append(index)
    while choices > 0:
      for option in options:
        print(option[0] + ":", option[1])
        
      print("You have", choices, "choices remaining")
      ans = input("Type the name of the joker you would like or 'Skip' if you wouldn't like any of them")
      if ans == "Skip":
        return
      for option in options:
        if ans in option:
          if len(pljokers) < 5:
            pljokers.append(option[0])
            jokers.remove(option)
          options.remove(option)
          choices -= 1
          break
    return money
    
    
def shop(deck, money, pljokers, handvalues):
  global jokers
  global fates
  global crystals
  price = 5

  print("-"*15, "Welcome to the Shop", "-"*15)
  print("You have $" + str(money))
  print()
  singles = []
  svariants = []

  packs = []
  pvariants = []
  
  singles, svariants = shoproll("single", svariants)

  packs, pvariants = shoproll("pack", pvariants)

  shopping = True

  while shopping:
    displayshop(singles, svariants, packs, pvariants, price)
    ans = input('''
    If you would like to:
    Reroll Loose Items: Type 'Reroll'
    Check the Description of a Loose Item: Type the Name of that Item
    Sell a joker: Type 'Sell'
    Progress onto the Next Dealer: Type 'Continue\'
    ''').title()

    if ans == "Reroll":
      if money >= price:
        money-=price
        price+=1
        print("\nShop Rerolled\n")
        singles, svariants = shoproll("single", svariants)
      print("You have $" + str(money))
      continue
    elif ans == "Continue":
      print("Next Dealer")
      return deck, money, pljokers, handvalues
    elif ans == "Sell":
      print("Your Jokers:")
      for option in pljokers:
        print(option)
      response = input("Which Joker would you like to sell").title()
      try: 
        pljokers.remove(response)
        money += 2
        print("You have $" + money)
      except:
        print(response, "is not one of your jokers. Try Again.")
    else:
      buy, index = browse(ans, singles, svariants, packs, pvariants, money)

      if buy == False:
        print("You have $" + str(money))
        continue
      else:
        if ans in singles[index]:
          ans = singles[index]
          if ans in fates:
            if money >= ans[2]:
              svariants.pop(singles.index(ans))
              singles.remove(ans)
              money -= ans[2]
              deck, money, pljokers = usefate(ans, deck, money, pljokers)
              print("You have $" + str(money))
              continue
            else:
              print("You don't have enough money for this")
              print("You have $" + str(money))
              continue
          elif ans in crystals:
            if money >= ans[2]:
              svariants.pop(singles.index(ans))
              singles.remove(ans)
              money -= ans[2]
              handvalues = usecrystal(ans, handvalues)
              print("You have $" + str(money))
              continue
            else:
              print("You don't have enough money for this")
              print("You have $" + str(money))
              continue
          else:
            if len(pljokers) < 5:
              if money >= ans[2]:
                svariants.pop(singles.index(ans))
                singles.remove(ans)
                money -= ans[2]
                pljokers.append(ans[0])
                print("You have $" + str(money))
                continue
              else:
                print("You don't have enough money for this")
                print("You have $" + str(money))
                continue
        elif ans in packs[index]:
          ans = packs[index]
          if money >= ans[2]:
            pvariants.pop(packs.index(ans))
            packs.remove(ans)
            money -= ans[2]
            money = openpack(ans, money)
            print("You have $" + str(money))
            continue
          else:
            print("You don't have enough money for this")
            print("You have $" + str(money))
            continue
            
                
  


#TESTING

pljokers = ["Mirror", "Jimbo"]
#shop(decks["standard"], money, pljokers, handvalues)
playdeckrift(decks, basedealers, table, hands, discards, round, money, handvalues, jokers) 
