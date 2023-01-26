from deepface import DeepFace
import cv2
import numpy as np
from PIL import Image
from io import BytesIO
import base64
from retinaface import RetinaFace
from deepface import DeepFace


class ImageProcessor:

    @staticmethod
    def pillow_to_cv2_img(img):
        """
        Converts a pillow image to a numpy array
        """
        # convert a pillow image to a RGB numpy array
        img = np.array(img)
        # convert a RGB numpy array to a BGR numpy array
        img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
        return img
        
    @staticmethod
    def cv2_img_to_pillow(img):
        """
        Converts an image from a numpy array to a pillow image.
        """
        # convert image from BGR to RGB format
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        # convert a RGB numpy array to a pillow image
        img = Image.fromarray(img)
        return img

    @staticmethod
    def convertToRGB(img):  # argument types: Mat
        """
        This method converts bgr image to rgb
        """
        return cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    @staticmethod
    def convertToGRAY(img):  # argument types: Mat
        """
        This method converts bgr image to grayscale
        """
        return cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    @staticmethod
    def rectangle(img, rect):  # argument types: Mat, list
        """
        Draws a rectangle around the detected face
        """
        (x, y, w, h) = [int(val) for val in rect]
        cv2.rectangle(img, (x - 10, y - 10), (w + 10, h + 10), (0, 255, 0), 2, cv2.LINE_AA)
        
    @staticmethod
    def text(img, text, point):
        """
        Draws text on an image
        """
        cv2.putText(img, text, point, cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 1, cv2.LINE_AA)

    @staticmethod
    def pil_image_to_base64(pil_image):
        """
        Convert a pillow image to a base64 image
        """
        buf = BytesIO()
        pil_image.save(buf, format="JPEG")
        return base64.b64encode(buf.getvalue())

    @staticmethod
    def base64_to_pil_image(base64_img):
        """
        Converts a base64 image to a pillow image
        """
        return Image.open(BytesIO(base64.b64decode(base64_img)))
        
    @staticmethod
    def detect_emotion(frame):
        """
        Detects emotion
        """
        # use retina face for face detection and extraction (https://github.com/serengil/retinaface)
        result = RetinaFace.detect_faces(img_path=frame)
        
        for result_key in result:
            # get the coordinates of the face on the image
            (x, y, w, h) = result[result_key]["facial_area"]
            
            # detect emotion (https://pypi.org/project/deepface/)
            demography = DeepFace.analyze(img_path=frame[y: h, x: w], actions = ['emotion'], enforce_detection=False, detector_backend="opencv")
            
            # get the dominant emotion
            dominant_emotion = demography["dominant_emotion"]
            
            # draw bounding boxes of frame
            ImageProcessor.rectangle(frame, (x, y, w, h))
            
            # write emotion on bounding box
            ImageProcessor.text(frame, dominant_emotion, (x, y))
            
        return frame
