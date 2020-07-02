# -*- coding: utf-8 -*-
"""
Created on Sun Jun 28 16:53:46 2020

@author: Aleksandre
"""

import random as rand
import math
import matplotlib.pyplot as plt
import numpy as np
import scipy.stats as stats


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
    decipher(test_res,n,results)
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

def decipher(arr,n,res):
    if len(arr) > 1:
        if arr[0] == False:
            for i in range(int(math.pow(2,n-1))):
                res.append(False)
        else:
            decipher(arr[0],n-1,res)
        if arr[1] == False:
            for i in range(int(math.pow(2,n-1))):
                res.append(False)
        else:
            decipher(arr[1],n-1,res)
    else:
        res.append(arr)
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


def plot_avg_tests_over_p(n,p,x,y):
    #p - base probability
    #y - number of iterations of probability
    avg_tests_over_p = find_avg_tests_over_p(n,p,x,y)
    
    # These are the "Tableau 20" colors as RGB.    
    tableau20 = [(31, 119, 180), (174, 199, 232), (255, 127, 14), (255, 187, 120),    
             (44, 160, 44), (152, 223, 138), (214, 39, 40), (255, 152, 150),    
             (148, 103, 189), (197, 176, 213), (140, 86, 75), (196, 156, 148),    
             (227, 119, 194), (247, 182, 210), (127, 127, 127), (199, 199, 199),    
             (188, 189, 34), (219, 219, 141), (23, 190, 207), (158, 218, 229)]    
  
    # Scale the RGB values to the [0, 1] range, which is the format matplotlib accepts.    
    for i in range(len(tableau20)):    
        r, g, b = tableau20[i]    
        tableau20[i] = (r / 255., g / 255., b / 255.)    
    
    # You typically want your plot to be ~1.33x wider than tall. This plot is a rare    
    # exception because of the number of lines being plotted on it.    
    # Common sizes: (10, 7.5) and (12, 9)    
    plt.figure(figsize=(12, 10))    
  
    # Remove the plot frame lines. They are unnecessary chartjunk.    
    ax = plt.subplot(111)    
    ax.spines["top"].set_visible(False)    
    ax.spines["bottom"].set_visible(False)    
    ax.spines["right"].set_visible(False)    
    ax.spines["left"].set_visible(False)    
  
    # Ensure that the axis ticks only show up on the bottom and left of the plot.    
    # Ticks on the right and top of the plot are generally unnecessary chartjunk.    
    ax.get_xaxis().tick_bottom()    
    ax.get_yaxis().tick_left()    
  
    # Limit the range of the plot to only where the data is.    
    # Avoid unnecessary whitespace.    
    plt.ylim(0, int(avg_tests_over_p[1][-1])+1)    
    plt.xlim(0, 1)    
    
    plt.yticks(range(0, int(avg_tests_over_p[1][-1])+10, 10), [str(x) for x in range(0, int(avg_tests_over_p[1][-1])+10, 10)], fontsize=14)    
    plt.xticks(fontsize=14)    
    
    for y in range(10, int(avg_tests_over_p[1][-1])+10, 10):    
        plt.plot(range(0, 10), [y] * len(range(0, 10)), "--", lw=0.5, color="black", alpha=0.3)
        
    plt.tick_params(axis="both", which="both", bottom="off", top="off",    
                labelbottom="on", left="off", right="off", labelleft="on") 
    
    #plt.text(1, int(avg_tests_over_p[1][-1]), " # of tests", fontsize=14, color=tableau20[6])
    plt.plot(avg_tests_over_p[0],avg_tests_over_p[1],color=tableau20[6])
    #plt.text(1, int(math.pow(2,n)), " # of samples: " + str(int(math.pow(2,n))), fontsize=14, color=tableau20[4])
    plt.plot([int(math.pow(2,n)),int(math.pow(2,n))],color=tableau20[4])
    plt.title("Average number of tests vs Probability of infection")
    plt.xlabel("Probability of Infection")
    plt.ylabel("Average number of tests required")
    #plt.legend(["Tests","Number of Samples: " + str(int(math.pow(2,n)))])
    plt.savefig("avg_tests_over_p "+str(n),dpi=700)
    plt.show()
    
    return avg_tests_over_p


def find_variance_p(n,p,x):
    avg = find_avg_tests(n,p,x)
    total_sq_dist = 0
    for i in range(x):
        total_sq_dist+= math.pow((avg[1][i]-avg[0]),2)
    return [total_sq_dist/(x-1),avg[0]]

def find_avg_sd_tests_over_n(n,p,x,y):
    num_samples = []
    sd = []
    for k in range(3,n+1):
        num_samples.append(math.pow(2,k))
    for j in range(3,n+1):
        sd_total = 0
        for i in range(y):
            sd_total+= math.sqrt(find_variance_p(j,p,x)[0])
        sd.append((sd_total/y)/math.pow(2,j))
    return[num_samples,sd]

