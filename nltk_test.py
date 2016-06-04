from nltk.corpus import wordnet as wn
import itertools
import sys

for i,j in enumerate(wn.synsets(sys.argv[1])):                                                       
        print("meaning ",i)
        print("definition ",j.definition())                                                           
        print("synonyms ",",".join(j.lemma_names()))                                                  
        print("hypernyms ",",".join(list(itertools.chain(*[l.lemma_names() for l in j.hypernyms()]))))
        print("hyponyms ",",".join(list(itertools.chain(*[l.lemma_names() for l in j.hyponyms()]))))
