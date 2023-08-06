'''
Library for reading word vector files (text or binary)
@Python3
'''
import numpy
import codecs

from .common import *
from . import word2vec
from . import glove
from .glove import GloveMode

name = 'pyemblib'
version = '0.1.2'


class Embeddings(dict):
    '''Wrapper for word embeddings; inherits from Dictionary.
    Keys are words, values are embedding arrays.
    '''
    @property
    def size(self):
        if not hasattr(self, '_size'):
            for any_vector in self.values():
                break
            self._size = len(any_vector)
        return self._size
    @property
    def dimension(self):
        return self.size
    @property
    def shape(self):
        return (len(self), self.size)

    def has(self, key):
        return not self.get(key, None) is None

    def toarray(self, ordered=False):
        '''Returns the embedding vocabulary in fixed order and
        a NumPy array of the embeddings, in vocab order.
        '''
        if ordered:
            vocab = list(self.keys())
            vocab.sort()
            vocab = tuple(vocab)
        else:
            vocab = tuple(self.keys())
        embed_array = []
        for v in vocab: embed_array.append(self[v])
        return (vocab, numpy.array(embed_array))


def read(fname, format=Format.Word2Vec, size_only=False, lower_keys=False, **kwargs):
    '''Returns Embeddings instance mapping words/keys to embedding vectors

    Parameters
       fname               :: name of embedding file to read
       mode                :: pyemblib.Mode indicator (text or binary format)
       size_only           :: if True, only reads the size of the embeddings and stops
       first_n             :: only read the first n embeddings
       separator           :: character separating the key from the embedding vector
       filter_to           :: only return embeddings whose keys are in this list
       lower_keys          :: lowercase all keys before returning
       errors              :: flag passed to UTF-8 decoding
       skip_parsing_errors :: if True, prints a warning message when a line fails
                              to parse, but continues reading; default behavior
                              aborts on parsing error

    DEPRECATED PARAMETERS
       replace_errors :: if True, uses utf-8 decoding flag "replace"
    '''
    if format == Format.Word2Vec:
        output = word2vec.read(fname, size_only=size_only, lower_keys=lower_keys, **kwargs)
    elif format == Format.Glove:
        output = glove.read(fname, size_only=size_only, **kwargs)

    if size_only:
        return output
    else:
        (words, vectors) = output

        wordmap = Embeddings()
        for i in range(len(words)):
            if lower_keys: key = words[i].lower()
            else: key = words[i]
            wordmap[key] = vectors[i]
        return wordmap
    
def load(*args, **kwargs):
    '''Alias for read'''
    return read(*args, **kwargs)

def getSize(fname, format=Format.Word2Vec, **kwargs):
    '''Gets (vocab size, # of dimensions) for an embedding file
    '''
    return read(fname, size_only=True, format=format, **kwargs)

def write(embeds, fname, format=Format.Word2Vec, **kwargs):
    '''Writes a dictionary of embeddings { term : embed}
    to a file, in the format specified.
    '''
    if format == Format.Word2Vec:
        word2vec.write(embeds, fname, **kwargs)
    else:
        return NotImplemented

def readVocab(fname, format=Format.Word2Vec, **kwargs):
    '''Gets the set of words embedded in the given file
    '''
    embs = read(fname, format=format, **kwargs)
    return set(embs.keys())

def listVocab(embeds, fname):
    '''Writes the vocabulary of an embedding to a file,
    one entry per line.
    '''
    with open(fname, 'wb') as stream:
        for k in embeds.keys():
            stream.write(k.encode('utf-8'))
            stream.write(b'\n')

def closestNeighbor(query, embedding_array, normed=False, top_k=1):
    '''Gets the index of the closest neighbor of embedding_array
    to the query point.  Distance metric is cosine.

    SLOW. DO NOT USE THIS FOR RAPID COMPUTATION.
    '''
    embedding_array = numpy.array(embedding_array)
    if not normed:
        embedding_array = numpy.array([
            (embedding_array[i] / numpy.linalg.norm(embedding_array[i]))
                for i in range(embedding_array.shape[0])
        ])

    ## assuming embeddings are unit-normed by this point;
    ## norm(query) is a constant factor, so we can ignore it
    dists = numpy.array([
        numpy.dot(query, embedding_array[i])
            for i in range(embedding_array.shape[0])
    ])
    sorted_ixes = numpy.argsort(-1 * dists)
    return sorted_ixes[:top_k]

def unitNorm(embeds):
    for (k, embed) in embeds.items():
        embeds[k] = numpy.array(
            embed / numpy.linalg.norm(embed)
        )

def analogyQuery(embeds, a, b, c):
    return (
        numpy.array(embeds[b])
        - numpy.array(embeds[a])
        + numpy.array(embeds[c])
    )


class NearestNeighbors:
    '''Used to get nearest embeddings to a query by cosine distance.
    '''
    
    def __init__(self, embeds):
        e = embeds.copy()
        unitNorm(e)

        vocab = tuple(embeds.keys())
        embed_array = []
        for v in vocab:
            embed_array.append(embeds[v])
        self._vocab = numpy.array(vocab)
        self._embed_array = numpy.transpose(numpy.array(embed_array))

    def nearest(self, query, k=1):
        indices = numpy.argsort(
            numpy.matmul(
                numpy.array(query),
                self._embed_array
            )
        )
        rev_sort_keys = self._vocab[indices][::-1]
        if k is None: return rev_sort_keys
        else: return rev_sort_keys[1:k+1]
