
"""
    Takes a long string as input and returns an array of shorter strings 
    that do not exceed the 'max_length'. The script also tries to break 
    the text where sentences end. 

    chunk_text()
"""

# import libs
import math


def break_sentence(sentence, max_length):

    # sentence is valid
    if len(sentence) < max_length: return [sentence]

    # break into words
    words = [word for word in sentence.split(' ') if len(word) > 0]

    # need to break
    nbr_of_breaks = math.ceil( len(sentence) / (1.0 * max_length) )

    # compute number of words per chunk
    nbr_words_per_chunk = len(words) / (1.0 * nbr_of_breaks)

    # init
    chunk = []
    chunks = []

    for i in range(0, len(words)):

        # select word
        word = words[i]

        # append
        chunk.append(word)

        # if chunk is full
        if len(chunk) >= nbr_words_per_chunk:
            
            # append chunk
            chunks.append(chunk)

            # reset
            chunk = []

    # append last 
    if len(chunk):
        chunks.append(chunk)
        
    # convert to string
    chunks = [' '.join(chunk) for chunk in chunks]

    return chunks


def chunk_text(text, max_length, LOG=False):
    
    # init variables
    dataframe = []

    # split input text into words
    sentences = [datum.strip() for datum in text.split('.') if len(datum) > 0]

    # convert too-long sentences to smaller
    for i, sentence in enumerate(sentences):

        # chunk
        chunks = break_sentence(sentence, max_length)

        # append
        for chunk in chunks:
            dataframe.append(chunk)
            
    # init variables
    chunk = []
    chunks = []
    total_nbr_of_chars = 0

    # chunk text
    for i in range(0, len(dataframe)):

        # extract the sentence
        datum = dataframe[i]

        # count how many characters
        nbr_of_chars = len(datum)

        # check if the carriage is full
        if total_nbr_of_chars + nbr_of_chars > max_length:

            # append chunk
            chunks.append(chunk)

            # reset variables
            total_nbr_of_chars = 0
            chunk = []

        # append to chunk
        chunk.append(datum)

        # increment
        total_nbr_of_chars += nbr_of_chars

    # append last chunk
    if len(chunk) > 0:
        chunks.append(chunk)

    # convert each chunk to string
    chunks = ['.'.join(chunk) for chunk in chunks]

    # log
    if LOG:
        print(f'INFO: Text was split into {len(chunks)} chunks')

    return chunks
