# %% Load required libraries
from anonymization import Anonymization
import pdftotext

import os

# %%
PDF_dir='./PDF'

def pdf_to_text():
    #pdf_files = [f for f in os.listdir('./PDF') if os.path.isfile(f)]
    pdf_files = [f.path for f in os.scandir(PDF_dir)]
    pdf_files = list(filter(lambda f: f.endswith(('.pdf','.PDF')), pdf_files))
    # Load PDFs available
    for f in pdf_files: 
        with open(f, "rb") as f:
            pdf = pdftotext.PDF(f)

        # print(type(f.name))    
        txtfile = f.name.replace('.pdf','.txt')

        # Save pdf text to a txt file.
        with open(txtfile, 'w') as ft:
            ft.write("\n\n".join(pdf))


# %%
if __name__ == "__main__":

    # convert pdf to texts
    pdf_to_text()
    #txt_files = [f for f in os.listdir(PDF_dir) if os.path.isfile(f)]
    txt_files = [f.path for f in os.scandir(PDF_dir)]
    txt_files = list(filter(lambda f: f.endswith(('.txt')), txt_files))
    # print(txt_files)

    for f in txt_files:
        a = Anonymization(f)
        a.anonymizes()

# %%
