from bs4 import BeautifulSoup
from PartnerCard import PartnerCard


class Parser:
    @staticmethod
    def parse_partners_info(content):
        # Parse the HTML content
        soup = BeautifulSoup(content, "html.parser")

        # Find all partner-card elements
        partner_cards = soup.find_all("a", class_="partner-card ng-star-inserted")

        partners_info = []
        for card in partner_cards:
            href = card["href"].split("/")[-1]
            name = card.find("div", class_="partner-card__title").get_text(strip=True)
            country = (
                card.find("div", class_="partner-card__country")
                .get_text(strip=True)
                .replace("location_on", "")
                .strip()
            )

            partners_info.append(
                PartnerCard(name=name, country=country, partner_id=href)
            )
        return partners_info