def plot_avg_sd_tests_over_n(n,p,x,y):
    avg = find_avg_sd_tests_over_n(n,p,x,y)
    
            # These are the "Tableau 20" colors as RGB.    
    tableau20 = [(31, 119, 180), (174, 199, 232), (255, 127, 14), (255, 187, 120),    
             (44, 160, 44), (152, 223, 138), (214, 39, 40), (255, 152, 150),    
             (148, 103, 189), (197, 176, 213), (140, 86, 75), (196, 156, 148),    
             (227, 119, 194), (247, 182, 210), (127, 127, 127), (199, 199, 199),    
             (188, 189, 34), (219, 219, 141), (23, 190, 207), (158, 218, 229)]    
  
    # Scale the RGB values to the [0, 1] range, which is the format matplotlib accepts.    
    for i in range(len(tableau20)):    
        r, g, b = tableau20[i]    
        tableau20[i] = (r / 255., g / 255., b / 255.)    
    
    # You typically want your plot to be ~1.33x wider than tall. This plot is a rare    
    # exception because of the number of lines being plotted on it.    
    # Common sizes: (10, 7.5) and (12, 9)    
    plt.figure(figsize=(10, 10))    
  
    # Remove the plot frame lines. They are unnecessary chartjunk.    
    ax = plt.subplot(111)    
    ax.spines["top"].set_visible(False)    
    ax.spines["bottom"].set_visible(False)    
    ax.spines["right"].set_visible(False)    
    ax.spines["left"].set_visible(False)   
    
    plt.yticks(fontsize=14)
    plt.xticks(fontsize=14)    
    
    #for y in range(0, 0.5, 10):    
        #plt.plot(range(0, 10), [y] * len(range(0, 10)), "--", lw=0.5, color="black", alpha=0.3)
        
    plt.tick_params(axis="both", which="both", bottom="off", top="off",    
                labelbottom="on", left="off", right="off", labelleft="on") 
    
    plt.plot(avg[0],avg[1],color=tableau20[6])
    plt.text(20, 0.1, "p = "+str(p), fontsize=14, color=tableau20[6])
    plt.title("Avg Standard Deviation as a fraction of # of Samples")
    plt.ylabel("Fraction of # of Samples")
    plt.xlabel("# of Samples")
    plt.savefig("avg_sd_over_n "+str(n),dpi=500)
    plt.show()
    
    return avg


def plot_test_normdist(n,p,x):
    res = find_variance_p(n,p,x)
    mu = res[1]
    variance = res[0]
    sigma = math.sqrt(variance)
    y = np.linspace(mu - 3*sigma, mu + 3*sigma, 100)
        # These are the "Tableau 20" colors as RGB.    
    tableau20 = [(31, 119, 180), (174, 199, 232), (255, 127, 14), (255, 187, 120),    
             (44, 160, 44), (152, 223, 138), (214, 39, 40), (255, 152, 150),    
             (148, 103, 189), (197, 176, 213), (140, 86, 75), (196, 156, 148),    
             (227, 119, 194), (247, 182, 210), (127, 127, 127), (199, 199, 199),    
             (188, 189, 34), (219, 219, 141), (23, 190, 207), (158, 218, 229)]    
  
    # Scale the RGB values to the [0, 1] range, which is the format matplotlib accepts.    
    for i in range(len(tableau20)):    
        r, g, b = tableau20[i]    
        tableau20[i] = (r / 255., g / 255., b / 255.)    
    
    # You typically want your plot to be ~1.33x wider than tall. This plot is a rare    
    # exception because of the number of lines being plotted on it.    
    # Common sizes: (10, 7.5) and (12, 9)    
    plt.figure(figsize=(10, 10))    
  
    # Remove the plot frame lines. They are unnecessary chartjunk.    
    ax = plt.subplot(111)    
    ax.spines["top"].set_visible(False)    
    ax.spines["bottom"].set_visible(False)    
    ax.spines["right"].set_visible(False)    
    ax.spines["left"].set_visible(False)    
  
    # Ensure that the axis ticks only show up on the bottom and left of the plot.    
    # Ticks on the right and top of the plot are generally unnecessary chartjunk.    
    ax.get_xaxis().tick_bottom()    
    ax.get_yaxis().tick_left()    
  
    # Limit the range of the plot to only where the data is.    
    # Avoid unnecessary whitespace.          
    
    #plt.yticks(range(0, 0.5, 10), [str(x) for x in range(0, 0.5, 10)], fontsize=14)    
    plt.yticks(fontsize=14)
    plt.xticks(fontsize=14)    
    
        
    plt.tick_params(axis="both", which="both", bottom="off", top="off",    
                labelbottom="on", left="off", right="off", labelleft="on") 
    
    plt.plot(y, stats.norm.pdf(y, mu, sigma),color=tableau20[6])
    plt.text(40, 0.02, "μ: "+str(round(mu,2))+" σ: "+str(round(math.sqrt(variance),2)), fontsize=14, color=tableau20[6])
    plt.title("Normal Distribution of # of tests, p = "+str(p))
    plt.savefig("Normal_Dist "+str(n),dpi=500)
    plt.show()
    
    return [mu,math.sqrt(variance)]

#print(plot_avg_sd_tests_over_n(7,1/128,500,15))
print(plot_avg_tests_over_p(7,1/128,300,128))
#print(plot_test_normdist(5,1/128,1000))


#print(binary_test(find_infected(4,1/16)[2],0,16))