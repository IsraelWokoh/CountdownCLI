# Developed for Python 3.7.0b3
# IDE: PyCharm 2018.1
# Interpreted in PyPy3 v6.0.0

## KEY VARIABLE NOMENCLATURE ##
	# Identifier = Class (note the Title Case)
	# abcIdentifier = associated with Letters Round
	# numIdentifier = associated with Numbers Round
	# setupIdentifier = associated with initial necessary background processes
	# identifierTry = for exception handling
	# identifierVal = for validation
	# identifierYN = for Yes/No choice

from random import randint
from csv import reader # Reads CSV
from itertools import accumulate as acc, permutations as allPerms # Aliases

# Player template
class Player():
	def __init__(s):
		s.name = ''
		s.total = 0
		s.testMode = None
		s.full = False

	def addScore(s, score): # Called at the end of each round
		s.total += score # Update score
		print(f'\nPoints scored: {score}') # Points earned
		print(f'Current total score: {s.total}\n') # Current total
		buffer = input("Press ENTER to continue.")

	def reset(s):
		s.total = 0
		print('\nPoints reset.')

	def getName(s): # Called when the game starts
		if not s.testMode:
			newNameVal = False
			while not newNameVal: # Whilst name not validated
				newName = input('Enter your name: ').lstrip() # Prompt
				if newName != '': # If not empty
					newNameVal = True # Pass
				else:
					print('Please enter something.\n')
			s.name = newName.title() # Changes default empty value for name
		else:
			s.name = 'Tester'

	def getScore(s):
		print(f'\n{s.name}, your current total is {s.total}\n')
		buffer = input("Press ENTER to continue.")

	def test(s): # Speeds up program testing
		testVal = False
		while not testVal:
			s.testMode = input('\nTest mode? (Y/N) ').lower()
			if s.testMode not in ['y','n']:
				print('Y for Yes, N for No.')
			else:
				testVal = True
		if s.testMode == 'y':
			s.testMode = True
		else:
			s.testMode = False
		print(f'Test Mode is now: {s.testMode}\n')
		return s.testMode

												####### SETUP SECTION #######

#### SETUP ####
### Procedures in the backend of the game ###
def loadDict(): # Loads dictionary from TXT file
	wordDict = [] # Dictionary file
	conWords = [] # All nine-letter words
	with open('npn3.txt', 'r') as wordList: # Open dictionary
		for line in wordList:
			line = line.strip() # Removes carriage returns
			if ("'" or '-') in line: # No possessive case or contractions
				continue
			if 4 <= len(line) <= 9:
				wordDict.append(line)
		conWords = [word for word in wordDict if len(word) == 9]
	return wordDict, conWords

def start(): # Let's get it started!
	player1.getName() # Get name
	wordDict, conWords = loadDict() # Create dictionary
	vowels, cons = getWeight() # Get vowel and consonants, with probabilities
	return wordDict, conWords, vowels, cons # Returned, since they are used globally

def getWeight(): # Reads each letter and assigns number to it, essentially determining the likelihood of it appearing
	with open('Letter weights.csv', 'r') as weights: # Opening file I made, based on Wiki
		weights = reader(weights) # Must specify delimiter to get intended separation?
		# Addendum: delimiter not necessary - correctly separates when using list comprehension below.

		# Gotta love list comprehensions!
		weights =  [group for group in weights] # CSV into list
		for group in weights:
			for item in group:
				if item.isnumeric():
					group[group.index(item)] = int(item)
		vowels = [group for group in weights if group[0] in 'aeiou'] # Duplicates vowels in separate list

		# Removing the vowels from original list
		for item in vowels: # Is there a way...
			if item in weights: # ...to do this...
				weights.remove(item) # ...in list comprehension form?
			# weights[] now only contains consonants

		# Reassignment of acc. values
		nums = list(acc(thing for group in vowels for thing in group if type(thing) == int)) # Acc. of vowel values
		for x in range(len(vowels)):
			vowels[x][1] = nums[x] # Assign acc. values to vowels

		nums = list(acc(thing for group in weights for thing in group if type(thing) == int))
		for x in range(len(weights)):
			weights[x][1] = nums[x]
		# Is dict conversion necessary? Could it even be a hindrance?
		# Addendum: yes, it was a hindrance. As of 0.51, they're 2D arrays.
		cons = list(weights)
		return vowels, cons

