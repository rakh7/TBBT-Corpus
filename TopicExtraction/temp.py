from topic_extractor import LDA

if __name__ =="__main__":
	lda = LDA()

	doc_a = "Sheldon and Leonard’s apartment"
	doc_b = "I’ve been thinking about time travel again."
	doc_c = "Why, did you hit a roadblock with invisibility?"
	doc_d = "Put it on the back burner. Anyway, it occurs to me, if I ever did perfect a time machine, I’d just go into the past and give it to myself, thus eliminating the need for me to invent it in the first place."
	doc_e = "Interesting."
	
	#doc_b = "My mother spends a lot of time driving my brother around to baseball practice."
	#doc_c = "Some health experts suggest that driving may cause increased tension and blood pressure."
	#doc_d = "I often feel pressure to perform well at school, but my mother never seems to drive my brother to do better."
	#doc_e = "Health professionals say that brocolli is good for your health."
# compile sample documents into a list
	doc_set = [doc_d]

	print(lda.get_topic(doc_set))
