import numpy as np
from tkinter import *
from PIL import Image, ImageTk
from tkinter import font as font


class Maze:
    maze = None
    __walls = None
    __start = None # name of the room
    __goal = None # name of the room
    __search_algorithm = None

    def __init__(self):
        self.maze = np.array([
            ['A', 'B', 'C'],
            ['D', 'E', 'F'],
            ['G', 'H', 'I']
        ])
        self.__walls = {
            "AB": False,
            "AD": False,
            "BC": False,
            "BE": False,
            "CF": False,
            "DE": False,
            "DG": False,
            "EF": False,
            "EH": False,
            "FI": False,
            "GH": False,
            "HI": False
        }
        self.__start = ""
        self.__goal = ""
        self.__search_algorithm = ""

    def set_start(self, start: str):
        self.__start = start

    def set_goal(self, goal: str):
        self.__goal = goal

    def set_search_algorithm(self, search_algorithm):
        self.__search_algorithm = search_algorithm

    def get_start(self):
        return self.__start

    def get_goal(self):
        return self.__goal

    def get_search_algorithm(self):
        return self.__search_algorithm

    def get_walls(self):
        return self.__walls

    def set_walls(self, wall_edges):
        for wall in wall_edges:
            wall_set = wall[0] + wall[2]
            self.__walls[wall_set] = True

    def coordinate(self, l: str):
        """
            Returns the coordinates of a room in ndarray
        """
        for i in range(3):
            for j in range(3):
                if self.maze[i][j] == l:
                    c = (i, j)
                    return c

    def room_name(self, t):
        return self.maze[t[0]][t[1]]

    def neighbors(self, c_room: str):
        """Looks the neighbor rooms of the current room and if there is no wall between them, adds to the dictionary
        :param c_room: room that's neighbors will be found
        :return: dictionary that has the room names as key and cost to reach them as value
        """
        n_dict = {}
        c_coordinate = self.coordinate(c_room)  # coordinates of the current room
        # look up
        if c_coordinate[0] != 0:
            up_room = self.maze[c_coordinate[0] - 1][c_coordinate[1]]
            try:
                if self.__walls[up_room + c_room] is False:
                    n_dict[up_room] = 1
            except KeyError:
                if self.__walls[c_room + up_room] is False:
                    n_dict[up_room] = 1
        # look down
        if c_coordinate[0] != 2:
            down_room = self.maze[c_coordinate[0] + 1][c_coordinate[1]]
            try:
                if self.__walls[down_room + c_room] is False:
                    n_dict[down_room] = 1
            except KeyError:
                if self.__walls[c_room + down_room] is False:
                    n_dict[down_room] = 1
        # look right
        if c_coordinate[1] != 2:
            right_room = self.maze[c_coordinate[0]][c_coordinate[1] + 1]
            try:
                if self.__walls[c_room + right_room] is False:
                    n_dict[right_room] = 2
            except KeyError:
                if self.__walls[right_room + c_room] is False:
                    n_dict[right_room] = 2
        # look left
        if c_coordinate[1] != 0:
            left_room = self.maze[c_coordinate[0]][c_coordinate[1] - 1]
            try:
                if self.__walls[c_room + left_room] is False:
                    n_dict[left_room] = 2
            except KeyError:
                if self.__walls[left_room + c_room] is False:
                    n_dict[left_room] = 2
        return n_dict

    def __str__(self):
        """
        :return: the image of the maze as string
        """
        maze_str = ""
        for i in range(3):
            for j in range(3):
                maze_str = maze_str + "\t" + self.maze[i][j] + "\t"

                if j != 2:
                    neighbor_wall = self.maze[i][j] + self.maze[i][j + 1]
                    if self.__walls[neighbor_wall] is True:
                        maze_str = maze_str + "|"

            maze_str += "\n"
            for j in range(3):
                if i != 2:
                    neighbor_wall = self.maze[i][j] + self.maze[i + 1][j]

                    if self.__walls[neighbor_wall] is True:
                        maze_str += "   ___\t"
                    else:
                        maze_str += "    \t"

            maze_str += "\n\n"

        return maze_str


