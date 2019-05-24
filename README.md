# NATAS

This library will have methods for processing historical English corpora, especially for studying neologisms. The first functionalities to be released relate to normalization of historical spelling and OCR post-correction. This library is maintained by [Mika Hämäläinen](https://mikakalevi.com).

**NOTE: The normalization methods depend on Spacy, which takes some time to load. If you want to speed this up, you can change the Spacy model in use**

## Installation

Note: It is highly recommended to use a virtual environment because of the strict version requirements for dependencies

    sudo pip3 install natas --process-dependency-links --allow-all-external 
    spacy download en_core_web_md #this step is optional, it's only needed if spacy was updated

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

If you use the library, please cite  the following publication

Mika Hämäläinen, Tanja Säily, Jack Rueter, Jörg Tiedemann, and Eetu Mäkelä. 2019. Revisiting NMT for Normalization of Early English Letters. In *Proceedings of the 3rd Joint SIGHUM Workshop on Computational Linguistics for Cultural Heritage, Social Sciences, Humanities and Literature*.
