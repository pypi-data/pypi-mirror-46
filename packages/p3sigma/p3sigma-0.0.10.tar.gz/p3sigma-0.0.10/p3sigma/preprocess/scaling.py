def scaler_one(x_train,x_test,slist):
    import numpy as np
    from sklearn.preprocessing import StandardScaler
    scaler = StandardScaler()
    for i in slist:
        val=np.array(x_train.loc[:,i]).reshape(-1, 1)
        x_train[i] = scaler.fit_transform(val)
        val=np.array(x_test.loc[:,i]).reshape(-1, 1)
        x_test[i] = scaler.transform(val)
    return x_train,x_test
