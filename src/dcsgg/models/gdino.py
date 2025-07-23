from transformers import AutoProcessor, AutoModelForZeroShotObjectDetection
import torch
from dcsgg.utils import gdino_utils

class GDINO:
    def __init__(self, box_thresh=0.25, device='auto', verbosity=0):
        self.device = device if 'cuda' in device or 'cpu' in device else 'cuda' if torch.cuda.is_available() else 'cpu'
        model_id = "IDEA-Research/grounding-dino-base"

        self.processor = AutoProcessor.from_pretrained(model_id)
        self.model = AutoModelForZeroShotObjectDetection.from_pretrained(model_id).to(self.device)

        self.box_thresh, self.text_thresh = box_thresh, None
        self.verbosity = verbosity

    def inference_phrasewise(self, image, text):
        if self.verbosity > 0: print("Calling GDINO")
        inputs = self.processor(images=image, text=text, return_tensors="pt").to(self.device)
        with torch.no_grad():
            outputs = self.model(**inputs)

        token_spans = gdino_utils.get_token_spans(
            text)  # only call this if you have no custom method to provide token spans (in ProDG we have it)
        batch = {"image": image, "caption": text, "token_spans": token_spans}
        conf = gdino_utils.GDINOStructure(self.model, self.processor.tokenizer, self.text_thresh, self.box_thresh,
                                          self.device)
        boxes, phrases, logits = gdino_utils.postprocess_gdino_villain_style(conf, outputs, batch)
        return {'boxes': boxes, 'labels': phrases, 'logits': logits}