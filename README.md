**NOTE: this library is not functional yet**

# Historical normalization

For a list of non-modern spelling variants, the tool can produce an ordered list of the candidate normalizations. The candidates are ordered based on the prediction score of the NMT model.

    from natas import normalize_words
    print(normalize_words(["seacreat", "wiþe"]))
    >> [['secret', 'secrete'], ['with', 'withe', 'wide', 'white', 'way']]

Nothing too interesting to see here yet. This library will be released during the year 2019

sudo pip3 install https://github.com/OpenNMT/OpenNMT-py/archive/0.8.2.zip