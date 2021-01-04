
import sys
import numpy as np
from geneticalgorithm import geneticalgorithm as ga
import json

palette = []
target = []

#def getLinearCombination(palette, target):
#    return [0.5, 0.5, 0.5]

def loadPalette():
    with open('palette1.json') as f:
        data = json.load(f)
        global palette 
        palette = np.matrix(data)

    print( "loaded palette of "+str(len(palette)) + " colors")
    
    #return np.matrix([ \
    #[255, 0, 0],
    #[0, 255, 0],
    #[0, 0, 255]])

def getLoss(palette, target, lc):
    mse = (np.square(target - lc*palette)).mean(axis=1)
    return float(mse)

def f(lc):
    global palette
    global target

    mse = (np.square(target - lc*palette)).mean(axis=1)
    return np.sum(mse)
    
def run(r, g, b):
    global target
    global palette
    loadPalette()
    target = np.matrix([r, g, b])
    #lc = getLinearCombination(palette, target )

    # ga
    varbound=np.array([[0,1]] * len(palette))
    algorithm_parameters={'max_num_iteration': 200,\
                                       'population_size':100,\
                                       'mutation_probability':0.1,\
                                       'elit_ratio': 0.01,\
                                       'crossover_probability': 0.5,\
                                       'parents_portion': 0.3,\
                                       'crossover_type':'uniform',\
                                       'max_iteration_without_improv':None}
    model=ga(function=f, dimension=len(palette), variable_type='real', variable_boundaries=varbound, convergence_curve=False, algorithm_parameters=algorithm_parameters)
    #print(model.param)
    model.run()

    print("output is: ")
    output = np.matrix(model.output_dict['variable'])
    output /= output.max()
    print(output)

    # get most important indices
    print(np.asarray(output).reshape(-1).argsort()[-3:][::-1])
    
    #type(output)

    #print(output)
    #loss = getLoss(palette, target, lc)
    #print(loss)

if __name__ == "__main__":
    run( int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]) )