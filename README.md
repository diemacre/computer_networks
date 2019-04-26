# LINK-STATE ROUTING ALGORITHM MANUAL

## AUTHOR: DIEGO MARTIN CRESPO

### INSTRUCTIONS

####Requirements:
* Python 3
* Pip
* Python libraries:
	* Pandas (in terminal: “pip install pandas”)
	* Networkx(in terminal: “pip install networkx” )

####STEPS:
1. Save and decompress the downloaded file
2. Open the decompressed folder in the terminal
3. To execute it enter: “python project.py” in the terminal
4. Enter 1 in the terminal
5. Enter the name of the file with the matrix located in folder ./data. Example: “example.txt”
	*The file with the matrix should have the following form: 
		*0 2 10 1 -1
		*2 0 8 7 9 
		*10 8 0 -1 4 
		*1 7 -1 0 4 
		*-1 9 4 4 0
	In this example there are 5 routers. The matrix is symmetrical as the graph should be undirected. The separation of the matrix should be with spaces and routers that are not connected should have cost -1.
	When the file is loaded you should see a plot of the graph. To continue, close the prompted window (the graph draw).
	Then use the commands 2-5 to use the program with the loaded file. For more detail explanation of each command see this report or commented code.
6. Follow the prints/instructions of each command when used
7. To exit enter command 6