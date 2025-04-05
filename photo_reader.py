from PIL import Image
from pytesseract import pytesseract
import cv2
import os, argparse
import langid
from os import listdir
from os.path import isfile, join
from autocorrect import Speller

path_to_tesseract = r"C:\Users\dan24\AppData\Local\Programs\Tesseract-OCR\tesseract.exe"

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("-i", "--image", required=True, help="path to input image")
    ap.add_argument("-p", "--pre_processor", default="thresh", help="the preprocessor usage")
    args = vars(ap.parse_args())


def read_image(args):
    if not('\\' in args["image"] or "/" in args["image"]):
        name = args["image"]
        args["image"] = 'files\\img\\' + args["image"]
        args["image"] = os.path.join(os.getcwd(), args["image"])
        if not(args["image"][args["image"].rfind("\\"):] in [".jpg", ".png", ".jpeg"]):
            mypath = args["image"][:args["image"].rfind("\\")]
            onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f)) and f[:f.rfind(".")] == name]
            if onlyfiles:
                args["image"] = mypath + "\\" + onlyfiles[0]
        if not os.path.exists(args["image"]):
            print("Image not found")
            return 'Image not found'
    try:
        if args["pre_processor"] is None:
            args["pre_processor"] = "thresh"
    except Exception:
        args["pre_processor"] = "thresh"

    image = cv2.imread(args["image"])

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    if args["pre_processor"] == "thresh":
        cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
    if args["pre_processor"] == "blur":
        cv2.medianBlur(gray, 3)

    filename = f"{os.getpid()}.jpg"
    cv2.imwrite(filename, gray)

    pytesseract.tesseract_cmd = path_to_tesseract

    text = pytesseract.image_to_string(Image.open(filename))
    if langid.classify(text)[0] == "ru":
        lang = "rus"
    else:
        lang = langid.classify(text)

    text_lang = pytesseract.image_to_string(Image.open(filename), lang='rus')
    os.remove(filename)

    spell = Speller(lang='ru')

    if __name__ == "__main__":
        print(spell(text_lang))
        cv2.imshow("image", image)
        cv2.imshow("Output In Grayscale, gray", gray)
        cv2.waitKey(0)
        return

    return spell(text_lang)


def compiler(text):
    pass


if __name__ == "__main__":
    read_image(args)