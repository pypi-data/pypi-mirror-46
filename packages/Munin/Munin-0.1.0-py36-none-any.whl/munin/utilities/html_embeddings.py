#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from collections import namedtuple
from io import BytesIO, StringIO

import markdown
from pycm import *

from warg import NOD

__author__ = "cnheider"
__doc__ = """
Created on 27/04/2019

@author: cnheider
"""

import matplotlib.pyplot as plt

MetricEntry = namedtuple("MetricEntry", ("Description", "Math", "Values", "Aggregated"))


def generate_metrics(y_test, y_pred, classes, decimals=1):
    cm = ConfusionMatrix(actual_vector=y_test, predict_vector=y_pred)
    cm.relabel({k: v for k, v in zip(range(len(classes)), classes)})

    support = MetricEntry(
        "Occurrence of each class (P)",
        generate_math_html("TP+FN"),
        {k: numpy.round(v, decimals) for k, v in cm.P.items()},
        numpy.round(sum(cm.P.values()) / len(classes), decimals),
    )

    sensitivity = MetricEntry(
        "True Positive Rate (TPR)",
        generate_math_html("\dfrac{TP}{TP+FN}"),
        {k: numpy.round(v, decimals) for k, v in cm.TPR.items()},
        numpy.round(sum(cm.TPR.values()) / len(classes), decimals),
    )

    specificity = MetricEntry(
        "True Negative Rate (TNR)",
        generate_math_html("\dfrac{TN}{TN+FP}"),
        {k: numpy.round(v, decimals) for k, v in cm.TNR.items()},
        numpy.round(sum(cm.TNR.values()) / len(classes), decimals),
    )

    precision = MetricEntry(
        "Positive Predictive Rate (PPV)",
        generate_math_html("\dfrac{TP}{TP+FP}"),
        {k: numpy.round(v, decimals) for k, v in cm.PPV.items()},
        numpy.round(sum(cm.PPV.values()) / len(classes), decimals),
    )

    npv = MetricEntry(
        "Negative Predictive Value (NPV)",
        generate_math_html("\dfrac{TP}{TP+FP}"),
        {k: numpy.round(v, decimals) for k, v in cm.NPV.items()},
        numpy.round(sum(cm.NPV.values()) / len(classes), decimals),
    )

    accuracy = MetricEntry(
        "Trueness",
        generate_math_html("\dfrac{TP+TN}{TP+TN+FP+FN}"),
        {k: numpy.round(v, decimals) for k, v in cm.ACC.items()},
        numpy.round(sum(cm.ACC.values()) / len(classes), decimals),
    )

    f1_score = MetricEntry(
        "Harmonic mean of precision and sensitivity",
        generate_math_html("2*\dfrac{PPV*TPR}{PPV+TPR}"),
        {k: numpy.round(v, decimals) for k, v in cm.F1.items()},
        numpy.round(sum(cm.F1.values()) / len(classes), decimals),
    )

    mcc = MetricEntry(
        "Matthews correlation coefficient",
        generate_math_html("\dfrac{TP*TN-FP*FN}{\sqrt{(TP+FP)(TP+FN)(TN+FP)(TN+FN)}}"),
        {k: numpy.round(v, decimals) for k, v in cm.MCC.items()},
        numpy.round(sum(cm.MCC.values()) / len(classes), decimals),
    )

    roc_auc = MetricEntry(
        "Receiver Operating Characteristics (ROC), "
        "Sensitivity vs (1 − Specificity), "
        "(True Positive Rate vs False Positive Rate), "
        "Area Under the Curve (AUC)",
        generate_math_html("\dfrac{TNR+TPR}{2}"),
        {k: numpy.round(v, decimals) for k, v in cm.AUC.items()},
        numpy.round(sum(cm.AUC.values()) / len(classes), decimals),
    )

    metrics = NOD.dict_of(
        support, sensitivity, specificity, precision, npv, accuracy, f1_score, mcc, roc_auc
    ).as_flat_tuples()

    return (("Metric", "Description", "Formula", f"Values", "Macro Avg"), metrics)


def generate_math_html(equation="e^x", inline=True, classes="math_span"):
    """
    For inline math, use \(...\).
    For standalone math, use $$...$$, \[...\] or \begin...\end.
    md = markdown.Markdown(extensions=['mdx_math'])
    md.convert('$$e^x$$')

      :param classes:
    :param equation:
    :param inline:
    :return:
  """
    md = markdown.Markdown(extensions=["mdx_math"], extension_configs={"mdx_math": {"add_preview": True}})
    if inline:
        stripped = md.convert(f"\({equation}\)").lstrip("<p>").rstrip("</p>")
        return f'<span class="{classes}"><{stripped}></span>'
    return md.convert(f"$${equation}$$")


def generate_qr():
    import pyqrcode
    import io
    import base64

    code = pyqrcode.create("hello")
    stream = io.BytesIO()
    code.png(stream, scale=6)
    png_encoded = base64.b64encode(stream.getvalue()).decode("ascii")
    return png_encoded


def plt_html_svg(*, size=(400, 400), dpi=100):
    fig_file = StringIO()
    plt.savefig(fig_file, format="svg", dpi=dpi)
    fig_svg = f'<svg width="{size[0]}" height="{size[1]}" {fig_file.getvalue().split("<svg")[1]}'
    return fig_svg


def plt_html(title="image", *, format="png", size=(400, 400), dpi=100):
    if format == "svg":
        return plt_html_svg(size=size, dpi=dpi)

    import base64

    fig_file = BytesIO()
    plt.savefig(fig_file, format=format, dpi=dpi)
    fig_file.seek(0)  # rewind to beginning of file
    b64_img = base64.b64encode(fig_file.getvalue()).decode("ascii")
    return (
        f"<img "
        f'width="{size[0]}" '
        f'height="{size[1]}" '
        f'src="data:image/{format};base64,{b64_img}" '
        f'alt="{title}"/><br>'
    )
