import numpy as np
import matplotlib.pyplot as plt
from tools.soc import SOC


def init_plot():
    plt.close('all')
    plt.figure(figsize=(16, 9))


def addplot(data, label, ymin=None):
    np.seterr(divide='ignore')
    # prob_gamma, counts = soc.soc_main(data)
    prob_gamma, counts = SOC(data)
    log_prob = np.log10(prob_gamma)
    p = np.array(prob_gamma)
    p = p[np.nonzero(p)]
    c = counts[np.nonzero(counts)]
    log_p = np.log10(p)
    a = (log_p[np.argmax(c)] - log_p[np.argmin(c)]) / (np.max(c) - np.min(c))
    b = log_prob[0]
    y = b * np.power(10, (a * counts))
    x = np.log10(counts)
    order = np.argsort(x)
    x = x[order]
    y = y[order]
    if ymin is None:
        plt.plot(x, y, marker=".", label=label)
    elif True in (yt < ymin for yt in y):
        plt.plot(x, y, marker=".", label=label)
    np.seterr(divide='warn')


def plot(label):
    plt.legend(loc='center left', bbox_to_anchor=(1, 0.5), ncol=3, fontsize=6)
    plt.grid('both')
    plt.xlabel('log(ni)')
    plt.ylabel('log(Yi)')
    plt.title("SOC for " + label)
    plt.tight_layout()
    plt.draw()