def chooseABC(strLen, abcCount = 0, abcString = '', vowelsLeft = 3, consLeft = 4):
	if not player1.testMode:
		print(f'\nYou\'ve chosen {abcCount}/{strLen} letters.')
		if vowelsLeft > 0: # Printing negative numbers...
			print(f'\nRequired vowels left: {vowelsLeft}')
		if consLeft > 0: # ...is ugly! Messages will only remain as long as they're needed
			print(f'Required consonants left: {consLeft}')

	if abcCount == strLen: # Max length - EXIT CASE
		print(f'\nLetters chosen!\nYour letters are: {abcString.strip()}\n') #T# Removes leading whitespace
		getWord(abcString)

	else: # If more letters needed
		if not player1.testMode:
			if vowelsLeft == strLen - abcCount: # Can only choose vowels
				print('You must choose a vowel.')
			elif consLeft == strLen - abcCount: # Can only choose consonants
				print('You must choose a consonant.')

			choiceVal = False  # Assume invalidity, trigger validation
			while not choiceVal: # Ensures valid input
				choice = input('Vowel or Consonant? (enter V or C)\n').upper()

				if choice not in ['V', 'C']: # Invalid entry
					if choice == '': # If null entry
						print('Please enter something.\n') # Prompt for entry
					else:  # Otherwise invalid
						print('Invalid letter.\nV for a Vowel, C for a Consonant.\n') # Prompt for validity
				else:  # Valid entry
					if vowelsLeft == strLen - abcCount and choice == 'C': # Can only choose vowels
						print('\nYou must choose a vowel!')
					elif consLeft == strLen - abcCount and choice == 'V': # Can only choose consonants
						print('\nYou must choose a consonant!')
					else:
						choiceVal = True # Pass

		else:
			testString = 'CVCVCVCVC'
			choice = testString[abcCount]


		if choice == 'V':
			vowelsLeft -= 1 # Required vowels left
		else:
			consLeft -= 1 # Required consonants left
		choice = replaceVC(choice) # Replace V/C placeholder with actual letter
		abcCount += 1 # Increment count (up to 9)
		abcString += f'{choice} ' # Spacing for readability
		if not player1.testMode:
			print(f'Chosen Letters: {abcString}')
		chooseABC(strLen, abcCount, abcString, vowelsLeft, consLeft) # Recurse

def replaceVC(abcType): # Replace placeholder with real letter
	if abcType == 'V': # If Vowel placeholder
		index = randint(0, max([i for pair in vowels for i in pair if type(i) == int])) # Sets range from 0 to max value in vowels[]
		for x in range(len(vowels)): # Checks range that randint falls into
			if index <= vowels[x][1]:
				return vowels[x][0].upper() # Return as choice

	else: # If Consonant placeholder
		index = randint(0, max([i for pair in cons for i in pair if type(i) == int])) # Sets range from 0 to max value in cons[]
		for x in range(len(cons)): # Check range that randint falls into
			if index <= cons[x][1]:
				return cons[x][0].upper() # Return as choice

def getWord(abcString):
	abcString = abcString.replace(' ', '') # Removing whitespace within the string for easy iteration over chars
	playerWord = input('Enter your word: ').lower()
	score = 0
	if playerWord == '': # Is this necessary, given the following ELIF?
		print('Nothing entered.')
	elif len(playerWord) < 4: # Too short
		print('Word must be at least four letters long to \
score points!') # Line break!
	else: # Long enough
		charVal = True # Assume true
		for userChar in playerWord:
			if userChar.upper() in abcString: # I had to remember that lowercase != uppercase.
				# Had to do an explicit upper()
				abcString = abcString.replace(userChar.upper(), '', 1) # Removes only one instance of letter if it appears
			else:
				if userChar.isnumeric():
					print('Invalid: numbers have been entered.')
				else:
					print(f'Letter \'{userChar.upper()}\' unavailable!')
				charVal = False
				break # Stop!
		if charVal: # Correct characters
			for word in wordDict: # Checking against every word in dictionary
				if playerWord == word: # If the player's word appears...
					if len(playerWord) == 9:
						score = 18 # Double points
					else:
						score = len(playerWord) #...score based on length of the word
					break # Stop searching, no point continuing.
			else:
				print('Word does not exist.')
	player1.addScore(score)
	if not player1.full:
		repeatVal = False
		while not repeatVal:
			repeatYN = input('\nPlay another Letters Round? \
(Y/N) ').strip().lower()
			if repeatYN not in ['y', 'n']:
				print('Y for Yes, N for No.')
			else:
				repeatVal = True
		if repeatYN == 'y':
			abcRound()

