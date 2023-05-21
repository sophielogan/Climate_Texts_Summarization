import gensim
from gensim.utils import simple_preprocess
import nltk
nltk.download('stopwords')
from nltk.corpus import stopwords
import gensim.corpora as corpora
from pprint import pprint
import string

stop_words = stopwords.words('english')
stop_words.extend(['from', 'subject', 're', 'edu', 'use'])

def sent_to_words(sentences):
    for sentence in sentences:
        # deacc=True removes punctuations
        yield(gensim.utils.simple_preprocess(str(sentence), deacc=True))

def remove_stopwords(texts):
    return [[word for word in simple_preprocess(str(doc)) if word not in stop_words] for doc in texts]

def text_topics(data, col, num_topics=10):
  
  data = data[col].values.tolist()
  data_words = list(sent_to_words(data))
  
  # remove stop words
  data_words = remove_stopwords(data_words)

  # Create Dictionary
  id2word = corpora.Dictionary(data_words)
  
  # Create Corpus
  texts = data_words
  
  # Term Document Frequency
  corpus = [id2word.doc2bow(text) for text in texts]

  # Build LDA model
  lda_model = gensim.models.LdaMulticore(corpus=corpus,
                                        id2word=id2word,
                                        num_topics=num_topics)
  # Print the Keyword in the 10 topics
  print(lda_model.print_topics())
  doc_lda = lda_model[corpus]
  
  return doc_lda
