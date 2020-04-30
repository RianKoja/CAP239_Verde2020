########################################################################################################################
# Define a decision tree finding function, and create a figure to present it.
#
# Written by Rian Koja to publish in a GitHub repository with specified licence.
########################################################################################################################

# Standard imports:
import pandas as pd
import os
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import sklearn
from sklearn import cluster


def ticker_fig(ticker1, ticker2, df):
    fig = plt.gcf()
    if fig.get_axes():
        plt.figure(plt.gcf().number+1)
    this_df = df.dropna(subset=[ticker1, ticker2])
    x = this_df[ticker1].tolist()
    y = this_df[ticker2].tolist()

    ax = sns.scatterplot(x=ticker1, y=ticker2, hue="Setor", size="Patrimônio Líq.", data=this_df)
    ax.grid(axis='both')
    for ii, txt in enumerate(this_df['Código do fundo'].tolist()):
        ax.annotate(txt, (x[ii], y[ii]), fontsize=7)

    fig = plt.gcf()
    fig.set_size_inches(13, 8)
    plt.tight_layout()
    plt.draw()


def box_plot_fig_2d(label_x, label_y, df):
    fig = plt.gcf()
    if fig.get_axes():
        plt.figure(plt.gcf().number+1)
    sns.boxplot(x=label_x, y=label_y, data=df)


def box_plot_fig(label_y, df):
    fig = plt.gcf()
    if fig.get_axes():
        plt.figure(plt.gcf().number+1)
    ax = sns.boxplot(y=label_y, data=df)
    ax.grid(axis='both')


def k_means_normalized_graph(ticker1, ticker2, df, k):
    # based on https://www.springboard.com/blog/data-mining-python-tutorial/
    df_red = df[["Código do fundo", "Setor", ticker1, ticker2]].dropna()
    print(df_red)
    np_array = df_red[[ticker1, ticker2]].values
    min_max_scaler = sklearn.preprocessing.MinMaxScaler()
    np_array_scaled = min_max_scaler.fit_transform(np_array)
    kmeans = cluster.KMeans(n_clusters=k)
    kmeans.fit(np_array_scaled)
    labels = kmeans.labels_
    centroids = min_max_scaler.inverse_transform(kmeans.cluster_centers_)
    df_red["Group"] = labels
    cross_tab = pd.crosstab(df_red["Setor"], df_red["Group"])
    print(cross_tab)
    # Create heatmap:
    fig = plt.gcf()
    if fig.get_axes():
        plt.figure(plt.gcf().number+1)
    fig = plt.gcf()
    sns.set()
    sns.heatmap(cross_tab, cmap="YlGnBu", annot=True, cbar=False, fmt="d", square=True, linewidths=0.5)
    plt.title("Incidence Matrix obtained from k-means based on " + ticker1 + " and " + ticker2 + " with k=" + str(k))
    fig.set_size_inches(9, 7)

    # Create new figure for the scatter plot:
    plt.figure(plt.gcf().number+1)
    fig = plt.gcf()
    fig.set_size_inches(13, 8)

    for i in range(k):
        # plot the centroid
        lines = plt.plot(centroids[i, 0], centroids[i, 1], 'kx')
        # make the centroid x's bigger
        plt.setp(lines, ms=15.0)
        plt.setp(lines, mew=4.0)
        # select only data observations with cluster label == i
        ds = np_array[np.where(labels == i)]
        # plot the data observations
        plt.plot(ds[:, 0], ds[:, 1], 'o', markersize=7, label=str(i))

    ax = plt.gca()

    # Added tickers as labels:
    this_df = df.dropna(subset=[ticker1, ticker2])
    x = this_df[ticker1].tolist()
    y = this_df[ticker2].tolist()
    for ii, txt in enumerate(this_df['Código do fundo'].tolist()):
        ax.annotate(txt, (x[ii], y[ii]), fontsize=7)

    plt.title("K-Means grouping for \"" + ticker1 + "\" and \"" + ticker2 + "\" with k=" + str(k))
    plt.xlabel(ticker1)
    plt.ylabel(ticker2)
    ax.set_facecolor('white')
    ax.grid(b=True, axis='both', color='black')
    ax.legend()
    plt.tight_layout()
    plt.draw()


def k_means_graph(ticker1, ticker2, df, k):
    # based on https://www.springboard.com/blog/data-mining-python-tutorial/
    df_reduced = df[[ticker1, ticker2]].dropna()
    np_array = np.array(df_reduced)
    kmeans = cluster.KMeans(n_clusters=k)
    kmeans.fit(np_array)
    labels = kmeans.labels_
    centroids = kmeans.cluster_centers_

    # Create new figure:
    fig = plt.gcf()
    if fig.get_axes():
        plt.figure(plt.gcf().number+1)
    fig = plt.gcf()
    fig.set_size_inches(13, 8)

    for i in range(k):
        # select only data observations with cluster label == i
        ds = np_array[np.where(labels == i)]
        # plot the data observations
        plt.plot(ds[:, 0], ds[:, 1], 'o', markersize=7)
        # plot the centroids
        lines = plt.plot(centroids[i, 0], centroids[i, 1], 'kx')
        # make the centroid x's bigger
        plt.setp(lines, ms=15.0)
        plt.setp(lines, mew=4.0)

    ax = plt.gca()

    # Added tickers as labels:
    this_df = df.dropna(subset=[ticker1, ticker2])
    x = this_df[ticker1].tolist()
    y = this_df[ticker2].tolist()
    for ii, txt in enumerate(this_df['Código do fundo'].tolist()):
        ax.annotate(txt, (x[ii], y[ii]), fontsize=7)

    plt.title("K-Means grouping for " + ticker1 + " and " + ticker2 + " with k=" + str(k))
    plt.xlabel(ticker1)
    plt.ylabel(ticker2)
    ax.grid(axis='both')
    plt.tight_layout()
    plt.draw()


def save_all(xlsx_name):
    for ii in range(1, plt.gcf().number+1):
        plt.figure(num=ii)
        plt.savefig("fig_{:02d}".format(ii) + xlsx_name + ".png")

