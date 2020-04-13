
import os
import networkx as nx
from Chromosome import Chromosome
from GA import GA

# read the network details
def readNet(fileName):
    
    G = nx.read_gml(fileName, label='id')
    net = {}
    mat = []
    degrees = []
    net['noNodes'] = G.number_of_nodes()
    net["noEdges"] = G.number_of_edges()
    for i in G.nodes:
        mat.append([0 for _ in G.nodes])
    degrees = [0 for _ in G.nodes]
    for i,j in G.edges:
        mat[i-1][j-1]=mat[j-1][i-1]=1
        degrees[i-1]=degrees[i-1]+1
        degrees[j-1]=degrees[j-1]+1
    net['mat']=mat
    net['degrees'] = degrees
    
    
    print(net['noNodes'])
    print(net["noEdges"])
    print(net["degrees"])
    print(net["mat"]) 
    
    return net


def main():
    crtDir =  os.getcwd()
    filePath = os.path.join(crtDir, 'net.gml')
    network = readNet(filePath)
    
    # gaParam is a dictionary
    # popSize = populationSize, used for initialization of first generation
    # noGen = no of generations, the condition used stop the algorithm
    gaParam = {"popSize": 500, "noGen" : 50}

    # problParam is a dictionary
    problParam = {'function' : fcEval, 
                  'noNodes' : network["noNodes"], 
                  'noEdges' : network["noEdges"],
                  'degrees' : network["degrees"],
                  'mat':network["mat"]}
    
    # store the best/average solution of each iteration
    allBestFitnesses = []
    allAvgFitnesses = []
    generations = []
    globalBest = Chromosome(problParam)
    ga = GA(gaParam, problParam)
    ga.initialisation()
    ga.evaluation()
    stop = False
    g = -1
   # print("PARAM:"+str(gaParam['noGen']))

    file = open("output.txt","a")
    lines=""

    while (not stop and g < gaParam['noGen']):
        g += 1
        ga.oneGeneration()
     
        
        allPotentialSolutionsFit = [c.fitness for c in ga.population]
        avgFit = sum(allPotentialSolutionsFit) / len(allPotentialSolutionsFit)
        
        bestChromo = ga.bestChromosome()
        if bestChromo.fitness > globalBest.fitness:
            globalBest = bestChromo
            
        lines = ["------ gen: "+str(g)+"--------"+'\n',
                
                'Local = ' + str(bestChromo.fitness)+'\n',
                'Global = ' + str(globalBest.fitness)+'\n']
        file.writelines(lines)
        

        
    printResult(globalBest, problParam)
   
    file.close()
    
def oldestAncestor(tata, x):
    if tata[x] != x:
        tata[x] = oldestAncestor(tata, tata[x])
    return tata[x]
    
    

def decode(c):
    #print("decode")
    tata = [i for i in range(0, c.problParam["noNodes"])]
    
    # consider perechea i si c.repres[i] ca fiind o muchie orientata i->repres[i]
    # deci i este tatal lui repres[i]
    for i in range(0, c.problParam["noNodes"]):
        tata[oldestAncestor(tata, c.repres[i])] = oldestAncestor(tata, i)
    for i in range(0, c.problParam["noNodes"]):
        tata[i] = oldestAncestor(tata, i)
    """    
    print("repres: "+str(c.repres))
    print("tata final: "+str(tata))
    print("------------")
    """
    return tata

def normalizationDecode(dec, problParam):
    ap = [0 for _ in range(0, problParam["noNodes"])]
    abnormal = []
    normal = []
    index = 1
    for classLabel in dec:
        if ap[classLabel] == 0:
            abnormal.append(classLabel)
            ap[classLabel] = index
            index = index + 1
        normal.append(ap[classLabel])
    return normal

def printResult(globalBest, problParam):
    
    file = open("output.txt","a")
    dec = decode(globalBest)
    normal = normalizationDecode(dec, problParam)
    ap = [0 for _ in range(0, problParam["noNodes"])]
    index = 1
    file.writelines("----------- global result ------------"+'\n')
   # print("----------- global result ------------")
    for classLabel in normal:
        if ap[classLabel] == 0:
            ap[classLabel] = index
            index = index + 1
    file.writelines("no of Label Classes is: "+str(index)+'\n')
   # print("no of Label Classes is: "+str(index))
    for i in range(0, problParam["noNodes"]):
        file.writelines(str(i+1)+" "+str(normal[i])+'\n')
        #print(str(i)+" "+str(normal[i]))
    
def modularity(communities, param):
    noNodes = param['noNodes']
    mat = param['mat']
    degrees = param['degrees']
    noEdges = param['noEdges']
    M = 2 * noEdges
    Q = 0.0
    for i in range(0, noNodes):
        for j in range(0, noNodes):
            if (communities[i] == communities[j]): # Kronecker function
                Q += (mat[i][j] - degrees[i] * degrees[j] / M)              
    return Q * 1 / M

def fcEval(c):
    communities = decode(c)
    a = modularity(communities, c.problParam)
    return a

main()