#Ancillary Service

## Product Requirement Overview:

Build a “service” that does the following three jobs:

● Receive packets of data in real-time and pass this on to an ancillary service for processing.

● Collate the output from the ancillary service for a particular Primary Resource ID into a single data packet.

● Once all data packets for a particular Resource are received, pass on the collated output data further for downstream processing with minimum latency by calling a webhook.


## Assumptions
* The service needs to be highly scalable. 
  * Hence, we will need a Redis instance. For the purpose of assignment, I have used in-memory cache. 
  * Ancillary Service is a long-running job 'asynchronous' job. It can be used in a 'synchronous' manner also but that would mean we cannot scale this service for high traffic rate.


---
## System Requirements
python 3.7 or higher


> Development setup (for Ubuntu/Mac):
### Open Terminal :

* Ubuntu
  * `sudo apt-get install python-pip`
* MAC 
  
  This command should install python3 and pip3.
  * `brew install python@3.7`


### Clone Project to your directory

`git clone https://github.com/achugh95/cran.git`

`cd cran`

### Check python version on your development system

`python --version or python3 --version`


> Setup environment:
### 1. Create a virtual environment

  - `python3 -m venv <path>`

### 2. Activate virtual environment

  - `source <path_to_virtual_environment>/bin/activate`

### 3. Install requirements. Use the package manager pip to install the dependencies. 
`pip3 install -r requirements.txt`


### 4. Run migrations

`python3 manage.py makemigrations`

`python3 manage.py migrate`

### 5. Run Project
Open terminal and run the following commands:

`python3 manage.py runserver`


---

### Sample command to run tests
```
python3 ancillary/tests.py
```

### Sample Curl for API trigger
```
curl --location --request POST 'localhost:8000/api/v1/ancillary/packet/send-data/' \
--header 'Content-Type: application/json' \
--data-raw '{
    "resource_id": 101,
    "payload": "Bat Ball",
    "packet_index": 1,
    "last_chunk_flag": true
}'
```