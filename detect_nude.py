import tensorflow as tf
import io
import numpy as np
import skimage.io
from PIL import Image 

class detect_nude:

    def __init__(self, config):
        self.filter_nudes = config["filter_nudes"]
        self.filter_kissing = config["filter_kissing"]
        self.model = self.load_model()

    def load_model(self):
        model = tf.keras.models.load_model('model.h5')
        return model

    def detect(self, frame):
        image = self.preprocess_image(frame)
        inputs = np.expand_dims(image, axis=0)
        sfw_probability, nsfw_probability = self.model.predict(inputs)[0]
        print(sfw_probability > 0.7)
        return sfw_probability > 0.7

    def preprocess_image(self, pil_image: Image):
        if pil_image.mode != "RGB":
            pil_image = pil_image.convert("RGB")

        pil_image_resized = pil_image.resize(
            (256, 256), resample=Image.BILINEAR
        )

        fh_im = io.BytesIO()
        pil_image_resized.save(fh_im, format="JPEG")
        fh_im.seek(0)

        image = skimage.io.imread(
            fh_im, as_gray=False
        ).astype(np.float32)

        height, width, _ = image.shape
        h, w = (224, 224)

        h_off = max((height - h) // 2, 0)
        w_off = max((width - w) // 2, 0)
        image = image[h_off:h_off + h, w_off:w_off + w, :]


        image = image[:, :, ::-1]

        vgg_mean = [104, 117, 123]
        image = image - np.array(vgg_mean, dtype=np.float32)

        return image