TESTS = simplexe nash_equilibrium knapsack subset_sum

test:
	$(foreach test,$(TESTS),python3 -m unittest tests.$(test);)

test_verbose:
	$(foreach test,$(TESTS),python3 -m unittest tests.$(test) -v;)

preview_web:
	mkdir -p web/_output
	cp -ru src web
	cp -ru tests web
	cd web; quarto preview

render:
	cp -ru src web
	cp -ru tests web
	cd web; quarto render

render_show:
	cp -ru src web
	cp -ru tests web
	cd web; quarto render
	xdg-open web/_output/*.pdf

update_gamut:
	java -jar gamut.jar -g SymmetricTwoByTwo -f baked_gamut/2x2_Symmetric_Games.txt
	java -jar gamut.jar -g PrisonersDilemma -f baked_gamut/prisoners_dilemma_game.txt
	java -jar gamut.jar -g Chicken -f baked_gamut/chicken_game.txt
    #java -jar gamut.jar -g CoordinationGame -p 2 -f baked_gamut/coordination_game.txt
    #java -jar gamut.jar -g BattleOfTheSexes -f baked_gamut/battle_of_the_sexes_game.txt
    #java -jar gamut.jar -g BertrandOligopoly -p 2 -a 2 -f baked_gamut/bertrand_oligopoly_game.txt
    #java -jar gamut.jar -g MajorityVoting -p 4 -f baked_gamut/majority_voting_game.txt
    #java -jar gamut.jar -g TravelersDilemma -p 2 -f baked_gamut/travelers_dilemma_game.txt
    #java -jar gamut.jar -g TwoByTwoGame -type 1 -f baked_gamut/two_by_two_game.txt
    #java -jar gamut.jar -g AsymmetricTwoByTwo -p 2 -o baked_gamut/asymmetric_two_by_two_game.txt
    #java -jar gamut.jar -g NPlayerSymmetric -p 2 -o baked_gamut/n_player_symmetric_game.txt
    #java -jar gamut.jar -g NPlayerAsymmetric -p 2 -o baked_gamut/n_player_asymmetric_game.txt
    #java -jar gamut.jar -g NPlayerRepeatedGame -p 2 -t 5 -o baked_gamut/n_player_repeated_game.txt
    #java -jar gamut.jar -g GraphicalGame -n 2 -o baked_gamut/graphical_game.txt
    #java -jar gamut.jar -g RandomGraphicalGame -n 2 -m 3 -o baked_gamut/random_graphical_game.txt

