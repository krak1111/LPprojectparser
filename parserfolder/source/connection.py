from random import shuffle
import time
import subprocess

from requests.exceptions import ConnectionError
import requests_html as rh

from . import support_func as support

VPN_STATUS = 'expressvpn status'
VPN_LIST = 'expressvpn list all'
VPN_DISCONNECT = 'expressvpn disconnect'

def run_command(command):
    p = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
    return list([str(v).replace('\\t', ' ').replace('\\n', ' ').replace('b\'', '').replace('\'', '')
                .replace('b"', '')
                 for v in iter(p.stdout.readline, b'')])

def connect_alias(alias):
    """
    Подключение к серверу
    """
    command = f'expressvpn connect {alias}'
    t_output = run_command(command)

    if 'We were unable to connect to this VPN location' in t_output:
        raise ConnectionError
    if 'not found' in t_output:
        raise ConnectionError
    print(f'Successfully connected to {alias}')


@support.memorize
def get_recommend_vpn_list():
    """
    Получение списка alias серверов,
    рекомендованых expressvpn
    """
    vpn_list = run_command(VPN_LIST)
    vpn_output = []
    for vpn_item in vpn_list[3:]:
        vpn_item_list = vpn_item.split()
        if vpn_item_list[-1] == 'Y':
            vpn_output.append(vpn_item_list[0])
    shuffle(vpn_output)
    return vpn_output


@support.memorize
def get_all_vpn_list():
    """
    Получение списка alias всех серверов,
    """
    vpn_list = run_command(VPN_LIST)
    vpn_output = []
    for vpn_item in vpn_list[2:]:  # Первые две строки служебные
        vpn_item_list = vpn_item.split()
        vpn_output.append(vpn_item_list[0])
    shuffle(vpn_output)
    return vpn_output

@support.counter_deco
def get_request(url):
    """
    Формирование запроса на sciencedirect
    """
    max_attemps = 10
    attemp = 1
    # Допускается с одноко vpn 400 запросов подряд
    if get_request.numerator >= 400:
        change_vpn()
        get_request.numerator = 0
        print('Changed')
    session = rh.HTMLSession()
    # попытка соединится с сервером
    while True:
        try:
            request = session.get(url, headers=support.give_header())
            text = request.text
            if 'There was a problem providing the content you requested' in text:
                print('Banned')
                change_vpn()  # Ветка, если мы забанены
                attemp += 1
                session = rh.HTMLSession()
                time.sleep(2)
                continue
            break
        except ConnectionError:  # ветка, если нет соединения
            print('Lose connection')
            change_vpn()
            session = rh.HTMLSession()
            time.sleep(2)
            attemp += 1

    return request


def is_connected():
    """
    Проверка, подключены ли мы к vpn
    """
    if run_command(VPN_STATUS) == ['Not connected ']:
        return False
    return True

def change_vpn():
    """
    Смена vpn сервера, если входного параметра нет,
    то сервер выбирается из числа рекомендованных.
    Сервер из списка выбирается случайным образом.
    """
    print('Changing VPN, relax please')
    run_command(VPN_DISCONNECT)
    vpn_server = next_vpn_server()
    connect_alias(vpn_server)
    return True

@support.counter_deco
def next_vpn_server():
    """
    Выбор следующего vpn сервера,
    если указан флак True, ты сервер выбирается следующим в списке рекомендованных,
    в противном случае из списка всех серверов
    """
    if next_vpn_server.numerator > len(get_recommend_vpn_list.itemlist):
        if next_vpn_server.numerator > len(get_all_vpn_list.itemlist):
            next_vpn_server.numerator = 1
            return get_recommend_vpn_list.itemlist[0]
        return get_all_vpn_list.itemlist[next_vpn_server.numerator-1]
    return get_recommend_vpn_list.itemlist[next_vpn_server.numerator-1]



if __name__ == '__main__':
    # print('Reccomend servers\n', get_recommend_vpn_list(), '\n\n')
    # print('All servers\n', get_all_vpn_list())
    change_vpn()
    print(is_connected())
