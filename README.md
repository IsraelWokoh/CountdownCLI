# CountdownCLI
Welcome to my command-line recreation of _Countdown_, the long-running Channel 4 game show.

# Introduction
In _Countdown_ (the TV show), two players face off in a series Letters Rounds, Numbers Rounds and a final Conundrum. Whoever has more points at the end of the game is the winner.

# _CountdownCLI_'s key differences from the original show
  - The game is functionally **single-player**.
  - There is **no time limit** for any Round.
  - Rounds can be played **individually**, outside the full game format.

# Rules
## Letters Round
Player picks 9 letters, including at least **3 vowels** and **4 consonants**, and makes the longest word they can. It must be at least four letters long to score. (The letter that appears is influenced by its frequency in English text.) Length of word = points scored. Double points for a 9-letter word! Zero for an invalid word. 

## Numbers Round
Player selects 6 numbers from two lists, large (25, 50, 75, 100) and small (1-10, twice). A random three-digit target (between 101 and 999) is generated. Using the four arithmetic operations, the Player must get as close to the target as possible, with points earned based on proximity to the asnwer. An exact answer earns 10, ±5 or less earns 7 and ±10 or less earns 5. >10 away, a prohibited move or an incorrect final answer earns nothing.

**Prohibited operations** (with examples) include:
  - **Exponentiation** (3^2 = 9)
  - **Non-integral division** (5 / 2 = 2.5)
  - **Subtraction resulting in negative numbers** (7 - 8 = -1)

## Conundrum
A randomly-selected nine-letter word is shuffled. The Player must guess the original word. An anagram of the original word is permitted (e.g. 'cautioned', 'education', 'auctioned'). Success earns 10 points, otherwise the Player scores 0.

# How to play
The following files have to be in the *same folder* to play this game:
  1) **Countdown.py**
  2) **npn3.txt**, the list of allowed words
  3) **Letter weights.csv**, assigning each letter of the alphabet its weight, according to its frequency of appearance in the English language. (See [this Wikipedia article on letter frequency](https://www.wikiwand.com/en/Letter_frequency) for more information. It's kind of interesting.)

# Test Mode
Speeds up the testing/playing process:
  - **Letters Round**: Automatically picks 4 vowels and 5 consonants.
  - **Numbers Round**: Selects 2 large and 4 small numbers

# Other notes
Conundrum Round is **disrespectfully slow**. This is because a nine-letter, character-unique word produces 362880 different permutations. (I tried filtering out duplicates where this wasn't the case, but it was too slow.) Every permutation has to be checked against the imported word list to check if it's a valid word. The shuffled permutation itself cannot be a valid word. There may yet be probably some algorithmic inefficiencies that can be ironed out...

I ran this game using PyPy3, which makes use of just-in-time (JIT) compilation to speed up operation. It was definitely faster than Python 3.7.0, the standard implementation at the time I wrote this. However, [the upcoming Python 3.11 is reportedly significantly faster than 3.10.](https://www.python.org/downloads/release/python-3110b1/#:~:text=The%20Faster%20Cpython%20Project%20is%20already%20yielding%20some%20exciting%20results.%20Python%203.11%20is%20up%20to%2010%2D60%25%20faster%20than%20Python%203.10.%20On%20average%2C%20we%20measured%20a%201.22x%20speedup%20on%20the%20standard%20benchmark%20suite.%20See%20Faster%20CPython%20for%20details.)

# Conclusion
That's everything you need to know to play this game. Enjoy!
