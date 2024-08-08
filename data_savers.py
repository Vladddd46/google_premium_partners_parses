import xml.etree.ElementTree as ET
import pandas as pd

def create_excel(partners_info, file_name):
	data = {
		"Name": [partner.name for partner in partners_info],
		"Country": [partner.country for partner in partners_info],
		"Partner Id": [partner.partner_id for partner in partners_info],
		"Website link": [partner.website_link for partner in partners_info]
	}

	df = pd.DataFrame(data)
	df.to_excel(file_name, index=False)
	print(f"Data successfully saved in excel: {file_name}")