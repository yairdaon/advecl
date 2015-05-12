2:	str2d.txt
	make clean
	python2.7 eulcl2D.py
str2d.txt: 2d.m
	rm -rvf str2d.txt
	math -script 2d.m

movie:
	rm -rvf frames/*.*
	python2.7 movie.py
clean:
	mkdir -p frames
	mkdir -p data
	rm -rvf *.pyc *~ frames/*.* data/*.* *.mpg *.mp4 
	clear
