# DW Tournament Planner

This is a Python module which uses the PostgreSQL database to keep track of players and matches in a game tournament.
<br>

The game tournament will use the Swiss system for pairing up players in each round: players are not eliminated, and each player should be paired with another player with the same number of wins, or as close as possible.
<br>

This project, the second in [Udacity’s Full Stack Web Developer Nanodegree](https://www.udacity.com/course/nd004), focuses on defining the database schema (SQL table definitions), and writing the code that will use it.
<br>
## How to Run

1. First, you need to install [VirtualBox](https://www.virtualbox.org/wiki/Downloads) and [Vagrant](https://www.vagrantup.com/downloads) on your machine.

2. Then, you'll need to clone this [repo](https://github.com/udacity/fullstack-nanodegree-vm) to your local machine.

3. Go to the vagrant directory in the cloned repository, then open a terminal window and type <b>vagrant up</b> to launch your virtual machine. This will take some time in your first run, because it needs to install some dependencies.

4. Once it is up and running, type <b>vagrant ssh</b> to log into it. This will log your terminal in to the virtual machine, and you'll get a Linux shell prompt. 

5. Copy the tournament directory in this repository and paste in the vagrant directory. This will overwrite the existing tournament directory.

6. Type the following commands on your virtual machine: <b>cd /vagrant/tournament</b> -> <b>psql</b> -> <b>create database tournament;</b> -> <b>\c tournament</b> -> <b>\i tournament.sql</b> -> <b>\q</b>

7. Finally, you can now run the tests for the project by typing <b>python tournament_test.py</b> on your virtual machine. The test results will be displayed on your terminal.
