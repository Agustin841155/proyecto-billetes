import web
import tensorflow.keras
from PIL import Image, ImageOps
import numpy as np

urls = ('/imagen', 'Upload')

class Upload():
    def GET(self):
        web.header("Content-Type","text/html; charset=utf-8")
        return """
        <html>
            <head> <center>Identificador de Imagenes </center> </head>
            <p> introduzca una imagen de un billete para saber su valor</p>
            <style>
                html {
            border: black 10px dotted;
            margin: 20px;
            padding: 20px;
            background-color: lightblue;
            } 
            </style>
            <body>
                <form method="POST" enctype="multipart/form-data" action="">
                    <input type="file" name="myfile" />
                    <br/>
                    <input type="submit" />
                </form>
            </body>
        </html>"""

    def POST(self):
        x = web.input(myfile={})
        filedir = 'imagen' 
        if 'myfile' in x: 
            filepath=x.myfile.filename.replace('\\','/') 
            filename=filepath.split('/')[-1] 
            fout = open(filedir +'/'+ filename,'wb') 
            fout.write(x.myfile.file.read()) 
            fout.close()
            np.set_printoptions(suppress=True)

            model = tensorflow.keras.models.load_model('keras_model.h5')

            data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)

            image = Image.open('imagen/'+filename)

            size = (224, 224)
            image = ImageOps.fit(image, size, Image.ANTIALIAS)

            image_array = np.asarray(image)

            image.show()

            normalized_image_array = (image_array.astype(np.float32) / 127.0) - 1

            data[0] = normalized_image_array

            prediction = model.predict(data)

            for i in prediction:
                if i[0] > 0.8:
                    billete ="Es un billete de $20"
                elif i[1] > 0.8:
                    billete ="Es un billete de $50"
                elif i[2] > 0.8:
                    billete ="Es un billete de $100 pesos"
                elif i[3] > 0.8:
                    billete ="Es un billete de $200 pesos"
                elif i[4] > 0.8:
                    billete ="Es un billete de $500 pesos"
                elif i[5] > 0.8:
                    billete = "Es un billete de $1000 pesos"
                else:
                    billete = "No reconozco el billete lo siento :("     
                return billete
if __name__ == "__main__":
   app = web.application(urls, globals()) 
   app.run()