def findWord(): # See if word exists in wordDict
	search = input('\nEnter the word you\'d like to search \
(press ENTER to cancel): ').lower().replace(' ','').strip()
	if search is '':
		print('Search cancelled.\n')

	else:
		results = [word for word in wordDict if search == (word[0: len(search)] or word)] # First matching letters
		if len(results) is 0: # No matches
			print('No matching words found.')
		else:
			if len(results) > 50: # Large number of results.
				print(f'There are too many results ({len(results)}) to show.\n')
				limitVal = False
				while not limitVal:
					try:
						limit = int(input(f'How many matches would you like to \
show? You can show {len(results)} at most: ')) # Choice to limit output
						if limit in range(len(results)+1): # Valid chosen limit input
							limitVal = True
						else: # Invalid chosen limit
							print(f'Number not in valid range. Must be between 0 \
and {len(results)}.\n')
					except ValueError:
						print('Please enter a NUMBER.\n')
				if limit is not 0:
					# Small difference in output
					if limit is len(results):
						print(f'ALL {limit} MATCHES FOUND:')
					else:
						print(f'FIRST {limit} MATCHES FOUND:')
					for x in range(limit): print(results[x]) # Prints on separate lines
				else:
					print('Not showing any results.') # No output
			else:
				print(f'MATCHES FOUND: {len(results)}') # Standard output
				for match in results: print(match)
			buffer = input('\nPress ENTER to continue.')

		# Choose to search another word
		repeatVal = False
		while not repeatVal:
			repeatYN = input('\nWould you like to search another word? (Y/N) ').lower().strip()
			if repeatYN in ['y','n']:
				repeatVal = True
			else:
				print('Y for Yes, N for No.')
		if repeatYN == 'y':
			findWord() # Potential recursion. Essentially a loop.

def abcRound(): # Letters Round
	print('\n----LETTERS ROUND----')
	if player1.testMode:
		lenVal = False
		while not lenVal:
			try:
				strLen = int(input('\nHow many letters do you want to \
select?\n(Between 4 and 9 inclusive - standard is 9) '))
				if 4 <= strLen <= 9:
					lenVal = True
				else:
					print('Number of letters must be between 4 and 9.\n')
			except ValueError:
				print('Enter a valid NUMBER.')
	else:
		strLen = 9
	chooseABC(strLen)

def numRound(): # Numbers Round
	chooseNums()


