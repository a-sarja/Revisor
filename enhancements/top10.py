from bs4 import BeautifulSoup
from requests import get
html = "https://www.av-comparatives.org/test-results/"

page = get(html)
soup = BeautifulSoup(page.text, 'html.parser')
div = soup.body.find("section", id="resultsection").table.tbody
result = []
for t in div.find_all('tr'):

    for span in t.find_all("span",class_ = "vendorname"):
             result.append((span.find("a").contents[0]).strip())

print(result[:10])