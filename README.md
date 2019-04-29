This library will have methods for processing historical English corpora, especially for studying neologisms. The first functionalities to be released relate to normalization of historical spelling and OCR post-correction.

**NOTE: The normalization methods depend on Spacy, which takes some time to load. If you want to speed this up, you can change the Spacy model in use**

**NOTE: this library is not functional yet**

## Historical normalization

For a list of non-modern spelling variants, the tool can produce an ordered list of the candidate normalizations. The candidates are ordered based on the prediction score of the NMT model.

    import natas
    print(natas.normalize_words(["seacreat", "wiþe"]))
    >> [['secret', 'secrete'], ['with', 'withe', 'wide', 'white', 'way']]

Possible keyword arguments are n_best=10, dictionary=None, all_candidates=True. 
- *n_best* sets the number of candidates the NMT will output
- *dictionary* sets a custom dictionary to be used to filter the NMT output (see more in the next section)
- *all_candidates*, if False, the method will return only the top first normalization candidate (this will improve the speed of the method)

## Check if a word is correctly spelled

You can check whether a word is correctly spelled easily

    import natas
    print(natas.is_correctly_spelled("cat"))
    print(natas.is_correctly_spelled("ca7"))
    >> True
    >> False

This will compare the word with Wiktionary lemmas with and without Spacy lemmatization. The normalization method depends on this step. By default, *natas* uses Spacy's *en_core_web_md* model. To change this model, do the following

    import natas, spacy
    nlp = spacy.load('en')
    natas.set_spacy(nlp)

If you want to replace the Wiktionary dictionary with another one, it can be passed as a keyword argument. Notice that the models operate on lowercased words.

    import natas
    my_dictionary=["hat", "rat"]
    natas.is_correctly_spelled("cat", dictionary=my_dictionary)
    natas.normalize_words(["ratte"], dictionary=my_dictionary)



sudo pip3 install https://github.com/OpenNMT/OpenNMT-py/archive/0.8.2.zip