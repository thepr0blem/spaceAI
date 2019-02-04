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
├── generation logs         # Top genes saved
├── images                  # Game graphics and screenshots
├── main.py                 # main file (contains game class)
├── game_classes.py         # in-game objects (Spaceship, obstacles etc.) 
├── helper_functions.py     # ReLU and softmax functions
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

The simulation will randomly initialize population of N Spaceships with randomly generated neural networks as their "brains". Size of the population can be set in ```settings.py``` file. Each ship has two genotypes ('a' and 'b'), those are two matrices: 
- ```genotype_a``` links input layer with hidden layer 
- ```genotype_b``` links hidden layer with output layer 

#### Fitness function 
To evaluate each individual we simply take the number of points gathered during single game. Given the simple rules of the game, the number of passed obstacles is the SCORE.

#### 2.2.2. Selection

N - population size
n - top scorers number

Selection step works as follows: 
- select n top scorers from previous generation (n defined as ```SELECTION_RATE * POPULATION_SIZE``` in ```settings.py```
- create a list with top scoring ships 
- move top n top scorers directly to next generation 

#### 2.3.3. Crossover

Generate new genoms based on randomly selected ships from n top players from previous generation. Steps:
- each iteration involves random generation of crossover weight ```xoW``` (range 0-1) 
- new genotypes are calculated with the following formulas:
```python
        gen_a_new = pilot_1.genotype_a * xoW + (1 - xoW) * pilot_2.genotype_a
        gen_b_new = pilot_1.genotype_b * xoW + (1 - xoW) * pilot_2.genotype_b
```

#### 2.3.4. Mutation 

Additionally, simple mechanism for mutation was implemented. It works as follows: 
- random variable ```mutationW``` is generated in range given by ```MUTATION_SCALE``` (adjustable in ```settings.py```)
```python         
mutationW = rd.uniform(1 - MUTATION_SCALE, 1 + MUTATION_SCALE)
```

- random variable called ```mutation``` is generated, if smaller than ```MUTATION_PROB``` (adjustable in ```settings.py```): mutation takes place
```python
        mutation = rd.random()
        # Check if mutation happens
        if mutation <= MUTATION_PROB:

            # Modify whole genes by multiplying their weights with mutation weight
            gen_a_new = gen_a_new * mutationW
            gen_b_new = gen_b_new * mutationW
```


## 3. Game engine 
### 3.1. Description 

The game has 4 modes:

#### A. Random Autopilot
Spaceship is steered by AI with randomly initialized neural network

#### B. Human Player 
Spaceship is steered by human player (```LEFT``` and ```RIGHT``` arrow keys)

#### C. Simulation 
In this mode population is generated and evolved until the user decides to stop on current generation and save latest genes of the most successful pilot to file

#### D. Top Pilot
Loads genes from previous simulations and initialize intelligent pilot to steer the spaceship

*Tips for moving between screens*:
- **GAME OVER** is displayed after spaceship dies in modes ```A```, ```B``` or ```D```. From **GAME OVER** user may go back to **MAIN MENU** or restart current mode.
- **SIMULATION** - press ```R``` in **SIMULATION** to go to **SIMULATION MENU**. Here you can save latest genes, restart simulation or go back to **MAIN MENU**

### 3.2. Classes and logic 

## 4. Potential next steps/ideas 
#### I. Test different NN architectures (variable number of layers) 
#### II. Add "coins" in the middle of each gap giving additional points if collected 

