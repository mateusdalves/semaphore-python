import threading
import time
import random
import string

num_semaphore = 5

available_parkings = threading.Semaphore(num_semaphore)

parking_lots = {}

parking_lock = threading.Lock()
remove_lock = threading.Lock()


def park_car(name, parking_time):
    # acquire lock while using and release it when done, used to avoid parking in the same memory position.
    with parking_lock:
        parking_lots[name] = {
            'name': name,
            'time': time.time()
            }

        print(f'Carro {name} foi estacionado pela cancela {threading.current_thread().name}, tempo de espera {parking_time} segundos')


def remove_car(name):
    with remove_lock:
        left_time = parking_lots[name]['time']
        parking_lots.pop(name)
        print(f'Carro {name} removido do estacionamento pela cancela {threading.current_thread().name}. tempo estacionado: {time.time() - left_time}')


def parking_entry(car_name, park_time):

    while True:
        time.sleep(1)
        if available_parkings._value < 0:
            print('Estamos sem vagas no momento, aguardando 1 segundo.')
            time.sleep(1)

        elif available_parkings._value >= 0:
            print('Vaga disponivel, estaremos estacionando')
            parking_thread = threading.Thread(target=park_car(car_name, park_time))
            parking_thread.start()


def parking_exit(car_name, wait_time):
    while True:
        time.sleep(wait_time)

        remove_thread = threading.Thread(target=remove_car(car_name))
        remove_thread.start()


if __name__ == '__main__':
    car_name = ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(5))
    park_time = random.uniform(2., 10.)

    parking_entry_thread = threading.Thread(target=parking_entry)

    parking_exit_thread = threading.Thread(target=parking_exit)

    parking_entry_thread.start()

    parking_exit_thread.start()

