# -*- coding: utf-8 -*-
"""
Created on Wed May 27 14:20:06 2020

@author: Giovanni Guarnieri Soares

Exercício 4 do trabalho
"""

import numpy as np
import matplotlib.pyplot as plt
from numpy.random import uniform


def make_predict_v2(y, country, doc=None):
    def rndg(prob1, prob2, total):
        if(uniform() < prob1/total):
            return 0
        elif(uniform() < (prob2+prob1)/total):
            return 1
        else:
            return 2
    glist = [0.20, 0.50, 0.80]
    p = [[0.5, 0.45, 0.05], [0.7, 0.25, 0.05]]
    pind = 1
    vals = [[1, 3, 5], [2, 4, 6]]
    bestg = []
    bestguess = []
    Nminl = []
    Nmaxl = []
    for i in range(len(y)-1):
        Nguess = []
        Nmin = []
        Nmax = []
        for g in glist:
            n = np.dot(p[pind], y[i])
            Nmin.append(g*np.dot(n, vals[0]))
            Nmax.append(g*np.dot(n, vals[1]))
            Nguess.append(abs(y[i+1]-(Nmin[-1]+Nmax[-1])/2))
        Nminl.append(Nmin[Nguess.index(min(Nguess))])
        Nmaxl.append(Nmax[Nguess.index(min(Nguess))])
        bestguess.append((Nminl[-1] + Nmaxl[-1]) / 2)
        bestg.append(glist[Nguess.index(min(Nguess))])
    plt.figure()
    plt.title(country)
    plt.ylabel("New Cases")
    plt.xlabel("Days")
    plt.title("Data for {}".format(country))
    plt.plot(range(len(y)), y, label="Data")
    plt.fill_between(range(len(Nminl)), Nminl, Nmaxl, alpha=0.2,
                     color='limegreen',
                     label=r'$N_{min}$ $N_{max}$ forecast band')
    plt.plot(range(len(bestguess)), bestguess, label="Predict")
    # plt.plot(range(len(Nminl)), Nminl,label="Nmin")
    # plt.plot(range(len(Nmaxl)), Nmaxl,label="Nmax")
    plt.legend()
    plt.draw()
    if doc is None:
        plt.show()
    else:
        doc.add_fig()
    plt.figure()
    plt.title("Best values of g\n country {}".format(country))
    plt.xlabel("Day")
    plt.ylabel("g")
    plt.plot(range(len(bestg)), bestg, label=" fitted g", c="firebrick")
    plt.grid("both")
    plt.legend()
    plt.tight_layout()
    plt.draw()
    if doc is None:
        plt.show()
    else:
        doc.add_fig()
    # predicting
    predictNmin = [Nminl[-1]]
    predictNmax = [Nmaxl[-1]]
    prob1 = bestg.count(0.2)
    prob2 = bestg.count(0.5)
    total = len(y)
    QTD = 1
    newglist = [bestg[-1]]
    media = []
    pred = 20
    for k in range(QTD):
        predictNmed = [bestguess[-1]]
        for i in range(pred):
            n1 = np.dot(p[pind], predictNmin[-1])
            n2 = np.dot(p[pind], predictNmed[-1])
            n3 = np.dot(p[pind], predictNmax[-1])
            ind = rndg(prob1, prob2, total)
            # print(ind)
            predictNmin.append(glist[ind]*np.dot(n1, vals[0]))
            predictNmax.append(glist[ind]*np.dot(n3, vals[1]))
            # predictNmed.append((predictNmin[-1]+predictNmax[-1])/2/QTD)
            predictNmed.append(glist[ind]*np.dot(n2, vals[0]))
            newglist.append(glist[ind])
        media.append(predictNmed)
    I = (np.ones((QTD)))
    predictNmed = np.dot(I, media)/QTD
    plt.figure()
    plt.ylabel("New Cases")
    plt.xlabel("Days")
    plt.title("Prediction for {}\n{} days".format(country,pred))
    plt.plot(range(len(y)), y, label="Dados")
    plt.plot(range(len(bestguess)), bestguess, label="Nmed", c="orange")
    # plt.plot(range(len(Nminl)), Nminl,label="Nmin", c="orange")
    # plt.plot(range(len(Nmaxl)), Nmaxl,label="Nmax", c="red")
    # plt.plot(range(len(Nminl)-1,len(Nminl)+20), predictNmin, c="orange",
    #          linestyle='--', label="Predict Nmin")
    # plt.plot(range(len(Nmaxl)-1, len(Nmaxl)+20), predictNmax, c="red",
    #          linestyle='--', label="Predict Nmax")
    plt.plot(range(len(bestguess)-1, len(bestguess)+pred), predictNmed,
             c="orange", linestyle='--', label="Predict Nmed")
    plt.legend()
    plt.draw()
    if doc is None:
        plt.show()
    else:
        doc.add_fig()
        plt.close('all')
    if QTD == 1:
        plt.figure()
        plt.title("Best values of g,\n country {}".format(country))
        plt.xlabel("Day")
        plt.ylabel("g")
        plt.plot(range(len(bestg)), bestg, label="fitted g", c="firebrick")
        plt.plot(range(len(bestg)-1, len(bestg)+pred), newglist,
                 linestyle='--', label="Generated g", c="firebrick")
        plt.legend()
        plt.grid("both")
        plt.tight_layout()
        plt.draw()
        if doc is None:
            plt.show()
        else:
            doc.add_fig()
            plt.close('all')

        bestguess.pop()
        bestg.pop()
        bestguess = bestguess+list(predictNmed)
        preds = 1-np.array(newglist)
        s = 1 - np.array(bestg)
        plt.figure()
        plt.title("Plot of s by time,\n country {}".format(country))
        plt.ylabel("s")
        plt.xlabel("Days")
        plt.plot(range(len(s)), s, label="fitted s", c="firebrick")
        plt.plot(range(len(s)-1, len(s)+pred), preds, '--',
                 label="Generated s", c="firebrick")
        plt.grid("both")
        plt.legend()
        plt.tight_layout()
        plt.draw()
        if doc is None:
            plt.show()
        else:
            doc.add_fig()
            plt.close('all')


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
        make_predict_v2(y, country)
    fread.close()


if __name__ == "__main__":
    main()
