def goodness_of_fit(lm):
    '''
    Measures goodness of fit by first checking if the distribution of the residuals are normal using Shapiro Wilk test.
    After normal distribution is proven, checks heteroskedacity by using Goldfield Quandt test.
    In some cases residuals variance increases with increasing input (heteroskedacity)
    This method checks if the variance is equal for all residuals afterwards.

    Parameters:
    regressor: output of the regression classifier of statsmodels

    Output:
    displays results


    '''

    import statsmodels.stats.diagnostic as smsdia
    from scipy.stats import shapiro
    stat, p = shapiro(lm.resid)
    print('Statistics = %.3f\n\nP-Value = %.3f\n' % (stat, p))
    alpha = 0.05
    if p > alpha:
        print('Distribution is Gaussian')
        test = smsdia.het_goldfeldquandt(lm.resid, lm.model.exog)
        print('F Statistics = %.3f\n\nP-Value = %.3f\n' % (test[0], test[1]))
        alpha=0.05
        if test[1] > alpha:
            print('Regression is homoscedastic')
        else:
            print('Regression is heteroskedastic')
    else:
        print('Sample does not look Gaussian (reject H0)')
