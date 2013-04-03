build: sentences sentences_clean stats build_lm

sentences:
	python WikiExtractor.py < cawiki-20130308-pages-meta-current.xml
	python SentenceExtractor.py > Sentences.txt
	touch sentences

sentences_clean:
	python SentenceCleaner.py Sentences.txt > SentencesClean.txt

stats:
	python BuildWordStats.py SentencesClean.txt WordStats
	for filename in $(wildcard WordStats.[0-9]-grams); do \
		sort "$$filename" -o "$$filename"; \
	done;
	python FilterWordStats.py WordStats

build_lm:
	python BuildLanguageModel.py WordStats.filtered catalan.lm

clean:
	rm -rf A[A-Z]
	rm -f Sentences.txt SentencesClean.txt WordStats.*
