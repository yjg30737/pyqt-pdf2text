import os.path
from pathlib import Path


import PyPDF2
import pytesseract
from pdf2image import convert_from_path


# content = pytesseract.image_to_string('sample.png')
# print(content)


def convert_scanned_pdf_to_text(filename, lang, tesseract_path=r'C:\Program Files\Tesseract-OCR\tesseract.exe', poppler_path=r'.\poppler-23.08.0\Library\bin'):
    pytesseract.pytesseract.tesseract_cmd = tesseract_path
    images = convert_from_path(poppler_path=poppler_path, pdf_path=filename)
    content = ''

    for i, image in enumerate(images):
        text = pytesseract.image_to_string(image, lang=lang)
        content += text
    return content


def convert_img_to_text(filename, save_f=False):
    content = pytesseract.image_to_string(filename)
    if save_f:
        dst_dirname = 'dst'
        os.makedirs(dst_dirname, exist_ok=True)
        res_filename = os.path.join(dst_dirname, os.path.basename(filename) + '.txt')
        with open(res_filename, 'w') as file:
            file.write(content)
    return content


def convert_searchable_pdf_to_text(filename, save_f=False):
    content = ''
    try:
        with open(filename, 'rb') as file:
            reader = PyPDF2.PdfReader(file)

            num_pages = len(reader.pages)

            for page_num in range(num_pages):
                page = reader.pages[page_num]
                content += page.extract_text()
        if save_f:
            dst_dirname = 'dst'
            os.makedirs(dst_dirname, exist_ok=True)
            res_filename = os.path.join(dst_dirname, os.path.basename(filename) + '.txt')
            with open(res_filename, 'w') as file:
                file.write(content)
    except Exception as e:
        raise Exception
    finally:
        return content


def convert_pdf_to_text_in_directory(dirname):
    dirname = Path(dirname)
    result_dict = dict()

    for filename in dirname.rglob('*.pdf'):
        text = convert_searchable_pdf_to_text(filename)
        result_dict[filename] = text

    return result_dict

# from nltk.tokenize import sent_tokenize
#
# def find_relevant_sentences(text, keywords):
#     sentences = sent_tokenize(text)
#     relevant_sentences = []
#
#     for sentence in sentences:
#         if any(keyword.lower() in sentence.lower() for keyword in keywords):
#             relevant_sentences.append(sentence)
#
#     return relevant_sentences
#
# content = convert_searchable_pdf_to_text('Suva - Wikipedia.pdf')
# # Find related sentences
# keywords = ['Suva', 'History']
# relevant_sentences = find_relevant_sentences(content, keywords)
# print(relevant_sentences)