def chooseNums(): # Choose numbers
	large = [25*i for i in range(1,5)] # Multiples of 25 up to 100
	small = 2 * [i for i in range(1,11)] # 1-10 twice

	print('\n----NUMBERS ROUND----')
	numsChosen = [] # List for selected numbers
	while len(numsChosen) < 6: # Choosing all six numbers
		if not player1.testMode:
			choiceVal = False
			while not choiceVal:
				choice = input('\nEnter L for a large number (25/50/75/100) \
or S for a small number (1-10)\n').upper().replace(' ','') # Explanation w/ line break
				if choice not in ['L','S']:
					print('Invalid entry.')
				else:
					choiceVal = True # Pass
		else:
			testNums = 'LSSLSS'
			choice = testNums[len(numsChosen)]
		if choice == 'L':
			if len(choice) is not 0:
				numsChosen.append(large[randint(0,len(large) - 1)]) # Add random large number
				large.remove(numsChosen[len(numsChosen) - 1]) # Removes the newly added element (if no duplicates allowed)
			else:
				print('All large numbers chosen. No more are available.\n')
		else:
			numsChosen.append(small[randint(0,len(small) - 1)]) # Add random small number
			small.remove(numsChosen[len(numsChosen) - 1]) # Removes that same number (if no duplicates allowed)
		if not player1.testMode:
			print(f'Your numbers so far are: {numsChosen}')

	target = randint(101,999) # Any three digit number
	print(f'\nTarget is {target}\nYour numbers are: {numsChosen}') # User can input now.

	score = 0
	answerVal = False
	while not answerVal:
		answer = input(f'Enter your closest answer. If you have no answer, \
just press the ENTER key: ').replace(' ','') # Handles accidental spaces
		if answer == '':
			print('No answer given.')
			answerVal = True
		else:
			if not answer.isnumeric():
				print('Please enter a VALID number.\n') # Prompt
			else:
				answer = int(answer)
				answerVal = True

	# Determining scoring
	if not (answer == '' or abs(target - answer) > 10): # If more than ten points away from target
		if check(numsChosen, answer): # Successful method check.
			if 6 <= abs(target - answer) <= 10: # Between 6-10 away...
				score = 5 #...gets 5 points
			elif 1 <= abs(target - answer) <= 5: # Between 1-5 away...
				score = 7 #...gets 7 points
			else: # Exact answer
				score = 10 # Full ten points

			if target == answer:
				print('You got the exact answer.')
			else:
				print(f'\nYou were {abs(target - answer)} away.') # Notify
		player1.addScore(score) # Update score

	else: # Points guaranteed if ≤10 away
		if answer is not '': # Answer is too far away
			print('Given answer outside of acceptable range.')
		print('No points scored.') # No score. Notify player

	if not player1.full:
		repeatVal = False
		while not repeatVal:
			repeatYN = input('\nPlay another Numbers Round? \
(Y/N) ').strip().lower()
			if repeatYN not in ['y', 'n']:
				print('Y for Yes, N for No.')
			else:
				repeatVal = True
		if repeatYN == 'y':
			numRound()

def check(numsChosen, answer, stepCount = 1, helper = False):
	if not helper: # Instructions at the start of every Numbers Round
		print('''\nThese are your valid operators:
+ denotes Addition,
- denotes Subtraction,
* denotes Multiplication,
/ denotes Division.
EXACTLY TWO numbers can have an operation performed on them.''')
		print('''\nThe proper input for an operation is:
x (insert operation) y
e.g. "16 / 2" (Spaces are optional)''')
		print('If you can\'t produce a method for your number, \
enter X to end the method check.\n')
		helper = True

	print(f'Your available numbers are: {sorted(numsChosen)}')
	step = input(f'Input step {stepCount}: ').replace(' ','') # x-y # Remove whitespace if present

	if step in ['X', 'x']:
		print('You forwent the method check.')
		return False
	for operation in '+-*/':
		if operation in step:
			break # Stop searching, as I need to use this operation
	else:
		print('Invalid operation!')
		return False

	# Only executed if operation found
	operands = step.split(operation) # Take the number either side of the operation sign
	if len(operands) != 2:
		print('Only two operands at a time allowed.')
		return False

	for x in range(len(operands)):
		try:
			operands[x] = int(operands[x])
		except ValueError:
			print('Invalid operand.')
			return False # Is there a way...
		else: # If no exception raised
			if operands[x] not in numsChosen:
				print(f'The number {operands[x]} was not found.')
				return False

	from operator import add, sub, mul, truediv as div
	if operation == '+': # Addition
		new = add(operands[0], operands[1])
	elif operation == '-': # Subtraction
		new = sub(operands[0], operands[1])
		if new < 0: # If result is negative
			print('Negative numbers are not allowed.')
			return False
	elif operation == '*': # Multiplication
		new = mul(operands[0], operands[1])
	else: # Division
		new = div(operands[0], operands[1])
		if new % 1 != 0: # If result is not an integer
			print('Only integers allowed.')
			return False
		else:
			new = int(new)
	print(f'{operands[0]} {operation} {operands[1]} = {new}\n') # Show operation and result
	for op in operands:
		numsChosen.remove(op) # Only removes one instance, since a list comprehension would
		#...eliminate all offending instances.
	numsChosen.append(new)
	if new == answer:
		return True
	elif len(numsChosen) == 1 and numsChosen[0] != answer: # No more moves
		print('No more moves - no more points!')
		return False

	stepCount += 1
	return check(numsChosen, answer, stepCount, helper) # Recurse!

