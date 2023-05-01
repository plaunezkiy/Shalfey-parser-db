import xmltodict
import requests
import re
import io
import gzip

# url = "https://altaivita.ru/sitemap.xml"
url = "https://domayurveda.ru/sitemap.4648067.xml.gz"

r = requests.get(url)
data = r.content
if ".gz" in url:
    file = io.BytesIO(data)
    data = gzip.GzipFile(fileobj=file).read()

data = xmltodict.parse(data)
pages = data["urlset"]["url"]

for page in pages:
    url = page["loc"]
    # pattern that extracts the path `http(s)://{host}/(path)`
    categories = ["folder", "tag"]
    products = ["product"]

    pattern = r"https?\:\/\/[\w.]+\/magazin\/(.*)"
    # print(page["loc"])
    path = re.findall(pattern, page["loc"])
    # print(page)
    if path:
        crumbs = path[0].strip("/").split('/')
        for category in categories:
            if category in url:
                print("Category", crumbs[-1])
        for product in products:
            if product in url:
                print("Product", crumbs[-1])

# print(cats)
