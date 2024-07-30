import random , copy , math , csv
from collections import Counter


import random
import copy

class GeneticAlgorithm:
    def __init__(self, popSize: int, items: dict, maxWeight: float, maxGenerations: int = 2000, elitPortion: float = 0.5, mutationChance: float = 0.3):
        self.population = []
        self.popSize = popSize
        self.maxGenerations = maxGenerations
        self.elitPortion = elitPortion
        self.mutationChance = mutationChance
        self.maxWeight = maxWeight
        # making sure that the same parent isn't selected twice, making it fair
        self.selectedAsParents = []
        # dictionary of items with their value, weight, and available amount
        self.items = items
        # current global high
        self.globalMax = {"solution": [], "value": 0, "generation": 0}
        self.visited = []

    def search(self):
        newPopulation = self.population
        generations = 0

        while generations <= self.maxGenerations:
            fitPopulation = []

            # calculating and arranging the populations fitness
            for item in newPopulation:
                fitPopulation.append(
                    (item, self.fitness(solution=item))
                )
            fitPopulation.sort(key=lambda a: a[1], reverse=True)
            
            # print out the current best solution before creating new children
            currentBestValue = fitPopulation[0][1]

            # holding a global maximum, not to lose it to mutation or reproduction
            if self.globalMax["value"] < currentBestValue:
                bestPath = copy.deepcopy(fitPopulation[0][0])
                self.globalMax = {"solution": bestPath, "value": currentBestValue, "generation": generations}
                
               

                self.visited.append([generations, currentBestValue])

            # elit portion of the population
            elitSize = int(len(fitPopulation) * self.elitPortion)
            elitPop = [x[0] for x in fitPopulation[:elitSize]]

            # select parents from the elit population to reproduce and fill back the population
            for i in range(elitSize):
                male, female = self.selectParents(population=elitPop)
                child = self.reproduce(male, female)
                elitPop.append(child)

            newPopulation = [x for x in elitPop]
            self.selectedAsParents = []
            generations += 1

        return self.globalMax

    def fitness(self, solution: list):
        total_value = 0
        total_weight = 0
        for item in solution:
            item_name, item_quantity = list(item.items())[0]
            total_value += self.items[item_name]['value'] * item_quantity
            total_weight += self.items[item_name]['weight'] * item_quantity
        if total_weight > self.maxWeight:
            return 0
        else:
            return total_value

    def createPopulation(self):
        # generate potential solutions (population) - about 10,000 of them
        solutions = []
        count = 0
        while count < self.popSize:
            solution = []
            for item_name, item_details in self.items.items():
                max_item_amount = min(item_details["availableAmount"], int(self.maxWeight / item_details["weight"]))
                solution.append({item_name: random.randint(0, max_item_amount)})
            solutions.append(solution)
            count += 1
        self.population = solutions

    def selectParents(self, population):
        x = random.randint(0, len(population) - 1)
        while True:
            y = random.randint(0, len(population) - 1)
            if x != y:
                return population[x], population[y]

    def reproduce(self, parent_one, parent_two):
        cutting_point = random.randint(0, len(parent_one) - 1)
        child = parent_one[:cutting_point] + parent_two[cutting_point:]
        if random.random() < self.mutationChance:
            return self.mutate(child)
        return child

    def mutate(self, child):
        copied = copy.deepcopy(child)
        for item_index, item in enumerate(copied):
            item_name, item_quantity = list(item.items())[0]
            max_amount = min(self.items[item_name]["availableAmount"], int(self.maxWeight / self.items[item_name]["weight"]))
            if item_quantity > max_amount:
                copied[item_index][item_name] = max_amount
        return copied



