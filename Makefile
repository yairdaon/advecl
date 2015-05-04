rk:
	make clean
	mkdir -p frames
	mkdir -p frames/rk
	python2.7 pkg/rk.py



euler:
	make clean
	mkdir -p frames
	mkdir -p frames/euler
	python2.7 pkg/euler.py

build7:
	python2.7 advecl/C/setup.py build_ext --inplace
	mv build advecl/C
	mv *.so advecl

build6:
	python2.7 advecl/C/setup.py build_ext --inplace
	mv build advecl/C
	mv *.so advecl

clean:
	rm -rvf build *.pyc frames *.so advecl/C/build advecl/C/*.so	
	rm -rvf *~ tests/*~ pkg/*~ pkg/*.pyc
	clear


tester:
	python2.7 tests/advecl_tests.py

push:
	git push https://github.com/yairdaon/advecl.git
pull:
	git pull https://github.com/yairdaon/advecl.git