def sma(data,col,w):
    '''
    This function simply returns simple moving average of the timeseries at desired window

    Parameters:
    data: raw data
    col: column name of timeseries
    w: desired window

    Output:
    Returns initial dataframe with simple moving average column added to the end    
    '''
    data[str(w)+'M SMA']=data[col].rolling(window=w).mean()
    return data
