from img2table.document import Image
from img2table.ocr import PaddleOCR
from PIL import Image as PIL_Image, ImageDraw

paddle_ocr = PaddleOCR(lang="en")
src = "D:/AJAYMON/AJAY/Programming/Auto_Excel_Mark_Entry/Codes/image to table/ab_cut.jpg"

# Instantiation of document, either an image or a PDF
doc = Image(src, dpi=200)

# Table extraction
extracted_tables = doc.extract_tables(ocr=paddle_ocr, implicit_rows=True, min_confidence=50)

# Load the image using PIL
img = PIL_Image.open(src)
img_cpy = img

# Create a draw object
draw = ImageDraw.Draw(img)

for table in extracted_tables:
    for row in table.content.values():
        for cell in row:
            draw.rectangle((cell.bbox.x1, cell.bbox.y1, cell.bbox.x2, cell.bbox.y2), outline="red", width=3)

import matplotlib.pyplot as plt
plt.figure(figsize=(10, 10))

plt.imshow(img)

# In[ ]:





# In[8]:


i=0

for table in extracted_tables:
    for row in table.content.values():
        for cell in row:
            im_crp = img_cpy.crop((cell.bbox.x1, cell.bbox.y1, cell.bbox.x2, cell.bbox.y2))
            im_crp.save(f"output/a{i}.jpg")
            i+=1
            


# In[9]:


print(type(doc))


# In[ ]:




