TESTS = simplexe nash_equilibrium knapsack subset_sum

test:
	$(foreach test,$(TESTS),python3 -m unittest tests.$(test);)

test_verbose:
	$(foreach test,$(TESTS),python3 -m unittest tests.$(test) -v;)


render:
	mkdir -p web/_output
	cp -ru src web
	cp -ru tests web
	cd web; quarto render

update_web: render
	rm -rf docs
	mkdir -p docs
	cp -r web/_output/* docs

preview_web:
	mkdir -p web/_output
	cp -ru src web
	cp -ru tests web
	cd web; quarto preview

preview_pdf: render
	xdg-open web/_output/*.pdf

update_gamut:
	java -jar gamut.jar -g SymmetricTwoByTwo -f baked_gamut/2x2_Symmetric_Games.txt
	java -jar gamut.jar -g BattleOfTheSexes -f baked_gamut/battle_of_the_sexes_game.txt
	java -jar gamut.jar -g PrisonersDilemma -f baked_gamut/prisoners_dilemma_game.txt
	java -jar gamut.jar -g Chicken -f baked_gamut/chicken_game.txt
	java -jar gamut.jar -g GrabTheDollar -actions 10 -f baked_gamut/grab_the_dollar_game.txt