# import libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
import statsmodels.api as sm
import itertools

from statsmodels.tsa.stattools import adfuller
from statsmodels.graphics.tsaplots import plot_pacf
from statsmodels.graphics.tsaplots import plot_acf

######################################
# EXPLORATORY DATA ANALYSIS FUNCTIONS#
######################################

def growth_rates(df):
    """Add 4 growth rate columns ('total_growth', '5yr_growth', '3yr_growth', '1yr_growth') to a dataframe. 
       Dataframe must have columns with montlhy dates from 2009-01 to 2018-04"""
    
    # Determine the change in values from the beggining to the end of the time period     
    df['total_growth'] = (df['2018-04'] - df['2009-01']) / df['2009-01']
    
    # Determine the change in values over the last five years     
    df['5yr_growth'] = (df['2018-04'] - df['2013-04']) / df['2013-04']

    # Determine the change in values over the last three years
    df['3yr_growth'] = (df['2018-04'] - df['2015-04']) / df['2015-04']

    # Determine the change in values over the last year    
    df['1yr_growth'] = (df['2018-04'] - df['2017-04']) / df['2017-04']
    

def top_growth_cities(df):
    """Enter a dataframe with total, 5yr, 3yr, and 1yr growth rates and return a set of cities that
       represent the top 5 for each growth period."""
    
    # Sort values by greatest total growth rates and return the top 5    
    top_total = list(df.sort_values('total_growth', ascending=False)['city_zipcode'].values[:5])
    
    # Sort values by greatest 5 year growth rates and return the top 5    
    top_5yr = list(df.sort_values('5yr_growth', ascending=False)['city_zipcode'].values[:5])

    # Sort values by greatest 3 year growth rates and return the top 5        
    top_3yr = list(df.sort_values('3yr_growth', ascending=False)['city_zipcode'].values[:5])

    # Sort values by greatest 1 year growth rates and return the top 5        
    top_1yr = list(df.sort_values('1yr_growth', ascending=False)['city_zipcode'].values[:5])
    
    # create a unique set of citied 
    top_cities = set(top_total + top_5yr + top_3yr + top_1yr)
    
    # return a dataframe that only includes cities in the top_cities set     
    return df[df['city_zipcode'].isin(top_cities)]


def stacked_growth(df):
    """Plot the growth rates of all cities in a dataframe in clustered bar chart,
       along with the mean growth rates of all cities, ordered from left to right by 
       1yr_growth rate."""
    
    # keys for columns to plot from the dataframe   
    grow_rates = ['total_growth', '5yr_growth', '3yr_growth', '1yr_growth']

    # get the mean growth rate for each time period      
    means = [df[i].mean() for i in grow_rates]

    # colors to assign horizontal lines
    colors = ['blue', 'red', 'gold', 'green']

    #plot clustered cities 
    fig = plt.figure(figsize=(14, 8))

    # sort by 1yr growth and plot clustered bar chart    
    df.sort_values('1yr_growth').plot(x= 'city_zipcode', 
                                      y = grow_rates, 
                                      kind='bar', 
                                      figsize=(14, 8))
    
    
    # plot growth rate means as horizontal lines
    plt.hlines(y= means, xmin=-1, xmax=len(df), color=colors, label=('Mean growth'))
    
    plt.legend()
    plt.title('City_zipcode Growth Rates')
    
    plt.show()

    
