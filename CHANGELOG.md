VERSIONS AND MODIFICATIONS - notes about changes made

0.1 - Preparing classes and methods
	Player - Game - Turn

0.2 - Initial design of methods

0.3 - Building chooseABC()

0.4 - Building getWeight()
	0.41 - split into vowels and consonants
	0.42 - getting getWeight() to acc values
	0.43 - streamlining by converting num.strs into int at the beginning
	0.44 - Separate acc for vowels and cons
		0.441 - Problems with where/how to store vowels and cons for replaceVC(). Couldn't get them working as class variables.

0.5 - Total removal of class implementation (except for Player)...
...simple subroutines makes parameter passing much easier.
	0.51 - cons and values no longer dicts, now 2D arrays. The numbers can now be fetched more easily...
	...using list comprehensions (debugging confirmed this works - remember screenshots.)
	0.52 - replaceVC() working - placeholder is now substituted by letter
	0.53 - Rules for min. vowels and consonants implemented. If choice is compulsory, it will prompt you at the beginning...
	...and again if you still enter the incorrect choice
	0.54 - loadDict() and getWeight() now fall under start() - __main__ code a little cleaner

0.6 - Built basis of getWord(); word is entered and checked against the dictionary...
...not yet checked against the abcString

0.7 - Moved round counters to Player class. Will be manipulated by turn()

0.8 - getWord() completely functional - now checks length, then check against the chosen letters...
...then checks against the dictionary.
...will later implement a longestWord() subroutine.

0.9 - Basis for chooseNums - incomplete but working
	0.95 - chooseNums almost fully functional. Scoring system works fine...
	...as does the big and small number lists (will verify whether small duplicates are allowed)
	...Method-checking now needs to be implemented - could be quite lengthy...
	0.96 - Beginning implementation of method-checking routine chooseNums()

1.0 - Countdown complete! lettersRound() fully functional, as is chooseNums()...
...with a method checking routine check()!
	1.01 - check() now recursive. methodVal was pretty much redundant because RETURN...
	...would instantly end the function regardless of what followed (if anything). So, no point having it.
	...(plus examiners love recursion).
	1.02 - realised replaceVC() and chooseNums() were using random.__randint__, so I just moved it...
	...to the top to avoid repetition.
	1.03 - Fixed bug in check() where my used-element-removal (through list comprehension) would
	...eliminate all instances of mine.
	1.04 - Modified chooseNums() to allow no answer to be given by pressing ENTER. Skips whole process.
	1.05 - Changed some prompt/error messages for clarity in the first run-through.
	1.06 - Fixed bug in chooseNums(); if the user triggered the exception block, it wouldn't accept...
	...ENTER as an input (due to handling of ValueError). Answer-checking section has been modified.

1.1 - Added conundrum round and related procedures
	1.11 - Got rid of wordMix in conundrum() - can just use perms[x] and exit containing WHILE loop.

1.2 - Instructions presented to user in check(). Runs once per numbers round.
	1.21 - Added boolean _helper_ to ensure instructions are only printed once...
	...makes method-checking a lot clearer.
	1.22 - Distance from target not output if no answer/erroneous answer given in chooseNums() after check()
	1.23 - Fixed bug where check() returns None when it should return False in check(). Check for lack of truth
	...instead of falsehood.

1.3 - For speed of debugging/error-checking/exception-raising, I've integrated TEST MODE...
...automatically choosing my name, and a standard 5C4V abcRound() and LSSLSS chooseNums().
	1.31 - Fixed bug where testMode was not properly falsified in Option 6 for turn().
	...fixed this by changing test() and testMode into an object method/attribute for Player(). Runs after...
	...instantiation of Player()

1.4 - Bug from v1.23 actually, verifiably fixed. Recursion fixed by returning the evaluation of...
...the function itself. (Duh, Izzy. That's obviously how recursion works.)
	1.41 - Player notified of (first) unavailable letter in getWord()
	1.42 - Changed condition from NO "'s" to NO "'", so that the possessive case AND all contractions...
	...are disallowed. Shortened wordDict by about a thousand elements.

1.5 - Test Mode implemented into abcRound() and conundrum().
...for abcRound(): variable letter length, still chooses letters for you.
...for conundrum(): 'parse' or 'relates' is the chosen word (reduces anagram process time)
	1.51 - Clearer instructions on how to use operators in check()
	1.52 - Whitespace cleared upon entry, so it should allow accidental spaces...
	...as long as the rest of the input is valid.
	1.53 - If non-existent number used in check(), offending numbers are displayed.
	NB: Known bug in check() (further detail in the routine) if three operands/two operations entered.

'''NB: At this point in the program, I consider it finished. I've fixed any bug that I've seen
and I can't seem to break it. Will give to another student to blind test, then to my friend or
CS teacher so they can try and purposely break it.'''

1.6 - Added findWord() subroutine let user see what words exist in the wordDict (there's only roughly 50k words)
	1.61 - Limited strLen to 4-9 letters (given that's the length of the words in wordDict)
	1.62 - More specific prompting in menu() if incorrect value entered...
	...and Test Mode doesn't show selection of letters until the end.

1.7 - Added reset() in Player class into menu() and fullGame()
	1.71 - Reworked code for Options in menu()
	1.72 - Removed instance boolean _conundrumPlayed_, since there is no CPU opponent (yet)
	1.73 - getWord() now checks for numerical (invalid) input. Returns error invalid letter...
	...or numerical input depending on which comes up first.
	1.74 - Added dividers in source code for (hopefully) easier navigation.

1.8 - Follows game rules more closely by scoring double points for 9-letter words.
	1.81 - Slightly rearranged menu order
	1.82 - Fixed bug where findWord would print all matches even when ≥ 50 matches existed.

1.9 - User can now choose how many matches are shown in findWord if there ≥ 50.
	1.91 - Specific notification for invalidity in chooseNums(), rearranged and trimmed code
	1.92 - Rearrangement of menu.
	1.93 - Cleaned up spacing of prompts for users. In getWeight(), everything below the...
	...list comprehension in the WITH block has been moved out of it.
	1.94 - Allowing up to 12 letters, for greater challenge. Changed auto-selection in chooseABC()...
	...by setting choice based on abcCount mod 2 - therefore alternates between C and V.
	1.95 - Better notifications. Player now presses ENTER after seeing scoring message.
	1.96 - Properly stripping whitespace in Player.getName() and Player.test()
	1.97 - findWord(), abcRound() and numRound() will recurse if the user wishes to do so...
	...will not implement it for Conundrum because it is too slow.
	1.98 - Instantiation and setup of Player moved from __main__ to start()
	1.99 - Header for Conundrum Round. New instance boolean, _full_...
	...Declining repeat of fullGame() doesn't end game, and moved from menu() to fullGame()

2.00 - permute() reworked to reduce computation time. No longer dupe-checking perms.
...Using join() built-in function to form words
split() now redundant. A basic list comprehension does its job.
Rearranged output in permute() to show end of permutation generation/anagram search.