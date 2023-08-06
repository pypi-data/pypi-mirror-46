#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import pathlib
from collections import namedtuple

import numpy as np
from sklearn.multiclass import OneVsRestClassifier
from sklearn.preprocessing import label_binarize, LabelBinarizer

import draugr
from draugr import plot_confusion_matrix
from munin.utilities.html_embeddings import generate_math_html, plt_html, plt_html_svg, generate_metrics

ReportEntry = namedtuple("ReportEntry", ("name", "figure", "prediction", "truth", "outcome", "explanation"))

__author__ = "cnheider"
__doc__ = """
Created on 27/04/2019

@author: cnheider
"""


def generate_html(
    file_name, template_page="classification_report_template.html", template_path=None, **kwargs
):
    if not template_path:
        template_path = pathlib.Path.joinpath(os.path.dirname(__file__), "templates")

    from jinja2 import Environment, select_autoescape, FileSystemLoader

    env = Environment(loader=FileSystemLoader(template_path), autoescape=select_autoescape(["html", "xml"]))
    template = env.get_template(template_page)
    with open(f"{file_name}.html", "w") as f:
        f.writelines(template.render(**kwargs))


def generate_pdf(file_name):
    import pdfkit

    pdfkit.from_file(f"{file_name}.html", f"{file_name}.pdf")


if __name__ == "__main__":

    import matplotlib.pyplot as plt

    do_generate_pdf = False
    plt.rcParams["figure.figsize"] = (3, 3)
    from warg import NOD

    data_path = pathlib.Path.home()
    num_classes = 3
    cell_width = (800 / num_classes) - 6 - 6 * 2

    plt.plot(np.random.random((3, 3)))

    a = ReportEntry(
        name=1,
        figure=plt_html_svg(size=[cell_width, cell_width]),
        prediction="a",
        truth="b",
        outcome="fp",
        explanation=None,
    )

    plt.plot(np.ones((9, 3)))

    b = ReportEntry(
        name=2,
        figure=plt_html(format="svg", size=[cell_width, cell_width]),
        prediction="b",
        truth="c",
        outcome="fp",
        explanation=None,
    )

    plt.plot(np.ones((5, 6)))

    c = ReportEntry(
        name=3,
        figure=plt_html(size=[cell_width, cell_width]),
        prediction="a",
        truth="a",
        outcome="tp",
        explanation=None,
    )

    d = ReportEntry(
        name="fas3",
        figure=plt_html(format="jpg", size=[cell_width, cell_width]),
        prediction="a",
        truth="a",
        outcome="tp",
        explanation=None,
    )

    e = ReportEntry(
        name="fas3",
        figure=plt_html(format="jpeg", size=[cell_width, cell_width]),
        prediction="c",
        truth="c",
        outcome="tn",
        explanation=plt_html(format="svg", size=[cell_width, cell_width]),
    )

    from sklearn import svm, datasets
    from sklearn.model_selection import train_test_split

    iris = datasets.load_iris()
    X = iris.data
    y = iris.target
    class_names = iris.target_names

    bina = LabelBinarizer()
    y = bina.fit_transform(y)
    n_classes = y.shape[1]

    X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=2)

    classifier = OneVsRestClassifier(svm.SVC(kernel="linear", probability=True))
    classifier.fit(X_train, y_train)
    y_pred = classifier.predict(X_test)

    y_p_max = y_pred.argmax(axis=-1)
    y_t_max = y_test.argmax(axis=-1)

    plot_confusion_matrix(y_t_max, y_p_max, class_names=class_names)

    title = "Classification Report"
    confusion_matrix = plt_html(format="png", size=[800, 800])
    predictions = [[a, b, d], [a, c, d], [a, c, b], [c, b, e]]

    metric_fields, metrics = generate_metrics(y_t_max, y_p_max, class_names)

    draugr.roc_plot(y_pred, y_test, n_classes)

    roc_figure = plt_html(format="png", size=[800, 800])

    bundle = NOD.dict_of(title, confusion_matrix, metric_fields, metrics, predictions, roc_figure)

    file_name = title.lower().replace(" ", "_")

    generate_html(file_name, **bundle)
    if do_generate_pdf:
        generate_pdf(file_name)
