import pandas as pd
import numpy as np
import os.path as op
from copy import deepcopy
import fitz
import random


def gen_color(content):
    """Generates a color randomly from a string
    :param content: a string
    :return:a triplet representing a color
    """
    color_str = str(content).split("-/-")[0]
    color = (0.3 + 0.5 * random.Random(color_str + 'a').random(),
             0.3 + 0.5 * random.Random(color_str + 'c').random(),
             0.3 + 0.5 * random.Random(color_str + 'b').random())
    return color


def add_square_from_coordinates(x,y,w,h,content,page):
    """

    :param x: coordinate x of the rectangle
    :param y: coordinate y
    :param w: width of the rectangle
    :param h: height of the rectangle
    :param content: content labelling the annotation
    :param page: page where to make the square
    :return: None, but the page has been annotated according to the arguments
    """
    rectangle = fitz.Rect(x, y, x+w, y+h)

    annot = page.addRectAnnot(rectangle)
    annot.setInfo({'content': f'{content}', 'name': '', 'title': '', 'creationDate': '', 'modDate': '',
                   'subject': ''})
    annot.setColors({"stroke": gen_color(
        content)})  # annot.setColors({"stroke":(0, 0, 1), "fill":(0.75, 0.8, 0.95)}) (Red, Yellow, Blue)
    annot.setBorder({'width': 1.5})
    annot.update(fill_color=None)


def add_annotation_from_text(text, content, page, type, debug=False):
    """Adds an annotation to a Pymupdf (fitz) pdf page
    :param annot_text: a string to look for in the pdf
    :param content: the label to give to this text
    :param page: the page number where the text can be found
    :param annot_type: 'Highlight' or 'Square' : the type of the annotations to make
    :return: None, but the page has been annotated according to the arguments
    """
    text.strip()
    rl = page.searchFor(text, hit_max=200)
    print(len(rl), rl) if debug else 0

    if rl:  #  If there's a match
        if type == 'Square':
            rectangle_encompass = fitz.Rect(min(w[0] for w in rl), min(w[1] for w in rl),
                                            max(w[2] for w in rl), max(w[3] for w in rl))

            annot = page.addRectAnnot(rectangle_encompass)
            annot.setInfo({'content': f'{content}', 'name': '', 'title': '', 'creationDate': '', 'modDate': '',
                           'subject': ''})
            annot.setColors({"stroke": gen_color(
                content)})  # annot.setColors({"stroke":(0, 0, 1), "fill":(0.75, 0.8, 0.95)}) (Red, Yellow, Blue)
            annot.setBorder({'width': 1.5})
            annot.update(fill_color=None)  # donc on peut faire des polyline_highlights avec fill_color = False ?

            print('Func(add_annotation) -- added Square') if debug else 0

        elif type == 'Highlight':
            print('Highlight') if debug else 0
            if len(rl) == 1:
                annot = page.addHighlightAnnot(rl[0])
                annot.setInfo({'content': f'{content}', 'name': '', 'title': '', 'creationDate': '', 'modDate': '',
                               'subject': ''})
                annot.setColors({"stroke": gen_color(content)})
                annot.update(fill_color=None)
                #  Add color annotation

            elif len(rl) > 1:
                for ix, k in enumerate(rl):
                    annot = page.addHighlightAnnot(k)
                    annot.setInfo({'content': f'{content}-/-{ix + 1}', 'name': '', 'title': '', 'creationDate': '',
                                   'modDate': '', 'subject': ''})
                    annot.setColors({"stroke": gen_color(content)})
                    annot.update(fill_color=None)

            print("Func(add_annotation) -- added 'HighLight'") if debug else 0

        else:
            print('WARNING: IncorrectSetting: incorrect annotation type detected')

    elif text == '':
        print("nothing to be found ") if debug == True else 0

    else:
        print(f'WARNING: NotFound: text to annotate is not found in page {page}') if debug == True else 0


