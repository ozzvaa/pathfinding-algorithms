from Grid_GUI import GUI
from Grid import Grid
from SearchAlgorithms import Pathfinding


grid = Grid.load_json("map1.json")
gui = GUI(grid=grid)


gui.run()

gui.grid.save_json("last_map.json")