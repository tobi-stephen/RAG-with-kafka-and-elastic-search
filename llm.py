import os
import logging
from typing import List

import numpy as np
from openai import OpenAI


# Set your OpenAI API key
os.environ['OPENAI_API_KEY'] = 'YOUR_OPENAI_KEY'

# Create an OpenAI client
client = OpenAI()

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


def prompt(message, model='gpt-4o', max_tokens=100):
    response = client.chat.completions.create(
        model=model,
        messages=message,
        max_tokens=max_tokens,  # Adjust as needed
        n=1,
        temperature=1,  # higher is more creative
        seed=3,  # ensures consistency in response.
        stop=None
    )

    # Get the assistant's response
    return response.choices[0].message.content.strip()


def get_embedding(text: str, model="text-embedding-3-large", **kwargs) -> List[float]:
    # replace newlines, which can negatively affect performance.
    text = text.replace("\n", " ")

    response = client.embeddings.create(input=[text], model=model, encoding_format="float", **kwargs)

    return response.data[0].embedding


def normalize_l2(x):
    x = np.array(x)
    if x.ndim == 1:
        norm = np.linalg.norm(x)
        if norm == 0:
            return x
        return x / norm
    else:
        norm = np.linalg.norm(x, 2, axis=1, keepdims=True)
        return np.where(norm == 0, x, x / norm)


def get_normalized_embedding(text: str):
    return normalize_l2(get_embedding(text)).tolist()
