import threading
import time
import random
import string


def park_car():
    available_parkings.acquire()
    # acquire lock while using and release it when done, used to avoid parking in the same memory position.
    with parking_lock:
        car_name = ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(8))
        parking_lots.append(car_name)
        print(f'Carro {car_name} foi estacionado pela {threading.current_thread().name}')


def remove_car():
    available_parkings.release()
    with remove_lock:
        car_name = parking_lots[-1]
        parking_lots.remove(car_name)
        print(f'Carro {car_name} removido do estacionamento pela {threading.current_thread().name}.')


def parking_entry():
    while True:
        global thr

        time.sleep(1)
        if available_parkings._value <= 0:
            print('Estamos sem vagas no momento, aguardando 1 segundo.')
            time.sleep(1)
            parking_entry()

        elif available_parkings._value > 0:
            print('Vaga disponivel, estaremos estacionando')
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
        remove_thread = threading.Thread(target=remove_car)
        thr -= 1
        remove_thread.name = f'Cancela-{thr}'
        remove_thread.start()


if __name__ == '__main__':
    num_semaphore = 5

    available_parkings = threading.Semaphore(num_semaphore)

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