def permute(): # Produces permutations of the word
	if not player1.testMode:
		string = conWords[randint(0, len(conWords) - 1)]
	else:
		string = 'relates'

	# Generating permutations of chosen word
	splStr = [char for char in string]
	perms = [''.join(perm) for perm in allPerms(splStr)]
	print(f'All {len(perms)} permutations generated.', end=' ')

	# Finding any anagrams
	anagrams = []
	for perm in perms:
		if perm in wordDict and perm not in anagrams: # No duplicates - BOTTLENECK
			anagrams.append(perm)
	print('Anagrams Done!', end = ' ')
	if player1.testMode:
		for elem in anagrams: print(elem)

	# Choosing scrambled version
	scramble = False
	while not scramble:
		x = randint(0, len(perms) - 1)
		if perms[x] not in anagrams:
			if player1.testMode: print(string, end = ' ')
			print(perms[x])
			scramble = True

	print(f'\nYour conundrum word is: {perms[x]}')
	answer = input('Input your answer: ').replace(' ', '') # Player answers
	# Removes accidental whitespace
	if answer in anagrams: # If in allowed answers
		print('Correct!')
		score = 10
	else: # Incorrect answer
		print(f'Incorrect answer. You could have had the following:') # Notify
		for word in anagrams: # Give possible answers
			print(word)
		score = 0
	player1.addScore(score)

def conundrum():
	permute() # Find all permutations

def fullGame():
	player1.full = True # Enforces particular rules
	resetVal = False
	while not resetVal:
		resetYN = input("\nReset your point total? (Y/N) ").lower()
		if resetYN not in ['y', 'n']:
			print('Y for Yes, N for No')
		else:
			if resetYN == 'y': # Start afresh
				player1.reset()
			resetVal = True
	player1.test()
	for cycle in range(1,4): # Mimics format of TV show
		abcRound()
		abcRound()
		numRound()
		print(f'At the end of Round {cycle}, you \
have {player1.total} points.\n') # Report score
	conundrum()
	print('\nFINAL SCORE')
	print(f'{player1.name}, you earned \
{player1.total} points in total.')
	playYN = input('Play again? (Y/N) ').lower()
	if playYN not in ['y', 'n']:
		print('Invalid choice. (Y \
for Yes and N for No.)')
	else:
		if playYN == 'y':
			fullGame()
	player1.full = False

def menu(): # Chooses type of round played/action taken
	play = True
	while play:
		print('\n----MAIN MENU----\n')
		choice = input('''1 to play a Letters Round
2 to play a Numbers Round
3 to play a Conundrum Round
4 to play a Full Game
5 to get your current total score
6 find a word in Word List
7 to reset points
8 to access Test Mode
9 to Quit
Choice: ''').replace(' ','') # Handles accidental whitespace
		if choice == '':
			print('Nothing entered - please enter something.')
		elif not choice.isnumeric():
			print('Please enter a NUMBER.')
		else:
			if int(choice) not in range(1,10):
				print('Invalid choice')
			else:
				if choice ==  '9':
					play = False
				else:
					if choice == '1':
						abcRound() # Letters round
					elif choice == '2':
						chooseNums() # Numbers round
					elif choice == '3':
						conundrum() # Play conundrum round
					elif choice == '4':
						fullGame() # Play full game
					elif choice == '5':
						player1.getScore() # Get current score
					elif choice == '6':
						findWord() # Search Word List
					elif choice == '7':
						player1.reset() # Set points to zero
					elif choice == '8':
						player1.test() # Disable/Enable Test Mode
	print(f'Quitting game. Thanks for playing, {player1.name}.') # Only when WHILE loop is executed

if __name__ == '__main__':
	player1 = Player() # Instantiation of Player
	player1.testMode = player1.test() # Determines test mode - changeable after each round
	wordDict, conWords, vowels, cons = start() # Setup and start game
	print(f'Welcome to Countdown Lite, {player1.name}!')
	menu()
