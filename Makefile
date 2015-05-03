build7:
	python2.7 advecl/C/setup.py build_ext --inplace
	mv build advecl/C
	mv *.so advecl

build6:
	python2.7 advecl/C/setup.py build_ext --inplace
	mv build advecl/C
	mv *.so advecl

clean:
	rm -rvf advecl/C/build
	rm -vf advecl/C/*.so	
	rm -vf *.so
	rm -rvf build
	rm -vf advecl*.so
	rm -rvf *~ tests/*~ advecl/*~


tester:
	python2.7 tests/advecl_tests.py

push:
	git push https://github.com/yairdaon/advecl.git
pull:
	git pull https://github.com/yairdaon/advecl.git