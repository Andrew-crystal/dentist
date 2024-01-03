from google.cloud import vision


class GGvision_client:
    def __init__(self):
        self.vision_client = vision.ImageAnnotatorClient()

    def detect_labels(self, img_byte_arr, page_idx):
        """Detects labels in the image file."""
        print('hiiii')
        image = vision.Image(content=img_byte_arr)

        response = self.vision_client.text_detection(image=image)
        texts = response.text_annotations
        for text in texts[1:]:
            result += text.description

        return result