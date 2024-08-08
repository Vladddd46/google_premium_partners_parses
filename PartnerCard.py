class PartnerCard:

	def __init__(self, name, country, partner_id, website_link=None):
		self.name = name
		self.country = country
		self.partner_id = partner_id
		self.website_link = website_link

	def __str__(self):
		return f"Name: {self.name} | Country: {self.country} | Partner Id: {self.partner_id} | Website link: {self.website_link}"

	def __repr__(self):
		return f"Name: {self.name} | Country: {self.country} | Partner Id: {self.partner_id} | Website link: {self.website_link}"

	def to_dict(self):
		return {
			"name": self.name,
			"country": self.country,
			"partner_id": self.partner_id,
			"website_link": self.website_link
		}