class HillClimbing:
    def __init__(self , items : dict , maxWeight : float , maxTries : int = 1000):
        self.items = items
        self.maxWeight = maxWeight
        self.maxTries = maxTries
        self.currentSol = None
        self.visited = []

    def search(self):
        count = 0
        self.currentSol = self.generateSol()
        best_solution = {"solution": self.currentSol, "value": self.stateSocre(self.currentSol)}
        while count <= self.maxTries:
            neighbor = self.getNeighbor(self.currentSol)
            oldEnergy = self.stateSocre(self.currentSol)
            newEnergy = self.stateSocre(neighbor)

            if oldEnergy < newEnergy:
                self.currentSol = copy.deepcopy(neighbor)
                current_value = self.stateSocre(self.currentSol)
                if current_value > best_solution["value"]:
                    best_solution = {"solution": self.currentSol, "value": current_value}
                count = 0
            else:
                count += 1
                
        return best_solution



    def stateSocre(self , solution):
        total_value = 0
        total_weight = 0
        itemsInSolution = [[*x].pop() for x in solution]
        for item in itemsInSolution:
            index = itemsInSolution.index(item)
            total_value += self.items[item]['value'] * solution[index][item]
            total_weight += self.items[item]['weight'] * solution[index][item]
        if total_weight > self.maxWeight:
            return 0
        else:
            return total_value

    def generateSol(self):
        '''We generate a random solution'''
        items = [*self.items]
        weight = 0
        potentialWeight = 0
        sol = []
        for item in items:
            potentialAmount = random.randint(0 , self.items[item]["availableAmount"])
            potentialWeight = weight + (potentialAmount * self.items[item]["weight"]) 
            while potentialWeight > self.maxWeight and potentialAmount > 0:
                potentialAmount -= 1
                potentialWeight = weight + (potentialAmount * self.items[item]["weight"])
            potentialAmount = 0 if potentialAmount < 0 else potentialAmount
            sol.append({item : potentialAmount})
            weight += potentialAmount * self.items[item]["weight"]
        return sol
    
    def getNeighbor(self , state):
        '''
            Inorder to find neighbors of state we decided to make a function that makes use of two methods.
                - Swapping the amounts between two items
                - Decrementing/incrementing the amount between items
            One of the two is choosen based on a probability , 70% of the time we swap amounts and 30% of the time we either increment/decrement them(50% chance of either happening)
        '''
        neighbors = []
        #generate 10 neighbours 
        for i in range(10):
            copied = copy.deepcopy(state)
            if random.random() < .98:
                #swaping is chosen
                itemOne = random.randint(0 , (len(state) - 1))
                itemTwo = random.randint(0 , (len(state) - 1))
                while itemOne == itemTwo:
                    itemTwo = random.randint(0 , (len(state) - 1))

                #we did this because our solution is a list of dictionaries , [{'itemName' : amount}]
                itemOneName = [*copied[itemOne]].pop()
                itemTwoName = [*copied[itemTwo]].pop()

                copied[itemOne][itemOneName] , copied[itemTwo][itemTwoName] = copied[itemTwo][itemTwoName] , copied[itemOne][itemOneName]
                neighbors.append((copied , self.stateSocre(copied))) 

            else:
                done = False
                while not done:
                    #incrementing/decrementing is chosen
                    selectedItem = random.randint(0 , (len(state) - 1))
                    if random.random() < 0.58:
                        #choose increment
                        itemName = [*copied[selectedItem]].pop()
                        maxAmount = self.items[itemName]["availableAmount"]
                        if (copied[selectedItem][itemName] + 1) < maxAmount: 
                            copied[selectedItem][itemName] += 1
                            done = True
                    else:
                        #choose decrement
                        itemName = [*copied[selectedItem]].pop()
                        if (copied[selectedItem][itemName] - 1) > 0:
                            copied[selectedItem][itemName] -= 1
                            done = True
                neighbors.append((copied , self.stateSocre(copied)))
        
        #order them form best to worst
        neighbors.sort(key= lambda a : a[1] , reverse=True)
        #return the best
        return neighbors[0][0]

