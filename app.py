from viktor.core import ViktorController
from viktor.parametrization import ViktorParametrization, MultiSelectField, Text
from viktor.views import SVGView, SVGResult, DataGroup, DataItem, DataResult, DataView
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np
from io import StringIO
from data import forecast_naive, forecast_exp, forecast_reg
from data import series


class Parametrization(ViktorParametrization):
    title = Text('# Comparing CO2 Concentration Forecasting Models')
    not_in_params = Text('The "Actual Values" data comes from the Mauna Loa CO2 dataset (a research facility that monitors the atmosphere). For the forecasts the data untill 2017 has been used as input data.')
    modeltype = MultiSelectField('Choose model types:', options=['Naive Seasonal', 'Exponential Smoothing', 'Linear Regression'], flex = 90)

class Controller(ViktorController):
    label = 'CO2 concentration'
    parametrization = Parametrization(width=30)

    @SVGView("CO2 concentration", duration_guess=1)
    def create_svg_result(self, params, **kwargs):

        #initialize figure
        fig = plt.figure(figsize = (8,5))
        idx = -144

        series[idx:].plot(label='Actual Values') #plot actual values

        plt.plot([17120, 17120], [385, 420], color='green', linestyle='dashed', linewidth=2)

        #plot forecasts
        if 'Naive Seasonal' in params.modeltype:
            forecast_naive[idx:].plot(label= 'Forecast - Naive Seasonal')

        if 'Exponential Smoothing' in params.modeltype:
            forecast_exp[idx:].plot(label= 'Forecast - Exponential Smoothing')

        if 'Linear Regression' in params.modeltype:
            forecast_reg[idx:].plot(label= 'Forecast - Linear Regression')

        plt.title('Forecasting Monthly CO2 Concentration')
        plt.ylabel('CO2 Concentration (ppm)')
        plt.xlabel('Time')

        svg_data = StringIO()
        fig.savefig(svg_data, format='svg')
        plt.close()

        return SVGResult(svg_data)
