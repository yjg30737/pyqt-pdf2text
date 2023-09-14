# pyqt-pdf2text
Converting PDF or Images into text file from PyQt with Tesseract and PyPDF2

## Requirements
* PyPDF2
* pytesseract
* pdf2image
* PyQt5>=5.14
  
Poppler is already included. (As of September 14, 2020, it is the latest version.)

## Note
The current GUI only uses Tesseract for image-to-text conversion and does not use it for PDF-to-text conversion. The functionality does exist in the script.py, so feel free to use it if you'd like.

## How to install
1. Install Tesseract from Google.
2. Add the installed path of Tesseract to your environment variables.
3. git clone
4. pip install -r requirements.txt
5. python main.py

## Preview
![image](https://github.com/yjg30737/pyqt-pdf2text/assets/55078043/9a26fed6-0e75-46c8-8cd7-1091740b1fb3)
