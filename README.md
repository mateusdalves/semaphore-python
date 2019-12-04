### semaphore-python
Python code for my Comp. Sci. grade work about semaphores.

Dependencies:

anaconda

#### Setup

initialize conda environment
```
conda env create -f environment.yml
conda activate semaphore-python

```

#### Run

```
python ./src/main.py
```

##### Code

```python 
# An example python program using semaphore provided by the python threading module

import threading

import time

num_semaphore = int(input('Digite a quantidade de vagas do estacionamento'))

wait_time = int(input('Digite o tempo, em segundos, que os carros devem ficar estacionados'))

park_requests = 0

remove_requests = 0

parked = 0

removed = 0

parked_lock = threading.Lock()

removed_lock = threading.Lock()

available_parkings = threading.Semaphore(num_semaphore)


def park_car():
    available_parkings.acquire()

    global parked_lock

    parked_lock.acquire()

    global parked

    parked = parked + 1

    parked_lock.release()

    print(f"Total de Carros Estacionados: {parked}")


def remove_car():
    available_parkings.release()

    global removed_lock

    removed_lock.acquire()

    global removed

    removed = removed + 1

    removed_lock.release()

    print(f"Total de carros removidos: {removed}")


# Thread that simulates the entry of cars into the parking lot

def parking_entry():
    # Creates multiple threads inside to simulate cars that are parked

    while (True):
        time.sleep(1)

        incoming_car = threading.Thread(target=park_car)

        incoming_car.start()

        global park_requests

        park_requests = park_requests + 1

        print(f"Parking Requests: {park_requests}")


# Thread that simulates the exit of cars from the parking lot

def parking_exit():
    # Creates multiple threads inside to simulate cars taken out from the parking lot

    while( True) :
        time.sleep(wait_time)

        outgoing_car = threading.Thread(target=remove_car)

        outgoing_car.start()

        global remove_requests

        remove_requests = remove_requests + 1

        print(f"Remove Requests: {remove_requests}")


# Start the parking eco-system

parking_entry_thread = threading.Thread(target=parking_entry)

parking_exit_thread = threading.Thread(target=parking_exit)

parking_entry_thread.start()

parking_exit_thread.start()

```
