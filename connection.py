from random import choice
import subprocess
import time

from requests.exceptions import ConnectionError
import requests_html as rh
from expressvpn import wrapper


from support_func import counter_deco
from settings import HEADERS

VPN_STATUS = 'expressvpn status'
VPN_LIST = 'expressvpn list all'

def get_recommend_vpn_list():
    """
    Получение списка alias серверов,
    рекомендованых expressvpn
    """
    vpn_list = wrapper.run_command(VPN_LIST)
    vpn_output = []
    for vpn_item in vpn_list[2:]:
        vpn_item_list = vpn_item.split()
        if vpn_item_list[-1] == 'Y':
            vpn_output.append(vpn_item_list[0])

    return vpn_output

def get_all_vpn_list():
    """
    Получение списка alias всех серверов,
    """
    vpn_list = wrapper.run_command(VPN_LIST)
    vpn_output = []
    for vpn_item in vpn_list[2:]:
        vpn_item_list = vpn_item.split()
        vpn_output.append(vpn_item_list[0])

    return vpn_output

@counter_deco
def get_request(url, headers):
    """
    Формирование запроса на sciencedirect
    """
    max_attemps = 10
    attemp = 1
    # Допускается с одноко vpn 200 запросов подряд
    if get_request.numerator >= 200:
        change_vpn(recommend=False)
        get_request.numerator = 0
        print('Changed')
    session = rh.HTMLSession()
    # попытка соединится с сервером
    while True:
        try:
            request = session.get(url, headers=headers)
            text = request.html.text
            if 'There was a problem providing the content you requested' in text:
                print('Banned')
                change_vpn()  # Ветка, если мы забанены
                if attemp >= max_attemps:
                    raise ConnectionError
                attemp += 1
                continue
            break
        except ConnectionError:  # ветка, если нет соединения
            print('Lose connection')
            change_vpn()
            if attemp >= max_attemps:
                raise ConnectionError
            attemp += 1

    return request


def is_connected():
    """
    Проверка, подключены ли мы к vpn
    """
    if wrapper.run_command(VPN_STATUS) == ['Not connected ']:
        return False
    return True

def change_vpn(recommend=True):
    """
    Смена vpn сервера, если входного параметра нет,
    то сервер выбирается из числа рекомендованных.
    Сервер из списка выбирается случайным образом.
    """
    wrapper.disconnect()
    if recommend:
        vpn_list = get_recommend_vpn_list()
    else:
        vpn_list = get_all_vpn_list()
    choosen_vpn = choice(vpn_list)
    wrapper.connect_alias(choosen_vpn)
    return True



if __name__ == '__main__':    
    # print('Reccomend servers\n', get_recommend_vpn_list(), '\n\n')
    # print('All servers\n', get_all_vpn_list())
    change_vpn()
    print(is_connected())