def graph_growth(df):
    """Plot the total, 5yr, 3yr, and 1yr growth rates for each city in the data frame in 
       individual bar charts. Plot a horixontal line that represents the mean.""" 
    
    
    f = plt.figure(figsize= ( 16, 16))
    # create space between plots
    plt.subplots_adjust(hspace= 1)

    # set the value for x to the key for the city name in the dataframe
    x = 'city_zipcode'
    # set the lenth of the horizintal line 
    x_len = len(df)

    # plot total growth     
    ax1 = f.add_subplot(2,2,1)
    df.sort_values('total_growth').plot(x=x, y='total_growth', kind='bar', ax=ax1)
    plt.hlines(y=df.total_growth.mean(), xmin=0, xmax=x_len, label=('Mean Total Growth'))
    plt.title('Total Growth')
    plt.legend()

    # plot 5yr growth
    ax2 = f.add_subplot(2,2,2)
    df.sort_values('5yr_growth').plot(x=x, y='5yr_growth', kind='bar', ax=ax2)
    plt.hlines(y=df['5yr_growth'].mean(), xmin=0, xmax=x_len, label=('Mean 5-year Growth'))
    plt.title('5-year Growth')
    plt.legend()

    # plot 3yr growth
    ax3 = f.add_subplot(2,2,3)
    df.sort_values('3yr_growth').plot(x=x, y='3yr_growth', kind='bar', ax=ax3)
    plt.hlines(y=df['3yr_growth'].mean(), xmin=0, xmax=x_len, label=('Mean 3-year Growth'))
    plt.title('3-year Growth')
    plt.legend()

    # plot 1yr growth
    ax4 = f.add_subplot(2,2,4)
    df.sort_values('1yr_growth').plot(x=x, y='1yr_growth', kind='bar', ax=ax4)
    plt.hlines(y=df['1yr_growth'].mean(), xmin=0, xmax=x_len, label=('Mean 1-year Growth'))
    plt.title('1-year Growth')
    plt.legend()
    
    plt.show()   


def melt_data(df):
    """takes a dataframe and converts value data stored horizontally to a 
       vertical time series and change the index to datetime"""

    #drop unnecessary columns     
    df = df.drop(columns=['SizeRank', 'total_growth', '5yr_growth', '3yr_growth', '1yr_growth']).copy()
    
    # melt data to covert to value to a vertical orientation
    melted = pd.melt(df, id_vars=['city_zipcode', 'State', 'Metro', 'CountyName'], var_name='time')
    # convert 'time' to datetime
    
    melted['time'] = pd.to_datetime(melted['time'], infer_datetime_format=True)
    
    # make 'time' the index
    melted.set_index('time', inplace=True)
    
    # return the new time series dataframe
    return melted


def YoY_change(ts_dict):
    """take a dictionary of monthly time series dataframes and
       creates a column with the YoY change in value for
       each key:value pair"""
    
    # iterate through each key and calculate the percent change in each value 
    # over the last 12 month period
    for v in ts_dict:
        df = ts_dict[v]
        df['YoY_change'] = df.value.pct_change(periods=12)


def YoY_rate_o_change(ts_dict):
    """take a dictionary of monthly time series dataframes and
       creates a column with the YoY rate of change in value for
       each key:value pair"""

    # iterate through each key and calculate the differnce in each YoY change 
    # over the last 3 periods
    for v in ts_dict:
        df = ts_dict[v]
        df['YoY_rate_change'] = df.YoY_change.diff(periods=3)


def get_time_series(df):
    """takes a dataframe and returns a dictionary with unique city names as 
       keys and a dataframe for that city as a value. Also calulates new values
       'YoY_change' and 'YoY_rate_o_change' and adds new columns"""
    
    # create keys to use in new dictionary
    list_of_cities = list(df.city_zipcode)
    
    # create an empty dictionary to populate
    time_series_dict = {}
    
    # iterate through the list of cities and create new key:value pairs for city and city data
    for c in list_of_cities:
        time_series_dict[c] = melt_data(df[df['city_zipcode'] == c])
    
    # calculate YoY change in value for each city
    YoY_change(time_series_dict)
    
    # calcualte YoY rate of change for each city
    YoY_rate_o_change(time_series_dict)
    
    # return a dictionary with cities and city data
    return time_series_dict


def plot_time_series(ts, variable):
    """takes a dictionary of time series data frames and plots a 
        chosen variable (ex. 'value') in a series of subplots"""
    
    # creat figure and space between subplots
    fig = plt.figure(figsize=(20,18))
    plt.subplots_adjust(hspace= .5)
    
    # determine the number of subplots to create
    nrows = len(ts)//3 + 1
    ncols = 3
    
    # use dict keys as plot titles
    titles = list(ts.keys())
    
    # iterate through dict and plot each plot in a new sub plot 
    for i,v in enumerate(ts):
        ax = fig.add_subplot(nrows, ncols, i+1)
        ts[v][variable].plot(label=variable, ax=ax)
        plt.title(titles[i])
        plt.ylabel(variable)
        
    plt.show()


