
.PHONY: clean clean_all develop build_ext_inplace

develop: clean
	pip install -e .[dev]

build_ext_inplace:
	python setup.py build_ext --inplace

clean:
	rm -rf build

clean_so:
	find fluidimage -name "*.so" -delete

cleanall: clean clean_so

black:
	black -l 82 fluidimage try

tests:
	OMP_NUM_THREADS=1 pytest

_tests_coverage:
	mkdir -p .coverage
	OMP_NUM_THREADS=1 coverage run -p -m pytest

_report_coverage:
	coverage combine
	coverage report
	coverage html
	coverage xml
	@echo "Code coverage analysis complete. View detailed report:"
	@echo "file://${PWD}/.coverage/index.html"

coverage: _tests_coverage _report_coverage
