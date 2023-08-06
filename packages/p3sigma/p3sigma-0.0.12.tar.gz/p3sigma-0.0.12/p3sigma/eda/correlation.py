def show_correlation(data,method='pearson'):
    import seaborn as sns
    corr = data.corr(method=model)
    sns.heatmap(corr,cmap='RdBu_r',vmin=-1,vmax=1)
