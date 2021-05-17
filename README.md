# PedCupSim
Repository of the paper submitted to ECSA 2021

### Creating CAPS Models

CAPS modeling tool can be downloaded from http://caps.disim.univaq.it

### Models and Configurations 

+ config_model1.json:  with QR in the entrance, RFID and camera
in the corridor and people counter in the exits

+ config_model2.json:  with QR in the entrance, RFID and camera in the
corridor and QR in the exit

+ config_model3.json: With people counter in the entrance, RFID and camera in the corridor
and people counter in the exits

+ config_model4.json: with People Counter in the entrance, RFID and cameras in the corridors
and QR Reader in the exits

+ config_model5.json: with QR Reader in the entrance, camera in the corridors and
people counter in the exits

+ config_model6.json: with QR reader in the entrance, RFID readers in the corridors
and people counter in the exits

+ config_model7.json: People counter in the entrance, camera in the corridors
and people counter in the exits

+ config_model8.json: People counter in the entrance, RFID in the corridors and
QR reader in the exits


### Parameters Used

#### Scenario 1, 

qoe_penalty = 10
qos_penalty = 5
qos_goal = 150.0
qoe_goal = 1200


#### Scenario 2

qoe_penalty = 10
qos_penalty = 10
qos_goal = 150
qoe_goal = 800

#### Scenario 3

qoe_penalty = 5
qos_penalty = 10
qos = 100
qoe = 400

#### Scenario 4

qoe_penalty = 15
qos_penalty = 3
qos = 125
qoe = 100

### Analysis

+ settings.conf contains all the settings for performing Agent to IoT Data
Composition and further to perform result analysis
+ ped_to_cup_generator.py imlements the Agent IoT Data Composition algorithm dicussed in the paper. It converts the excel
data obtained from the ABBS process to IoT data using a config file available in the *config_dir*
+ Data_Loader_Energy.py coverts the simulated data into aggregated uniform time
interval datasets
+ Data_Loader_Sensor_Data.py parses the log.txt obtained from CupCarbon simulation 
and extracts the data read by the server for different instants of time.
+ resutls_analyzer.py implements the Trade off analysis algorithm discussed in the paper
and it generates plots for the specified scenario under *plots* directory.
 

### Scenario Results Pair

+ S1 : M3_C1
+ S2 : M5_C1
+ S3 : M5_C1
+ S4 : M3_C1

### Requirements 

+ Python 3.7 or higher - https://www.python.org/downloads/
+ Pandas - https://pandas.pydata.org/pandas-docs/stable/getting_started/install.html
+ plotly - https://pypi.org/project/plotly/

### Contact

For any questions feel free to contact: karthik.vaidhyanathan@univaq.it
