TESTS = simplexe nash_equilibrium knapsack subset_sum

test:
	$(foreach test,$(TESTS),python3 -m unittest tests.$(test);)

test_verbose:
	$(foreach test,$(TESTS),python3 -m unittest tests.$(test) -v;)

preview_web:
	mkdir -p web/_output
	cp -ru src web
	cd web; quarto preview

render:
	cp -ru src web
	cd web; quarto render

render_show:
	cp -ru src web
	cd web; quarto render
	xdg-open web/_output/*.pdf