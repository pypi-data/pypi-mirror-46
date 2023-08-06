class Submarine: #capital letter
#self is object that you call
	'''
		-----------------
		Test Documentaton
		-----------------
	'''

	def __init__(self,price=10000,budget=40000): #always type "self" in bracket #initial

		self.captain = 'Prawit' #ref self
		self.sub_name = 'Uncle I'
		# self.price = 10000 #million
		self.price = price
		self.kilo = 0
		self.budget = budget
		self.totalcost = 0

	def Missile(self): #dont 4get "self"
		print('We are Department of Missile')

	def Calcommission(self):
		percent = self.price * (0.1)
		print('Loong! You got : {} Million Baht'.format(percent)) # .format is place holder
		'''
		อิอิ
		'''
	def Goto(self,enemypoint,distance):
		print(f"Let's go to {enemypoint} distance :{distance} KM")
		#		print('Let\'s go')
		self.kilo = self.kilo + distance #kilo from init #distance from Goto
		self.Fuel()

	def Fuel(self):
		deisel = 20
		cal_fuel_cost = self.kilo * deisel
		print('Current fuel cost: {:,d} Baht'.format(cal_fuel_cost)) #{:,d} comma added
		self.totalcost += cal_fuel_cost #added #totalcost = totalcost + cal fuel
	
	@property
	def BudgetRemaining(self):
		remaining = self.budget - self.totalcost #tabbbbbbbbbbb
		# print('Budget Remaining : {:,.2f} Baht'.format(remaining))	
		return remaining
		#property is to print out of def & no ()
class ElectricSubmarine(Submarine): #inheritance from above class
	def __init__(self,price=10000,budget=40000):
		self.sub_name = 'Uncle III'
		self.Battery_distance = 100000
		#100000 km/100%
		super().__init__(price,budget)
		#inheritance by type super
		#copy everything about

	def Battery(self):
		allbattery = 100
		calculate = (self.kilo/self.Battery_distance)*100
		print('We have Battery remain {} %'.format(allbattery-calculate))

	def Fuel(self):
		deisel = 20
		cal_fuel_cost = self.kilo * deisel
		print('Current Power cost: {:,d} Baht'.format(cal_fuel_cost)) #{:,d} comma added
		self.totalcost += cal_fuel_cost	

if __name__ =='__main__':

	tesla = ElectricSubmarine(400000,2000000)
	print(tesla.captain)
	print(tesla.budget)
	tesla.Goto('Japan',10000)
	print(tesla.BudgetRemaining)

	# tesla.Fuel()
	tesla.Battery()
	print(tesla.BudgetRemaining)
	tesla.Fuel()


	#############33
	kongtabbok = ElectricSubmarine(400000,2000000)
	print(kongtabbok.captain)
	print(kongtabbok.budget)
	kongtabbok.Goto('Japan',10000)
	print(kongtabbok.BudgetRemaining)




# print('----Submarine No.1----')
# kongtabreuw = Submarine(1000) #กองทัพเรือ
# print(kongtabreuw.captain)
# print(kongtabreuw.sub_name)
# print(kongtabreuw.kilo)
# kongtabreuw.Goto('China',7000)
# print(kongtabreuw.kilo)
# kongtabreuw.Fuel()
# Current_budget = kongtabreuw.BudgetRemaining
# print(Current_budget * 0.2)
# print(kongtabreuw.BudgetRemaining)
# kongtabreuw.Calcommission()
# #######################################
# print('----Submarine No.2----')
# kongtabbok = Submarine(70000)
# print('Before...')
# print(kongtabbok.captain)
# print('After...')
# kongtabbok.captain = 'Srivara'
# print(kongtabbok.captain)


















#class is an object for reference def
# sub = ['Sriwvara','Uncle II',5000]
# print('------')
# print(sub[0])
# print(sub[1])
# print(sub[2])
