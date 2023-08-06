def initial_look(data):
    '''
    This function initally shows the number of unique and null values for each feature.
    A simple algorithm tries to classify the feaures as categoric and continuous.

    Parameters:
    data: raw data

    Output:
    dataframe with results 

    '''
    import pandas as pd
    typelist=data.dtypes.to_dict()
    initial_look=pd.DataFrame(index=data.columns,columns=['Count','Null','Null (%)','Unique','Unique (%)','Type','Categoric'])
    for i in data.columns:
        initial_look.loc[i,'Count']=data[i].count()
        initial_look.loc[i,'Null']=data[i].isnull().sum()
        initial_look.loc[i,'Null (%)']=round(data[i].isnull().sum()/(data[i].count()+data[i].isnull().sum())*100)
        initial_look.loc[i,'Unique']=data[i].nunique()
        initial_look.loc[i,'Unique (%)']=round(data[i].nunique()/(data[i].count())*100)
        initial_look.loc[i,'Categoric']=0
        if typelist[i]=='object':
            initial_look.loc[i,'Categoric']=1

        if initial_look.loc[i,'Unique (%)']<5:
            initial_look.loc[i,'Categoric']=1

        for i in pd.DataFrame(data.dtypes).index:
            initial_look.loc[i,'Type']=pd.DataFrame(data.dtypes).loc[i,0]
    return initial_look
