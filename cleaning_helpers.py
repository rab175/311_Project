def mostly_nan(df):
    mostly_nans = []
    for col in df.columns:
        nan_count = df[col].isna().value_counts()
        if nan_count.index[0] == True:
            mostly_nans.append(col)
    
    return mostly_nans


def drop_empty_cols(df, percent_nan=.75):
    mostly_nans = []
    for col in df.columns:
        nan_count = df[col].isna().value_counts(normalize=True)
        nan_rate = nan_count.index[0]
        if nan_rate > percent_nan:
            mostly_nans.append(col)
    
    df.drop(columns=mostly_nans, inplace=True)
        
    return df

def check_na(df):
    for col in df.columns: 
        print(col, ': \n', df[col].isna().value_counts(normalize=True))
        print('-----'*5, '\n')
        
        
def datetime_converter(df, col):
    df.col = pd.to_datetime(df.col, format='%m/%d/%Y %I:%M:%S %p')
    
    return df
