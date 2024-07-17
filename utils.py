def load_lexicon(path):
    import gzip
    dictionary={}
    for line in gzip.open(path,'rb'):
        word,category=line.decode('utf8').strip().split('\t')
        dictionary[word]=category
    return dictionary

import re
re_tokenize=re.compile(r'[a-zšđčćž]+')
dali_re=re.compile(r'\b(da li|dal)\b')
jeli_re=re.compile(r'\b(je li|jel)\b')

def tokenize(text):
    return re_tokenize.findall(text)

def count(text,lexicon,verbose=False):
    from collections import Counter
    events={}
    for token in tokenize(text.lower()):
        if token in lexicon:
            if lexicon[token] not in events:
                events[lexicon[token]]=[]
            events[lexicon[token]].append(token)
    if verbose:
        return {'stats':[(k,len(events[k])) for k in events],'events':events}
    else:
        return [(k,len(events[k])) for k in events]

def dalijeli(text,verbose):
    dali=dali_re.findall(text)
    jeli=jeli_re.findall(text)
    events={'dali':dali,'jeli':jeli}
    if verbose:
        return {'stats':[(k,len(events[k])) for k in events],'events':events}
    else:
        return [(k,len(events[k])) for k in events]

lexicons={'e:je':'lexicons/yat-lexicon.gz','rdrop':'lexicons/rdrop-lexicon.gz','k:h':'lexicons/kh-lexicon.gz','hdrop':'lexicons/hdrop-lexicon.gz','sto:sta':'lexicons/stosta-lexicon.gz'}
functions={'dali:jeli':dalijeli}


def call_function(function,text,verbose=False):
    if function in lexicons:
        lexicon=load_lexicon(lexicons[function])
        return count(text,lexicon,verbose)
    elif function in functions:
        return functions[function](text,verbose)

