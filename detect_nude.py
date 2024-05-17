import tensorflow as tf
import io
import numpy as np
import skimage.io
from PIL import Image 
from random import sample 
from nudenet import NudeDetector

nude_detector = NudeDetector()

class detect_nude:

    def __init__(self, config):
        self.model = self.load_model()
        self.__labels = [
            "FEMALE_GENITALIA_COVERED",
            "FACE_FEMALE",
            "BUTTOCKS_EXPOSED",
            "FEMALE_BREAST_EXPOSED",
            "FEMALE_GENITALIA_EXPOSED",
            "MALE_BREAST_EXPOSED",
            "ANUS_EXPOSED",
            "FEET_EXPOSED",
            "BELLY_COVERED",
            "FEET_COVERED",
            "ARMPITS_COVERED",
            "ARMPITS_EXPOSED",
            "FACE_MALE",
            "BELLY_EXPOSED",
            "MALE_GENITALIA_EXPOSED",
            "ANUS_COVERED",
            "FEMALE_BREAST_COVERED",
            "BUTTOCKS_COVERED",
        ]
        self._bad_labels = [
            "BUTTOCKS_EXPOSED",
            "FEMALE_BREAST_EXPOSED",
            "FEMALE_GENITALIA_EXPOSED",
            "ANUS_EXPOSED",
            "MALE_GENITALIA_EXPOSED",
        ]

    def load_model(self):
        model = tf.keras.models.load_model('model.h5')
        return model

    def detect(self, frames):
        frames = sample(frames, len(frames) // 2)
        preprocessed = []
        for frame in frames:
            preprocessed.append(
                self.preprocess_image(Image.fromarray(frame))
            )

        for value in self.model.predict(np.array(preprocessed)):
            if value[1] > 0.5:
                return False
        return self._layerTwoDetect(frames)

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
    
    def _layerTwoDetect(self, frames):
        detection_example = [
            {'class': 'BELLY_EXPOSED',
            'score': 0.799403190612793,
            'box': [64, 182, 49, 51]},
            {'class': 'FACE_FEMALE',
            'score': 0.7881264686584473,
            'box': [82, 66, 36, 43]},
        ]
        
        def _is_bad_label(label):
            return label in self._bad_labels
        
        def _has_bad_label(detections):
            return any(_is_bad_label(d['class']) and d['score'] > 0.6 for d in detections)
        
        for frame in frames:
            if _has_bad_label(nude_detector.detect(frame)):
                return False
        
        return True
