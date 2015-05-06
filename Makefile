cl:
	make clean
	python2.7 pycl/eulcl.py

py:
	make clean


	python2.7 pure_py/rk.py
	python2.7 pure_py/euler.py

clean:
	mkdir -p frames
	mkdir -p frames/euler
	mkdir -p frames/rk
	rm -rvf build *.pyc  *.so advecl/C/build advecl/C/*.so *~ tests/*~ pkg/*~ pkg/*.pyc  frames/euler/* frames/rk/*
	clear


tester:
	python2.7 tests/advecl_tests.py

push:
	make clean
	git add -A
	git commit
	git push https://github.com/yairdaon/advecl.git
pull:
	git pull https://github.com/yairdaon/advecl.git
