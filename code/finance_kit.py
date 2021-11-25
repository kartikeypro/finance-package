import pandas as pd
import numpy as np
import scipy 

def call_data():
    data = pd.read_csv("../Data/Portfolios_Formed_on_ME_monthly_EW.csv"
                       ,header =0, index_col = 0, parse_dates=True,na_values=-99.99)
    data = data[["Lo 20","Hi 20"]]
    data.columns = ["small cap","high cap"]
    data = data/100
    data.index = pd.to_datetime(data.index,format="%Y%m").to_period("M")
    return data

def drawdown(data: pd.Series):
    """
    wealth_index: index to track the wealth
    previous_peaks: Cumulative of the peaks achieved by the wealth index
    drawdowns: difference between the wealth index and the precious peaks
    """
    wealth_index = 1000*(1+data).cumprod()
    previous_peaks = wealth_index.cummax()
    drawdown = (wealth_index - previous_peaks)/previous_peaks
    return pd.DataFrame({"Wealth":wealth_index,"Peaks":previous_peaks,"Drawdown":drawdown})


def skewness(data:pd.Series):
    """
    This function measures the skewness of the data provided in the series.
    It only accepts pandas series.
    """
    mean = data.mean()
    num = np.mean(np.power(data-data.mean(),3))
    den = data.std()**3
    return num/den

def kurtosis(data:pd.Series):
    """
    This function measures the skewness of the data provided in the series.
    It only accepts pandas series.
    """
    mean = data.mean()
    num = np.mean(np.power(data-data.mean(),4))
    den = data.std()**4
    return num/den

def is_normal(data:pd.Series,level=0.01):
    """
    This function validates if the series is normal or not by passing it through jarque_bera test
    level is the extent to which the normality would be considered
    """
    statistic, p_value = scipy.stats.jarque_bera(data)
    return p_value>level

def var(r: pd.Series, level=0.05,kind="historic"):
    """
    Allows to calculate
    """
    if (kind=="historic"):
        return r.sort_values()[int((level)*r.shape[0])]
    elif(kind=="normal"):
        return norm.ppf(level)*r.std(ddof=0)+r.mean()

