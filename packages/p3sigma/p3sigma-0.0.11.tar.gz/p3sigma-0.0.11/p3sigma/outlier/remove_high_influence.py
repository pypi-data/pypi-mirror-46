def remove_high_influence(x_train,y_train,lm):
    '''
    This function studentize residuals and remove the ones with high influence
    studentizing means that removing one observation at the time and fit a line using the remaining ones.
    Effect on response variable is measured and the observations with high impact are labelled outliers.
    Outliers are removed afterwards.

    parameters:
    x_train: supplied for removing Outliers
    y_train: supplied for deleting same rows for convenience
    lm: regression classifier in order to obtain the influences

    returns:
    x_train & y_train without the outliers
    '''

    import pandas as pd
    import numpy as np
    influence = lm.get_influence()
    resid_student = influence.resid_studentized_external
    resid = pd.concat([x_train,pd.Series(resid_student,name = "Studentized Residuals")],axis = 1,join='inner')
    ind = resid.loc[np.absolute(resid["Studentized Residuals"]) > 3,:].index
    y_train.drop(ind,axis = 0,inplace = True)
    x_train.drop(ind,axis = 0,inplace = True)
    print('{} observations are removed'.format(len(ind)))
    print(resid.loc[np.absolute(resid["Studentized Residuals"]) > 3,:])
    return x_train,y_train
