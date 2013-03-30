build:
	python WikiExtractor.py < cawiki-20130308-pages-meta-current.xml
	python SentenceExtractor.py > Sentences.txt

clean:
	rm -rf A[A-Z]
	rm -f Sentences.txt
