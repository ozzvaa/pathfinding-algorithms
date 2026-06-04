from Grid_GUI import GUI
from Grid import Grid
from SearchAlgorithms import Pathfinding


grid = Grid.load_json("maps/smile_10_10.json")
grid = Grid.load_json("maps/snail_20_20.json")
grid = Grid.load_json("maps/swirlies_50_50.json")
grid = Grid.load_json("maps/empty_50_70.json")


# gui = GUI(grid=grid)
gui = GUI(rows=2, cols=2)
gui.run()

gui.grid.save_json("./maps/test.json")