class Frontier:
    """
        A sorted list that holds tuple(path, cost)
    """
    __frontier = None
    __size = None

    def __init__(self):
        self.__frontier = []
        self.__size = 0

    def get_size(self):
        return self.__size

    def add_path(self, path_tuple: tuple):
        self.__frontier.append(path_tuple)
        self.__size += 1

    def sort_frontier(self):
        """
        Sort the frontier considering the cost of the paths (second element in tuples)
        if same, then sort by alphabetic order

        length of the paths might also be considered for sorting
        """
        self.__frontier.sort(key=lambda tup: tup[1])
        if self.__size >= 2:
            if self.__frontier[0][1] == self.__frontier[1][1] and self.__frontier[0][0][-1:] > self.__frontier[1][0][-1:]:
                tmp_tuple = self.__frontier[0]
                self.__frontier[0] = self.__frontier[1]
                self.__frontier[1] = tmp_tuple

    def remove_path(self):
        """
        Remove the first element (lowest cost) from frontier
        :return: Removed item
        """
        if self.__size == 0:
            print("Fringe is already empty")
            return False
        else:
            self.__size -= 1
            return self.__frontier.pop(0)

    def get_frontier_information(self):
        """
        :return: string that contains the frontier elements
        """
        fringe_str = ""
        for i in range(self.__size):
            fringe_str += "{:<8s} ({:d})\n".format(self.__frontier[i][0], self.__frontier[i][1])
        return fringe_str


class Uniform_Cost_Search:
    __start = None # coordinate tuple
    __goal = None  # coordinates from maze ndarray
    __maze = None
    __frontier = None
    __solution = None
    __expanded_path = None
    __expanded_cost = None
    __expanded_room = None

    def __init__(self, start_room: str, goal_room: str, m: Maze):
        self.__frontier = Frontier()
        self.__maze = m
        self.__start = self.__maze.coordinate(start_room)
        self.__goal = self.__maze.coordinate(goal_room)
        self.__solution = ""
        self.__expanded_path = ""
        self.__expanded_cost = 0
        self.__expanded_room = ""

    def get_start_room(self):
        return self.__maze.room_name(self.__start)

    def get_goal_room(self):
        return self.__maze.room_name(self.__goal)

    def get_expanded_path(self):
        return self.__expanded_path

    def get_expanded_cost(self):
        return self.__expanded_cost

    def get_expanded_room(self):
        return self.__expanded_room

    def frontier_information(self):
        """
        :return: String that contains the elements of the frontier
        """
        return self.__frontier.get_frontier_information()

    def start_search(self):
        """
            Initialize the search by pushing the start room to frontier
        """
        tmp_path = self.__maze.maze[self.__start[0]][self.__start[1]]
        tmp_cost = 0
        self.__frontier.add_path((tmp_path, tmp_cost))

    def expand_room(self):
        """
        Expand the room from the path that has the lowest cost. Set the solution until the goal is reached or frontier is empty.
        :return: True if there cannot be no more expand
        """
        if self.__frontier.get_size() == 0:
            print("Fringe is empty. Cannot continue to search.")
            self.__solution = False
            return True

        expanded_tuple = self.__frontier.remove_path()
        self.__expanded_path = expanded_tuple[0]
        self.__expanded_cost = expanded_tuple[1]
        self.__expanded_room = self.__expanded_path[-1:]

        if self.__maze.coordinate(self.__expanded_room) == self.__goal: # if coordinates are equal
            self.__solution = expanded_tuple
            return True

        neighbor_dict = self.__maze.neighbors(self.__expanded_room)

        if len(neighbor_dict) != 0:
            for key in neighbor_dict.keys():
                if len(self.__expanded_path) >= 3:
                    if key != self.__expanded_path[len(self.__expanded_path) - 3]:  # do not turn back
                        tmp_path = self.__expanded_path + "-" + key
                        tmp_cost = self.__expanded_cost + neighbor_dict[key]
                        self.__frontier.add_path((tmp_path, tmp_cost))
                else:
                    tmp_path = self.__expanded_path + "-" + key
                    tmp_cost = self.__expanded_cost + neighbor_dict[key]
                    self.__frontier.add_path((tmp_path, tmp_cost))

        self.__frontier.sort_frontier()

    def get_solution(self):
        if not self.__solution:
            return "Solution cannot be found"
        else: # solution is set as expanded tuple if the expanded node is equal to goal
            return "{: <15} :{: <5}".format(self.__solution[0], self.__solution[1])


