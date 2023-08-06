def label_one(x_train,x_test,llist):
    import numpy as np
    from sklearn.preprocessing import LabelEncoder
    labelencoder = LabelEncoder()
    for i in llist:
        x_train[i] = labelencoder.fit_transform(x_train[i])
        x_test[i] = labelencoder.transform(x_test[i])
    return x_train,x_test