def annotate_pdf(adf, pdf_path, dest_pdf_path, debug=False):
    """Takes a dataframe of annotations (adf) with minimal set of columns and
    :param adf: the adf containing info on what to annot on the pdf : must at least have columns 'annot_text', 'content', and 'annot_type'.
    :param pdf_path:the directory of the pdf you want to annot following the adf "instructions"
    :param dest_pdf_path: the path where to store the new pdf
    :return: None, but the pdf has been annotated accordingly and copied at the same directory with the name 'pdf_name' + '-marked.pdf'.
    """

    if not isinstance(adf, pd.DataFrame):
        raise Exception(f'TypeError : expected pd.Dataframe for adf, yet received object of type : {type(adf)}')

    if not op.exists(pdf_path):
        raise Exception(f'FileNotFound: pdf_path not exists at {pdf_path}')

    if not op.exists(op.dirname(dest_pdf_path)):
        raise Exception(f'DirNotFound: the directory of dest_pdf_path not exists at {op.dirname(dest_pdf_path)}')

    pdf = fitz.open(pdf_path)

    for index, row in adf.iterrows():

        if ('page' in adf.columns) and row['page']:
            if 'text' in adf.columns :
                add_annotation_from_text(row['text'], row['content'], pdf[row['page'] - 1], row['type'])
                print('test') if debug else 0
            elif all(c in adf.columns for c in 'xywh'):
                add_square_from_coordinates(row['x'], row['y'], row['w'], row['h'], row['content'], pdf[row['page'] - 1])
            else :
                print('WARNING no annot_text column nore coordinates provided')

        else:
            for page in pdf:
                print(page) if debug else 0
                add_annotation_from_text(row['text'], row['content'], page, row['type'])

    pdf.save(dest_pdf_path)
    return dest_pdf_path


def df_to_adf(df):
    """Transforms a Dataframe so that it matches genannot requirements
    :param dlf: a data frame with one column per label of annotation. WARNING : each of them must be name annot_{label_name}
    :return: a data frame with the three columns required by annotate_pdf
    """

    frames = []
    for c in df.columns:
        if 'annot_' not in c:
            continue

        adf1 = df[df[c].notnull()]
        adf1 = adf1[['page', c]]
        adf1.rename(columns={c: 'text'}, inplace=True)
        adf1['content'] = c[6:]
        adf1['type'] = "Highlight"

        frames.append(adf1)

    adf = pd.concat(frames)
    adf['text'] = adf['text'].astype(str)


    for index,row in adf.iterrows() :
        if ' ;; ' in row['text'] :
            l = row['text'].split(' ;; ')
            for annot in l :
                new_row = row
                new_row['text'] = annot
                adf = adf.append(new_row)


    adf.drop_duplicates(inplace=True, subset = ['text', 'page'])


    return adf


if __name__ == '__main__':

    # from scuts import visuallize_df
    # from shared import RESSOURCES_DIR
    #
    # pdf_path = op.join(RESSOURCES_DIR, 'pdf_test_annot_3.pdf')
    # adf = pd.DataFrame({'annot_text': ['by air or by water;',
    #                                    'the word mark ‘FEELING’, filed on 5 J vehicles ;; trees and transmissions for land vehicles;'],
    #                     'annot_type': ['Highlight', 'Square'],
    #                     'content': ['highlight', 'square'],
    #                     'page' : [1, 1]})
    # annotate_pdf(adf, pdf_path, '/home/antoine/PycharmProjects/pdfannot/ressources/pdf_test_annot_3.pdf-marked')
    #
    # # Test df_to_adf
    # df = pd.read_excel(RESSOURCES_DIR + '/seraphin/20020207_R1035_2000-2_FR.xlsx')
    # pdf_path = RESSOURCES_DIR + '/seraphin/20020207_R1035_2000-2_FR.pdf'
    # dest_pdf_path = RESSOURCES_DIR + '/seraphin/20020207_R1035_2000-2_FR_annotated.pdf'
    # adf = df_to_adf(df)
    # annotate_pdf(adf, pdf_path, dest_pdf_path)


    #test square_from_coordinate

    pdf_path = '/home/antoine/Desktop/ACHORD -Kbis-01-08-2018.pdf'
    dest_pdf_path = '/home/antoine/Desktop/ACHORD -Kbis-01-08-2018_annotated.pdf'
    adf = pd.read_excel('/home/antoine/Desktop/ACHORD -Kbis-01-08-2018 - annot.xlsx')
    annotate_pdf(adf, pdf_path, dest_pdf_path)