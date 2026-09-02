# Tokenization and Embeddings

A language model does not operate directly on raw strings. Text is encoded and tokenized into integer token IDs.

## UTF-8 and bytes

UTF-8 encodes Unicode characters as one or more bytes. A byte contains 8 bits, so there are 256 possible byte values from 0 through 255.

## Byte-level BPE

Byte-level BPE starts from the 256 byte values and learns merge rules from frequent adjacent token pairs. Training learns the vocabulary and merge rules. Encoding applies those learned rules to new text.

## Token IDs

A token ID is an integer index assigned to a token in the tokenizer vocabulary. A token ID is not an embedding vector and is not a probability.

## Embedding lookup

An embedding matrix has shape [vocabulary_size, embedding_dimension]. A token ID selects one row of this matrix. The selected row is the embedding vector for that token.

If a sequence has 3 tokens and the embedding dimension is 4, the embedding tensor has shape [3, 4]. Axis 0 indexes tokens and axis 1 indexes embedding features.
