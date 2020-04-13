
from random import randint, seed, uniform, sample

# integer representation

class Chromosome:
    def __init__(self, problParam = None):
        self.__problParam = problParam
        # # random values, without constraints
        # self.__repres = [generateNewValue(0,problParam['noChars']) for _ in range(problParam['noDiffChars'])] 
        # random values with constraints
        genes = [0 for _ in range(0, problParam["noNodes"])]
        for i in range(0, problParam["noNodes"]):
            while True:
                genes[i] = randint(0, problParam["noNodes"]-1)
                if genes[i] != i:
                    break 
                        
        self.__repres = genes
        self.__fitness = 0.0
    
    @property
    def problParam(self):
        return self.__problParam
    
    @property
    def repres(self):
        return self.__repres 
    
    @property
    def fitness(self):
        return self.__fitness 
    
    @repres.setter
    def repres(self, l = []):
        self.__repres = l 
    
    @fitness.setter 
    def fitness(self, fit = 0.0):
        self.__fitness = fit 
    
    def crossover(self, c):
        offspring = Chromosome(self.__problParam)
        for i in range(0, c.problParam["noNodes"]):
            bit = randint(0,1)
            if bit == 0:
                offspring.repres[i] = self.__repres[i]
            else:
                offspring.repres[i] = c.repres[i]   
        return offspring
    
    def mutation(self):
        pos = randint(0, self.__problParam["noNodes"]-1)
        old = self.__repres[pos]
        while True:
            self.__repres[pos] = randint(0, self.__problParam["noNodes"]-1)
            if self.__repres[pos] != old and self.__repres[pos] != pos:
                break 
        
    def __str__(self):
        return "\nChromo: " + str(self.__repres) + " has fit: " + str(self.__fitness)
    
    def __repr__(self):
        return self.__str__()
    
    def __eq__(self, c):
        return self.__repres == c.__repres and self.__fitness == c.__fitness