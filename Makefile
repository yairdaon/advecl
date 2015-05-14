local:	rk1.txt rk2.txt rk3.txt
	mkdir -p res
	python test_speed.py res/CPU.txt 0
	python test_speed.py res/GPU.txt 1:0


amd:	rk1.txt rk2.txt rk3.txt
	mkdir -p res
	python test_speed.py res/cedar.txt 0:0
	python test_speed.py res/tahiti.txt 0:1

locPix:	rk1.txt rk2.txt rk3.txt
	rm -rvf frames/*.* *.mpg *.mp4 
	python2.7 pix.py 2 1:0
	ffmpeg

amdPix:	rk1.txt rk2.txt rk3.txt
	rm -rvf frames/*.* *.mpg *.mp4 
	python pix.py 2 0:0

clean:
	mkdir -p frames
	rm -rvf *.pyc *~ frames/*.* *.mpg *.mp4 res/*.* *.txt pdf/*.aux pdf/*.log pdf/*.pdf pdf/*.backup tmp_ker*
	clear


# Create time step strings
strings:
	math -script rk2d.m

rk1.txt:rk2d.m
	rm -rvf rk1.txt rk2.txt rk3.txt
	math -script rk2d.m
rk2.txt:rk2d.m
	rm -rvf rk1.txt rk2.txt rk3.txt
	math -script rk2d.m
rk3.txt:rk2d.m
	rm -rvf rk1.txt rk2.txt rk3.txt
	math -script rk2d.m