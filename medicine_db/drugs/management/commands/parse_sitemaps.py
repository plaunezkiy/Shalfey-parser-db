from django.core.management.base import BaseCommand, CommandError
from drugs.models import Provider, XMLSiteMap, ProviderCategory, Drug
from tqdm import tqdm
import requests
import re
import xmltodict
from bs4 import BeautifulSoup
import requests
import io
import gzip


class Command(BaseCommand):
    """"""
    request_headers = { 'User-Agent': 'Mozilla/5.0 (Windows NT 6.0; WOW64; rv:24.0) Gecko/20100101 Firefox/24.0' }

    def handle(self, *args, **options):
        providers = Provider.objects.filter(excluded=False).exclude(sitemap__isnull=True)
        for provider in providers:
            print(provider)
            sitemaps = provider.sitemap.all()
            for sitemap in sitemaps:
                if sitemap.excluded:
                    print("excluded")
                    continue
                if sitemap.sitemap_parser_code:
                    print("done")
                    continue
                self.parse_sitemap(sitemap.url, provider)
                quit()

        # print(len(providers))
    
    def parse_sitemap(self, map_url, provider):
        # return
        r = requests.get(map_url.strip())
        print(map_url)
        # print(r.headers)
        data = r.content
        if ".gz" in map_url:
            file = io.BytesIO(data)
            data = gzip.GzipFile(fileobj=file).read()

        data = xmltodict.parse(data)
        # print(data.keys())
        # categories available(
            # ["ayurveda", "kosmetika", "suveniry-iz-indii", 
            #   "blagovoniya", "aroma-maslo", "healthy-food", 
            #   "indian-spices", "ayurvedicheskiy-vrach"]
        # )
        pages = data["urlset"]["url"]
        categories = ["ayurveda", "kosmetika", "suveniry-iz-indii", 
                      "blagovoniya", "aroma-maslo", 
                      "indian-spices"]
        # cat = {cat: {} for cat in categories}
        for page in pages:
            page_url = page["loc"]
            pattern = r"https?\:\/\/[\w.]+\/(.*)"
            path = re.findall(pattern, page_url)
            if path:
                crumbs = path[0].strip('/').split('/') 
                for category in categories:
                    if category in crumbs:
                        Drug.objects.get_or_create(slug=crumbs[-1], url=page_url, provider=provider)
                        # if len(crumbs) > 1:
                        #     if cat[category].get(crumbs[1], None):
                        #         cat[category][crumbs[1]] += 1
                        #     else:
                        #         cat[category][crumbs[1]] = 1
            continue
            ####################################
            # All insertable code should be below
            ####################################
            categories = ["folder", "tag"]
            products = ["product"]
            # pattern that extracts the path `http(s)://{host}/(path)`
            # print(page["loc"])
            if path:
                crumbs = path[0].strip("/").split('/')
                for category in categories:
                    if category in page_url:

                        print("Category", crumbs[-1])
                        ProviderCategory.objects.get_or_create(slug=crumbs[-1], url=page_url, provider=provider)
                for product in products:
                    if product in page_url:
                        print("Product", crumbs[-1])
                        Drug.objects.get_or_create(slug=crumbs[-1], url=page_url, provider=provider)
                        # if cats.get(crumbs[0], None):
                        #     cats[crumbs[0]] += 1
                        # else: cats[crumbs[0]] = 1
        # print(cat)
        # for c in categories:
        #     print(c, cat[c])
        #     print()
