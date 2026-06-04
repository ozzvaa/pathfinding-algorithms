from statistics import mean

from Grid_GUI import GUI
from SearchAlgorithms import Grid, Pathfinding

maps = [
    "maps/smile_10_10.json",
    "maps/snail_20_20.json",
    "maps/swirlies_50_50.json",
    "maps/empty_50_70.json",
    "maps/unsolvable_10_10.json",
]

settings_list = [
    {"name": "A*_Manhattan", "use_heuristic": True, "use_manhattan": True},
    {"name": "A*_Euclidean", "use_heuristic": True, "use_manhattan": False},
    {"name": "Dijkstra", "use_heuristic": False, "use_manhattan": True},
]

def get_setting_by_name(name):
    for s in settings_list:
        if s["name"] == name:
            return s
    return None

stats = [] # map - with stats

def run_test(map_path, settings, show=False):
    grid = Grid.load_json(map_path)

    alg = Pathfinding(
        grid,
        diagonals=True,
        use_heuristic=settings["use_heuristic"],
        use_manhattan=settings["use_manhattan"],
    )


    alg.run()

    stats = alg.get_stats()
    stats = {"algorithm": settings["name"], **stats, "solved": alg.solved}
    if show:
        GUI(grid=grid, algorithm=alg).run()
    return stats

def main(show=False):
    for m in maps:
        print(f"\nMAP: {m}")

        for s in settings_list:
            test_results = run_test(m, s, show)

            print(test_results)



def display_res(map_path, settings):
    grid = Grid.load_json(map_path)
    alg = Pathfinding(
        grid,
        diagonals=True,
        use_heuristic=settings["use_heuristic"],
        use_manhattan=settings["use_manhattan"],
    )
    gui = GUI(grid=grid, algorithm=alg)
    gui.run()
    print(alg.get_stats())

if __name__ == "__main__":
    main()
    # mapname = "maps/empty_50_70_sth.json"
    # settings = get_setting_by_name("A*_Manhattan")
    # res = run_test(mapname, settings )
    # print(res)
    # display_res(mapname, settings)

