# ELG API for BERT base fine-tuned for Swedish Sentiment Analysis (SSA)

This git repository contains [ELG compatible](https://european-language-grid.readthedocs.io/en/stable/all/A3_API/LTInternalAPI.html) Flask based REST API for the BERT base fine-tuned for Swedish Sentiment Analysis

[Huggingface SSA](https://huggingface.co/marma/bert-base-swedish-cased-sentiment) contains the model that was trained on ~20k of App Store reviews in Swedish.
Original author: Martin Malmsten from the National Library of Sweden / KBLab, published under ??? license. The model was fine-tuned based on one of the models available under [KB Swedish bert models](https://github.com/Kungbib/swedish-bert-models).


This ELG API was developed in EU's CEF project: [Microservices at your service](https://www.lingsoft.fi/en/microservices-at-your-service-bridging-gap-between-nlp-research-and-industry)

## Local development

Setup virtualenv, dependencies
```
python3 -m venv kb-senti-elg-venv
source  kb-senti-elg-venv/bin/activate
python3 -m pip install -r requirements.txt
```

The model can be downloaded to local (optional), because the transformers library downloads and caches the model anyway.
```python shell
from transformers import pipeline
sa = pipeline(
    task='sentiment-analysis',
    model='marma/bert-base-swedish-cased-sentiment
)
# Save pipeline
path = 'local_kb_bert_senti'
sa.save_pretrained(path)
```

Run the development mode flask app
```
FLASK_ENV=development flask run --host 0.0.0.0 --port 8000
```

## Building the docker image

```
docker build -t kb-senti-elg .
```


Or pull directly ready-made image `docker pull lingsoft/kb-senti:tagname`.

## Deploying the service

```
docker run -d -p <port>:8000 --init --memory="2g" --restart always kb-senti-elg
```

## REST API

### Call pattern

#### URL

```
http://<host>:<port>/process
```

Replace `<host>` and `<port>` with the hostname and port where the 
service is running.

#### HEADERS

```
Content-type : application/json
```

#### BODY

For text request
```json
{
  "type":"text",
  "content": text to be analyzed for the Sentiment Analysis task
}
```

Or stucturedText request
```json
{
  "type":"structuredText",
  "texts":[
    {
      "content":"The text of this node",
    },
  ]
}


#### RESPONSE

```json
{
  "response":{
    "type":"classification",
    "warnings":[...], /* optional */
    "classes":[
      {
        "class":"POSITIVE or NEGATIVE",
        "score":number
      }
    ]
  }
}
```

### Response structure

- `class`: (str)
  - either `POSITIVE` or `NEGATIVE`
- `score` (float)
  - confidence score of the entity, probability [0-1].

### Example call

```
curl --location --request POST 'http://localhost:8000/process' \
--header 'Content-Type: application/json' \
--data-raw '{
"type":"structuredText",
"texts": [{"content":"Jag gillar det inte."},{"content": "Lätt att boka. Resan blev inställt. Fick tillbaka pengar. Topp service"}]
}'
```

### Response should be

```json
{
  "response": {
    "type": "classification",
    "warnings": [],
    "classes": [
      {
        "class": "NEGATIVE",
        "score": 0.9969109892845154
      },
      {
        "class": "POSITIVE",
        "score": 0.9993164539337158
      }
    ]
  }
}
```
