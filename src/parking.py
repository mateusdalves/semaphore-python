import threading
import time
import random
import string


def park_car():
    car_name = ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(8))
    parking_lots.append(car_name)
    print(f'Carro {car_name} foi estacionado')


def remove_car():
    car_name = parking_lots[-1]
    parking_lots.remove(car_name)
    print(f'Carro {car_name} removido do estacionamento.')


def parking_entry():
    if len(parking_lots) == parking_spaces:
        print('Estamos sem vagas no momento, aguardando 1 segundo.')
        time.sleep(1)
        parking_entry()
    elif parking_spaces > len(parking_lots) >= 0:
        print('Vaga disponivel, estaremos estacionando')
        park_car()


def parking_exit():
    time.sleep(park_time)

    remove_car()


if __name__ == '__main__':

    parking_spaces = 5

    parking_lots = []

    num_cars = 200

    park_time = float(random.uniform(1., 5.))

    start_time = time.time()

    while num_cars > 0:
        parking_entry()
        parking_exit()
        num_cars -= 1

    print(f'Finished Parking, time: {time.time() - start_time}')
