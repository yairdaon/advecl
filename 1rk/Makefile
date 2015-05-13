1:	str1d.txt
	make clean
	python2.7 eulcl1D.py
str1d.txt: 1d.m
	math -script 1d.m

clean:
	mkdir -p frames
	rm -rvf *.pyc *~ frames/*.* *.mpg *.mp4
	clear

push:
	make clean
	git add -A
	git commit
	git push https://github.com/yairdaon/advecl.git
pull:
	git pull https://github.com/yairdaon/advecl.git