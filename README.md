#JSON Loading Challenge

This challenge focuses on using the json module for saving and loading an implementation of Wolves, Rabbits and Grass:

https://github.com/reddit-pygame/json-loading-challenge


##WTF is Wolves, Rabbits and Grass?

It's a simulation of a commonly used example of a predator-prey relationship. I actually started out doing foxes and rabbits, but I found better assets for wolves. In a nutshell, rabbits eat grass, wolves eat rabbits, population dynamics ensue.
 To keep things simple, the rabbits and wolves are asexual - a single critter is capable of reproducing.

##How the sim works

#####Grass

Grass is the food source for the rabbits. A grass's growth increases each tick until it reaches its maximum growth and decreases when eaten by rabbits.

#####Rabbits

Rabbits are the food source for the wolves. Rabbits move randomly unless they are eating. When a rabbit's food <= 50% it will start eating from the first
 grass it encounters until it has reached its max food. After reaching their reproductive age they have a chance to create an offspring. After giving birth they can't
 give birth again until their gestation period (and, yes, I know that's a totally incorrect use of the term) has elapsed.

#####Wolves

Wolves are essentially the same as rabbits, but they eat rabbits instead of grass and nothing eats them.

#####Simulation

Updating the simulation is independent of drawing to the screen and multiple updates may occur before drawing again. This allows faster simulation
 speed at the expense of fidelity - it's possible a rabbit could be born, live through a few updates and get eaten without ever appearing on the screen.

#####Controls

UP/DOWN - change the simulation speed

#Challenge

Saving the simulation has already been implemented (Sim.save in sim.py) and occurs automatically on exit - your challenge, should you choose to accept it,
is to implement loading the save file using the json module. The MenuScreen class (in menu.py) has a method stub, `load_saved`, that is called
when the "Load Sim" button is clicked. You should be able to complete this challenge by "filling in" the load_saved method with the proper functionality.     

###Some Links

[json module docs](https://docs.python.org/2/library/json.html)

[Module of the week - json](https://pymotw.com/2/json/)

##Not Challenging Enough?

If you're looking to stretch your pygame muscles a bit, here are a few ideas for additional features:

- Display the number of wolves, rabbits and grass

- Allow the user to add grass, rabbits or wolves manually

- Add a graph screen that shows the changes of the populations over time

- Add a configuration screen that allows the user to change the attributes (gestation period, reproduction chance, etc.) of the
wolves, rabbits and grass when starting a new sim. This will likely require changes to the Wolf, Rabbit and Grass classes and a 
more robust save function.

- Whatever else piques your interest

Good luck, have fun and feel free to ask for help if you need it.