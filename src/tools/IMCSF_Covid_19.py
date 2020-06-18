# -*- coding: utf-8 -*-
"""
Created on Wed May 27 14:20:06 2020

@author: Giovanni Guarnieri Soares

Exercício 3 do trabalho

Arrumar a barra de erro
"""



import numpy as np
import matplotlib.pyplot as plt


def makePredict(y, country, meandays=7, savegraphs=True, doc=None):
    glist = [0.20, 0.50, 0.80]
    g = glist[0]
    
    p = [[0.5, 0.45, 0.05], [0.7, 0.25, 0.05]]
    pind = 1
    vals = [[1, 3, 5], [2, 4, 6]]
    
    
    '''
    Here we calculate the means by making a sublist from the original list and
    summing its values, how many days will be determined by the variable MEANDAYS
    and then we'll calculate G by this mean, using the value of a certain day
    and this sum of MEANDAYS before.
    After that, calculate Nmin and Nmax by the model. For Nguess we make a mean
    between Nmin and Nmax, and Deltank is the MEANDAYS minus the actual day
    divided by the actual day.
    '''
    for pind in range(len(p)):
        # Starting the lists to store model values.
        Nmin = []  # Nmin list
        Nmax = []  # Nmax list
        Nguess = []  # A mean between the Nmax and Nmin
        Nk7 = []  # Storing all the means from meandays
        g = []  # Storing values of g
        deltank = []  # Storing Delta NK
        for i in range(meandays, len(y)):
            # Nk7.append((sum(y[i-meandays:i]) + y[i])/meandays)
            Nk7.append((sum(y[i-meandays:i]))/meandays)
            if y[i] < Nk7[-1]:
                g.append((y[i]/Nk7[-1]))
                w = [1, 1]
            else:
                g.append((Nk7[-1]/y[i]))
                w = [1, 1]
            n = np.dot(p[pind], y[i])
            Nmin.append(g[-1]*np.dot(n, vals[0]))
            Nmax.append(g[-1]*np.dot(n, vals[1]))
            Nguess.append((w[0]*Nmin[-1]+w[1]*Nmax[-1])/sum(w))
            if y[i] != 0:
                deltank.append((Nk7[-1]-y[i])/y[i])
            else:
                deltank.append(np.nan)
        
        
        # Calculating deltag to calculate s and plot
        deltag = [0]
        for i in range(1, len(g)):
            g0 = g[i-1]
            if g0 < g[i]:
                deltag.append(g0-g[i] - (1-g[i])**2)
            else:
                deltag.append(g0-g[i] + (1-g0)**2)
        
        deltag = np.array(deltag)
        deltank = np.array(deltank)
        s = (2*deltag + deltank)/3
        
        
        '''
        Now all the plottings, we are going to show how good the model works by
        predicting data we already have, by plotting the variables Nmin, Nmax, Nguess
        with the original data.
        
        '''
        plt.figure()
        plt.title("Graph with the data and the mean of 7 days for each data,\n p={}, {}, {}\n {}"
                  .format(p[pind][0],p[pind][1],p[pind][2], country))
        plt.ylabel("New Cases")
        plt.xlabel("Days")
        plt.plot(range(len(y)-meandays), y[meandays:], label="Dados")
        plt.plot(range(len(Nk7)), Nk7, label="{} days means".format(meandays))
        plt.legend()
        if savegraphs:
            plt.savefig("{}meananddata{}.png".format(country,pind))
        plt.draw()
        plt.figure()
        plt.title("Original Data with predictions,\n p={}, {}, {}\n {}"
                  .format(p[pind][0],p[pind][1],p[pind][2], country))
        plt.ylabel("New Cases")
        plt.xlabel("Days")
        plt.plot(range(len(y)-meandays), y[meandays:], label="Dados")
        plt.plot(range(len(Nguess)), Nguess, label="Predict")
        plt.plot(range(len(Nmin)), Nmin, label="Nmin")
        plt.plot(range(len(Nmax)), Nmax, label="Nmax")
        plt.legend()
        if savegraphs:
            plt.savefig("{}originaldata{}.png".format(country,pind))
        plt.draw()
        if doc is None:
            plt.show()
        else:
            doc.add_fig()
        # Plotting the values of calculated g
        
        g = np.array(g)
        plt.figure(figsize=(20, 10))
        # meang = abs(sum(g)/len(g)-g)
        plt.title("Values of g,\n p={}, {}, {}\n {}"
                  .format(p[pind][0],p[pind][1],p[pind][2], country))
        plt.xlabel("Day")
        plt.ylabel("g")
        # plt.errorbar(range(len(g)), g, yerr=meang, xerr=0, hold=True, ecolor='k',
        # fmt='none', label='data', elinewidth=0.5, capsize=1)
        plt.plot(range(len(g)), g, 'o-')
        if savegraphs:
            plt.savefig("{}originalg{}.png".format(country,pind))
        plt.draw()
        if doc is None:
            plt.show()
        else:
            doc.add_fig()
        # Plotting the values of calculated s
        
        s = np.array(s)
        # means = abs(sum(s)/len(s)-s)
        plt.figure(figsize=(20, 10))
        plt.title("Values of s,\n p={}, {}, {}\n {}"
                  .format(p[pind][0], p[pind][1], p[pind][2], country))
        plt.xlabel("Day")
        plt.ylabel("s")
        # plt.errorbar(range(len(s)), s, yerr=meang, xerr=0, hold=True, ecolor='k',
        # fmt='none', label='data', elinewidth=0.5, capsize=1)
        plt.plot(range(len(s)), s, 'o-')
        if savegraphs:
            plt.savefig("{}originals{}.png".format(country,pind))
        plt.draw()
        if doc is None:
            plt.show()
        else:
            doc.add_fig()
        '''
        Here we start to predict without the backup from original data, and we're going
        to show this by a dotted line.
        '''
        
        preddays = 20  # How many days will be predicted
        predictNmin = [Nmin[-1]]  # Prediction of Nmin
        predictNmax = [Nmax[-1]]  # Prediction of Nmax
        predictg = []  # g calculated with the prediction
        predictNmed = y[-meandays-1:]  # Starting the prediction with real data
        predictNk7 = []  # The meandays list to the prediction
        predictdeltank = []  # The Delta NK list to the prediction
        for i in range(meandays, preddays+meandays):
            predictNk7.append(sum(predictNmed[i-meandays:i])/meandays)
            # predictNk7.append((sum(predictNmed[i-meandays:i]) +
                               # predictNmed[i])/meandays)
            if predictNmed[i] < predictNk7[-1]:
                predictg.append((predictNmed[i]/predictNk7[-1]))
                w = [1, 1]
            else:
                predictg.append((predictNk7[-1]/predictNmed[i]))
                w = [1, 1]
            n = np.dot(p[pind], predictNmed[-1])
            predictNmin.append(predictg[-1]*np.dot(n, vals[0]))
            predictNmax.append(predictg[-1]*np.dot(n, vals[1]))
            # predictNmed.append(predictNmin[-1])
            predictNmed.append((w[0]*predictNmin[-1]+w[1]*predictNmax[-1])/sum(w))
            predictdeltank.append((predictNk7[-1]-predictNmed[-1])/predictNmed[-1])
        plt.figure()
        plt.title("Plot showing the prediction for the next {} days,\n p={}, {}, {}\n{}"
                  .format(preddays, p[pind][0],p[pind][1],p[pind][2], country))
        plt.ylabel("New Cases")
        plt.xlabel("Days")
        plt.plot(range(len(y)-meandays), y[meandays:], label="Dados")
        plt.plot(range(len(Nguess)), Nguess, label="Nmed", c="orange")
        plt.plot(range(len(y)-meandays-1, len(y)+preddays-meandays),
                 predictNmed[meandays:], c="orange", linestyle='--',
                 label="Predict Nmed")
        plt.legend()
        if savegraphs:
            plt.savefig("{}predictmeananddata{}.png".format(country,pind))
        plt.draw()
        if doc is None:
            plt.show()
        else:
            doc.add_fig()
        predictg = np.array(predictg)
        # meanpredictg = abs(sum(predictg)/len(predictg)-predictg)
        plt.figure(figsize=(20, 10))
        plt.title("Predict values of g,\n p={}, {}, {}, {}"
                  .format(p[pind][0],p[pind][1],p[pind][2], country))
        plt.xlabel("Day")
        plt.ylabel("g")
        plt.plot(range(len(g)), g, c="b", label="g from data")
        # plt.errorbar(range(len(g)), g, yerr=meang, xerr=0, hold=True, ecolor='k',
        # fmt='none', label='data', elinewidth=0.5, capsize=1)
        plt.plot(range(len(g)-1, len(g)+preddays-1), predictg, c="b",
                 linestyle='--', label="Generated g")
        # plt.errorbar(range(len(g)-1, len(g)+preddays-1), predictg,
        # yerr=meanpredictg, xerr=0, hold=True, ecolor='k',
        # fmt='none', label='data', elinewidth=0.5, capsize=1)
        plt.legend()
        if savegraphs:
            plt.savefig("{}predictg{}.png".format(country,pind))
        plt.draw()
        if doc is None:
            plt.show()
        else:
            doc.add_fig()
        predictdeltag = [0]
        for i in range(1, len(predictg)):
            g0 = predictg[i-1]
            if g0 < predictg[i]:
                predictdeltag.append(g0-predictg[i] - (1-predictg[i])**2)
            else:
                predictdeltag.append(g0-predictg[i] + (1-g0)**2)
        
        predictdeltag = np.array(predictdeltag)
        predictdeltank = np.array(predictdeltank)
        predicts = (2*predictdeltag + predictdeltank)/3
        # meanpredicts = abs(sum(predicts)/len(predicts)-predicts)
        plt.figure(figsize=(20, 10))
        plt.title("Predict values of s,\n p={}, {}, {}\n {}"
                  .format(p[pind][0],p[pind][1],p[pind][2], country))
        plt.xlabel("Day")
        plt.ylabel("s")
        plt.plot(range(len(s)), s, c="b", label="s from data")
        # plt.errorbar(range(len(s)), s, yerr=means, xerr=0, hold=True, ecolor='k',
        # fmt='none', label='data', elinewidth=0.5, capsize=1)
        plt.plot(range(len(s)-1, len(s)+preddays-1), predicts, c="b",
                 linestyle='--', label="Generated s")
        # plt.errorbar(range(len(s)-1, len(s)+preddays-1), predicts,
                     # yerr=meanpredicts, xerr=0, hold=True, ecolor='k',
                     # fmt='none', label='data', elinewidth=0.5, capsize=1)
        plt.legend()
        if savegraphs == True:
            plt.savefig("{}predicts{}.png".format(country,pind))
        plt.draw()
        if(doc == None):
            plt.show()
        else:
            doc.add_fig()


def main():
    fread = open("daily-cases-covid-19.csv", "r")
    next(fread)

    countrylist = ['Brazil,', 'Portugal,', 'Spain,', 'France,', 'Belgium,',
                   'United States,', 'Italy,', 'China,', 'South Korea,']
    
    countrylist.sort()
    
    for country in countrylist:
        y = []
        
        for line in fread:
            ctr, code, m, yr, data = line.split(",")
            if int(data) > 50 and country in line and "excl." not in line:
                break
        
        
        for line in fread:
            if country in line and "excl." not in line:
                ctr, code, m, yr, data = line.split(",")
                y.append(int(data))
            if country in line and "May 20" in line:
                break
        
        country=country[:-1]
        makePredict(y, country, meandays=7, savegraphs=False)
    
    fread.close()
    

if __name__ == "__main__":
    main()
