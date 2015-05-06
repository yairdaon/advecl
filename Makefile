cl:
	make clean
	mkdir -p frames
	mkdir -p frames/cl
	python2.7 pkg/eulcl.py

py:
	make clean
	mkdir -p frames
	mkdir -p frames/euler
	mkdir -p frames/rk

	python2.7 pure_py/rk.py
	python2.7 pure_py/euler.py

clean:
	rm -rvf build *.pyc frames *.so advecl/C/build advecl/C/*.so	
	rm -rvf *~ tests/*~ pkg/*~ pkg/*.pyc
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
