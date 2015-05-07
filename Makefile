cl:
	make clean
	python2.7 eulcl.py
clean:
	mkdir -p frames
	mkdir -p frames/euler
	mkdir -p frames/rk
	rm -rvf *.pyc *~ frames/*.* *.mpg *.mp4
	clear

push:
	make clean
	git add -A
	git commit
	git push https://github.com/yairdaon/advecl.git
pull:
	git pull https://github.com/yairdaon/advecl.git
