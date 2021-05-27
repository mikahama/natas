from natas import ocr_builder
from mikatools import *
#from gensim.models import Word2Vec
#from gensim.models.keyedvectors import Word2VecKeyedVectors
import natas

print(natas.normalize_words(["seacreat", "wiþe"], n_best=5))
print(natas.ocr_correct_words(["paft", "friendlhip"]))

#print(natas.is_correctly_spelled("cat"))
#print(natas.is_correctly_spelled("ca7"))

#model = Word2Vec.load("/Users/mikahama/Downloads/models/model_fi_1820-1917.w2v")
#model = Word2VecKeyedVectors.load_word2vec_format("/mnt/c/Users/Mika/Downloads/enwiki_20180420_100d.txt")
#print("ok")
#seed_words = set(json_load("natas/wiktionary_lemmas.json"))
#print("ok")
#res = ocr_builder.extract_parallel(seed_words, model, dictionary=seed_words, lemmatize=False, use_freq=False)
#json_dump(res, "test.json")

