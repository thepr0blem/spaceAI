# spaceAI

Simple space runner implementation in Python Arcade + AI player with neural network trained using genetic algorithm.

### Content of this document 
1. Introduction
2. Neural network architecture and training using genetic algorithm
3. Game engine
4. Potential next steps and ideas 

## 1. Introduction 
### 1.1. General idea 

The main purpose of this exercise (beside the obvious, which is self-development) is to build a simple "space runner" game which will be an environment for genetic algorithm implementation.

### 1.2. Technologies used

```Arcade``` library

### 1.3. Project structure 

```
├── images                  # Game graphics and screenshots
├── drawer.py               # contains helper class Drawer
├── ext_functions.py        # contains helper functions used in neural network implementation and evolving of population
├── game_classes.py         # in-game objects (Spaceship, obstacles etc.) 
├── key_event_handler.py    # contains helper class KeyEventHandler (collection of methods used to handle key press events) 
├── main.py                 # main file (contains MyGame class)
├── settings.py             # Game and simulation settings
├── requirments.txt         # Required libraries
└── README.md                 
```

### 1.4. How to use 

Run ```main.py``` script. Required technologies are listed in ```requirments.txt``` file. 

## 2. Neural network architecture and training using genetic algorithm 
### 2.1. NN architecture 

Making decision on which direction ship moves using neural network. Properties of neural network:
Input: x coordinates of the ship and closest obstacle (```x_ship```, ```gap_x1```, ```gap_x2```)
Structure of NN:
- 3 input values
- 1 hidden layer with 8 neurons - can be adjusted in ```settings.py```
- 3 output values (0 - STAY, 1 - LEFT, 2 - RIGHT)

<img src="https://github.com/thepr0blem/spaceAI/blob/master/images/nn_edit.png" width="700">

### 2.2. Genetic algorithm 
#### 2.2.1. Introduction

Neural network will be optimized using Genetic Algorithm (GA), which simulates natural process of population evolution through selection, crossover and mutation. In this case, I will treat NN weights as a set of properties (genotype) which can be mutated. This will allow to find an optimal or close to optimal set of weights which will be used to steer the Spaceship between obstacles. 

The simulation will randomly initialize population of N Spaceships with randomly generated neural networks as their "brains". Size of the population can be set in ```settings.py``` file. Each ship has two genotypes ('a' and 'b'), those are two matrices and two vectors: 
- ```genotype_a``` links input layer with hidden layer (weight matrix + bias vector)
- ```genotype_b``` links hidden layer with output layer (weight matrix + bias vector)

#### Fitness function 
To evaluate each individual we simply take the number of points gathered during single game. Given the simple rules of the game, the number of passed obstacles is the SCORE.

```python
def calc_fitness(self):
    """
    - Calculates pilot's fitness based on his current score and proportion of 'stay' decisions to total decisions
    - The latter is the tweak implemented to eliminate ships which perform well, but do many neccessary movements
    Additional points are granted when ships have scored > 3 points. 
    """

    # Relative part of stay decisions
    if self.pilot_score > 3:
        moves_distr_score = self.stay_decs_count / (self.move_decs_count + self.stay_decs_count)
    else:
        moves_distr_score = 0

    self.fitness = self.pilot_score + amp_func(moves_distr_score, STAY_FRAC)
```

Additional ```add_score``` function translates fraction of "Stay" decisions to premium fitness points. 

```python
def add_score(x, stay_frac):
    """
    - Calculates additional score for "stay" decisions being a certain fraction of all decisions made by the pilot.
    - Helps pilots to evolve to a state when they do not make unneccessary movements when going straight.
    """

    if 0 < x <= stay_frac:
        return (1/stay_frac) * x
    elif 1 >= x > stay_frac:
        return -(1/(1-stay_frac)) * x + 1/(1-stay_frac)
    elif x > 1 or x <= 0:
        return 0
```

#### 2.2.2. Selection

N - population size
n - top scorers number

