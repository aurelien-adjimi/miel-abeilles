import beehive

def main():
    hive = beehive.Bees() # Creates an instance of the beehive.Bees() class and stores it in the hive variable. This initializes the bee simulation environment
    avgList = [] # This list will be used to store the average values ​​of the generation
    hive.generate_initial_bees() # Calls the method on the hive object, which initially generates a population of bees

    for i in range(100): # To simulate for 100 generation 
        if i % 10 == 0: # checks if i (the generation number) is a multiple of 10
            hive.mutation() # Introduce a mutation of the hive
        hive.evaluation() # Evaluate the population and select the best
        fit = hive.mate() # For the mating
        avg = hive.avg(fit) # calculate the average of the fitness scores ​​of the bees.
        avgList.append(avg) # Add the average value to the list

        fitList = [] # To store the individual fitness scores
        for n in hive.bees:
            fitList.append(n.fitnessScore)

    hive.generate_genealogy()
    for generation_info in hive.genealogy_tree:
        print(f"Generation {generation_info['Generation']}: Bee {generation_info['Bee']} (Parents: {generation_info['Parents']})")

    hive.best_path_visualisation()
    hive.best_bees_visualisation()
    hive.avg_generation_visualisation(avgList)

main()