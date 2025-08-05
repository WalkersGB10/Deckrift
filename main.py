import random
import time


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

