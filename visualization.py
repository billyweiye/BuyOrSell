# visualization of the trend analysis
from matplotlib import pyplot as plt 
import seaborn as sns

def plot_trend_analysis(data):
    # set up the figure
    fig, ax = plt.subplots(1) 
    fig.set_figheight(30)
    fig.set_figwidth(60)
    fig.set_dpi(300)

    # plot the price first
    sns.lineplot(x='date', y='close', data=data, ax=ax,color='#0D0D0D') 

    # plot the buy_or_sell spot
    custom_palette = {'buy': '#A5014D', 'strong_buy': '#710022','sell':'#848E2F','strong_sell':'#324103','hold':'blue'}

    sns.scatterplot(x='date',y='close',hue='buy_or_sell',data=data,palette=custom_palette,ax=ax)

    return fig

#均线交叉
def plot_ma(data):
    # set up the figure
    fig, ax = plt.subplots(1) 
    fig.set_figheight(30)
    fig.set_figwidth(60)
    fig.set_dpi(300)

    # plot the price first
    sns.lineplot(x='date', y='ma20', data=data, ax=ax,color='#A5014D') 
    sns.lineplot(x='date', y='ma100', data=data, ax=ax,color='#848E2F') 

    return fig