def plot_time_series2(ts):
    """takes a dictionary of time series dataframes and makes three plots 
       for each key:value pair: 'value', YoY_change', and 'YoY_rate_change'"""
    
    # create subplot values
    nrows = len(ts)
    ncols = 3
    
    # creat figure and space between subplots
    fig = plt.figure(figsize=(16,(nrows*3)))
    plt.subplots_adjust(hspace= 1.2)
    
   
    # use dict keys as plot titles
    titles = list(ts.keys())
    
    # columns to plot from eact dataframe
    variables = ['value', 'YoY_change', 'YoY_rate_change']
    
    # set base value to iterate on for axes
    axs = 0
    
    # iterate through each key:value pair and each variable to plot
    # enumerate to use as axes values
    for i,v in enumerate(ts):
        for x in variables:
            axs += 1 
            ax = fig.add_subplot(nrows, ncols, axs)
            ts[v][x].plot(label=x, ax=ax)
            plt.title(titles[i] + '_' + x)
            plt.ylabel(x, fontsize= 10)
            plt.xticks(fontsize= 10, rotation=45)
            plt.hlines(y=0, xmin='2009-01', xmax='2018-04', colors='orange', linestyles='--')

    plt.show()


def avg_YoY_change(ts_dict):
    """take a dictionary of time series data frames and calculate
       the average YoY change for each one"""
    
    # create an empty list to add averages to
    avg_YoY = []
    
    # iterate through the dict and claculate the average YoY change for each 
    # key:value pair and add it to the list of averages
    for v in ts_dict:
        avg = ts_dict[v]['YoY_change'].mean()
        avg_YoY.append(avg)

    # combine the city names and average values and return a sorted list
    city_names = list(ts_dict.keys())
    avg_YoY = list(zip(city_names, avg_YoY))
    return sorted(avg_YoY, key=lambda x: x[1])


def plot_avg_YoY(ts_dict):
    """take a dicitonary of time series dataframes and plot a bar chart
       of average YoY growth"""
    
    # get a sorted list of average YoY changes
    avgs = avg_YoY_change(ts_dict)
    
    # establish x and y values 
    x = [i[0] for i in avgs]
    y = [i[1] for i in avgs]
    
    # plot avearges in a bar chart
    fig = plt.figure(figsize=(14,6))
    plt.bar(x=x, height=y)
    plt.xticks(rotation='vertical')
    plt.show()

###########################
# STATIONARITY FUNCTIONS #
##########################

def plot_rolling_stats(ts, title=None):
    """takes in a time series and optional title and plots 
       values, rolling mean, and rolling std."""
    
    # calculate rolling mean and standard deviation over 12 periods
    roll_mean = ts.rolling(window=12, center=False).mean()
    roll_std = ts.rolling(window=12, center=False).std()
    
    # plot the value, rolling mean, and rolling std in one plot
    fig = plt.figure(figsize=(12,4))
    orig = plt.plot(ts, color='blue', label='Value')
    mean = plt.plot(roll_mean, color='orange', label='Rolling Mean')
    std = plt.plot (roll_std, color='green', label='Rolling Std')
    plt.legend(loc='best')
    plt.title(title + ' ' + 'Rolling Mean & Standard Deviation')
    plt.show()

    
def subtract_rollmean(ts, window=12):
    """takes a takes a time series and window of periods (default = 12)
       and subtracts the rolling mean and returns a new series"""
    # calculate the rolling means and subtract them from the original time series
    roll_mean = ts.rolling(window=window).mean()
    ts_minus_rollmean = ts - roll_mean
    
    return ts_minus_rollmean
    

