import ConfigParser
import os
import sys
from . import const

# minimum topic for keyword weight (0-1)
TOPIC_KEYWORD = 0.65
# minimum desired relevancy (0-1)
RELEVANCE_SCORE = 0.6
# minimum fitness to extract top keyword from web pages
MIN_FITNESS_EXTRACT = 0.7
WEBPAGE_FITNESS_BIAS = 0.05
# weighting word from diff position
WEIGHT_TITLE = 2
WEIGHT_TEXT = 1
FITNESS_ALGORITHM = 'wt'

# -- SEARCH ENGINE CONFIG --
GOOGLE_SEARCH_API = 'AIzaSyAzSBR81G4qA0EF6Knnn_mHCYrvyTUdpyA'
GOOGLE_CSE_ID = '011614286650078081785:zlrnesfpjks'
BING_SUBS_KEY = '753b5658d01347639bd51317c9602876'
# -- SEARCH ENGINE CONFIG --

# -- Genetic Config --
GA_MAX_GENERATION = 100
GA_MAX_SURVIVED_PAGES = 20
GA_MAX_CRAWLING_QUEUE = 40
GA_MUTATION_RATE = 0.7
# -- end Genetic Config --

# -- SOS Config --
SOS_MAX_GENERATION = 200
SOS_MAX_FITNESS = 0.7
SOS_MAX_GEN = 5
# -- end SOS Config --

# -- BeautifulSoup Config --
MIN_URL_LENGTH = 50
MIN_NEWS_WORD_COUNT = 500
DECOMPOSE_SELECTOR = [
    '.detail_tag', '.lihatjg', '.banner-ads', '.article-tags', '.wpgal'
    '.text-muted.small', '.linksisip', 'figure', '.baca-juga', '.seamless-ads', 
    '.article-ad', '.article-content-body__item-page_hidden', '.inner-link-baca-juga',
    '.foto_detail_caption','.foto_detail'
]
TEXT_SELECTOR = [
    'article', '.artikel', '.post-content', '.article', '.article-content',
    '.single-content', '.content_detail', '#detikdetailtext', '.content',
    '.article-content-body__item-content', '.read__content'
]

# -- end BeautifulSoup Config --


def makeConfig():
    print "Creating GACrawler Configs..."
    gapi = raw_input('Google Search API Key: ')
    gcse = raw_input('Google Custom Search Engine Key: ')
    bing = raw_input('Bing Subscription Key: ')

    config = ConfigParser.ConfigParser(allow_no_value=True)
    config.optionxform = str
    config.add_section("API")
    config.set("API", "google_search_api", gapi)
    config.set("API", "google_cse_id", gcse)
    config.set("API", "bing_subs_key", bing)

    config.add_section("crawler")
    config.set("crawler",
               "; WARNING, Only use this if you know what you're doing.")
    config.set(
        "crawler",
        "; You can run gacrawler-init again anytime to restore the default options."
    )
    config.set("crawler", "relevance_score", RELEVANCE_SCORE)
    config.set("crawler", "topic_keyword", TOPIC_KEYWORD)
    config.set("crawler", "min_fitness_extract", MIN_FITNESS_EXTRACT)
    config.set("crawler", "webpage_fitness_bias", WEBPAGE_FITNESS_BIAS)
    config.set("crawler", "weight_title", WEIGHT_TITLE)
    config.set("crawler", "weight_text", WEIGHT_TEXT)
    config.set(
        "crawler",
        "; Fitness Algorithm: wt (weight table), bm25 (okapi bm25)"
    )
    config.set("crawler", "fitness_algorithm", FITNESS_ALGORITHM)

    config.add_section("GA")
    config.set("GA", "; WARNING, Only use this if you know what you're doing.")
    config.set(
        "GA",
        "; You can run gacrawler-init again anytime to restore the default options."
    )
    config.set("GA", "ga.max_generation", GA_MAX_GENERATION)
    config.set("GA", "ga.max_survived_pages", GA_MAX_SURVIVED_PAGES)
    config.set("GA", "ga.max_crawling_queue", GA_MAX_CRAWLING_QUEUE)
    config.set("GA", "ga.mutation_rate", GA_MUTATION_RATE)

    config.add_section("SOS")
    config.set("SOS",
               "; WARNING, Only use this if you know what you're doing.")
    config.set(
        "SOS",
        "; You can run gacrawler-init again anytime to restore the default options."
    )
    config.set("SOS", "sos.max_generation", SOS_MAX_GENERATION)
    config.set("SOS", "sos.max_fitness", SOS_MAX_FITNESS)
    config.set("SOS", "sos.max_gen", SOS_MAX_GEN)

    config.add_section("BS4")
    config.set("BS4",
               "; WARNING, Only use this if you know what you're doing.")
    config.set(
        "BS4",
        "; You can run gacrawler-init again anytime to restore the default options."
    )
    config.set("BS4", "bs4.min_url_length", MIN_URL_LENGTH)
    config.set("BS4", "bs4.min_news_word_count", MIN_NEWS_WORD_COUNT)
    config.set("BS4", "; Separate selector with comma (,)")
    config.set("BS4", "bs4.decompose_selector", ','.join(DECOMPOSE_SELECTOR))
    config.set("BS4", "bs4.text_selector", ','.join(TEXT_SELECTOR))

    try:
        with open(const.SETTING_FILE, "wb") as config_file:
            config.write(config_file)
    except Exception as ex:
        sys.exit("Error: " + str(ex))
        pass
    finally:
        print "Configuration is set"


def main():
    if not os.path.exists(const.SETTING_FILE):
        makeConfig()
    else:
        prompt = raw_input(
            "Configuration is set. Do you want to restore to default settings? (Default: N) [y/N] "
        )
        prompt = prompt.strip().lower()
        if prompt == '' or prompt == "n" or prompt == "no":
            sys.exit("Exit: Aborted")
        elif prompt == "y" or prompt == "yes":
            makeConfig()
        else:
            sys.exit("Exit: Input [y/N]")

if __name__ == "__main__":
    main()