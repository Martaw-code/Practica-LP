make:
	python3 jsbach.py test-HalloBach.jsb

gramatica:
	java -cp "/usr/local/lib/antlr-4.9-complete.jar:$CLASSPATH" org.antlr.v4.Tool -Dlanguage=Python3 -no-listener -visitor jsbach.g4


joc1:
	python3 jsbach.py test-HalloBach.jsb
joc2:
	python3 jsbach.py test-mcdEuclides.jsb
joc3:
	python3 jsbach.py test-TorresDeHanoi.jsb
joc4:
	python3 jsbach.py test-4OctaveScale.jsb
joc5:
	python3 jsbach.py test-VarisExemples.jsb


clean:
	rm -f jsbachVisitor.*
	rm -f jsbachParser.*
	rm -f jsbachLexer.*
	rm -f *.interp
	rm -f *.tokens
	rm -f .output.wav.icloud
	rm -f *.wav
	rm -f *.midi
	rm -f *.pdf
	rm -f *.mp3
	rm -f *.lily
