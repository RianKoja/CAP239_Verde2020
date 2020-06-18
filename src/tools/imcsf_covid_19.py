# -*- coding: utf-8 -*-
"""
Created on Wed May 27 14:20:06 2020

@author: Giovanni Guarnieri Soares

Exercício 3 do trabalho

Arrumar a barra de erro
"""
# Standard imports:
import numpy as np
import matplotlib.pyplot as plt


def make_predict(y, country, meandays=7, savegraphs=True, doc=None):
    p = [[0.5, 0.45, 0.05], [0.7, 0.25, 0.05]]
    vals = [[1, 3, 5], [2, 4, 6]]

    '''
    Here we calculate the means by making a sublist from the original list and
    summing its values, how many days will be determined by the variable
    MEANDAYS and then we'll calculate G by this mean, using the value of a
    certain day and this sum of MEANDAYS before.
    After that, calculate n_min and n_max by the model. For n_guess we make a
    mean between n_min and n_max, and Deltank is the MEANDAYS minus the actual
    day divided by the actual day.
    '''
    for pind in range(len(p)):
        # Starting the lists to store model values.
        n_min = []  # n_min list
        n_max = []  # n_max list
        n_guess = []  # A mean between the n_max and n_min
        nk7 = []  # Storing all the means from meandays
        g = []  # Storing values of g
        deltank = []  # Storing Delta NK
        for i in range(meandays, len(y)):
            # nk7.append((sum(y[i-meandays:i]) + y[i])/meandays)
            nk7.append((sum(y[i-meandays:i]))/meandays)
            if y[i] < nk7[-1]:
                g.append((y[i]/nk7[-1]))
                w = [1, 1]
            else:
                g.append((nk7[-1]/y[i]))
                w = [1, 1]
            n = np.dot(p[pind], y[i])
            n_min.append(g[-1]*np.dot(n, vals[0]))
            n_max.append(g[-1]*np.dot(n, vals[1]))
            n_guess.append((w[0]*n_min[-1]+w[1]*n_max[-1])/sum(w))
            if y[i] != 0:
                deltank.append((nk7[-1]-y[i])/y[i])
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
        predicting data we already have, by plotting the variables
        n_min, n_max, n_guess with the original data.

        '''
        plt.figure()
        plt.title("Original Data with predictions,\n p={}, {}, {}, {}"
                  .format(p[pind][0], p[pind][1], p[pind][2], country))
        plt.ylabel("New Cases")
        plt.xlabel("Days")
        plt.plot(range(len(y)-meandays), y[meandays:], label="New Daily Cases")
        plt.plot(range(len(n_guess)), n_guess, label="Predict")
        plt.fill_between(range(len(n_min)), n_min, n_max, alpha=0.2, color='limegreen',
                         label=r'$N_{min}$ $N_{max}$ forecast band')
        # plt.plot(range(len(n_min)), n_min, label="n_min")
        # plt.plot(range(len(n_max)), n_max, label="n_max")
        plt.legend()
        if savegraphs:
            plt.savefig("{}originaldata{}.png".format(country, pind))
        plt.draw()
        if doc is None:
            plt.show()
        else:
            doc.add_fig()
        plt.close('all')

        '''
        Here we start to predict without the backup from original data, and we're going
        to show this by a dotted line.
        '''
        preddays = 20  # How many days will be predicted
        predict_nmin = [n_min[-1]]  # Prediction of n_min
        predict_nmax = [n_max[-1]]  # Prediction of n_max
        predictg = []  # g calculated with the prediction
        predict_nmed = y[-meandays-1:]  # Starting the prediction with real data
        predict_nk7 = []  # The meandays list to the prediction
        predictdeltank = []  # The Delta NK list to the prediction
        for i in range(meandays, preddays+meandays):
            predict_nk7.append(sum(predict_nmed[i-meandays:i])/meandays)
            # predict_nk7.append((sum(predict_nmed[i-meandays:i]) +
            # predict_nmed[i])/meandays)
            if predict_nmed[i] < predict_nk7[-1]:
                predictg.append((predict_nmed[i]/predict_nk7[-1]))
                w = [1, 1]
            else:
                predictg.append((predict_nk7[-1]/predict_nmed[i]))
                w = [1, 1]
            n = np.dot(p[pind], predict_nmed[-1])
            predict_nmin.append(predictg[-1]*np.dot(n, vals[0]))
            predict_nmax.append(predictg[-1]*np.dot(n, vals[1]))
            # predict_nmed.append(predict_nmin[-1])
            predict_nmed.append((w[0]*predict_nmin[-1]+w[1]*predict_nmax[-1])/sum(w))
            predictdeltank.append((predict_nk7[-1]-predict_nmed[-1])/predict_nmed[-1])
        plt.figure()
        plt.title("Plot showing the prediction for the next {} days,\n p={}, {}, {}, {}"
                  .format(preddays, p[pind][0], p[pind][1], p[pind][2], country))
        plt.ylabel("New Cases")
        plt.xlabel("Days")
        # plt.plot(range(len(y)-meandays), y[meandays:], label="Dados")
        plt.plot(range(len(n_guess)), n_guess, label="Nmed", c="orange")
        plt.plot(range(len(y)-meandays-1, len(y)+preddays-meandays),
                 predict_nmed[meandays:], c="orange", linestyle='--',
                 label="Predict Nmed")
        plt.legend()
        if savegraphs:
            plt.savefig("{}predictmeananddata{}.png".format(country, pind))
        plt.draw()
        if doc is None:
            plt.show()
        else:
            doc.add_fig()
        plt.close('all')
        predictg = np.array(predictg)
        # meanpredictg = abs(sum(predictg)/len(predictg)-predictg)
        fig, ax1 = plt.subplots()
        ax1.set_title("Predict values of g and s,\n p={}, {}, {}, {}"
                  .format(p[pind][0], p[pind][1], p[pind][2], country))
        ax1.set_xlabel("Day")
        ax1.set_ylabel("g")
        ax1.plot(range(len(g)), g, c="black", label="g from data")
        # plt.errorbar(range(len(g)), g, yerr=meang, xerr=0, hold=True, ecolor='k',
        # fmt='none', label='data', elinewidth=0.5, capsize=1)
        ax1.plot(range(len(g)-1, len(g)+preddays-1), predictg, c="black",
                 linestyle='--', label="Generated g")
        # plt.errorbar(range(len(g)-1, len(g)+preddays-1), predictg,
        # yerr=meanpredictg, xerr=0, hold=True, ecolor='k',
        # fmt='none', label='data', elinewidth=0.5, capsize=1)
        ax2 = ax1.twinx()
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
        ax2.set_xlabel("Day")
        ax2.set_ylabel("s")
        ax2.plot(range(len(s)), s, c="firebrick", label="s from data")
        # plt.errorbar(range(len(s)), s, yerr=means, xerr=0, hold=True, ecolor='k',
        # fmt='none', label='data', elinewidth=0.5, capsize=1)
        ax2.plot(range(len(s)-1, len(s)+preddays-1), predicts, c="firebrick",
                 linestyle='--', label="Generated s")
        # plt.errorbar(range(len(s)-1, len(s)+preddays-1), predicts,
        # yerr=meanpredicts, xerr=0, hold=True, ecolor='k',
        # fmt='none', label='data', elinewidth=0.5, capsize=1)
        ax1.legend(loc='upper center', bbox_to_anchor=(1.3, 1))
        ax2.legend(loc='upper center', bbox_to_anchor=(1.3, 0.8))
        plt.tight_layout()
        # plt.legend()
        plt.draw()
        if doc is None:
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
        country = country[:-1]
        make_predict(y, country, meandays=7, savegraphs=False)
    fread.close()

if __name__ == "__main__":
    main()
