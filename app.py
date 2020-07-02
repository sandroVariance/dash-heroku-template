# -*- coding: utf-8 -*-
"""
Created on Tue Jun 30 05:39:25 2020

@author: Aleksandre
"""

# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import pandas as pd
import math
import random as rand
from dash.dependencies import Input, Output

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

# assume you have a "wide-form" data frame with no index
# see https://plotly.com/python/wide-form/ for more options


def find_infected(n,p):
    
    #n - power of 2
    #p - infection probability
    
    #initialize all samples as false
    samples = [False] * int(math.pow(2,n))
    
    #randomly set each sample to True with probability p
    for i in range(int(math.pow(2,n))):
        if rand.random() < p:
            samples[i] = True
    
    #test the samples
    test_res = binary_test(samples,0,int(math.pow(2,n)))
    results = []
    #decipher(test_res,n,results)
    test_num = count_tests(test_res)
    
    #print("NUMBER OF TESTS: ",test_num)
    #print("RESULTS: " ,results)
    #print("ORIGINAL SAMPLES: ", samples)
    
    return [test_num,results,samples]

def group_test(arr):
    for i in range(len(arr)):
        if arr[i] == True:
            return True
    return False
# Returns index of x in arr if present, else -1 
def binary_test(arr, start, end):
    results = []
    #Initial test
    if group_test(arr) == False:
        results.append(False)
    else:
    #divide samples into two groups
        if end-start>1 and len(arr)>1:
            mid  = (start+end)//2
            #test each group
            group_1 = group_test(arr[start:mid])
            group_2 = group_test(arr[mid:end])
            #if a group test positive, recurse binary_test on that group
            if group_1:
                results.append(binary_test(arr, start, mid))
            else:
                results.append(False)
            if group_2:
                results.append(binary_test(arr, mid, end))
            else:
                results.append(False)
        else:
            results.append(arr[start:end])
        
    #return bool array
    return results

def count_tests(arr):
    if arr == False or arr == True or len(arr)==1:
        return 1
    else:
        return 1 + count_tests(arr[0]) + count_tests(arr[1])
    
def find_avg_tests(n,p,x):
    total_tests = 0
    num_tests = []
    for i in range(x):
        tests = find_infected(n,p)[0]
        total_tests += tests
        num_tests.append(tests)
    return [total_tests/x,num_tests]

def find_avg_tests_over_p(n,p,x,y):
    prob = []
    num_tests = []
    for i in range(y):
        prob.append(i*p)
        num_tests.append(find_avg_tests(n,p*i,x)[0])
    return [prob,num_tests]

app.layout = html.Div(children=[
    html.H1(children='Hello Dash'),

    html.Div(children='''
        Dash: A web application framework for Python.
    '''),

    dcc.Graph(
        id='example-graph',
    ),
   html.Label('number of samples'),
   dcc.Slider(
        id='n_samp',
        min=3,
        max=7,
        marks={i: 'Label {}'.format(i) if i == 1 else str(int(math.pow(2,i))) for i in range(3, 8)},
        value=5,
    ),
    html.Div(id='slider-output-container')
])
@app.callback(
    Output('example-graph', 'figure'),
    [Input('n_samp', 'value')])
def update_figure(value):
    #filtered_df = df[df.year == selected_year]
    
    #fig = px.scatter(filtered_df, x="gdpPercap", y="lifeExp", 
                     #size="pop", color="continent", hover_name="country", 
                     #log_x=True, size_max=55)
    data = find_avg_tests_over_p(value,1/32,500,32)
    df_2 = pd.DataFrame({"p":data[0], "tests":data[1]})
    fig = px.line(df_2, x="p", y="tests")
    fig.update_layout(transition_duration=100)

    return fig

#data = find_avg_tests_over_p(int(5),1/32,500,32)
#df = pd.DataFrame({"x": [1, 2, 7], "SF": [4, 1, 2], "Montreal": [2, 4, 5]})
#df_2 = pd.DataFrame({"p":data[0], "tests":data[1]})
#fig = px.bar(df, x="x", y=["SF", "Montreal"], barmode="group")
#fig = px.line(df_2, x="p", y="tests")


   




if __name__ == '__main__':
    app.run_server(debug=True)