def ets_decomposition(data,column,model):
    '''
    This function performs ets decomposition and plot the components of the timeseries data

    Parameters:
    data: raw data
    column: name of the timeseries column
    model: 'M' for multiplicative and 'A' for additive

    Output:
    graph
    '''
    from statsmodels.tsa.seasonal import seasonal_decompose
    if model=='M':
        model='multiplicative'
    elif model=='A':
        model='additive'
    result=seasonal_decompose(pd.DataFrame(column),model=model)

    return result.plot()
