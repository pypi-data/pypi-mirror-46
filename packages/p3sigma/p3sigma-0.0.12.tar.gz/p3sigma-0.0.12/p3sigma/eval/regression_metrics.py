def regression_metrics(y_test,y_pred):
    from sklearn import metrics
    import numpy as np

    print('MAE = %.2f\n'%(metrics.mean_absolute_error(y_test, y_pred)))
    print('MSE = %.2f\n'%(metrics.mean_squared_error(y_test, y_pred)))
    print('RMSE = %.2f\n'%(np.sqrt(metrics.mean_squared_error(y_test, y_pred))))
    print('MPE = %.2f'%(np.mean(((y_test - y_pred) / y_test)) * 100)+'%\n')
    print('MAPE = %.2f'%(np.mean(np.abs((y_test - y_pred) / y_test)) * 100)+'%')
