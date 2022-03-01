import os
from transformers import pipeline
from elg.model import ClassesResponse

model_path = 'local_kb_bert_senti/' if os.path.isdir(
    'local_kb_bert_senti') else 'marma/bert-base-swedish-cased-sentiment'

senti_analyzer = pipeline('sentiment-analysis', model=model_path)


def is_exceed_limit(text):
    tokens = senti_analyzer.tokenizer.tokenize(text)
    # max length is 512, max token length is 510. need to consider about\
    # [SOS] and [EOS]
    return len(tokens) > 510


def clf_func_elg(text):
    res = senti_analyzer(text)[0]
    elg_dict = {"class": res['label'], "score": res['score']}
    return ClassesResponse(**elg_dict)
