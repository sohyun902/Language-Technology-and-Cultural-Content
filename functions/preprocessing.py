from konlpy.tag import Okt

okt=Okt()

#띄어쓰기
def space(sent):
  sents_pos = okt.pos(sent)
  new_sent = ""
  for word_pos in sents_pos:
      if word_pos[1] in ['Josa', 'PreEomi', 'Eomi', 'Suffix', 'Punctuation']:
          new_sent = new_sent + word_pos[0]
      else:
          new_sent = new_sent + " "+word_pos[0]
  return new_sent

#불용어 제거
def clean_korean_documents(sents):
    for i, document in enumerate(sents):
        clean_words = []
        for word in okt.pos(document, stem=True): 
            if word[1] in ['Noun', 'Verb', 'Adjective']: 
                clean_words.append(word[0])
        sent = ' '.join(clean_words)
        sents[i] = sent

    f = open('../stopword_ko.txt', 'r', encoding='utf8')
    stopwords_ko = f.readlines()
    
    for i, sent in enumerate(sents):
        clean_words = []
        doc=sent.split(" ") 
        for word in doc: 
            if word not in stopwords_ko: 
                clean_words.append(word)
        sent = ' '.join(clean_words)
        sents[i] = sent

    return sents