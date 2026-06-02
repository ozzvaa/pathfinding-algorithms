from Grid_GUI import GUI
from SearchAlgorithms import A_star



gui = GUI()

gui.grid.set_start(gui.grid[0, 0])
gui.grid.set_finish(gui.grid[0, 5])


gui.run()