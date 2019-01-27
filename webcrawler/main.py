import json
from subprocess import Popen

closespider_pagecount="100"
crawler_seeds_fp = "crawler_seeds.json"
crawler_dir='scrapy'

if crawler_seeds_fp:
    with open(crawler_seeds_fp, 'r') as f:
        crawler_seeds = json.load(f)

for content in crawler_seeds["contents"]:
    publication = content["publication"]
    domain = content["domain"]
    for seed in content["seeds"]:
        args = ['scrapy', 'crawl', 'crawler', '-a', 'name=' + publication, '-a', 'domain=' + domain,
                '-a', 'seed=' + seed, '-s', 'CLOSESPIDER_PAGECOUNT=' + closespider_pagecount]
        Popen(args, cwd=crawler_dir)