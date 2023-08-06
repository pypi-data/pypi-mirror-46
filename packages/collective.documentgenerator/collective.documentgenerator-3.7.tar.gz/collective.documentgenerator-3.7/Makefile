#!/usr/bin/make
#
all: run

.PHONY: bootstrap buildout run test cleanall
bootstrap:
	virtualenv-2.7 .
	pip install -r requirements.txt
	./bin/python bootstrap.py --version=2.10.0

buildout:
	if ! test -f bin/buildout;then make bootstrap;fi
	bin/buildout -Nt 5

run:
	if ! test -f bin/instance;then make buildout;fi
	bin/instance fg

test:
	if ! test -f bin/test;then make buildout;fi
	rm -fr htmlcov
	bin/translation-manage -c
	bin/test

cleanall:
	rm -fr develop-eggs htmlcov include .installed.cfg lib .mr.developer.cfg parts downloads eggs