def subtract_w_rollmean(ts, halflife=4):
    """takes a time series and halflife (default = 4)
       and subtracts the weighted rolling mean and returns a new series"""
    # calculate the weighted rolling mean and subtract it from the original time series
    w_roll_mean = ts.ewm(halflife=halflife).mean()
    ts_minus_w_rollmean =  ts - w_roll_mean
    
    return ts_minus_w_rollmean


def adf_test(ts):
    """takes a time series and uses the advanced Dickey-Fuller Test
       to determine if the series is stationary and prints results"""
    
    # drop missing values
    ts = ts.dropna()
    
    print ('Results of Dickey-Fuller Test:')
    dftest = adfuller(ts)

    # Extract and display test results in a user friendly manner
    dfoutput = pd.Series(dftest[0:4], index=['Test Statistic',
                                             'p-value',
                                             '#Lags Used',
                                             'Number of Observations Used'])
    for key,value in dftest[4].items():
        dfoutput['Critical Value (%s)'%key] = value
    print (dfoutput)
    
def stationarity_check(ts, title=None):
    """takes a time series and optional title and plots values, 
       rolling mean, rolling std, and prints results of a Dickey-Fuller test"""
    plot_rolling_stats(ts, title=title)
    adf_test(ts)


def stationarity_transformer(ts, alpha=.05, transform=None):
    """Takes a time series and iterates through a number of transformation techniques
       and applies the adfuller test to return p-values below accepted levels for stationarity.
       Also takes arguments 'alpha' (default = .05) and 'transform' (default= None).
       'alpha' represents the maximum p-value allowed to be added to the final list.
       'transform' represents base transformations to make such as 'log' or 'sqrt'."""
    
    # create an empty list of p-values
    p_values = []
    
    # set values to use for rolling means and weighted rolling means
    roll_periods = [3, 6, 8, 12]
    half_lifes = [1, 2, 3, 4]
    
    alpha = alpha
    
    # set base values and name for time series
    v = ts
    name = 'Original'
    
    # check transform and if there is a value for it replace 'v' and 'name'
    if transform == 'log':
        v = np.log(ts)
        name = 'Log' 
    elif transform == 'sqrt':
        v = np.sqrt(ts)
        name = 'Sqrt'
    else:
        None

    # do adfuller test with no transformation other than base transformation and
    # if values are less than or equal to alpha add to list
    adf = adfuller(v)[1]
    if adf <= alpha:
        p_values.append((name , adf))
    
    # difference the base values by one period and conduct adfuller and add if <= alpha 
    v_diff = v.diff(periods=1) 
    adf_diff = adfuller(v_diff.dropna())[1]
    if adf <= alpha:
        p_values.append((name + 'diff: ', adf_diff))

    # iterate through periods of rolling means and subtract from base values and check/add p-value 
    for i in roll_periods:
        iteration_name = name + '_minus_roll_mean_' + str(i) +':'
        roll_minus = subtract_rollmean(v, window=i)
        adf_roll_minus = adfuller(roll_minus.dropna())[1]
        if adf_roll_minus <= alpha:
            p_values.append((iteration_name, adf_roll_minus))
    
    # iterate through periods of rolling means and subtract from differenced values and check/add p-value 
    for i in roll_periods:
        iteration_name = name + '_minus_roll_mean_diff_' + str(i) +':'
        roll_minus = subtract_rollmean(v, window=i)
        roll_minus_diff = roll_minus.diff(periods=1)
        adf_roll_minus_diff = adfuller(roll_minus.dropna())[1]
        if adf_roll_minus_diff <= alpha:
            p_values.append((iteration_name, adf_roll_minus_diff))
    
    # iterate through halflifes of weighted rolling means and subtract from base values and check/add p-value 
    for h in half_lifes:
        interation_name = name + '_minus_w_roll_mean_' + str(h) + ':'
        w_roll_minus = subtract_w_rollmean(v, halflife=h)
        adf_w_roll_minus = adfuller(w_roll_minus.dropna())[1]
        if adf_w_roll_minus <= alpha:
            p_values.append((iteration_name, adf_w_roll_minus))
  
    # iterate through halflifes of weighted rolling means and subtract from differenced values and check/add p-value 
    for h in half_lifes:
        iteration_name = name + '_minus_w_roll_mean_diff_' + str(h) + ':'
        w_roll_minus = subtract_w_rollmean(v, halflife=h)
        w_roll_minus_diff = w_roll_minus.diff(periods=1)
        adf_w_roll_minus_diff = adfuller(w_roll_minus_diff.dropna())[1]
        if adf_w_roll_minus_diff <= alpha:
            p_values.append((iteration_name, adf_w_roll_minus_diff))
        
    return p_values
      