Selection step works as follows: 
- select n top scorers from previous generation (n defined as ```SELECTION_RATE * POPULATION_SIZE``` in ```settings.py```
- create a list with top scoring ships 
- move top n top scorers directly to next generation 

```python
def selection(self):
    """Sorts pilots by their fitness and assigns the best units to top_ships variable"""

    # --- Selection ---
    # Sort ships by their performance (measured by pilot's score)
    self.prev_gen_ships_list = []
    self.prev_gen_ships_list = self.ships_list[:]
    self.prev_gen_ships_list.sort(key=lambda c: c.pilot.fitness, reverse=True)

    # Assign best scorers to top_ships
    self.top_ships = []
    self.top_ships = self.prev_gen_ships_list[:int(SELECTION_RATE * POPULATION_SIZE)]

```

#### 2.3.3. Crossover

Generate new child genoms from two pilot parents: 

```python
def cross_over(pilot_1, pilot_2):
    """
    Cross genoms of two pilots to produce child gens using the following formula:
    new = parent_1 * random + parent_2 * (1 - random), where random is number in range 0-1
    """

    # --- Crossover ---
    xoW = rd.random()  # Crossover weight

    # Crossing genes of parents
    gen_a_new = pilot_1.genotype_a * xoW + (1 - xoW) * pilot_2.genotype_a
    gen_b_new = pilot_1.genotype_b * xoW + (1 - xoW) * pilot_2.genotype_b
    bias_a_new = pilot_1.bias_a * xoW + (1 - xoW) * pilot_2.bias_a
    bias_b_new = pilot_1.bias_b * xoW + (1 - xoW) * pilot_2.bias_b

    return gen_a_new, gen_b_new, bias_a_new, bias_b_new
```

#### 2.3.4. Mutation 

```python         
def mutate(gen_a_new, gen_b_new, bias_a_new, bias_b_new):
    """
    Mutates genes by replacing genes with new random values with probability of MUTATION_PROB (modified in settings.py)
    """

    mutation = rd.random()
    # Check if mutation happens
    if mutation <= MUTATION_PROB:

        # Modify whole genes by multiplying their weights with mutation weight
        gen_a_new = np.random.randn(NEURONS, 3)
        gen_b_new = np.random.randn(3, NEURONS)
        bias_a_new = np.random.randn(NEURONS, 1) * 0.5
        bias_b_new = np.random.randn(3, 1) * 0.5

    return gen_a_new, gen_b_new, bias_a_new, bias_b_new
```


## 3. Game engine 
### 3.1. Description 

The game has 3 modes:

#### A. Random Autopilot
Spaceship is steered by AI with randomly initialized neural network

#### B. Human Player 
Spaceship is steered by human player (```LEFT``` and ```RIGHT``` arrow keys)

#### C. Simulation 
In this mode population is generated and evolved.

*Tips for moving between screens*:
- **GAME OVER** is displayed after spaceship dies in modes ```A``` or ```B```. From **GAME OVER** user may go back to **MAIN MENU** or restart current mode.
- **SIMULATION** - press ```R``` in **SIMULATION** to go to **SIMULATION MENU**. From here you can restart simulation or go back to **MAIN MENU**

### 3.2. Screenshots

#### Main Menu
<img src="https://github.com/thepr0blem/spaceAI/blob/master/images/Main_menu.PNG" width="500">

#### Sim Menu
<img src="https://github.com/thepr0blem/spaceAI/blob/master/images/Sim_menu.png" width="500">

#### A, B modes
<img src="https://github.com/thepr0blem/spaceAI/blob/master/images/scr_1.PNG" width="500">

#### Simulation mode
<img src="https://github.com/thepr0blem/spaceAI/blob/master/images/scr_2.png" width="500">


### 3.3. Game logic, structure and classes 

#### 3.3.1 Overview

The game has been created using ```arcade``` framework. To turn on the game run ```main.py``` script which contains MyGame class. 

#### 3.3.2. MyGame class

```MyGame``` class (```main.py```)is responsible for displaying the game window on the screen, drawing the content and updating screen/game state. It inherits from multiple classess where the most important is ```arcade.Window``` class and the others are helper classes responsible for handling key press events, drawing menu screens and tracking the collisions. The class has 3 important methods: 
- setup - to set up the game
- on_draw - called to draw the window
- update - updates current state of the game 

#### 3.3.3. Helper classes

The MyGame class has more methods which are inherited from helper classes. Namely: 
- ```collision_system.py``` contains ```CollisionSystem``` class - collection of methods used to track collisions between ship/population of ships and closest obstacle
- ```key_event_handler.py``` contains ```KeyEventHandler``` class -  collection of methoded used to track keyboard presses and handling respective actions
- ```drawer.py``` contains ```Drawer``` class -  collection of method used by MyGame class to draw different possible scenarios, like:
    - current game state
    - menu screens
    - game over screen
    - bottom bar with score/additional information

#### 3.3.4. Helper functions 

```ext_functions.py``` contains helper functions used in neural network implementation and evolving of population. Functions:
```softmax``` - computes softmax values for each sets of scores in vector x
```relu``` - neural network activation function - Rectified Linear Unit
```add_score``` - calculates additional score for "stay" decisions being a certain fraction of all decisions made by the pilot
```cross_over``` - cross genoms of two pilots to produce child genes
```mutate``` - mutates genes by replacing with random numbers with probability of MUTATION_PROB (modified in settings.py)

#### 3.3.5. Settings 

```settings.py``` contains overall game settings and evolution parameters such as: 
- screen width and height 
- obstacle vertical speed
- ship horizontal speed 
- population size
- mutation probability
- selection rate (% of ships taken as top scorers) 
- number of neurons in NN hidden layer

#### 3.3.6. Game classes

```game_classes.py``` contains classes for in game objects, such as: 

- Population - collection of SpaceShip objects, which together with their pilots will be evolving as playing

    Methods:
        - populate - generates collection of POPULATION_SIZE ships
        - erase_history - restars population by cleaning ships_list and performing fresh initialization
        - evolve - performs evolution algorithm steps: selection, crossover and mutation and reassigns Pilots genotypes
        - ressurect_ships - resurrects all ships in population and reposition them to the middle of the screen
        - check_if_all_dead - returns TRUE if all ships are dead
        - evolve - performs population evolution
        - selection - sorts pilots by their fitness
        
- Pilot - brain for SpaceShip class. Its genes store information on weights for nerual network that make a decision on next movement of the ship 

    Methods:
        - decide - making decision on which direction ship moves using neural network
        - calc_fitness - calculates pilot's fitness based on his current score and proportion of 'stay' decisions to total decisions

- SpaceShip - spaceship 

    Methods: 
        - draw - draws the spaceship
        - update - updates current state of spaceship e.g. position
    
- Obstacle - obstacle

    Methods:
        - draw - draws space obstacle
        - respawn - respawn obstacle "above" the visibile screen area after passing by the spaceship y position
        - update - updates current state of obstacle (moves obstacle down the screen)
        - level_up - increase obstacle vertical movement every x points

## 4. Potential next steps/ideas 
I. Test different NN architectures (e.g. variable number of layers) 


### Sources 

Graphics: 
- textures come from amazing [Kenney.nl](https://Kenney.nl) 
- background: [PXHere.com](https://pxhere.com/en/photo/915272)

Reference documents: 
- [Genetic Algorithm Wikipedia page](https://en.wikipedia.org/wiki/Genetic_algorithm)
- ```arcade``` - [arcade.academy](http://arcade.academy/)
