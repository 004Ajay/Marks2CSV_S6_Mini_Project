from pdf2image import convert_from_path
pdf_path = "D:/AJAYMON/AJAY/Programming/Auto_Excel_Mark_Entry/Codes/CV_Tesseract/Text-Extraction-Table-Image_workOnThis/img/Exam sheets.pdf"
pages = convert_from_path(pdf_path)

output_folder = "D:/AJAYMON/AJAY/Programming/Auto_Excel_Mark_Entry/Codes/CV_Tesseract/Text-Extraction-Table-Image_workOnThis/test_images"

for i in range(len(pages)):
    pages[i].save(f'{output_folder}/img{i}.jpg', 'JPEG')