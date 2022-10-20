from viktor.core import ViktorController
from viktor.parametrization import ViktorParametrization, OptionField
from viktor.views import SVGView
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np
from io import StringIO

class Parametrization(ViktorParametrization):
    modeltype = OptionField('Choose a model type for forecastnig co2 emissions:', options=['Naive', 'Exponential Smoothing', 'Linear Regression'], default='naive')


class Controller(ViktorController):
    label = 'Plot emissions'
    parametrization = Parametrization

    @SVGView("Plot", duration_guess=1)
    def create_svg_result(self, params, **kwargs):

        #initialize figure
        fig = plt.figure(figsize = (8,5))

        if params.modeltype == 'Naive' :
            model_name = 'Naive Seasonal'
            x = np.random.randn(10)

        if params.modeltype == 'Exponentional Smoothing':
            model_name = 'Exponentional Smoothing'
            x = np.random.randn(10)

        if params.modeltype == 'Linear Regression':
            model_name = 'Linear Regression'
            x = np.random.randn(10)
        
        if params.modeltype == None:
            model_name = 'Linear Regression'
            x = np.random.randn(10)      

        plt.plot(x)
        plt.title(model_name)

        svg_data = StringIO()
        fig.savefig(svg_data, format='svg')
        plt.close()

        return SVGResult(svg_data)