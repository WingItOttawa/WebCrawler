# <!-- omit in toc --> WebCrawler - Documentation

- [Project Setup](#project-setup)
- [Running the Crawler](#running-the-crawler)
- [Database Integration](#database-integration)
    - [`master` collection](#master-collection)
    - [`filter` collection](#filter-collection)
    - [`word-frequency` collection](#word-frequency-collection)
    - [`leaning-probability` collection](#leaning-probability-collection)
- [Crawling Algorithm](#crawling-algorithm)
- [Next Steps](#next-steps)


# Project Setup

Note: these instructions are for macOS.
1. Navigate to your WingIt project folder
2. Clone the repository from here: https://github.com/WingItOttawa/WebCrawler
3. Install Scrapy using one of the methods listed under this installation guide (good luck this took a lot of effort): https://doc.scrapy.org/en/1.5/intro/install.html#mac-os-x. Try the virtualenv method first, but don’t hesitate to give the Homebrew one a shot. You might need to use `pip3` instead of `pip`. You should be able to check that Scrapy is installed using `which scrapy`.


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


# Database Integration

We will be using Firebase as a host and using Firestore as a database.

## `master` collection

| docId | title | url | content | wing | wing-value |
| ----- | ----- | --- | ------- | ---- | --------- |

The [`master`](#master-collection) collection contains every document that is crawled by the web crawler, post filtering of unnecessary content by the [`filter`](#filter-collection) collection.

## `filter` collection

| docId | title | url | content |
| ----- | ----- | --- | ------- |

The [`filter`](#filter-collection) collection is a temporary space to store documents that have just been crawled. Once a significant number of documents has been crawled (e.g. 100), the entries are checked for common phrases in order to eliminate things like navbars, footers, ads, etc. that are present on multiple pages for a particular news publication. Then, they are uploaded in bulk to the [`master`](#master-collection) collection, and the [`filter`](#filter-collection) collection is emptied.

## `word-frequency` collection

| word | far-left | moderate-left | centrist | moderate-right | far-right |
| ---- | -------- | ------------- | -------- | -------------- | --------- |

The [`word-frequency`](#word-frequency-collection) collection contains a list of every unique word that appears in every article in the [`master`](#master-collection) collection, as well as a value indicating how likely it is to appear in an article of a given political leaning.

## `leaning-probability` collection

| leaning | probability |
| ------- | ----------- |

The [`leaning-probability`](#leaning-probability-collection) collection is used to store the probability of any given article having a given political leaning.


# Crawling Algorithm
1. If it hasn’t been crawled before and is less than two weeks old, crawl.
2. If it has been crawled before but is less than two days old, crawl.
3. Otherwise, don’t crawl.


# Next Steps
- [ ] Modify crawler to integrate with Firestore database instead of storing in `.html` files
- [ ] Implement the crawling algorithm described in the [Crawling Algorithm](#crawling-algorithm) section