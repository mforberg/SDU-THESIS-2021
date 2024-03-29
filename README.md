# SDU-THESIS-2021
Master Thesis in Software Engineering at University of Southern Denmark Spring 2021

## Setup
The setup the project consists of the user installing Java 8 (1.8), cloning the Evocraft repository using the git command "git clone https://github.com/real-itu/Evocraft-py", installing grpc with the following command "pip install grpcio", and lastly installing scikit-learn: "pip install -U scikit-learn". There might be more common installations like google and tqdm the user has to install. The attached code should be placed inside the evocraft-py folder to run properly.

## Running the Algorithm
To run the algorithm, the user needs Java 8 as their active JDK and PyCharm. The user needs to locate and go to the folder named "Evocraft-py" in a command prompt. In the command prompt, the following is typed to start the server: "java -jar spongevanilla-1.12.2-7.3.0.jar". Given it is the first time running the Jar file, it will create an eula.txt file. The user manually needs to edit the file, so that the file reads "eula=true", and the command for starting the server can be executed again. The server is running when it prints "[... INFO]: Done ...". \\
When the server is running, the algorithm can be run by opening the project in PyCharm and running the "main.py" file. It might be necessary to change the folders to "source root" within PyCharm.
The algorithm uses four hardcoded coordinates to specify the cube it shall run the algorithm on. The coodinates can be found and modified in the file located at: \newline "Evocraft-py/SDU-THESIS-2021/content\_generation/variables/map\_variables.py". \newline In order to find a specific location to run the algorithm on, the user needs to purchase Minecraft and set their version to 1.12.2, then opening the game, go into multiplayer and join the server with "localhost" as the IP. To find the coordinates inside Minecraft, the user can press F3 while playing the game to see their current coordinates
