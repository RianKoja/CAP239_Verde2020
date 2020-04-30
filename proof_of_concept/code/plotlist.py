########################################################################################################################
# From possible combinations of available plot styles and indicators, create a selected amount of plot figures.
#
# Written by Rian Koja to publish in a GitHub repository with specified licence.
########################################################################################################################


# Standard imports:
import matplotlib.pyplot as plt

# Local imports:
import code.graphs as graphs
import code.trees as trees


def makeplots(xls_df, xlsx_name):

    graphs.ticker_fig("P/VPA", "Vacância Física", xls_df)

    graphs.ticker_fig("Rentab. Patr. no Período", "Rentab. Período", xls_df)

    graphs.ticker_fig("P/VPA", "DY Patrimonial", xls_df)

    graphs.ticker_fig("P/VPA", "DY Ano", xls_df)

    graphs.ticker_fig("DY (3M) Média", "DY (12M) Média", xls_df)

    graphs.ticker_fig("P/VPA", "Variação Preço", xls_df)

    graphs.box_plot_fig("P/VPA", xls_df)

    graphs.box_plot_fig("DY Ano", xls_df)

    graphs.k_means_normalized_graph("P/VPA", "DY Ano", xls_df, 4)

    graphs.k_means_normalized_graph("P/VPA", "Vacância Física", xls_df, 7)

    graphs.save_all(xlsx_name)

    plt.show(block=False)
    plt.pause(0.001)

    # Now the decision tree:
    trees.decision_tree("P/VPA", "Vacância Física", "DY Ano", xls_df, "_1_" + xlsx_name)
