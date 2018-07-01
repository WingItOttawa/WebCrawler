# <!-- omit in toc --> WebCrawler - Documentation

- [Project Setup](#project-setup)
- [Running the Crawler](#running-the-crawler)
    - [Notes](#notes)
- [Crawling Algorithm](#crawling-algorithm)
- [Design Plan (Deprecated)](#design-plan-deprecated)


# Project Setup

Note: these instructions are for macOS.
1. Navigate to your WingIt project folder
2. Clone the repository from here: https://github.com/WingItOttawa/WebCrawler
3. Install Scrapy using one of the methods listed under this installation guide (good luck this took a lot of effort): https://doc.scrapy.org/en/1.5/intro/install.html#mac-os-x. Try the Homebrew method first, but don’t hesitate to give the virtualenv one a shot. You might need to use `pip3` instead of `pip`. You should be able to check that Scrapy is installed using `which scrapy`.


# Running the Crawler

1. Navigate to the directory `WebCrawler/webcrawler`
2. Use the following command to run the crawler

```bash
scrapy crawl [crawler_name] -a name="[publication_name]" -a domain="[domain]" seed="[seed]" [-s CLOSESPIDER_PAGECOUNT=max_pages]
```

For example:
```bash
scrapy crawl crawler -a name="CBC" -a domain="www.cbc.ca" -a seed="http://www.cbc.ca/news" -s CLOSESPIDER_PAGECOUNT=100
```

To break it down:
- Using `-a` indicates a command line argument
- Using `-s` indicates a custom setting

3. Results of the crawl can be found in the `WebCrawler/webcrawler/data/[publication_name]` directory (see [Notes](#notes) for details)


## Notes
- In the future, storage will be accomplished using a database instead of `.html` files
- Crawling algorithm described in the [Crawling Algorithm](#crawling-algorithm) section still needs implementing


# Crawling Algorithm
1. If it hasn’t been crawled before, crawl.
2. If it has been crawled before but is less than two days old, crawl.
3. Otherwise, don’t crawl.

After a website has been crawled, the Title, Javascript and HTML is then removed, and the remaining text is then written to a file.
After all of the files have been written for a publication source, similar text between files is found and is assumed to be redundant, and so the similar texts would be removed from all of the files.
In theory, this would increase the chances of the resulting article text to only contain article contents.

# Design Plan (Deprecated)
Here’s the way I see this being designed. Scrapy has two basic customizable components: the `start_urls` (i.e. the initial seeds for the crawler), and the `parse` function. In order to run the crawler (also known as a spider), we use a command line argument like this: `scrapy crawl spider_name`. The neat thing is that we can pass arguments that can be used for customization. So we should be able to write a single spider file, then pass in each news publication’s base URL for crawling (as well as the domain limiter to prevent it from crawling unrelated sites), something like this:

```bash
scrapy crawl crawler -a name="CBC" -a domain="www.cbc.ca" -a seed="http://www.cbc.ca/news" -s CLOSESPIDER_PAGECOUNT=100
```

More info can be found [here](https://docs.scrapy.org/en/latest/topics/spiders.html#spider-arguments).