def all_stationarity(ts):
    """takes a time series and checks stationarity with adfuller for multiple transformation types
       and returns any transformation with a p-value less than or equal to .05"""
    tests = [None, 'log', 'sqrt']
    
    for t in tests:
        test = stationarity_transformer(ts, transform=t)
        display(test)


#######################
# MODELING FUNCTIONS #
######################


def SARIMA_iterator(ts, order=2, show=False):
    """takes a time series and optional arguments 'order' and 'show' and returns
       an optimal order and seasonal order for a SARIMAX model based on lowest AIC score.
       'order' indicates the end of the range of values the function will iterate through
       for values (p,d,q) and (P,D,Q) -- default = 2
       'show' is a True/False value that determines if the function displays step-by-step iterations."""

    # Define the p, d and q parameters to take any value between 0 and 2
    p = d = q = range(0, order)

    # Generate all different combinations of p, q and q triplets
    pdq = list(itertools.product(p, d, q))

    # Generate all different combinations of seasonal p, q and q triplets
    pdqs = [(x[0], x[1], x[2], 12) for x in list(itertools.product(p, d, q))]

    # Run a grid with pdq and seasonal pdq parameters calculated above and get the best AIC value
    ans = []
    for comb in pdq:
        for combs in pdqs:
            try:
                mod = sm.tsa.statespace.SARIMAX(ts,
                                                order=comb,
                                                seasonal_order=combs,
                                                enforce_stationarity=False,
                                                enforce_invertibility=False)

                output = mod.fit()
                ans.append([comb, combs, output.aic])
                if show == True:
                    print('ARIMA {} x {}12 : AIC Calculated ={}'.format(comb, combs, output.aic))
            except:
                continue
            
    ans_df = pd.DataFrame(ans, columns=['pdq', 'pdqs', 'aic'])
    display(ans_df.loc[ans_df['aic'].idxmin()])


def SARIMA_modeler(ts, order, s_order, trend):
    """takes a time series, a tuple (p,d,q) for 'order', a tuple (P,D,Q,m) for 's_order'
       and string ‘n’,’c’,’t’,’ct’ for no trend, constant, linear, and constant with linear trend, respectively,
       and returns a fitted SARIMAX model"""
    
    # create a SRAIMAX model based on inputs 'order', 's_order', and 'trend'
    SARIMA_MODEL = sm.tsa.statespace.SARIMAX(ts,
                                         order= order,
                                         seasonal_order= s_order,
                                         trend= trend,
                                         enforce_stationarity=False,
                                         enforce_invertibility=False)
    output = SARIMA_MODEL.fit()
    
    return output


def model_details(model):
    """takes a fitted SARIMAX model and displays coefficients, p-values, and AIC, and plots
       diagnostic plots for heteroskedasticity, residual distribution, and correlation."""
    
    print('Model coefficients: ', model.params)
    print('\n Model p_values: ', model.pvalues)
    print('\n Model AIC: ', model.aic)
    
    model.plot_diagnostics(figsize=(12,12))


def plot_model(ts, model, title=None):
    """takes a time series and a fitted model and plots them together to observe fit."""
    fig = plt.figure(figsize=(12,6))

    plt.plot(model.predict(), label='model')
    plt.plot(ts, label='original', alpha=.7)
    plt.legend()
    plt.title(title)
    plt.xlabel('Dates')
    plt.ylabel('Values')
    plt.show()
    
