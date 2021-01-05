
import sys
import numpy as np
from geneticalgorithm import geneticalgorithm as ga
import json


class Color():
    def __init__(self):
        self.palette = []
        self.target = []

        self.RGB_SCALE = 255
        self.CMYK_SCALE = 100

    def rgb_to_cmyk(self, r, g, b):
        # if black
        if (r, g, b) == (0, 0, 0):
            return 0, 0, 0, self.CMYK_SCALE

        # rgb [0,255] -> cmy [0,1]
        c = 1 - r / self.RGB_SCALE
        m = 1 - g / self.RGB_SCALE
        y = 1 - b / self.RGB_SCALE

        # extract out k [0, 1]
        min_cmy = min(c, m, y)
        c = (c - min_cmy) / (1 - min_cmy)
        m = (m - min_cmy) / (1 - min_cmy)
        y = (y - min_cmy) / (1 - min_cmy)
        k = min_cmy

        # rescale to the range [0,CMYK_SCALE]
        return c * self.CMYK_SCALE, m * self.CMYK_SCALE, y * self.CMYK_SCALE, k * self.CMYK_SCALE

    def cmyk_to_rgb(self, c, m, y, k):
        r = self.RGB_SCALE * (1.0 - c / float(self.CMYK_SCALE)) * (1.0 - k / float(self.CMYK_SCALE))
        g = self.RGB_SCALE * (1.0 - m / float(self.CMYK_SCALE)) * (1.0 - k / float(self.CMYK_SCALE))
        b = self.RGB_SCALE * (1.0 - y / float(self.CMYK_SCALE)) * (1.0 - k / float(self.CMYK_SCALE))
        return r, g, b

    def loadPalette(self):
        with open('palette_cmyk.json') as f:
            data = json.load(f)
            self.palette = np.matrix(data)

            """
            convert rgb to cmyk
            i = 0
            for c in data:
                #print(c[0])
                c,m,y,k = rgb_to_cmyk(c[0], c[1], c[2])
                print("[%.2f,\t"% c, end='')
                print("%.2f,\t"% m, end='')
                print("%.2f,\t"% y, end='')
                print("%.2f],"% k)
                i += 1
            """

        print( "loaded palette of "+str(len(self.palette)) + " colors")

    """
    def getLoss(palette, target, lc):
        mse = (np.square(target - lc*palette)).mean(axis=1)
        return float(mse)
    """

    def f(self, lc):
        mse = (np.square(self.target - lc * self.palette)).mean(axis=1)
        return np.sum(mse)

    def runGeneticAlgorithm(self):
        # ga
        varbound=np.array([[0,100]] * len(self.palette))
        algorithm_parameters={'max_num_iteration': 4000,\
                                'population_size':100,\
                                'mutation_probability':0.1,\
                                'elit_ratio': 0.01,\
                                'crossover_probability': 0.5,\
                                'parents_portion': 0.3,\
                                'crossover_type':'uniform',\
                                'max_iteration_without_improv':None}
        model=ga(function=self.f, 
                dimension=len(self.palette), 
                variable_type='real', 
                variable_boundaries=varbound, 
                convergence_curve=True, 
                algorithm_parameters=algorithm_parameters)
                
        #print(model.param)
        model.run()

        print("output variable is: ")
        output = np.matrix(model.output_dict['variable'])
        output /= output.max()
        print(output)

        return output
        
    def run(self, c, m, y, k):
        self.loadPalette()
        self.target = np.matrix([c, m, y, k])

        best_lc = self.runGeneticAlgorithm()

        num_colors = 5

        # get most important indices
        print("most important color indices: ", end='')
        print(np.asarray(best_lc).reshape(-1).argsort()[-num_colors:][::-1])
        best3_indices = np.asarray(best_lc).reshape(-1).argsort()[-num_colors:][::-1]

        best_lc_array = np.asarray(best_lc)[0]

        percentages = []
        for i in range(num_colors):
            percentages.append(best_lc_array[best3_indices[i]])
            print("%.2f" % float(best_lc_array[best3_indices[i]]))

        return best_lc

    def getPalette(self):
        return self.palette


if __name__ == "__main__":
    color = Color()
    color.run( float(sys.argv[1]), float(sys.argv[2]), float(sys.argv[3]), float(sys.argv[4]) )
