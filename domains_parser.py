import re
import json



def main():
	"""
		Парсинг JSON'а со списком областей наук и подобластей

		Вид:
			primary : {
				"Primary url_form_name" :{
					name : 'primary name',
					secondary : {
						"first Domain_url_form" или одно слово без кавычек если domain в одно слово :{
							name : "Domain name" или domain (если одно слово),
							tertiary : {
								"Subdomain_url_form" или одно слово без кавычек если domain в одно слово :{
									name : "Domain name" или domain (если одно слово),
									sid : 12345
								},
							},
						},
					},
				},
				etc...
			}
	"""
	to_json_pattern = re.compile(r'\"{0}(?P<word>[a-zA-Z0-9]+):', re.S)

	with open('domains.json', 'r', encoding = 'utf-8') as file:
		i = 0
		domains_json = ''

		for line in file:
			p = to_json_pattern.sub(r'"\g<word>":' , line)
			domains_json += p
	
	json_loader = json.loads(domains_json)

	print(json_loader)

			
if __name__ == '__main__':
	main()