class A_Star_Search:
    __start = None # coordinate tuple
    __goal = None  # coordinates from maze ndarray
    __maze = None
    __frontier = None
    __solution = None
    __expanded_path = None
    __expanded_cost = None
    __expanded_room = None

    def __init__(self, start_room: str, goal_room: str, m: Maze):
        self.__frontier = Frontier()
        self.__maze = m
        self.__start = self.__maze.coordinate(start_room)
        self.__goal = self.__maze.coordinate(goal_room)
        self.__solution = ""
        self.__expanded_path = ""
        self.__expanded_cost = 0
        self.__expanded_room = ""

    def get_start_room(self):
        return self.__maze.room_name(self.__start)

    def get_goal_room(self):
        return self.__maze.room_name(self.__goal)

    def get_expanded_path(self):
        return self.__expanded_path

    def get_expanded_cost(self):
        return self.__expanded_cost

    def get_expanded_room(self):
        return self.__expanded_room

    def frontier_information(self):
        """
        :return: String that contains the elements of the frontier
        """
        return self.__frontier.get_frontier_information()


    def hamming_distance(self, r1: str):
        c_coordinate = self.__maze.coordinate(r1)
        g_coordinate = self.__goal

        x = abs(g_coordinate[1] - c_coordinate[1])
        y = abs(g_coordinate[0] - c_coordinate[0])

        goal_room_name = self.__maze.room_name(c_coordinate)
        current_room_name = self.__maze.room_name(g_coordinate)
        hamming_distance = sum(c != g for c, g in zip(current_room_name, goal_room_name))

        return x * 2 + y + hamming_distance


    def start_search(self):
        """
            Initialize the search by pushing the start room to frontier
        """
        tmp_path = str(self.__maze.maze[self.__start[0]][self.__start[1]]) # tuple of the start node
        tmp_cost = 0 + self.hamming_distance(tmp_path)
        self.__frontier.add_path((tmp_path, tmp_cost))

    def expand_room(self):
        """
        Expand the room from the path that has the lowest cost. Set the solution until the goal is reached or frontier is empty.
        :return: True if there cannot be no more expand
        """
        if self.__frontier.get_size() == 0:
            print("Fringe is empty. Cannot continue to search.")
            self.__solution = False
            return True

        expanded_tuple = self.__frontier.remove_path()
        self.__expanded_path = expanded_tuple[0]
        self.__expanded_room = self.__expanded_path[-1:]
        expanded_cost = expanded_tuple[1] - self.hamming_distance(self.__expanded_room)
        self.__expanded_cost = expanded_tuple[1]

        if self.__maze.coordinate(self.__expanded_room) == self.__goal:
            self.__solution = expanded_tuple
            return True

        neighbor_dict = self.__maze.neighbors(self.__expanded_room)
        if len(neighbor_dict) != 0:
            for key in neighbor_dict.keys():
                if len(self.__expanded_path) >= 3:
                    if key != self.__expanded_path[len(self.__expanded_path) - 3]:  # do not turn back
                        tmp_path = self.__expanded_path + "-" + key
                        tmp_cost = expanded_cost + neighbor_dict[key] + self.hamming_distance(key)
                        self.__frontier.add_path((tmp_path, tmp_cost))
                else:
                    tmp_path = self.__expanded_path + "-" + key
                    tmp_cost = expanded_cost + neighbor_dict[key] + self.hamming_distance(key)
                    self.__frontier.add_path((tmp_path, tmp_cost))

        self.__frontier.sort_frontier()


    def get_solution(self):
        if not self.__solution:
            return "Solution cannot be found"
        else: # solution is set as expanded tuple if the expanded node is equal to goal
            return "{: <15} :{: <5}".format(self.__solution[0], self.__solution[1])



