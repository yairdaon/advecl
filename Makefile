loc:	rk1.txt rk2.txt rk3.txt
	mkdir -p res
	python test_speed.py res/GPU.txt 1:0 
	python test_speed.py res/CPU.txt 0 


amd:	3Drk1.txt 3Drk2.txt 3Drk3.txt
	mkdir -p res
	python test_speed.py res/cedar.txt 0:0
	python test_speed.py res/tahiti.txt 0:1


locPix:	rk1.txt rk2.txt rk3.txt
	rm -rvf loc/*.* *.mpg *.mp4 
	mkdir -p loc
	python2.7 pix.py 1 1:0 loc 0.001 1000
	ffmpeg -i loc/frame%d.png loc_movie.mpg

amdPix:	rk1.txt rk2.txt rk3.txt
	rm -rvf amd/*.* *.mpg *.mp4 
	mkdir -p amd
	python pix.py 3 0:0 amd 0.0005 1000
	ffmpeg -i amd/frame%d.png amd_movie.mpg	

pure:	pure/*.png
	rm -rvf pure/*.* *.mpg *.mp4 
	mkdir -p pure
	python2.7 pure.py 

clean:
	mkdir -p frames
	rm -rvf *.pyc *~ frames/*.* *.mpg *.mp4  pdf/*.aux pdf/*.log pdf/*.pdf pdf/*.backup tmp_ker*
	clear


# Create time step strings
strings:
	math -script rk2d.m
	math -script rk3d.m

rk1.txt:rk2d.m
	rm -rvf rk1.txt rk2.txt rk3.txt
	math -script rk2xd.m
rk2.txt:rk2d.m
	rm -rvf rk1.txt rk2.txt rk3.txt
	math -script rk2d.m
rk3.txt:rk2d.m
	rm -rvf rk1.txt rk2.txt rk3.txt
	math -script rk2d.m


3Drk1.txt:rk3d.m
	rm -rvf 3Drk1.txt 3Drk2.txt 3Drk3.txt
	math -script rk3d.m
3Drk2.txt:rk3d.m
	rm -rvf 3Drk1.txt 3Drk2.txt 3Drk3.txt
	math -script rk3d.m
3Drk3.txt:rk3d.m
	rm -rvf 3Drk1.txt 3Drk2.txt 3Drk3.txt
	math -script rk3d.m