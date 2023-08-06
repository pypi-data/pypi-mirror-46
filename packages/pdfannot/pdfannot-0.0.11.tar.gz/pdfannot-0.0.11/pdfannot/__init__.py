__version__ = "2019.04.19.1"

import os.path as op
from .genannot import annotate_pdf
from .extractannot import pdfannot2df

exple_pdf = op.join(op.dirname(op.dirname(__file__)), 'ressources/pdf_without_annot.pdf')