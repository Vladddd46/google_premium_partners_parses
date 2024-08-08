from PageScrapper import PageScrapper
from Parser import Parser
from PartnerCard import PartnerCard
import os
import json
from config import *
from utils import *
from data_savers import *


# returns raw html string, where info about partners is stored
def get_raw_html(page_scrapper):
    raw_html = ""
    if USE_FILE == True:
        if not os.path.exists(FILENAME):
            page_scrapper.download_html(filename=FILENAME)
        with open(FILENAME, "r", encoding="utf-8") as file:
            raw_html = file.read()
    else:
        raw_html = page_scrapper.get_html()
    return raw_html


def read_partners_cards_from_json(filename):
    partners_info = []
    if file_exist(filename) == True:
        data = read_json(filename)
        partners_info = [
            PartnerCard(i["name"], i["country"], i["partner_id"], i["website_link"])
            for i in data
        ]
    return partners_info


def remove_partners_card_duplicates(partners_cards):
    # first go partners where website_link is not null
    # this is done in order to remove duplicates without websitelinks
    partners_cards = sorted(partners_cards, key=lambda card: card.website_link is None)
    seen_names = set()
    unique_partner_cards = []
    for card in partners_cards:
        if card.name not in seen_names:
            unique_partner_cards.append(card)
            seen_names.add(card.name)
    return unique_partner_cards


def cache_data(cache_filename, partners_info):
    partners_info += read_partners_cards_from_json(cache_filename)
    partners_info = remove_partners_card_duplicates(partners_info)
    save_json(cache_filename, [i.to_dict() for i in partners_info])
    return partners_info


def get_partners_info():
    page_scrapper = PageScrapper(LINK, PAGES_TO_SCRAP)
    raw_html = get_raw_html(page_scrapper)
    partners_info = Parser.parse_partners_info(raw_html)

    print(
        f"==Start retrieving partners website links. Number of partners found:{len(partners_info)}=="
    )

    # saving partners info without website links
    partners_info = cache_data(CACHE_FILENAME, partners_info)

    iteration_num = 0
    for i in range(len(partners_info)):
        iteration_num += 1
        print(
            f"#{iteration_num} Retrieving website link for partner={partners_info[i].name}"
        )
        if partners_info[i].website_link == None:
            partners_info[i].website_link = page_scrapper.get_partner_link(
                partners_info[i].partner_id
            )
        if iteration_num % 100 == 0:
            partners_info = cache_data(CACHE_FILENAME, partners_info)
    partners_info = cache_data(CACHE_FILENAME, partners_info)
    partners_info = sorted(partners_info, key=lambda card: (card.country, card.name))
    return partners_info


def main():
    partners_info = get_partners_info()
    create_excel(partners_info, RESULT_FILENAME)


if __name__ == "__main__":
    main()
