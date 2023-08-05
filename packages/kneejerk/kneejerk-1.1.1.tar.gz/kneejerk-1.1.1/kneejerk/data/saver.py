import csv
import json

import click

from .utils import _ensure_path_exists


def persist_scores(fpaths, scores, output_path):
    """
    Given a list of fpaths to images, scores,
    and a place to save, generates a ``.csv``
    that will be used for later data loading

    Parameters
    ----------
    fpaths: list, fpath-like
        Absolute locations of images
    scores: list, numeric
    output_path: fpath-like
    """

    with open(output_path, 'w', newline='') as f:
        csvout = csv.writer(f)
        for pair in sorted(zip(fpaths, scores),
                           key=lambda x: x[0]):
            csvout.writerow(pair)


@click.pass_context
def persist_metadata(ctx):
    dirname = ctx.obj['dirname']
    _ensure_path_exists(dirname)
    with open(f'{dirname}/metadata.json', 'w') as f:
        json.dump(ctx.obj, f)
