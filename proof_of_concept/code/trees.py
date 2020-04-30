########################################################################################################################
# Entry file to run analysis on a table of financial indicators for Brazilian real state funds.
#
# Based on https://www.datacamp.com/community/tutorials/decision-tree-classification-python
#
# Written by Rian Koja to publish in a GitHub repository with specified licence.
########################################################################################################################


# Standard imports:
import pandas as pd
from sklearn.tree import DecisionTreeClassifier  # Import Decision Tree Classifier
from sklearn.model_selection import train_test_split  # Import train_test_split function
from sklearn import metrics  # Import scikit-learn metrics module for accuracy calculation
from sklearn.tree import export_graphviz
from sklearn.externals.six import StringIO
import pydotplus
import os
import matplotlib.pyplot as plt
import matplotlib.image as mpimg


def decision_tree(ticker1, ticker2, ticker3, df, xlsx_name):
    feature_cols = [ticker1, ticker2, ticker3]
    this_df = df.dropna(subset=feature_cols)
    X = this_df[feature_cols]
    y = this_df["Setor"]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=1)  # 70% training and 30% test

    # Create Decision Tree classifier object
    clf = DecisionTreeClassifier(criterion="entropy", max_depth=2)

    # Train Decision Tree Classifer
    #clf = clf.fit(X_train, y_train)
    clf = clf.fit(X, y)

    # Predict the response for test dataset
    #y_pred = clf.predict(X_test)
    y_pred = clf.predict(X)

    # Model Accuracy, how often is the classifier correct?
    print("Tree model Accuracy on ", ticker1, ticker2, ticker3, ": ", metrics.accuracy_score(y, y_pred))

    #Next line only needed in windows:
    #os.environ["PATH"] += os.pathsep + 'C:\\Program Files (x86)\\Graphviz2.38\\bin'
    dot_data = StringIO()
    export_graphviz(clf, out_file=dot_data, filled=True, rounded=True, special_characters=True,
                    feature_names=feature_cols, class_names=y.unique())
    graph = pydotplus.graph_from_dot_data(dot_data.getvalue())

    fig_name = os.path.join(os.getcwd(),"Decision_tree_" + xlsx_name + '.png')
    graph.write_png(fig_name)

    fig = plt.figure()
    img = mpimg.imread(fig_name)
    fig.figimage(img)
    fig.show()
    plt.pause(0.001)

    return