def game_first_page(maze: Maze):
    """
    :param maze: the maze object to be settled inside the page

    This method creates the first page of the game when you execute. The page includes an image of rooms, selection of start, goal and walls,
    and choose option of search algorithm. And also a start button that, destroys the page to go to the algorithm page
    """
    def initialize_start():
        """Set the start room of the game maze"""
        maze.set_start(start_listbox.get(start_listbox.curselection()))

    def initialize_goal():
        """Set the goal room of the game maze"""
        maze.set_goal(goal_listbox.get(goal_listbox.curselection()))

    def initialize_walls():
        """Set the walls between rooms of the game maze"""
        walls = []
        for index in walls_list_box.curselection():
            wall = walls_list_box.get(index)
            walls.append(wall)
        maze.set_walls(walls)

    def initialize_algorithm():
        """Set the search algorithm of the game maze"""
        if algorithm_var.get() == 0:
            maze.set_search_algorithm("Uniform Cost Search")
        else:
            maze.set_search_algorithm("A* Search")

    def initialize_algorithm_page():
        """Destroy the current page"""
        first_page.destroy()

    # Create the page
    first_page = Tk()
    first_page.geometry("1000x800")

    # Create  a header for the page
    header_font = font.Font(weight="bold", size=20)
    header_label = Label(master=first_page, text="Set The Maze", font=header_font, relief=FLAT)

    # put the robot image to the screen
    img = Image.open("Robot.png")
    resized_image = img.resize((100, 100))
    image = ImageTk.PhotoImage(resized_image)
    image_label = Label(image=image)

    # Create the image of the rooms as labels
    label_font = font.Font(weight="bold")
    header_font = font.Font(weight="bold", size=14)
    room_map_label = Label(master=first_page, text="Empty Rooms Map", font=header_font, anchor=CENTER)
    A_label = Label(master=first_page, text="A", foreground="black", font=label_font, height=5, width=10, relief=RIDGE)
    B_label = Label(master=first_page, text="B", foreground="black", font=label_font, height=5, width=10, relief=RIDGE)
    C_label = Label(master=first_page, text="C", foreground="black", font=label_font, height=5, width=10, relief=RIDGE)
    D_label = Label(master=first_page, text="D", foreground="black", font=label_font, height=5, width=10, relief=RIDGE)
    E_label = Label(master=first_page, text="E", foreground="black", font=label_font, height=5, width=10, relief=RIDGE)
    F_label = Label(master=first_page, text="F", foreground="black", font=label_font, height=5, width=10, relief=RIDGE)
    G_label = Label(master=first_page, text="G", foreground="black", font=label_font, height=5, width=10, relief=RIDGE)
    H_label = Label(master=first_page, text="H", foreground="black", font=label_font, height=5, width=10, relief=RIDGE)
    I_label = Label(master=first_page, text="I", foreground="black", font=label_font, height=5, width=10, relief=RIDGE)

    # create listbox for selecting start room and button for saving the selection
    start_lb_label = Label(master=first_page, text="Root", font=label_font)
    start_listbox = Listbox(master=first_page, width=5, height=10, font=label_font, activestyle="dotbox")
    start_listbox.insert(1, "A")
    start_listbox.insert(2, "B")
    start_listbox.insert(3, "C")
    start_listbox.insert(4, "D")
    start_listbox.insert(5, "E")
    start_listbox.insert(6, "F")
    start_listbox.insert(7, "G")
    start_listbox.insert(8, "H")
    start_listbox.insert(9, "I")
    set_start_button = Button(master=first_page, text="Set", width=5, command=initialize_start)

    # create listbox for selecting the goal room and button for saving the selection
    goal_lb_label = Label(master=first_page, text="Goal", font=label_font)
    goal_listbox = Listbox(master=first_page, width=5, height=10, font=label_font, activestyle="dotbox")
    goal_listbox.insert(1, "A")
    goal_listbox.insert(2, "B")
    goal_listbox.insert(3, "C")
    goal_listbox.insert(4, "D")
    goal_listbox.insert(5, "E")
    goal_listbox.insert(6, "F")
    goal_listbox.insert(7, "G")
    goal_listbox.insert(8, "H")
    goal_listbox.insert(9, "I")
    set_goal_button = Button(master=first_page, text="Set", width=5, command=initialize_goal)

    # Create listbox for selecting walls of the rooms and button to save the selection
    walls_lb_label = Label(master=first_page, text="Walls", font=label_font)
    walls_list_box = Listbox(master=first_page, width=5, height=13, selectmode=MULTIPLE, font=label_font, activestyle="dotbox", selectbackground="red")
    walls_list_box.insert(1, "A-B")
    walls_list_box.insert(2, "A-D")
    walls_list_box.insert(3, "B-C")
    walls_list_box.insert(4, "B-E")
    walls_list_box.insert(5, "C-F")
    walls_list_box.insert(6, "D-E")
    walls_list_box.insert(7, "D-G")
    walls_list_box.insert(8, "E-F")
    walls_list_box.insert(9, "E-H")
    walls_list_box.insert(10, "F-I")
    walls_list_box.insert(11, "G-H")
    walls_list_box.insert(12, "H-I")
    set_walls_button = Button(master=first_page, text="Set", width=5, command=initialize_walls)

    # Create a radiobutton for selecting algorithm
    algorithms = ["Uniform Cost Search", "A* Search"]
    algorithm_var = IntVar()
    font_label = font.Font(size=12)
    for i in range(2):
        algorithm_radiobutton = Radiobutton(master=first_page, text=algorithms[i], font=font_label, variable=algorithm_var, value=i, command=initialize_algorithm)
        algorithm_radiobutton.place(x=80, y=400+35*i)

    #  Create the START button to destroy the first page
    start_button = Button(master=first_page, text="Start", width=10, height=2, command=initialize_algorithm_page)

    # place the widgets on screen
    header_label.pack()
    image_label.place(x=432, y=100)
    room_map_label.place(x=390, y=260)
    A_label.place(x=330, y=300)
    B_label.place(x=430, y=300)
    C_label.place(x=530, y=300)
    D_label.place(x=330, y=400)
    E_label.place(x=430, y=400)
    F_label.place(x=530, y=400)
    G_label.place(x=330, y=500)
    H_label.place(x=430, y=500)
    I_label.place(x=530, y=500)
    start_lb_label.place(x=700, y=280)
    goal_lb_label.place(x=770, y=280)
    walls_lb_label.place(x=840, y=280)
    start_listbox.place(x=700, y=300)
    goal_listbox.place(x=770, y=300)
    walls_list_box.place(x=840, y=300)
    set_start_button.place(x=700, y=510)
    set_goal_button.place(x=770, y=510)
    set_walls_button.place(x=840, y=570)
    start_button.place(x=850, y=650)

    first_page.mainloop()


