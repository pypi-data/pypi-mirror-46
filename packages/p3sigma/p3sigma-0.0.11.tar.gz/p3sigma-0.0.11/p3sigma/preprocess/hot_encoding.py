def hot_one(x_train,x_test,hlist):
    from sklearn.preprocessing import OneHotEncoder
    onehotencoder = OneHotEncoder(sparse=False)
    import numpy as np
    for i in hlist:
        val=np.array(x_train.loc[:,i]).reshape(-1, 1)
        x_train_ohe=onehotencoder.fit_transform(val)
        for j in range(0,len(x_train_ohe[0])-1):
            x_train[i+' Feature '+str(j)]=x_train_ohe[:,j]
        x_train.drop(columns=[i],inplace=True)

        val=np.array(x_test.loc[:,i]).reshape(-1, 1)
        x_test_ohe=onehotencoder.transform(val)
        for j in range(0,len(x_test_ohe[0])-1):
            x_test[i+' Feature '+str(j)]=x_test_ohe[:,j]
        x_test.drop(columns=[i],inplace=True)
    return x_train,x_test
