import pandas as pd
import plotly.offline as opy
import plotly.graph_objs as go
import plotly.figure_factory as ff


def get_plotly_plot(aspect_name_list):
    df=pd.read_csv('src/data_frame.csv')
    context={}
    name=aspect_name_list
    y1=[df.Positive[df.Aspect==x].values[0]/100 for x in name]
    y2=[df.Negative[df.Aspect==x].values[0]/100 for x in name]
    y3=[df.Neutral[df.Aspect==x].values[0]/100 for x in name]
    context={}
    trace1 =  go.Bar(name='Positive',x=name, y=y1,showlegend=True)
    trace2 =  go.Bar(name='Negative',x=name, y=y2,showlegend=True)
    trace3 =  go.Bar(name='Neutral',x=name, y=y3,showlegend=True)
    fig=go.Figure([trace1,trace2,trace3])                                                                                                 
    fig.update_layout(title =  dict(text ='Aspect Sentiment Distribution',
                                   font =dict(family='Sherif',
                                   size=25,
                                   color = 'blue')),
                        xaxis_title="Aspect Words",
                        yaxis_title="Percentage of Sentiment",
                        font=dict(
                        family="Courier New, monospace",
                        size=16,
                        color="red"),
                        yaxis = dict(
                        tickmode = 'linear',
                        tickformat= ',.0%',
                        range=[0,1],
                        dtick = 0.1    ))
    div = opy.plot(fig, auto_open=False, output_type='div')
    context['graph'] = div
    return context