def game_second_page(maze: Maze, search_algorithm):
    """
    :param maze: The maze object that is ready to be applied search algorithms
    :param search_algorithm: The chosen search algorithm object reference from the first page

    """
    expand_counter = 1

    def iterate_algorithm():
        """
        Do the search and update the screen in every step
        """
        nonlocal expand_counter

        for r in room_dict.values():
            r.config(foreground="black", image=delete_image)

        room_dict[maze.get_goal()].config(foreground="red")

        frontier_label.config(text="Frontier:\n" + search_algorithm.frontier_information())
        step_label.config(text="Step = {}".format(expand_counter))
        loop_result = search_algorithm.expand_room()
        expand_counter += 1
        expanded_path_label.config(text="Expand Path: {} ({})".format(search_algorithm.get_expanded_path(), search_algorithm.get_expanded_cost()))
        expanded_room_label.config(text="Expand Room: {}".format(search_algorithm.get_expanded_room()))

        for r in search_algorithm.get_expanded_path():
            if r != "-":
                room_dict[r].config(foreground="blue", image=image)

        room_dict[search_algorithm.get_expanded_room()].config(foreground="blue", image=image)

        if loop_result:
            if search_algorithm.get_solution() == "Solution cannot be found":
                expanded_path_label.config(text="Cannot reach to the goal room")
                expanded_room_label.config(text="Expanded Room: {}".format(search_algorithm.get_expanded_room()))

            else:
                expanded_path_label.config(text="Search Path: {} ({})".format(search_algorithm.get_expanded_path(), search_algorithm.get_expanded_cost()))
                expanded_room_label.config(text="Goal Room: {}".format(search_algorithm.get_expanded_room()))
            next_button.config(state=DISABLED)
            finish_button.config(state=ACTIVE)
            sol_path = search_algorithm.get_expanded_path()

            for r in sol_path:
                if r != "-":
                    room_dict[r].config(foreground="green")

        elif expand_counter == 10:
            expanded_path_label.config(text="Goal Room cannot found")
            next_button.config(state=DISABLED)
            finish_button.config(state=ACTIVE)


    def terminate():
        """Destroy the current page"""
        second_page.destroy()

    # create the window of second page
    second_page = Tk()
    second_page.geometry("1000x900")

    # create the image of robot and empty image
    img = Image.open("Robot.png")
    resized_image = img.resize((50, 50))
    image = ImageTk.PhotoImage(resized_image)
    delete_img = Image.open("delete_image.png")
    resized_delete_image = delete_img.resize((50, 50))
    delete_image = ImageTk.PhotoImage(resized_delete_image)

    # create a search, start, goal and step labels to be shown through the search
    label_font = font.Font(weight="bold", size=20)
    search_algorithm_label = Label(master=second_page, text=maze.get_search_algorithm(), font=label_font)
    start_goal_label = Label(master=second_page, text="Start: {}\t\tGoal: {}".format(maze.get_start(), maze.get_goal()), font=label_font)
    step_label = Label(master=second_page, text="Step = 0", font=label_font)

    label_font2 = font.Font(weight="bold", size=15)

    # create a new label to show the frontier information
    frontier_label = Label(master=second_page, text="Frontier:\n" + search_algorithm.frontier_information(), font=label_font2, padx=8, pady=5)

    # create new labels for expanded room, expanded path and its cost
    expanded_path_label = Label(master=second_page, text="Expand Path: {} ({})".format(search_algorithm.get_expanded_path(), search_algorithm.get_expanded_cost()), font=label_font2)
    expanded_room_label = Label(master=second_page, text="Expand room: {}".format(search_algorithm.get_expanded_room()), font=label_font2)

    # now create 9 labels for rooms
    A_label = Label(master=second_page, text="A", image=delete_image, foreground="black", font=label_font, relief=FLAT, compound="top")
    B_label = Label(master=second_page, text="B", image=delete_image, foreground="black", font=label_font, relief=FLAT, compound="top")
    C_label = Label(master=second_page, text="C", image=delete_image, foreground="black", font=label_font, relief=FLAT, compound="top")
    D_label = Label(master=second_page, text="D", image=delete_image, foreground="black", font=label_font, relief=FLAT, compound="top")
    E_label = Label(master=second_page, text="E", image=delete_image, foreground="black", font=label_font, relief=FLAT, compound="top")
    F_label = Label(master=second_page, text="F", image=delete_image, foreground="black", font=label_font, relief=FLAT, compound="top")
    G_label = Label(master=second_page, text="G", image=delete_image, foreground="black", font=label_font, relief=FLAT, compound="top")
    H_label = Label(master=second_page, text="H", image=delete_image, foreground="black", font=label_font, relief=FLAT, compound="top")
    I_label = Label(master=second_page, text="I", image=delete_image, foreground="black", font=label_font, relief=FLAT, compound="top")

    # create 16 labels for walls
    up_wall = Label(master=second_page, height=1, width=59, relief=FLAT, background="black")
    right_wall = Label(master=second_page, height=31, width=2, relief=FLAT, background="black")
    left_wall = Label(master=second_page, height=31, width=2, relief=FLAT, background="black")
    down_wall = Label(master=second_page, height=1, width=59, relief=FLAT, background="black")

    A_B_Label = Label(master=second_page, height=9, width=2, relief=FLAT)
    A_D_Label = Label(master=second_page, height=1, width=18, relief=FLAT)
    B_C_Label = Label(master=second_page, height=9, width=2, relief=FLAT)
    B_E_Label = Label(master=second_page, height=1, width=18, relief=FLAT)
    C_F_Label = Label(master=second_page, height=1, width=18, relief=FLAT)
    D_E_Label = Label(master=second_page, height=9, width=2, relief=FLAT)
    D_G_Label = Label(master=second_page, height=1, width=18, relief=FLAT)
    E_F_Label = Label(master=second_page, height=9, width=2, relief=FLAT)
    E_H_Label = Label(master=second_page, height=1, width=18, relief=FLAT)
    F_I_Label = Label(master=second_page, height=1, width=18, relief=FLAT)
    H_I_Label = Label(master=second_page, height=9, width=2, relief=FLAT)
    G_H_Label = Label(master=second_page, height=9, width=2, relief=FLAT)

    # create next button that executes the search algorithm
    next_button = Button(master=second_page, text="Next", width=10, height=2, command=iterate_algorithm)

    # create finish button to terminate the program
    finish_button = Button(master=second_page, text="Finish", width=10, height=2, command=terminate)

    # Packing the labels
    search_algorithm_label.pack(side=TOP)
    start_goal_label.place(x=335, y=76)
    step_label.place(x=450, y=130)
    frontier_label.place(x=100, y=145)
    expanded_path_label.place(x=400, y=190)
    expanded_room_label.place(x=400, y=240)
    up_wall.place(x=285, y=281)
    down_wall.place(x=287, y=752)
    left_wall.place(x=283, y=295)
    right_wall.place(x=685, y=295)
    A_label.place(x=335, y=305)
    B_label.place(x=461, y=305)
    C_label.place(x=587, y=305)
    D_label.place(x=335, y=458)
    E_label.place(x=461, y=458)
    F_label.place(x=587, y=458)
    G_label.place(x=335, y=611)
    H_label.place(x=461, y=611)
    I_label.place(x=587, y=611)
    A_B_Label.place(x=414, y=302)
    A_D_Label.place(x=303, y=429)
    B_C_Label.place(x=546, y=302)
    B_E_Label.place(x=435, y=429)
    C_F_Label.place(x=553, y=429)
    D_E_Label.place(x=414, y=450)
    D_G_Label.place(x=303, y=590)
    E_F_Label.place(x=546, y=450)
    E_H_Label.place(x=435, y=590)
    F_I_Label.place(x=553, y=590)
    H_I_Label.place(x=546, y=611)
    G_H_Label.place(x=414, y=611)
    next_button.place(x=850, y=800)
    finish_button.place(x=100, y=800)

    # to manage the view of rooms
    room_dict = {
        "A": A_label,
        "B": B_label,
        "C": C_label,
        "D": D_label,
        "E": E_label,
        "F": F_label,
        "G": G_label,
        "H": H_label,
        "I": I_label
    }

    # to manage the view of walls
    walls_dict = {
        "AB": A_B_Label,
        "AD": A_D_Label,
        "BC": B_C_Label,
        "BE": B_E_Label,
        "CF": C_F_Label,
        "DE": D_E_Label,
        "DG": D_G_Label,
        "EF": E_F_Label,
        "EH": E_H_Label,
        "FI": F_I_Label,
        "GH": G_H_Label,
        "HI": H_I_Label
    }

    # set the root node's color as green and goal nodes red at start
    room_dict[maze.get_start()].config(foreground="green")
    room_dict[maze.get_goal()].config(foreground="red")

    # set the walls as black when true
    maze_walls = maze.get_walls()
    for key in maze_walls.keys():
        if maze_walls[key] is True:
            walls_dict[key].config(background="black")

    second_page.mainloop()

def main():
    game_maze = Maze()
    game_first_page(game_maze)

    if game_maze.get_search_algorithm() == "A* Search":
        search_algorithm = A_Star_Search(game_maze.get_start(), game_maze.get_goal(), game_maze)
    else:
        game_maze.set_search_algorithm("Uniform Cost Search")
        search_algorithm = Uniform_Cost_Search(game_maze.get_start(), game_maze.get_goal(), game_maze)

    search_algorithm.start_search()
    game_second_page(game_maze, search_algorithm)


main()
