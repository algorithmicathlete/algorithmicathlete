from draw_bracket import BracketDrawer
from simulation import run
from plots import stacked_bar, pie_chart

SIMULATIONS = 100_000
if __name__ == '__main__':
    appearances, total_upsets, perfect_brackets, upset_bracket = run(SIMULATIONS)

    print("Average # of upsets:", total_upsets/SIMULATIONS)
    print("Most upsets:", upset_bracket['count'])
    print("Perfect Brackets (no upsets):", perfect_brackets)

    bd = BracketDrawer(upset_bracket["history"], *upset_bracket["final_four"])
    im = bd.draw_bracket()
    im.show()

    stacked_bar(appearances)
    pie_chart(appearances)