def kpss(data,column):
    '''
    This functions applies Kwiatkowski-Phillips-Schmidt-Shin (KPSS) Test
    H0:data is not stationary
    HA:data is stationary

    Parameters:
    data: raw data
    column: timeseries data

    Output:
    Prints out if the data is stationary

    '''
    from pandas import Series
    from statsmodels.tsa.stattools import kpss
    result = kpss(data[column])
    if result[0]>=result[3]['1%']:
        print('Significant @ 1%')
        print('p-value: %f' % result[1])
        print('data is NOT stationary!')
    elif result[0]>=result[3]['1%']:
        print('Significant @ 5%')
        print('p-value: %f' % result[1])
        print('data is NOT stationary!')
    elif result[0]>=result[3]['1%']:
        print('Significant @ 10%')
        print('p-value: %f' % result[1])
        print('data is NOT stationary!')
    else:
        print('data is stationary!')
        print('p-value: %f' % result[1])
    return result
