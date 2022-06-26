import os 
from typing import Any, Dict, List
from datetime import datetime, timedelta, timezone

from scrapers import InternetContent

from newsapi import NewsApiClient
from newsapi.newsapi_exception import NewsAPIException


class NewsApi:

    # All possible sources from the APINews.org
    SOURCES = {'abc-news': 'ABC News', 'abc-news-au': 'ABC News (AU)', 'aftenposten': 'Aftenposten', 'al-jazeera-english': 'Al Jazeera English', 'ansa': 'ANSA.it', 'argaam': 'Argaam', 'ars-technica': 'Ars Technica', 'ary-news': 'Ary News', 'associated-press': 'Associated Press', 'australian-financial-review': 'Australian Financial Review', 'axios': 'Axios', 'bbc-news': 'BBC News', 'bbc-sport': 'BBC Sport', 'bild': 'Bild', 'blasting-news-br': 'Blasting News (BR)', 'bleacher-report': 'Bleacher Report', 'bloomberg': 'Bloomberg', 'breitbart-news': 'Breitbart News', 'business-insider': 'Business Insider', 'business-insider-uk': 'Business Insider (UK)', 'buzzfeed': 'Buzzfeed', 'cbc-news': 'CBC News', 'cbs-news': 'CBS News', 'cnn': 'CNN', 'cnn-es': 'CNN Spanish', 'crypto-coins-news': 'Crypto Coins News', 'der-tagesspiegel': 'Der Tagesspiegel', 'die-zeit': 'Die Zeit', 'el-mundo': 'El Mundo', 'engadget': 'Engadget', 'entertainment-weekly': 'Entertainment Weekly', 'espn': 'ESPN', 'espn-cric-info': 'ESPN Cric Info', 'financial-post': 'Financial Post', 'focus': 'Focus', 'football-italia': 'Football Italia', 'fortune': 'Fortune', 'four-four-two': 'FourFourTwo', 'fox-news': 'Fox News', 'fox-sports': 'Fox Sports', 'globo': 'Globo', 'google-news': 'Google News', 'google-news-ar': 'Google News (Argentina)', 'google-news-au': 'Google News (Australia)', 'google-news-br': 'Google News (Brasil)', 'google-news-ca': 'Google News (Canada)', 'google-news-fr': 'Google News (France)', 'google-news-in': 'Google News (India)', 'google-news-is': 'Google News (Israel)', 'google-news-it': 'Google News (Italy)', 'google-news-ru': 'Google News (Russia)', 'google-news-sa': 'Google News (Saudi Arabia)', 'google-news-uk': 'Google News (UK)', 'goteborgs-posten': 'Göteborgs-Posten', 'gruenderszene': 'Gruenderszene', 'hacker-news': 'Hacker News', 'handelsblatt': 'Handelsblatt', 'ign': 'IGN', 'il-sole-24-ore': 'Il Sole 24 Ore', 'independent': 'Independent', 'infobae': 'Infobae', 'info-money': 'InfoMoney', 'la-gaceta': 'La Gaceta', 'la-nacion': 'La Nacion', 'la-repubblica': 'La Repubblica', 'le-monde': 'Le Monde', 'lenta': 'Lenta', 'lequipe': "L'equipe", 'les-echos': 'Les Echos', 'liberation': 'Libération', 'marca': 'Marca', 'mashable': 'Mashable', 'medical-news-today': 'Medical News Today', 'msnbc': 'MSNBC', 'mtv-news': 'MTV News', 'mtv-news-uk': 'MTV News (UK)', 'national-geographic': 'National Geographic', 'national-review': 'National Review', 'nbc-news': 'NBC News', 'news24': 'News24', 'new-scientist': 'New Scientist', 'news-com-au': 'News.com.au', 'newsweek': 'Newsweek', 'new-york-magazine': 'New York Magazine', 'next-big-future': 'Next Big Future', 'nfl-news': 'NFL News', 'nhl-news': 'NHL News', 'nrk': 'NRK', 'politico': 'Politico', 'polygon': 'Polygon', 'rbc': 'RBC', 'recode': 'Recode', 'reddit-r-all': 'Reddit /r/all', 'reuters': 'Reuters', 'rt': 'RT', 'rte': 'RTE', 'rtl-nieuws': 'RTL Nieuws', 'sabq': 'SABQ', 'spiegel-online': 'Spiegel Online', 'svenska-dagbladet': 'Svenska Dagbladet', 't3n': 'T3n', 'talksport': 'TalkSport', 'techcrunch': 'TechCrunch', 'techcrunch-cn': 'TechCrunch (CN)', 'techradar': 'TechRadar', 'the-american-conservative': 'The American Conservative', 'the-globe-and-mail': 'The Globe And Mail', 'the-hill': 'The Hill', 'the-hindu': 'The Hindu', 'the-huffington-post': 'The Huffington Post', 'the-irish-times': 'The Irish Times', 'the-jerusalem-post': 'The Jerusalem Post', 'the-lad-bible': 'The Lad Bible', 'the-next-web': 'The Next Web', 'the-sport-bible': 'The Sport Bible', 'the-times-of-india': 'The Times of India', 'the-verge': 'The Verge', 'the-wall-street-journal': 'The Wall Street Journal', 'the-washington-post': 'The Washington Post', 'the-washington-times': 'The Washington Times', 'time': 'Time', 'usa-today': 'USA Today', 'vice-news': 'Vice News', 'wired': 'Wired', 'wired-de': 'Wired.de', 'wirtschafts-woche': 'Wirtschafts Woche', 'xinhua-net': 'Xinhua Net', 'ynet': 'Ynet'}
    
    def __init__(self) -> None:
        self.client = NewsApiClient(api_key=self.get_api_key())

        ## Check cross-over with `australian-financial-review`, `google-news`, `google-news-au`, "hacker-news"
        ## TODO: to add later: "cnn", "espn","nbc-news", "msnbc", "fox-news", "new-york-magazine", "news-com-au",
        self.sources = ["axios", "abc-news-au", "bbc-news", "bloomberg", "google-news-au", "national-geographic", "national-review", "new-scientist", "politico", "recode", "reuters", "techcrunch", "the-wall-street-journal", "the-washington-post", "the-washington-times", "vice-news", "the-verge"]

    def get_api_key(self) -> str:
        return os.environ["NEWS_API_KEY"]

    def get_content(self) -> List[InternetContent]:
        return list(
            map(lambda x: self.convert_raw_entry(x), self.get_raw_content())
        )

    def convert_raw_entry(self, x: Dict) -> InternetContent:
        return InternetContent(
            id=x["url"],
            timestamp=datetime.strptime(x["publishedAt"][:19],  "%Y-%m-%dT%H:%M:%S"),
            title=x["title"],
            url=x["url"],
            content_type=NewsApi.SOURCES.get(x["source"]["id"], x["source"]["id"]),
            subtype="",
            content={
                "description": x["description"],
                "img": x["urlToImage"],

                # Not in API response
                "comments": 0,
                "upvotes": 0,
            }
        )

    def get_raw_content(self) -> List[Dict]:
        raw_content = []
        to_param =  datetime.now(tz=timezone.utc)
        from_param =  to_param - timedelta(days=1)

        for s in self.sources:
            try:
                resp = self.client.get_everything(
                    to = to_param,
                    from_param = from_param,
                    sources=s,
                    page_size=100
                ).get("articles", [])
                raw_content.extend(resp)
            except NewsAPIException as e:
                print(e)
        return raw_content
