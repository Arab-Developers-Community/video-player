import tensorflow as tf
import io
import numpy as np
import skimage.io
from PIL import Image 
from random import sample 

class detect_nude:

    def __init__(self, sample_rate):
        self.sample_rate = sample_rate
        self.model = self.load_model()


    def load_model(self):
        model = tf.keras.models.load_model('model.h5')
        return model

    def detect(self, frames):
        frames = sample(frames, self.sample_rate if len(frames) > self.sample_rate else len(frames))
        preprocessed = []
        for frame in frames:
            preprocessed.append(
                self.preprocess_image(Image.fromarray(frame))
            )

        for value in self.model.predict(np.array(preprocessed)):
            if value[1] > 0.5:
                return False
        return True

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
    