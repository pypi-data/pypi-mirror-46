class Submarine:
	'''
		------------------
		test Documentation
		This is a program for submarine
		------------------	
	'''

	def __init__(self, price=10000, budget=40000): #default value

		self.captain = 'Captain Thailand'
		self.sub_name = 'Sub 1'
		self.price = price
		self.kilo = 0
		self.budget = budget
		self.totalcost = 0
		# print(self.kilo)

	def Missile(self):
		print('We are Department of Missile')

	def Calcommission(self):
		'''This is a function for calculating commission'''
		pc = 10 #percent
		percent = self.price * (pc/100)
		print('Hey! You received: {} Million Baht'.format(percent))

	def Goto(self, enemypoint, distance):
		# print(f"Let's go to {enemypoint} Distance: {distance}")
		print('Let\'s go to {} Distance: {} KM'.format(enemypoint,distance))
		self.kilo = self.kilo + distance
		self.Fuel()

	def Fuel(self):
		diesel = 20 # 20B /Liter
		cal_fuel_cost = self.kilo * diesel
		print('Current Fuel Cost: {:,d} Baht'.format(cal_fuel_cost))
		self.totalcost += cal_fuel_cost

	@property	# for making this function to be a noun for further usage in RETUEN value
	def BudgetRemaining(self):
		remaining = self.budget - self.totalcost
		print('Remaining budget is {:,.2f} Baht'.format(remaining))
		return remaining

#### Inheritance class
class ElectricSubmarine(Submarine): #### Inherited from Submarine class

	def __init__(self, price=10000, budget=40000):
		self.sub_name = 'Sub 2'
		# Submarine can go out 100000 km/ 100 percent
		self.battery_distance = 100000 # submarine
		super().__init__(price,budget)  ## inherit class or copy all functions from the original class

	def Battery(self):
		allbattery = 100
		calculate = self.kilo / self.battery_distance
		print('Cal:', calculate)
		print('We have Battery remaining: {} %'.format(allbattery-calculate))


	def Fuel(self):
		kilowatcost = 5 # 20B /Liter
		cal_power_cost = self.kilo * kilowatcost
		print('Current Power Cost: {:,d} Baht'.format(cal_power_cost))
		self.totalcost += cal_power_cost

if __name__ == '__main__':

	tesla = ElectricSubmarine(40000,2000000)
	print(tesla.captain)
	print(tesla.budget)
	tesla.Goto('Japan',10000)
	print(tesla.BudgetRemaining)
	tesla.Battery()

	print('----------------------')

	team3 = Submarine(40000,2000000)
	print(team3.captain)
	print(team3.budget)
	team3.Goto('Japan',10000)
	print(team3.BudgetRemaining)
	# team3.Battery() # can't

	print('----------------------')

# print(team3.Battery)


'''
team1 = Submarine(12343) # navy is the object of the class
print(team1.kilo)
team1.Goto('China',123)
print(team1.kilo)
team1.Fuel()
current_budget = team1.BudgetRemaining
print(current_budget * 0.2)
# print(navy.captain)
# print(navy.sub_name)

team1.Calcommission()
#######################
print('------Sub No.2--------')
team2 = Submarine(70000)
print('before...')
print(team2.captain)
print('After.,,')
team2.captain = 'Captain USA'
print(team2.captain) # possible to change variable in the class
'''