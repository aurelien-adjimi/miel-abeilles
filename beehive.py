import random
import math
import pandas as pd
import matplotlib.pyplot as plt

class Bee: 

    def __init__(self, id = 0) -> None:
        self.id = id
        self.listOfFlower = []
        self.fitnessScore = 0

# Allow to read a csv file to get the coordinates
    def csv(self):
        df = pd.read_csv('Assets/flower.csv', header = 0) # Read the csv via the path with Pandas 
        return [(x, y) for x, y in zip(df['x'], df['y'])] # Extract the flowers coordinates 

# Generate a random path    
    def random_generate(self):
        df = self.csv() # To get the flower coordinates list
        random.shuffle(df) # Shuffle randomly the tuples 
        self.listOfFlower = [(x, y) for x, y in df]  # Create a new list 
        self.set() # Call 'set' method to calculate the fitness score

# To define the flower order to gather
    def setFlower(self, flower:list):
        self.listOfFlower = flower # Assign the flower list given as a value of attribute 'listOfFlower'
        self.set()

# To calculate the fitness score for bees
    def set(self):
        for i in range(len(self.listOfFlower)): # Runs all the flowers in the current order defined by the list
            x1, y1 = self.listOfFlower[i]
            x2, y2 = self.listOfFlower[(i + 1) % len(self.listOfFlower)]
            self.fitnessScore += int(math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)) # The Euclidian Distance is calculated 

class Bees:

    def __init__(self) -> None:
        self.hive = 0
        self.beeList = []
        self.bestBees = []
        self.bees = []
        self.child = []
        self.genealogy_tree = []

# To generate the first generation of bees
    def generate_initial_bees(self):
        for i in range(100):
            bee = Bee(i) # Each iteration a new instance of bee is created using 'Bee' class. Th eargument 'i' is given to the constructor so each bee is created with a unique id
            bee.random_generate() # Generate a random sequence to gather the flowers
            self.bees.append(bee) # The new bee is added to the list
            self.beeList.append((bee.id, bee.fitnessScore)) # The id and the fitness score are added as tuples to the list

# To generate 2 children for the best 50 bees
    def generate_children(self, flowerList1, flowerList2):
        child1 = Bee(self.hive) # Create a new instance of 'Bee'
        self.hive += 1 # Increment 'self.hive' is used to ensure that every child will be created with a unique ID
        child2 = Bee(self.hive) # Create a new instance of 'Bee'
        self.hive += 1 # Increment 'self.hive' is used to ensure that every child will be created with a unique ID
        child1.listOfFlower = flowerList1 # Assigns the list of flowers 'flowerList1' to 'listOfFlower' This means that child1 will follow the flower visiting sequence defined in flowerList1.
        child2.listOfFlower = flowerList2
        child1.set() # To calculate fitness score
        child2.set()
        return child1, child2 # Return the tuple with the 2 new bees

# To sort the bees by their fitness score and keep the best 50   
    def evaluation(self):
        classedList = sorted(self.bees, key=lambda x: x.fitnessScore) # Creates a new list by sorting the bees on their fitnessScore
        self.bees = classedList[:50] # Replace the 50 bees by the 50 child
        self.bestBees.append(self.bees[0].fitnessScore) # Add the fitness score 

# To generate mating for the best 50 bees
    def mate(self):
        availableBees = self.bees.copy() # Create a copy of the bees list in a new list. Used to make the selection of parents without affecting the original list 
        for i in range(25):
                rdmBee1 = random.choice(availableBees) # Select randomly a parent
                availableBees.remove(rdmBee1) # Remove the selected parent to avoid the doublon
                rdmBee2 = random.choice(availableBees)  # Select randomly a parent
                availableBees.remove(rdmBee2) # Remove the selected parent to avoid the doublon

                # Crossover operation between the 2 parents. 
                # Each parent is divided in 2 genoms and are mixed to create 2 new bees
                gen1bee1 = rdmBee1.listOfFlower[:len(rdmBee1.listOfFlower) // 2]
                gen1bee2 = [x for x in rdmBee2.listOfFlower if x not in gen1bee1]
                gen2bee1 = rdmBee2.listOfFlower[:len(rdmBee2.listOfFlower) // 2]
                gen2bee2 = [x for x in rdmBee1.listOfFlower if x not in gen2bee1]

                combinedList1 = gen1bee1 + gen1bee2
                combinedList2 = gen2bee1 + gen2bee2

                # The child created are added to the list 
                child1, child2 = self.generate_children(combinedList1, combinedList2)

                self.child.append(child1)
                self.child.append(child2)

        # The list is updated to include the current population
        self.bees = self.bees + self.child
        self.beeList = self.bees + self.child
        self.child = []

        fitnessList = []
        fitnessList = [x.fitnessScore for x in self.bees] # Create a score list
        return fitnessList

# To simulate a genetic mutation where the flower order in the gathering path is modified randomly. Allow to introduce genetic diversity.   
    def mutation(self):
        rdmBee = random.choice(self.bees) # Chose randomly a bee to mutate
        for i in range(10):
                randomFlowerIndex = random.randint(0, len(rdmBee.listOfFlower)-1) # Generate a random index which indicate the position of a flower for a bee
                firstHalf = rdmBee.listOfFlower[:randomFlowerIndex]
                secondHalf = rdmBee.listOfFlower[randomFlowerIndex:]
                rdmBee.listOfFlower = secondHalf + firstHalf # Make the mutation after having the two parts of a flower list

    def avg(self, list):
        sum_list = 0
        for i in range(len(list)):
            sum_list += list[i]
        avg = sum_list / len(list)
        return avg
    
# To generate the genealogic tree
    def generate_genealogy(self):
        random_bee = random.choice(self.bees)
        genealogy = []

        for generation in range(10, -1, -1):
            generation_info = {
                "Generation": generation,
                "Bee": random_bee.id,
                "Parents": []
            }

            if generation > 0:
                previous_generation = [bee for bee in self.bees if bee.id == random_bee.id - 1]
                for parent_bee in previous_generation:
                    generation_info["Parents"].append(parent_bee.id)

                if not previous_generation:
                    break

                random_bee = previous_generation[0]
            
            genealogy.append(generation_info)
        self.genealogy_tree = genealogy

# To visualise the best path  
    def best_path_visualisation(self):
        plt.scatter(*zip(*self.bees[0].listOfFlower), color='blue')
        plt.ylabel('y')
        plt.xlabel('x')
        plt.title(f"Best path:")
        plt.plot(*zip(*self.bees[0].listOfFlower), linestyle='--', color='blue')
        plt.show()

# To visualise the best bees fitness score evolution  
    def best_bees_visualisation(self):
        plt.plot(self.bestBees)
        plt.ylabel('Fitness Score:')
        plt.xlabel('Bee:')
        plt.title(f"Best fitness score for a bee by generation")
        plt.show()

# To visualise the average fitness score  
    def avg_generation_visualisation(self, listFitness):
        plt.plot(listFitness)
        plt.ylabel('AVG Fitness:')
        plt.xlabel('Generation:')
        plt.title(f"AVG fitness generation:")
        plt.show()

