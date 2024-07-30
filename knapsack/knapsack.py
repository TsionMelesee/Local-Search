import argparse

from localsearch import *



if __name__ == '__main__':
    #setting up command line arguments
    parser = argparse.ArgumentParser(description="Argument parser for selecting algorithm and file")
    parser.add_argument("--algorithm" , type=str , help="Define which algorithm to use: hc(hill climbing) , ga(genetic algorithm) , sa(simulated annealing)" , default='ga')
    parser.add_argument("--file" , type=str , help="path to a txt file containing the items to solve the knapsack problem for." , default='my-file.txt')
    
    args = parser.parse_args()

    #get the total allowed weight and items
    txtFile = open(args.file).read().split('\n')
    print("Best solution")
    maxWeight = float(txtFile[0])
    keys = ["item" , "weight" , "price"]
    items = {}
    for item in txtFile[2:]:
        
        splitedItem = item.split(',')
        
        items[splitedItem[0]] = {"value" : int(splitedItem[2]) , 'weight' : float(splitedItem[1]) , "availableAmount" : int(splitedItem[3])}        

    #choosing the algorithm based on the argument provided
    if args.algorithm == 'ga':
        algo = GeneticAlgorithm(popSize=700 , items=items , maxWeight=maxWeight , mutationChance=1 , maxGenerations=600)
        algo.createPopulation()
        ans = algo.search()
        print("*************************")
        print(ans)

    elif args.algorithm == 'hc':
        algo = HillClimbing(items=items , maxWeight=maxWeight , maxTries= 1000)
        ans = algo.search()
        print("**************************")
        print(ans)
    
    elif args.algorithm == 'sa':
        algo = SimulatedAnnealing(items=items , maxWeight=maxWeight , coolingRate=0.5 , temp=10000)
        ans = algo.search()
        print("#########################")
        print(ans)    
    
    else:
        print("Unkown algorithm choose. Choose from:  hc(hill climbing) , ga(genetic algorithm) and sa(simulated annealing) ")