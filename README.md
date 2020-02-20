# NATAS

This library will have methods for processing historical English corpora, especially for studying neologisms. The first functionalities to be released relate to normalization of historical spelling and OCR post-correction. This library is maintained by [Mika Hämäläinen](https://mikakalevi.com).

**NOTE: The normalization methods depend on Spacy, which takes some time to load. If you want to speed this up, you can change the Spacy model in use**

## Installation

Note: It is highly recommended to use a virtual environment because of the strict version requirements for dependencies. The library has been tested with Python 3.6

    pip3 install natas
    python3 -m natas.download
    python3 -m spacy download en_core_web_md

## Historical normalization

For a list of non-modern spelling variants, the tool can produce an ordered list of the candidate normalizations. The candidates are ordered based on the prediction score of the NMT model.

    import natas
    natas.normalize_words(["seacreat", "wiþe"])
    >> [['secret', 'secrete'], ['with', 'withe', 'wide', 'white', 'way']]

Possible keyword arguments are n_best=10, dictionary=None, all_candidates=True, correct_spelling_cache=True. 
- *n_best* sets the number of candidates the NMT will output
- *dictionary* sets a custom dictionary to be used to filter the NMT output (see more in the next section)
- *all_candidates*, if False, the method will return only the topmost normalization candidate (this will improve the speed of the method)
- *correct_spelling_cache*, used only when checking if a candidate word is correctly spelled. Set this to False if you are testing with multiple *dictionaries*.

## OCR post correction

You can use our pretrained model for OCR post correction by doing the following

    import natas
    natas.ocr_correct_words(["paft", "friendlhip"])
    >> [['past', 'pall', 'part', 'part'], ['friendship']]

This will return a list of possible correction candidates in the order of probability according to the NMT model. The same parameters can be used as for historical text normalization.

### Training your own OCR error correction model

You can extract the parallel data for the OCR model if you have an access to a word embeddings model on your OCR data, a list of known correctly spelled words and a vocabulary of the language.

    from natas import ocr_builder
    from natas.normalize import wiktionary
    from gensim.models import Word2Vec

    model = Word2Vec.load("/path/to/your_model.w2v")
    seed_words = set(["logic", "logical"]) #list of correctly spelled words you want to find matching OCR errors for
    dictionary = wiktionary #Lemmas of the English Wiktionary, you will need to change this if working with any other language
    lemmatize = True #Uses Spacy with English model, use natas.set_spacy(nlp) for other models and languages

    results = ocr_builder.extract_parallel(seed_words, model, dictionary=dictionary, lemmatize=lemmatize)
    >> {"logic": {
        "fyle": 5, 
        "ityle": 5, 
        "lofophy": 5, 
        "logick": 1
    }, 
    "logical": {
        "lofophy": 5, 
        "matical": 3, 
        "phical": 3, 
        "praaical": 4, 
        "pracical": 4, 
        "pratical": 4
    }}

The code results in a dictionary of correctly spelled English words (from *seed_words*) and their mapping to semantically similar non-correctly spelled words (not in *dictionary*). Each non-correct word has a [Levenshtein distance](https://en.wikipedia.org/wiki/Levenshtein_distance) calculated with the correctly spelled word. In our paper, we used 3 as the maximum edit distance.

Use the dictionary to make parallel data files for OpenNMT on a character level. This means splitting the words into letters, such as *l o g i c k* -> *l o g i c*. See [their documentation on how to train the model](https://github.com/OpenNMT/OpenNMT-py).

## Check if a word is correctly spelled

You can check whether a word is correctly spelled easily

    import natas
    natas.is_correctly_spelled("cat")
    natas.is_correctly_spelled("ca7")
    >> True
    >> False

This will compare the word with Wiktionary lemmas with and without Spacy lemmatization. The normalization method depends on this step. By default, *natas* uses Spacy's *en_core_web_md* model. To change this model, do the following

    import natas, spacy
    nlp = spacy.load('en')
    natas.set_spacy(nlp)

If you want to replace the Wiktionary dictionary with another one, it can be passed as a keyword argument. Use *set* instead of *list* for a faster look-up. Notice that the models operate on lowercased words.

    import natas
    my_dictionary= set(["hat", "rat"])
    natas.is_correctly_spelled("cat", dictionary=my_dictionary)
    natas.normalize_words(["ratte"], dictionary=my_dictionary)


By default, caching is enabled. If you want to use the method with multiple different parameters, you will need to set *cache=False*.

    import natas
    natas.is_correctly_spelled("cat") #The word is looked up and the result cached
    natas.is_correctly_spelled("cat") #The result will be served from the cache
    natas.is_correctly_spelled("cat", cache=False) #The word will be looked up again

# Cite

If you use the library, please cite one of the following publications depending on whether you used it for normalization or OCR correction.

## Normalization

Mika Hämäläinen, Tanja Säily, Jack Rueter, Jörg Tiedemann, and Eetu Mäkelä. 2019. [Revisiting NMT for Normalization of Early English Letters](https://www.aclweb.org/anthology/papers/W/W19/W19-2509/). In *Proceedings of the 3rd Joint SIGHUM Workshop on Computational Linguistics for Cultural Heritage, Social Sciences, Humanities and Literature*.

    @inproceedings{hamalainen-etal-2019-revisiting,
    title = "Revisiting {NMT} for Normalization of Early {E}nglish Letters",
    author = {H{\"a}m{\"a}l{\"a}inen, Mika  and
      S{\"a}ily, Tanja  and
      Rueter, Jack  and
      Tiedemann, J{\"o}rg  and
      M{\"a}kel{\"a}, Eetu},
    booktitle = "Proceedings of the 3rd Joint {SIGHUM} Workshop on Computational Linguistics for Cultural Heritage, Social Sciences, Humanities and Literature",
    month = jun,
    year = "2019",
    address = "Minneapolis, USA",
    publisher = "Association for Computational Linguistics",
    url = "https://www.aclweb.org/anthology/W19-2509",
    doi = "10.18653/v1/W19-2509",
    pages = "71--75",
    abstract = "This paper studies the use of NMT (neural machine translation) as a normalization method for an early English letter corpus. The corpus has previously been normalized so that only less frequent deviant forms are left out without normalization. This paper discusses different methods for improving the normalization of these deviant forms by using different approaches. Adding features to the training data is found to be unhelpful, but using a lexicographical resource to filter the top candidates produced by the NMT model together with lemmatization improves results.",
    }

## OCR correction

Mika Hämäläinen, and Simon Hengchen. 2019. [From the Paft to the Fiiture: a Fully Automatic NMT and Word Embeddings Method for OCR Post-Correction](https://www.aclweb.org/anthology/R19-1051/). In *the Proceedings of Recent Advances in Natural Language Processing*.

    @inproceedings{hamalainen-hengchen-2019-paft,
    title = "From the Paft to the Fiiture: a Fully Automatic {NMT} and Word Embeddings Method for {OCR} Post-Correction",
    author = {H{\"a}m{\"a}l{\"a}inen, Mika  and
      Hengchen, Simon},
    booktitle = "Proceedings of the International Conference on Recent Advances in Natural Language Processing (RANLP 2019)",
    month = sep,
    year = "2019",
    address = "Varna, Bulgaria",
    publisher = "INCOMA Ltd.",
    url = "https://www.aclweb.org/anthology/R19-1051",
    doi = "10.26615/978-954-452-056-4_051",
    pages = "431--436",
    abstract = "A great deal of historical corpora suffer from errors introduced by the OCR (optical character recognition) methods used in the digitization process. Correcting these errors manually is a time-consuming process and a great part of the automatic approaches have been relying on rules or supervised machine learning. We present a fully automatic unsupervised way of extracting parallel data for training a character-based sequence-to-sequence NMT (neural machine translation) model to conduct OCR error correction.",
    }