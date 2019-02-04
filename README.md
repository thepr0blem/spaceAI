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
├── images                  # Game graphics
├── main.py                 # main file (contains game class)
├── game_classes.py         # in-game objects (Spaceship, obstacles etc.) 
├── helper_functions.py     
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

![NN](https://github.com/thepr0blem/spaceAI/blob/master/images/nn_edit.png)

### 2.2. Genetic algorithm 
#### 2.2.1. Introduction

Neural network will be optimized using Genetic Algorithm (GA), which simulates natural process population evolution through selection, crossover and mutation

#### 2.2.2. Selection
#### 2.3.3. Crossover
#### 2.3.4. Mutation 
## 3. Game engine 
### 3.1. Description 
### 3.2. Classes and logic 
### 3.3. Screenshots  
## 4. Potential next steps/ideas 

	
