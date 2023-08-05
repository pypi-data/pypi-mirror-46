
# pdfannot

This package aims to create a two-way link between annotated pdf and excel data frame.

It allows you to :

   - create an excel file containing each string annotated of the pdf in a column 'annot_text', along with its 
   annotation in a column 'content'.
    
   - annotate a pdf given an excel file of the form described above.
   
It can be really useful for generating automatically annotated pdf documents with NLP models capable to
infer annotations from raw texts in a data frame.


### Prerequisites

fitz

### Installing

pip install pymupdf
(pipenv install pymupdf)

import fitz

### Authors

Arthur Renaud, Antoine Marullaz

### Examples

your DataFrame contains info on what to annot on the pdf :
    
- if it already has at least columns 'text' (texts to annotate),
 'content' (description of each annotation), and 'type' ('Square' or 'Highlight') :
   
      annotate_pdf(DataFrame, path_to_corresponding_pdf, path_destination_annotated_pdf)
    
will use your dataframe and the directory of your pdf passed in argument to annotate it and store where you want.


- if it is a DataFrame with one column per label of annotation (WARNING : each of them must be name annot_{label_name})
then you must first pass : 

      df_to_adf(DataFrame)

to make it acceptable by annotate_pdf.

next execute :

    annotate_pdf(DataFrame, path_to_corresponding_pdf, path_destination_annotated_pdf)
    
to annotate your pdf (this method allows only highlights).
