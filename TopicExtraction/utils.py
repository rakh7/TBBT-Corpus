from nltk.tokenize          import RegexpTokenizer
from stop_words             import get_stop_words
from nltk.stem.porter       import PorterStemmer
from gensim.models.ldamodel import LdaModel
from gensim                 import corpora, models


"""
This method takes list of documents in string format and returns a list of tokens
"""
def tokenize(docs):
	output = []
	for doc in docs:
		tokenizer = RegexpTokenizer(r'\w+')
		output.append(tokenizer.tokenize(doc.lower()))
	return output


"""
This method takes list of words and identifies stop words and removes them from the list
"""
def remove_stop_words(docs):
	output = []
	for doc in docs:
		en_stop = get_stop_words('en')
		stopped_tokens = [i for i in doc if not i in en_stop]
		output.append(stopped_tokens)
	return output


"""
This method takes words in each document and returns its corresponding base word
"""
def lemmatizer(docs):
	output = []
	for doc in docs:
		stemmer = PorterStemmer()
		texts = [stemmer.stem(i) for i in doc]
		output.append(texts)
	return output


"""
This method takes each lemmatized text and generates a document-term matrix
"""
def dt_matrix(terms):
	gen_dict = corpora.Dictionary(terms)
	print(terms)
	corpus = [gen_dict.doc2bow(term) for term in terms]
	print(corpus)
	print(gen_dict.token2id)
	return [corpus, gen_dict]

if __name__ == "__main__":
	doc_a = "Brocolli is good to eat. My brother likes to eat good brocolli, but not my mother."
	doc_b = "My mother spends a lot of time driving my brother around to baseball practice."
	doc_c = "Some health experts suggest that driving may cause increased tension and blood pressure."
	doc_d = "I often feel pressure to perform well at school, but my mother never seems to drive my brother to do better."
	doc_e = "Health professionals say that brocolli is good for your health."
# compile sample documents into a list
	doc_set = [doc_a, doc_b, doc_c, doc_d, doc_e]



	o1 = tokenize(doc_set)
	o2 = remove_stop_words(o1)
	o3 = lemmatizer(o2)
	o4 = dt_matrix(o3)



	#print(o1)
	#print(o2)
	#print(o3)
	#print(o4)

	ldamodel = LdaModel(o4[0], num_topics=3, id2word=o4[1], passes=20)

	print(ldamodel.print_topics(num_topics=3, num_words=3))
	print(ldamodel.show_topics(num_topics=3, num_words=3, log=False, formatted=True))