def plot_forcast_model(ts, model, alpha=.01, title=None):
    """takes a time series, a fitted model, and a level alpha (default = .01)
       and plots forecasted future values and the confidence interval."""
    
    # get predicted values for 36 steps going forward     
    prediction = model.get_forecast(steps=36)
    
    # get the confidence interval for predictions based on confidence level alpha
    pred_conf = prediction.conf_int(alpha=alpha)
    
    # plot original values and predicted values with confidence interval
    ax = ts.plot(label='observed', figsize=(16, 8))
    prediction.predicted_mean.plot(ax=ax, label='Forecast')
    ax.fill_between(pred_conf.index,
                    pred_conf.iloc[:, 0],
                    pred_conf.iloc[:, 1], color='k', alpha=.25)
    ax.set_xlabel('Dates')
    ax.set_ylabel('Values')

    plt.legend()
    plt.title(title)
    plt.show()


def expected_growth(model, steps=36, name='this area', alpha=.05, show=True):
    """take a model and default arguments 'steps' (number of steps to forcast forward, default = 36),
       'name' (name of area under analysis), 'alpha' (determines confidence interval), and 'show' 
       (dtermines wheter or not to print results) and returns upper, mean, and lower projected growth
       based on the confidence interval of projected mean growth."""
    
    # forcast future values from fitted model for speficied number of steps, get confidence interval
    # and get mean forcasted model results
    model_results = model.get_forecast(steps=steps)
    ci = model_results.conf_int(alpha=alpha)
    mean_forecast = model_results.predicted_mean
    
    # get confidence interval for printing
    con_int = int((1-alpha)*100)
    
    # calculate the upper, mean, and lower potential growth based on confidence interval
    upper_growth = (ci.iloc[-1,1] - ci.iloc[0,1]) / ci.iloc[0,1]
    mean_growth = (mean_forecast[-1] - mean_forecast[0]) / mean_forecast[0]
    lower_growth = (ci.iloc[-1,0] - ci.iloc[0,0]) / ci.iloc[0,0]
    
    # get the highest and lowest final values and show the range of potential outcomes
    highest_final_value = ci.iloc[-1,1]
    lowest_final_value = ci.iloc[-1,0]
    range_of_growth_values = round((highest_final_value - lowest_final_value), 2)
    
    # if show is true print out the results
    if show == True:
        print(f'With a {con_int}% confidence interval {name} is forecasted to grow at the following rates after {steps} months: \n')
        print(f'\t Upper Rate: {round((upper_growth*100),1)}%')
        print(f'\t Mean Rate: {round((mean_growth*100),1)}%')
        print(f'\t Lower Rate: {round((lower_growth*100),1)}%\n')
        print(f'With a range of ${range_of_growth_values} between the higest and lowest projected values.')
    
    return upper_growth, mean_growth, lower_growth


def ROI_calculator(model, ts, investment=10e6, steps=36, name='this area'):
    """Takes a model and time series and default arguments for 'investment', 'steps', and 'name', 
        and returns the amount of return projected over the time period specified"""
    
    # get the upper, mean, and lower growth projections based on confidence interval
    upper, mean, lower = expected_growth(model=model,
                                         steps = steps,
                                         show = False)

    # get the current median price of a property in the area under analysis
    current_price = ts[-1]
    
    # determine how mant properties could be purched with the initial investment
    n_properties = investment // current_price
    
    # calculate the amount of return we would get for the number of properties we purchased
    upper_return = round(current_price * upper * n_properties, 2)
    mean_return = round(current_price * mean * n_properties, 2)
    lower_return = round(current_price * lower * n_properties, 2)
    
    # print the results
    print(f'An initial investment of ${investment} in {name} would:\n')
    print(f'\t Allow us to buy approximately {n_properties} properties.')
    print(f'\t With a mean projected growth of {round((mean*100),1)}% over {steps} months we would net a ${mean_return} return')
    print(f'\t or ${mean_return / n_properties} per property.\n')
    print(f'\t With upper and lower growth rates at {round((upper*100),1)}% and {round((lower*100),1)}%,')
    print(f'\t we can project a total return between ${lower_return} and ${upper_return}')
    





    
