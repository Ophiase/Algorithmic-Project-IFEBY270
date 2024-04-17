TESTS = simplexe nash_equilibrium

test:
	$(foreach test,$(TESTS),python3 -m unittest tests.$(test);)

test_verbose:
	$(foreach test,$(TESTS),python3 -m unittest tests.$(test) -v;)

preview_web:
	mkdir -p web/_output
	cp -r src web
	cd web; quarto preview