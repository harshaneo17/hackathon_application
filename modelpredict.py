import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
from PIL import Image
import torch
import re
from io import BytesIO
import logging as log

from transformers import DonutProcessor, VisionEncoderDecoderModel

# sets the basic logging level as info
log.basicConfig(level=log.INFO)

processor = DonutProcessor.from_pretrained("naver-clova-ix/donut-base-finetuned-docvqa")
model = VisionEncoderDecoderModel.from_pretrained("naver-clova-ix/donut-base-finetuned-docvqa")

def read_image(file) -> Image.Image:
    """ This function takes file and converts it into PIL image format """
    opened_file = Image.open(BytesIO(file)).convert('RGB')
    log.info('_____LOADING IMAGE______')
    return opened_file

def get_answer(image, question, model, processor):

    
    pixel_values = processor(image, return_tensors="pt").pixel_values
    
    prompt = f"<s_docvqa><s_question>{question}</s_question><s_answer>"
    decoder_input_ids = processor.tokenizer(prompt, add_special_tokens=False, return_tensors="pt")["input_ids"]

    device = "cuda" if torch.cuda.is_available() else "cpu"
    model.to(device)
    log.info(f'device is {device}')

    outputs = model.generate(pixel_values.to(device),
                               decoder_input_ids=decoder_input_ids.to(device),
                               max_length=model.decoder.config.max_position_embeddings,
                               early_stopping=True,
                               pad_token_id=processor.tokenizer.pad_token_id,
                               eos_token_id=processor.tokenizer.eos_token_id,
                               use_cache=True,
                               num_beams=3,
                               bad_words_ids=[[processor.tokenizer.unk_token_id]],
                               return_dict_in_generate=True,
                               output_scores=True)
    
    seq = processor.batch_decode(outputs.sequences)[0]
    seq = seq.replace(processor.tokenizer.eos_token, "").replace(processor.tokenizer.pad_token, "")
    seq = re.sub(r"<.*?>", "", seq, count=1).strip()  # remove first task start token
    
    return processor.token2json(seq), outputs['sequences_scores'].item()*-1

def resultsjson(answer,score) -> list:
    """ This function takes listobject from the above function and makes it a response object.
    Returns response object """
    response = {"class": answer,"confidence": score}
    return response

def show_image(image):
    img = image.resize((600,600))
    img = np.asarray(img)
    plt.figure(figsize=(7,7))
    plt.imshow(img)




