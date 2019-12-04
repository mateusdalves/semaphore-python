import threading
import time
import random
import string


# function to 'park cars' in the parking lots array
def park_car():
    # acquire the semaphore, -1 to value
    parking_spaces.acquire()
    # here the thread is locked to avoid parking the same car twice by another thread
    with parking_lock:
        car_name = ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(8))
        parking_lots.append(car_name)
        print(f'Carro {car_name} foi estacionado pela {threading.current_thread().name}')


def remove_car():
    # release the semaphore, +1
    parking_spaces.release()
    # the thread is locked once again to avoid errors trying to remove the same value from array twice.
    with remove_lock:
        car_name = parking_lots[-1]
        parking_lots.remove(car_name)
        print(f'Carro {car_name} removido do estacionamento pela {threading.current_thread().name}.')


def parking_entry():
    while True:
        # global value to name threads.
        global thr

        time.sleep(1)

        # if there is a parking space available, the car will be parked, otherwise, it will not.

        if parking_spaces._value <= 0:
            print('Estamos sem vagas no momento, aguardando 1 segundo.')
            time.sleep(1)
            parking_entry()

        elif parking_spaces._value > 0:
            print('Vaga disponivel, estaremos estacionando')
            # Initializing the parking thread.
            parking_thread = threading.Thread(target=park_car)
            parking_thread.name = f'Cancela-{thr}'
            thr += 1
            parking_thread.start()



def parking_exit():
    # Random float to simulate parking time
    global thr
    park_time = float(random.uniform(1., 5.))
    while True:
        time.sleep(park_time)
        # initializing the remove car thread
        remove_thread = threading.Thread(target=remove_car)
        thr -= 1
        remove_thread.name = f'Cancela-{thr}'
        remove_thread.start()


if __name__ == '__main__':
    num_semaphore = 5

    parking_spaces = threading.Semaphore(num_semaphore)

    parking_lots = []

    parking_lock = threading.Lock()

    remove_lock = threading.Lock()

    global thr

    thr = 0

    parking_entry_thread = threading.Thread(target=parking_entry)

    parking_exit_thread = threading.Thread(target=parking_exit)

    # start parking cars
    parking_entry_thread.start()

    # start removing 'cars' from parking
    parking_exit_thread.start()


