# Fetch Take-Home Exercise — Site Reliability Engineering
## Bryan Song

Python script that takes in a yaml file as input, parses through input to make continuous requests to endpoints within the file.
Steps to Build:
- Enviornment setup
- Running the script

## Enviornment Setup
1. You will need to have Python3 installed on your machine.
    - Download Python3.* for your type of machine here: https://www.python.org/downloads/
2. Clone the github repository.
3. Create a python virtual enviornment
    - In the same folder as the cloned repository: ```python -m venv /path/to/new/virtual/environment```
4. Activate the enviornment by typing in the console: ```source /path/to/new/virtual/environment.../Scripts/activate```
5. After the virtual enviornment is activated, install requirements via the requirements.txt file that has been cloned from the repository: : ``` pip install -r /path/to/requirements.txt```

Now you're ready to run the script!

## Running the Script
1. Find the location of ```main.py``` from the cloned repository while in the virtual enviornment console.
2. Run the script by using python in virtual enviornment that was just set up: ```python main.py /path/to/input.yaml```
    - Make sure there is one argument when running the python file which points to file location of the input yaml file. An example input file has been included in the repository.

The script will continously complete the requests every 15 seconds.
Use ```ctrl+c``` to exit the program