class SimulatedAnnealing:
    '''This is a variant of Hill-Climbing algorithm that occasionally accepts bad solutions in the hopes of getting a better solution.'''
    def __init__(self , maxWeight : float , temp : float = 100 , coolingRate : float = 0.01 , items : dict = None):
        self.items = items
        self.maxWeight = maxWeight
        self.temp = temp
        self.coolingRate = coolingRate
        self.bestSol = None
        self.visited = []

    def search(self):
        self.currentSol = self.generateSol()
        self.bestSol = self.currentSol
        while self.temp > 1:
            #generate neighbour
            neighbor = self.getNeighbor(self.currentSol)
            
            oldEnergy = self.stateSocre(self.currentSol)
            newEnergy = self.stateSocre(neighbor)

            #if neighbour is better than current exchange
            if oldEnergy < newEnergy:
                self.currentSol = copy.deepcopy(neighbor)
                if self.stateSocre(self.currentSol) > self.stateSocre(self.bestSol):
                    self.bestSol = copy.deepcopy(neighbor)
            else:
                #which is negative at this point
                delta = newEnergy - oldEnergy
                if delta != 0:
                    try:
                        probability = math.e ** (-delta/self.temp)
                        if random.random() < probability:
                            self.currentSol = copy.deepcopy(neighbor)
                    except Exception as e:
                        pass
            self.temp -= (1- self.coolingRate)

        return {"solution" : self.bestSol , "value" : self.stateSocre(self.bestSol)}
    
    def stateSocre(self , solution):
        total_value = 0
        total_weight = 0
        itemsInSolution = [[*x].pop() for x in solution]
        for item in itemsInSolution:
            index = itemsInSolution.index(item)
            total_value += self.items[item]['value'] * solution[index][item]
            total_weight += self.items[item]['weight'] * solution[index][item]
        if total_weight > self.maxWeight:
            return 0
        else:
            return total_value
        
    def generateSol(self):
        
        items = [*self.items]
        weight = 0
        potentialWeight = 0
        sol = []
        '''We generate a random solution'''
        for item in items:
            potentialAmount = random.randint(0 , self.items[item]["availableAmount"])
            potentialWeight = weight + (potentialAmount * self.items[item]["weight"]) 
            while potentialWeight > self.maxWeight and potentialAmount > 0:
                potentialAmount -= 1
                potentialWeight = weight + (potentialAmount * self.items[item]["weight"])
            potentialAmount = 0 if potentialAmount < 0 else potentialAmount
            sol.append({item : potentialAmount})
            weight += potentialAmount * self.items[item]["weight"]
        
        return sol
    
    def getNeighbor(self , state):
        '''
            Inorder to find neighbors of state we decided to make a function that makes use of two methods.
                - Swapping the amounts between two items
                - Decrementing/incrementing the amount between items
            One of the two is choosen based on a probability , 70% of the time we swap amounts and 30% of the time we either increment/decrement them(50% chance of either happening)
        '''
        
        neighbors = []
        #generate 10 neighbours 
        for i in range(10):
            copied = copy.deepcopy(state)
            if random.random() < .58:
                #swaping is chosen
                itemOne = random.randint(0 , (len(state) - 1))
                itemTwo = random.randint(0 , (len(state) - 1))
                while itemOne == itemTwo:
                    itemTwo = random.randint(0 , (len(state) - 1))

                #we did this because our solution is a list of dictionaries , [{'itemName' : amount}]
                itemOneName = [*copied[itemOne]].pop()
                itemTwoName = [*copied[itemTwo]].pop()

                copied[itemOne][itemOneName] , copied[itemTwo][itemTwoName] = copied[itemTwo][itemTwoName] , copied[itemOne][itemOneName]
                neighbors.append((copied , self.stateSocre(copied))) 

            else:
                done = False
                while not done:
                    #incrementing/decrementing is chosen
                    selectedItem = random.randint(0 , (len(state) - 1))
                    if random.random() < 0.68:
                        #choose increment
                        itemName = [*copied[selectedItem]].pop()
                        maxAmount = self.items[itemName]["availableAmount"]
                        if (copied[selectedItem][itemName] + 1) < maxAmount: 
                            copied[selectedItem][itemName] += 1
                            done = True
                    else:
                        #choose decrement
                        itemName = [*copied[selectedItem]].pop()
                        if (copied[selectedItem][itemName] - 1) > 0:
                            copied[selectedItem][itemName] -= 1
                            done = True
                neighbors.append((copied , self.stateSocre(copied)))
        
        #order them form best to worst
        neighbors.sort(key= lambda a : a[1] , reverse=True)
        #return the best
        return neighbors[0][0]
    

