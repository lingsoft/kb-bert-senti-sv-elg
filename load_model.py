from transformers import pipeline

sa = pipeline(task='sentiment-analysis',
              model='marma/bert-base-swedish-cased-sentiment')
# Save pipeline
path = 'local_kb_bert_senti'
sa.save_pretrained(path)
