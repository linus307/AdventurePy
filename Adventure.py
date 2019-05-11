import os, pickle

class Game:
	def __init__(self, name, intro, outro, firstRoom):
		self.name = name
		self.intro = intro
		self.outro = outro
		self.firstRoom = firstRoom
		self.players = []
		self.loadGame()
		self.p = None
		
	def startGame(self):
		while(len(self.players) != 0):
			print("Choose Number of save:")
			for i in range(1, len(self.players) + 1):
				print("[" + str(i) + "] " + self.players[i-1].name)
			print("\n[" + str(len(self.players) + 1) + "] Create a new one")
			print("\n[" + str(len(self.players) + 2) + "] Delete one")
			terminalInput = int(input("\nNumber:")) - 1
			if(0 <= terminalInput < len(self.players)):
				self.p = self.players[terminalInput]
				break
			elif(terminalInput == len(self.players)):
				break
			elif(terminalInput == len(self.players) + 1):
				while(len(self.players) != 0):
					print("Choose Number of save you want to delete:")
					for i in range(1, len(self.players) + 1):
						print("[" + str(i) + "] " + self.players[i-1].name)
					print("\n[" + str(len(self.players) + 1) + "] Cancel operation")
					terminalInput = int(input("\nNumber:")) - 1
					if(0 <= terminalInput < len(self.players)):
						self.players.remove(self.players[terminalInput])
						break
					elif(terminalInput == len(self.players)):
						break
					else:
						print("Please input a valid value!")
			else:
				print("Please input a valid value!")
		if (self.p == None):
			print("Please create a save.")
			self.p = Player(str(input("Name save: ")), self.firstRoom)
			self.players.append(self.p)
			print(self.name)
			for text in self.intro[:-1]:
				print(text + "\nPress Enter ...\n")
				input()
			print(self.intro[-1])
		self.runGame()
		
	def loadGame(self):
		if(os.path.exists("./" + self.name + ".sav")):
			with open(self.name + '.sav', 'rb') as saveFile:
				self.players = pickle.load(saveFile)
			
	def saveGame(self):
		if(os.path.exists("./" + self.name + ".sav")):
			with open(self.name + '.sav', 'wb') as saveFile:
				pickle.dump(self.players, saveFile, protocol=pickle.HIGHEST_PROTOCOL)
		else:
			inputTerminal = ""
			while(True):
				inputTerminal = str(input("There is no existing savefile. If you want to create one type \"y\" and if you don't type \"n\". Remember you won't be able to save your progress without one!"))
				if(inputTerminal == "y"):
					with open(self.name + '.sav', 'wb') as saveFile:
						pickle.dump(self.players, saveFile, protocol=pickle.HIGHEST_PROTOCOL)
					return
				elif(inputTerminal == "n"):
					return
				else:
					print("Please input a valid value!")
			
	def runGame(self):
		global p
		p = self.p
		while True:
			inputTerminal = input()
			if(inputTerminal.split()[0] == "goto"):
				p.currentRoom.goto(inputTerminal.split()[1])
			if(inputTerminal == "discribe"):
				p.currentRoom.discribe()
			if(inputTerminal == "look_around"):
				p.currentRoom.lookAround()
			if(inputTerminal == "save"):
				self.saveGame()
				print("saved")
			if(inputTerminal == "exit"):
				return

class Event:
	def __init__(self, condition, event, unique = False):
		self.eventHappend = False
		self.unique = unique
		self.condition = condition
		self.event = event
		
	def testEvent(self):
		if(self.condition() and self.eventHappend == False):
			self.event()
			if(self.unique):
				self.eventHappend = True
	
	
class Room:
	def __init__(self, name, discription, findable, nextRooms = []):
		self.discribed = 0
		self.lookedAround = 0
		self.name = name
		self.discription = discription
		self.findable = findable
		self.nextRooms = nextRooms
		self.entranceEvent = Event(trueCondition, None)
		self.leavingEvent = Event(trueCondition, None)
		self.discribeEvent = Event(trueCondition, None)
		self.lookAroundEvent = Event(trueCondition, None)
		
	def discribe(self):
		print(self.discription)
		self.discribed += 1
		if(self.discribeEvent.event != None):
			self.discribeEvent.testEvent()
		
	def lookAround(self):
		print(self.findable)
		self.lookedAround += 1
		if(self.lookAroundEvent.event != None):
			self.lookAroundEvent.testEvent()
		
	def goto(self, nextRoom):
		if(nextRoom == self.name):
			print("I'm already in that room.")
		else:
			for room in self.nextRooms:
				if(room.name == nextRoom):
					if(self.leavingEvent.event != None):
						self.leavingEvent.testEvent()
					p.currentRoom = room
					break
			if(p.currentRoom == self):
				print("I can't find that place in here.")
			else:
				if(p.currentRoom.entranceEvent.event != None):
					p.currentRoom.entranceEvent.testEvent()


class Player:
	def __init__(self, name, start = None):
		if(type(name) != str and type(start) != Room):
			raise TypeError("Wrong parameter types while initializing Player object!")
		self.name = name
		self.currentRoom = start
		

def trueCondition():
	return True