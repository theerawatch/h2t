from utlis import *
import pytesseract
import cv2
import json
import os

def text_recognition(mat) -> dict:
    # hsv = detect_hsv(path)
    yellowHsv = [20,40,50,255,50,255]
    blueHsv = [40,179,40,255,40,255]
    pytesseract.pytesseract.tesseract_cmd = os.getenv('TESSERACT_PATH')

    # Step 1
    img = mat

    # Step 2
    yellowImgResult = detectColor(img, yellowHsv)
    blueImgResult = detectColor(img, blueHsv)

    # Step 3 & 4
    yellowImgContours, yellowContours = getContours(yellowImgResult, img, showGray=False,
                                        minArea=1500, filter=0,
                                        cThr=[100, 150], draw=True)
    blueImgContours, blueContours = getContours(blueImgResult, img, showGray=False,
                                        minArea=1500, filter=0,
                                        cThr=[100, 150], draw=True)
    yellowImgContours = cv2.resize(yellowImgContours, (0, 0), None, 0.5, 0.5)
    blueImgContours = cv2.resize(blueImgContours, (0, 0), None, 0.5, 0.5)

    # Step 5
    yellowRoiList = getRoi(img, yellowContours)
    blueRoiList = getRoi(img, blueContours)

    # Step 6
    yellowHighlightedText = []
    blueHighlightedText = []

    for x, roi in enumerate(yellowRoiList):
        text:str = pytesseract.image_to_string(roi)
        text = text.replace("\n","")
        text = text.replace("\f","") #remove new line on production
        yellowHighlightedText.append(text)

    for x, roi in enumerate(blueRoiList):
        text:str = pytesseract.image_to_string(roi)
        text = text.replace("\n","")
        text = text.replace("\f","") #remove new line on production
        blueHighlightedText.append(text)

    highlightList = {}
    # saveText(yellowHighlightedText,"yellow")
    # saveText(blueHighlightedText,"blue")
    highlightList['yellow'] = yellowHighlightedText
    highlightList['blue'] = blueHighlightedText

    with open(f'texts.json', 'w') as f:
        json.dump(highlightList,f,indent=4)

    return highlightList
