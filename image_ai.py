from PIL import Image
import numpy as np

def analyze_image(uploaded_file):

    img = Image.open(uploaded_file)
    img = img.resize((128,128))

    arr = np.array(img).mean()

    # تحليل تجريبي (Demo AI)
    if arr < 100:
        result = "Possible abnormal tissue detected"
        color = "red"
    else:
        result = "Image appears normal"
        color = "green"

    return result, color
