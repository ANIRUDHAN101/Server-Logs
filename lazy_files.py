#%%
import mmap
import os
NO_THREADS = 12

def get_chunk_files(file: str, NO_THREADS: int, memap=False) -> list:
    
    if not memap:
        file = file.readlines()
        
    file_size = file.size()
    chunk_size = file_size // NO_THREADS
    chunk_index = [i for i in range(0, file_size, chunk_size)]

    # # is the last chunk size is not divisible by NO_THREADS
    # # then add that chunk to the previous chunk to maintain 
    # # the no of chunks and not to miss any data
    chunk_index[-1] = file_size

    # # update the indexes for ewch lines
    # # for simplicity the indexex are moded to the right if the current 
    # # index if not the end of a line
    for i, index in enumerate(chunk_index):
        if chr(file[index-1]) != '\n':
            while chr(file[index-1]) != '\n':
                index += 1
            chunk_index[i] = index
     
    return chunk_index

# %%
