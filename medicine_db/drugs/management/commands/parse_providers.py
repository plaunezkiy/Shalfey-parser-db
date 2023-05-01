from django.core.management.base import BaseCommand, CommandError
from drugs.models import Provider, XMLSiteMap
from tqdm import tqdm
import requests
import re


class Command(BaseCommand):
    """Parses the sitemaps (if any) found in robots.txt for websites in 'providers.txt'"""
    request_headers = { 'User-Agent': 'Mozilla/5.0 (Windows NT 6.0; WOW64; rv:24.0) Gecko/20100101 Firefox/24.0' }

    def get_num_file_lines(self, fname):
        return sum(1 for _ in open(fname, 'r'))

    def handle(self, *args, **options):
        fname = 'providers.txt'
        flength = self.get_num_file_lines(fname)
        # load the file
        with open(fname, "r", encoding="utf-8") as providers:
            # progress bar for cosmetic purposes
            progress_bar = tqdm(desc="Parsing", total=flength)
            # go over providers (line by line)
            for provider_url in providers:
                progress_bar.update(1)
                # strip of spaces and newlines
                provider_url = provider_url.strip()
                # check if the provider already exists
                (provider, created) = Provider.objects.get_or_create(url=provider_url)
                # log status
                # print("Created" if created else "Updated", provider_url)
                # compile robots.txt url
                robots_url = f"{provider_url}/robots.txt"
                resp = requests.get(robots_url, headers=self.request_headers)
                # if the page exists, check if sitemaps present
                if resp.ok:
                    # try to get all sitemaps
                    sitemaps = re.findall("Sitemap: (.*)", resp.text)
                    # if none found, continue
                    if not sitemaps:
                        continue
                    # for each found sitemap, create a reference
                    for sitemap_url in sitemaps:
                        XMLSiteMap.objects.get_or_create(url=sitemap_url, parent=provider)
            progress_bar.close()
            self.stdout.write("Successfully parsed all providers", self.style.SUCCESS)
