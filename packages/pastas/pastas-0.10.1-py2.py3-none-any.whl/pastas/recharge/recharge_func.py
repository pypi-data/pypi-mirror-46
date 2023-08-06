"""recharge_func module

Author: R.A. Collenteur

Contains the classes for the different models that are available to calculate
the recharge from precipitation and evaporation data.

Each Recharge class contains at least the following:

Attributes
----------
nparam: int
    Number of parameters needed for this model.

Functions
---------
get_init_parameters(self, name)
    A function that returns a Pandas DataFrame of the parameters of the
    recharge function. Columns of the dataframe need to be ['value', 'pmin',
    'pmax', 'vary']. Rows of the DataFrame have names of the parameters. Input
    name is used as a prefix. This function is called by a Tseries object.
simulate(self, evap, prec, p=None)
    A function that returns an array of the simulated recharge series.

"""

import pandas as pd


class Linear:
    """Linear recharge model

    The recharge to the groundwater is calculated as:
    R = P - f * E

    """

    def __init__(self):
        self.nparam = 1

    def get_init_parameters(self, name):
        parameters = pd.DataFrame(
            columns=['initial', 'pmin', 'pmax', 'vary', 'name'])
        parameters.loc[name + '_f'] = (-1.0, -2.0, 0.0, 1, name)
        return parameters

    def simulate(self, prec, evap, p):
        """

        Parameters
        ----------
        prec, evap: array_like
            array with the precipitation and evaporation values. These
            arrays must be of the same length and at the same time steps.
        p: float
            parameter value used in recharge calculation.

        Returns
        -------
        recharge: array_like
            array with the recharge series.

        """
        recharge = prec + p * evap
        return recharge
