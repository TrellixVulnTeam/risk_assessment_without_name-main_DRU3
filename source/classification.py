"""Classification Module"""
from __future__ import annotations
from enum import Enum
import io
import torch
import fitz
import streamlit as st

from PIL import Image
from transformers import LayoutLMv2FeatureExtractor, LayoutLMv2Processor, LayoutLMv2Tokenizer

class ThirdPartyAuditDocType(str, Enum):
    """Object of different types of document"""
    BRC_AUDIT = 'BRC_Audit'
    BRC_CERT = 'BRC_Cert'
    FSSC_AUDIT = 'FSSC_Audit'
    FSSC_CERT = 'FSSC_Cert'
    HALAL = 'Hahal'
    KOSHER = 'Kosher'
    ORGANIC = 'Organic'
    OTHER = 'OTHER'
    SQF_AUDIT = 'SQF_Audit'
    SQF_CERT = 'SQF_Cert'

@st.cache(persist = True)
def init_model():
    """Initialize the components related to the model"""

    FEATURE_EXTRACTOR = LayoutLMv2FeatureExtractor()
    TOKENIZER = LayoutLMv2Tokenizer.from_pretrained('microsoft/layoutlmv2-base-uncased')
    PROCESSOR = LayoutLMv2Processor(FEATURE_EXTRACTOR, TOKENIZER)
    MODEL = torch.load("model/classify_model.pt", map_location = "cpu")

    return PROCESSOR, MODEL

def pdf2image(pdf_bytes: bytes):
    with fitz.open(stream = pdf_bytes) as document:
        first_page = document.load_page(0)
        first_page_pixmap = first_page.get_pixmap()
        image = first_page_pixmap.tobytes()

        return image


def inference_image(pdf_bytes: bytes) -> ThirdPartyAuditDocType:
    PROCESSOR, MODEL = init_model()
    image = Image.open(io.BytesIO(pdf2image(pdf_bytes))).convert('RGB')
    encoded_inputs = PROCESSOR(image, return_tensors='pt', padding='max_length', truncation=True)

    for key, value in encoded_inputs.items():
        encoded_inputs[key] = value.to(MODEL.device)

    outputs = MODEL(**encoded_inputs)
    # loss = outputs.loss
    logits = outputs.logits
    predicted_class_idx = logits.argmax(-1).item()
    result = MODEL.config.id2label[predicted_class_idx]
    return result

