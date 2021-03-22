from urllib.request import urlopen
from pathlib import Path
import json
import re
import os


API_ROOT = "https://vtes.dirtydevelopers.org/api/"
API_CRYPT = API_ROOT + "crypt"
API_SEARCH = API_ROOT + "search?name="
IMG_FOLDER = "C:/Users/Carlos/Pictures/vtes/vtes cards/"


def get_name(img_name):
    without_extension = img_name.rsplit('.', 1)[0]
    return re.sub("\(\d+\)", '', without_extension).strip()


def get_card_data(img_name, vamps_data):
    is_advanced = img_name.endswith("adv")
    pure_name = img_name[:-3] if is_advanced else img_name

    with urlopen(API_SEARCH + pure_name) as rs:
        possible_cards = json.loads(rs.read())[:2]

    if len(possible_cards) == 0:
        print("No results")
    elif len(possible_cards) > 1 and possible_cards[0]['card_type'] == 'Vampire':
        for vamp in possible_cards:
            if vamps_data[vamp['id']][1] == is_advanced:
                return vamp['id'], vamp['name']
        print("Advanced not equals for id " + possible_cards[0]['id'])
    else:
        return possible_cards[0]['id'], possible_cards[0]['name']
    return None, None


if __name__ == '__main__':
    crypt_data = {}
    print("Loading crypt data...")
    with urlopen(API_CRYPT) as crypt_rs:
        crypt_json = crypt_rs.read()
        data = json.loads(crypt_json)
        for vampire in data:
            crypt_data[vampire['id']] = (vampire['name'], vampire['advanced'])

    for folder in Path(IMG_FOLDER).iterdir():
        print("Processong " + folder.name)
        used_ids = set()
        for img in folder.iterdir():
            #print("\t" + img.name + " -> ", end='')
            img_name = get_name(img.name)
            card_id, card_name = get_card_data(img_name, crypt_data)
            if card_id:
                #print(card_id + " @ " + card_name)
                if card_id in used_ids:
                    print("\t" + img.name)
                else:
                    try:
                        img.rename(Path(img.parent, card_id + img.suffix))
                        used_ids.add(card_id)
                    except:
                        print("\t" + img.name)
    print("Done!")

