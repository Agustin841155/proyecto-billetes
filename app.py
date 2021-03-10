import tensorflow.keras
from PIL import Image, ImageOps
import numpy as np

np.set_printoptions(suppress=True)

model = tensorflow.keras.models.load_model('keras_model.h5')

data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)

image = Image.open('4.jpg')

size = (224, 224)
image = ImageOps.fit(image, size, Image.ANTIALIAS)

image_array = np.asarray(image)

image.show()

normalized_image_array = (image_array.astype(np.float32) / 127.0) - 1

data[0] = normalized_image_array

prediction = model.predict(data)
for i in prediction:
    if i[0] > 0.8:
        print("Es un billete de $20")
    elif i[1] > 0.8:
        print("Es un billete de $50")
    elif i[2] > 0.8:
        print("Es un billete de $100")
    elif i[3] > 0.8:
        print("Es un billete de $200")
    elif i[4] > 0.8:
        print("Es un billete de $500")
    elif i[5] > 0.8:
        print("Es un billete de $1000")        
