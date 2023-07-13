import cv2
from pytesseract import Output

img = cv2.imread(r'C:\Users\gpandey2\Desktop\FMC files\CD2 - Well Cleanup Datasheet_page-0001.jpg')
d = pytesseract.image_to_data(img, output_type=Output.DICT)
keys = list(d.keys())

data_pattern = 'FLOPETROL'

n_boxes = len(d['text'])
for i in range(n_boxes):
    if float(d['conf'][i]) > 60:
        if re.match(data_pattern, d['text'][i]):
            (x, y, w, h) = (d['left'][i], d['top'][i], d['width'][i], d['height'][i])
            img = cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
Image.fromarray(img)
