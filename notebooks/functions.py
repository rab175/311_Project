import sqlite3
import pandas as pd

conn = sqlite3.Connection('Northwind_small.sqlite')
cursor = conn.cursor()
    
def get_table(conn=conn, table=None):
    df = pd.read_sql(f'SELECT * from {table}', conn)
    return df


#check the basics of a dataframe
def inspect_dataframe(df):
    """Enter a pandas dataframe and get the
       first five rows, data types and counts,
       and central tendencies"""
    display(df.head())
    display(df.info())
    display(df.describe())
    
  
# compare two data arrays
from numpy import mean, std

def compare_2(a,b):
    """enter two series/arrays of data
       and get the size, mean, and standard deviation"""
    
    n1 = len(a)
    n2 = len(b)
    
    mu1 = a.mean()
    mu2 = b.mean()
    
    std1 = a.std()
    std2 = b.std()
    
    print(f'The size of group1 is: {n1}  \t  The size of group2 is {n2}')
    print(f'The mean of group1 is: {mu1} \t  The mean of group2 is: {mu2}')
    print(f'The std of group1 is: {std1} \t  The std of group2 is: {std2}')
    
def compare_many(list_of_arrays):
    """enter a list of arrays and return
       the size, mean, and standard deviation"""
    for i in range(len(list_of_arrays)):
        print(f'{i + 1}. n = {len(list_of_arrays[i])} \t mean = {round(list_of_arrays[i].mean(),2)} \t std {round(list_of_arrays[i].std(),2)}')
    

# test normality using the shapiro-wilks test
from scipy.stats import shapiro

def test_normality(x, alpha=.05):
    """enter a series of data and condust a 
       shapiro-wilks test for normality"""
    
    t, p = shapiro(x)
    if p < alpha:
        print(f'p = {p} \t Therefore the data is not normal')
        return False
    print(f'p = {p} \t Therefore the data is normal')
    return True


# test equal variance using levene's test
from scipy.stats import levene

def test_variance(a,b, alpha=.05):
    """enter two series of data and conduct 
       Levene's test for equal variance"""
       
       
    t, p = levene(a,b)
    if p < alpha:
        print(f'p = {p} \t Therefore the data do not have equal variances')
        return False
    print(f'p = {p} \t Therefore the data has equal variances')
    return True
    
    
# generate a random sample
from numpy import random,array
def random_sample(array, size=30):
    
    """draw a random selection of values
       with replacement of size n and add
       their mean to a list of means"""
    
    sample = []
    for i in range(size):
        sample.append(random.choice(array,size=30).mean())
    
    return sample

    
# check effect size
from numpy import var, sqrt
def cohen_d(a,b):
    
    """enter two series of data to derive 
       Cohen's d and determine effect size"""
    
    n1, n2 = len(a), len(b)
    
    diff = mean(a) - mean(b)
    
    var1, var2 = var(a), var(b)
    
    pooled_var = (n1 * var1 + n2 * var2) / (n1 + n2)
    
    d = diff / sqrt(pooled_var)
    
    return abs(d)    
    
    
# accept or reject null hypotheses based on p-value
def check_null_hypothesis(p, alpha=.05):
    """enter a p value to detemine and optional level 
       alpha (default = .05) to determine if you should 
       accept or reject null hypothesis"""
    
    if p > alpha: 
        print(f'With a p-value of {p}, which is greater than {alpha}, at this time we fail to reject the H0')
        return True
    print(f'With a p-value of {p}, which is less than {alpha} we can reject the H0 and accept Ha')
    return False
    

# establish the bonferoni alpha level
def bonferroni_alpha(obs=None, alpha=.05):
    """Enter the number of observaions and level 
       of alpha (default = .05) and return the bonferroni
       correction appha level"""
    return alpha/obs
    
    
    