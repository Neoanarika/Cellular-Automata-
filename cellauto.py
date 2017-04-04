import random
import time
import math 
class genetic:
	def mutate(self,rule):
		rule = list(rule)
		geneset = ['-','+','=','X']
		a = random.randint(0,8)
		new_gene = geneset[random.randint(0,3)]
		while(new_gene == rule[a]):
			new_gene = geneset[random.randint(0,3)]
		rule[a] = new_gene
		return ''.join(rule)

	def info_fitness(self,grid,sizeN):
		x = 0
		for row in grid:
			for unit in row:
				if(unit == 1):
					x+=1

		prob = x/(sizeN*sizeN)
		information = -prob * math.log2(prob) - (1-prob)*math.log2(1-prob)

		return information

	def fitness(self,grid,sizeN):
		x = 0
		for row in grid:
			for unit in row:
				if(unit == 1):
					x+=1

		return x
class grid:
	def inital_grid(self,x,prob):
		grid = [ [ 0 if random.random() > prob else 1 for _ in range(x)] for _ in range(x)]
		return grid

	def generate_grid(self,grid):
		for x in grid:
			l = 0
			for a in x:
				if(a == 1):
					if(l != len(x)-1):
						print("*",end='')
					else:
						print("*")
				else:
					if(l != len(x)-1):
						print(".",end='')
					else:
						print(".")
				l+=1
	
	def countingL(self,grid,sizeN):
		Lgrid = [['A' for x in i]for i in grid]
		y = 0
		for row in grid:
			x = 0
			for unit in row:
				if(x == 0):
					if(y == 0):
						Lgrid[0][0] = grid[0][1] + grid[1][0] + grid[1][1]
					elif(y == sizeN -1):
						Lgrid[sizeN-1][0] = grid[sizeN-1][1] + grid[sizeN-2][0] + grid[sizeN-2][1]
					else:
						Lgrid[y][0] = grid[y-1][0] + grid[y+1][0] + grid[y][1] + grid[y-1][1] + grid[y+1][1] 

				elif(x == sizeN -1):
					if(y == 0):
						Lgrid[0][sizeN-1]  = grid[0][sizeN-2] + grid[1][sizeN-2] + grid[1][sizeN-1]
					elif(y==sizeN-1):
						Lgrid[sizeN-1][sizeN-1] = grid[sizeN-1][sizeN-2] + grid[sizeN-2][sizeN-1] + grid[sizeN-2][sizeN-2]
					else: 
						Lgrid[y][sizeN -1] = grid[y+1][sizeN-1] + grid[y-1][sizeN-1] + grid[y][sizeN -2] + grid[y-1][sizeN -2] + grid[y+1][sizeN -2] 
				
				elif(y == 0):
					if(0 < x < sizeN-1):
						Lgrid[0][x] = grid[0][x-1] + grid[0][x+1] + grid[1][x] + grid[1][x-1] + grid[1][x+1]

				elif(y == sizeN-1):
					if(0 < x < sizeN-1):
						Lgrid[sizeN-1][x] = grid[sizeN-1][x-1] + grid[sizeN-1][x+1] + grid[sizeN-2][x] + grid[sizeN-2][x-1] + grid[sizeN-2][x+1]
				
				else:
					Lgrid[y][x] = grid[y-1][x] + grid[y-1][x+1] + grid[y-1][x-1] + grid[y][x+1] + grid[y][x-1] + grid[y+1][x-1] + grid[y+1][x] + grid[y+1][x+1]
				x+=1
			y+=1
		return Lgrid

	def new_grid(self,rules,grid,Lgrid):
		rule = list(rules)
		new_grid = [['A' for x in i]for i in grid]
		y = 0 
		for row in Lgrid:
			x = 0
			for unit in row:
				if(rule[unit] == "-"):
					new_grid[y][x] = 0
				elif(rule[unit] == "+"):
					new_grid[y][x] = 1
				elif(rule[unit] == "="):
					new_grid[y][x] = grid[y][x]
				elif(rule[unit] == "X"):
					if(grid[y][x] == 0):
						new_grid[y][x] = 1
					else:
						new_grid[y][x] = 0
				x +=1
			y+=1

		return new_grid

grid = grid()
genetic = genetic()
size = 50
rules = '--=+-----'
grid_prime = grid.inital_grid(size,0.1)
grids = grid_prime
#Visualisaiton 
x = 0
for _ in range(10000):
	grid.generate_grid(grids)
	print("")
	Lgrid = grid.countingL(grids,size)
	time.sleep(1.0/10.0)
	rule_mutate = genetic.mutate(rules)
	#if(genetic.fitness(grid.new_grid(rule_mutate,grid_prime,Lgrid),size) > genetic.fitness(grid.new_grid(rules,grid_prime,Lgrid),size)):
	#	rules = rule_mutate
	
	if(genetic.info_fitness(grid.new_grid(rule_mutate,grid_prime,Lgrid),size) > genetic.info_fitness(grid.new_grid(rules,grid_prime,Lgrid),size)):
		rules = rule_mutate

	print(rules +" "+str(x))
	grids = grid.new_grid(rules,grid_prime,Lgrid)
	x +=1

