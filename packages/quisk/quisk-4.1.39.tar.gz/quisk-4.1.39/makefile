
all:
	python setup.py build_ext --force --inplace
	@echo
	@echo 'Use "make soapy" to make the soapy module'

soapy:
	(cd soapypkg; make)

macports:
	env ARCHFLAGS="-arch x86_64" python setup.py build_ext --force --inplace -D USE_MACPORTS
