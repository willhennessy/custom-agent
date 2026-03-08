## Simple script to visualize the prompt pipeline
## Input string -> Token string -> Token IDs -> Embedding matrix
## For visual reference, see https://platform.openai.com/tokenizer

import tiktoken
from openai import OpenAI
client = OpenAI()

INPUT_TEXT = "Hello world! Let's tokenize the input and generate an embedding. 3, 2, 1, go."

## tokenize the input string
enc = tiktoken.encoding_for_model("text-embedding-3-large")
tokens = enc.encode(INPUT_TEXT)

## print token string pieces
print("Token strings")
for token in tokens:
    piece = enc.decode_single_token_bytes(token)
    print(token, "\t", piece)

## print the token IDs
print("\nToken IDs:", tokens)

## generate embedding
response = client.embeddings.create(
    model="text-embedding-3-large",
    input=INPUT_TEXT
)

embedding = response.data[0].embedding
print("\nEmbedding dimension: ", len(embedding))
print("\nEmbedding: ", embedding[:10], "...")