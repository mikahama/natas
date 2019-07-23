from natas import ocr_builder
from mikatools import *
from gensim.models import Word2Vec
#print(natas.normalize_words(["seacreat", "wiþe", "Dogge"]))

#print(natas.is_correctly_spelled("cat"))
#print(natas.is_correctly_spelled("ca7"))

model = Word2Vec.load("/Users/mikahama/Downloads/models/model_fi_1820-1917.w2v")
seed_words = set(open_read("words-in-dictionary").read().split("\n"))
res = ocr_builder.extract_parallel(seed_words, model, dictionary=seed_words, lemmatize=False, use_freq=False)
json_dump(res, "fin_parallel.json")