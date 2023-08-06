def hodrick_prescott(data,column,freq):
    '''
    This function seperates the trend and cylical components by using Hodrick-Prescott method

    Parameters:
    column: 1-D array of a pandas dataframe column
    freq: seasonality cycle

    Returns:
    data: previous dataframe with two new columns including trend and cycle and also the graph is plotted

    '''
    from statsmodels.tsa.filters.hp_filter import hpfilter
    if freq=='M':
        l=129600
    elif freq=='Q':
        l=1600
    elif freq=='Y':
        l=6.25

    data['cycle'],data['trend']=hpfilter(data[column],lamb=l)
    data[['cycle','trend']].plot()
    return data
