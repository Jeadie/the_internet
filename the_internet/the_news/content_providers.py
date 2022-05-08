from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Dict, List

import bs4
from pytz import UTC
import requests

from the_news.models import ContentLocation

@dataclass
class InternetContent:
    """Uniform content from an InternetContentProvider. Represents a single piece of internet content."""
    id: str
    timestamp: datetime
    title: str
    url: str
    content_type: ContentLocation
    content: Dict[str, object]

def get_internet_content() -> List[InternetContent]:
    """Gets content from all content providers.
    TODO: Add request method and beautiful soup construction into class.
    TODO: Add provders as parameter
    """
    result = []
    for provider in [RedditChannelContentProvider("technology"), ProductHuntContentProvider(), HackerNewsContentProvider(), IndieHackerContentProvider()]:
        resp = requests.get(provider.get_base_website())
        if resp.status_code != 200:
            continue

        soup = bs4.BeautifulSoup(resp.content, "html.parser")
        result.extend(provider.get_content(soup))
    return result


class InternetContentProvider:
    """ Provides a uniform interface for internet content to be collected from different locations."""

    # TODO: move get_base_website and get_content_id as class parameters
    def get_base_website(self) -> str:
        """ Returns the website to GET that contains the internet content."""

    def get_content_id(self) -> ContentLocation:
        """Returns the id for the content provider. Should not depend on the underlying content
        (i.e may relate to the sub-characteristics of a website, but not the specific content.
        """

    def get_content(self, page: bs4.BeautifulSoup) -> List[InternetContent]:
        """Parses the internet content from a website, as a BeautifulSoup object, and returns a list
        of individual content payloads. An individiual payload represents a single consumable piece
        of content.

        get_content is intended to isolate all the awkward, hard-coded random logic required in web
        scraping specific websites.
        """

class RedditChannelContentProvider(InternetContentProvider):
    """ Provides a uniform interface for internet content to be collected from different locations."""

    def __init__(self, channel) -> None:
        self.channel = channel

    def get_base_website(self) -> str:
        """ Returns the website to GET that contains the internet content."""
        return f"https://www.reddit.com/r/{self.channel}/top/?t=day"

    def get_content_id(self) -> ContentLocation:
        """Returns the id for the content provider. Should not depend on the underlying content
        (i.e may relate to the sub-characteristics of a website, but not the specific content.
        """
        return ContentLocation.REDDIT_CHANNEL_TODAY

    def get_content(self, page: bs4.BeautifulSoup) -> List[InternetContent]:
        """Parses the internet content from a website, as a BeautifulSoup object, and returns a list
        of individual content payloads. An individiual payload represents a single consumable piece
        of content.

        get_content is intended to isolate all the awkward, hard-coded random logic required in web
        scraping specific websites.
        """
        contents_list = page.select("[data-testid=\"post-container\"]")
        contents_list = filter(lambda x: len(x.find_all("span", text="promoted")) == 0, contents_list)

        return list(map(lambda x: self.convert_item_post(x), contents_list))

    def get_comments(self, x: bs4.Tag) -> InternetContent:
        comments_box = x.select("[data-test-id=\"comments-page-link-num-comments\"]")
        if not comments_box:
            return 0
        comment_text = comments_box[0].find("span").get_text()

        # Expected format ~"4.4k comments"
        return self.parse_number_text(comment_text.split(" ")[0])

    def parse_timestamp(self, x: bs4.Tag) -> datetime:
        timestamp_box = x.select("[data-testid=\"post_timestamp\"]")
        if not timestamp_box:
            return datetime.now(tz=UTC)
        # "3 days ago"
        # "14 hours ago"
        # "just now"
        # "1 minute ago"
        time_diff = timestamp_box[0].get_text()

        if time_diff == "just now":
            return datetime.now(tz=UTC)

        parts = time_diff.split(" ")

        deltas = {"hour": 0, "minute": 0, "day": 0}
        deltas[parts[1].strip("s")] = int(parts(0))

        return datetime.now(tz=UTC) - timedelta(days=deltas["day"], hours=deltas["hour"], minutes=deltas["minute"])

    def parse_number_text(self, x) -> int:
        if "k" in x:
            return int(1000*float(x[:-1]))

        return int(x)

    def get_upvotes(self, x: bs4.Tag) -> InternetContent:
        upvotes_button = x.select("[data-click-id=\"upvote\"]")
        if not upvotes_button:
            return 0

        upvote_text = upvotes_button[0].next_element.get_text()
        if not upvote_text:
            return 0
        return self.parse_number_text(upvote_text)

    def convert_item_post(self, x: bs4.Tag) -> InternetContent:
        title = x.find("h3")
        url = x.select("[data-testid=\"outbound-link\"]")[0]

        return InternetContent(
            id=str(url),
            timestamp= datetime.today(), # Does not have time
            title= title.get_text().strip(),
            url=url,
            content_type=self.get_content_id(),
            content={
                "comments": self.get_comments(x),
                "upvotes": self.get_upvotes(x),
            }
        )

class ProductHuntContentProvider(InternetContentProvider):
    """ Provides internet content from the days top products on ProductHunt. """

    def get_base_website(self) -> str:
        return "https://www.producthunt.com"

    def get_content_id(self) -> ContentLocation:
        return ContentLocation.PRODUCT_HUNT_TODAY

    def get_content(self, page: bs4.BeautifulSoup) -> List[InternetContent]:
        # The current day is section-0
        content_list = page.select("[data-test=\"homepage-section-0\"]")[0]

        items = content_list.select("[data-test^=\"post-item-\"]")
        return list(map(lambda x: self.convert_item_post(x), items))

    def get_upvotes(self, x: bs4.Tag) -> int:
        upvote_tag = x.select("[data-test='vote-button']")[0]
        if upvote_tag:
            return int(upvote_tag.findChildren("div" , recursive=False)[0].findChildren("div" , recursive=False)[-1].get_text())
        else:
            return 0

    def get_comments(self, x: bs4.Tag) -> int:
        comment_icon = x.select("[viewBox=\"0 0 13 13\"]")
        if comment_icon:
            comments = comment_icon[0].next_sibling.get_text().strip()
            if comments:
                return int(comments)
        return 0

    def convert_item_post(self, x: bs4.Tag) -> InternetContent:
        title_tag = x.select("[data-test^=\"post-name-\"]")[0]
        url = self.get_base_website() + title_tag.get("href")
        return InternetContent(
            id=str(url),
            timestamp= datetime.today(), # Does not have time
            title= title_tag.get_text().strip(),
            url=url,
            content_type=self.get_content_id(),
            content={
                "description": x.select("[data-test*='tagline'][data-test*='post']")[0].get_text(),
                "comments": self.get_comments(x),
                "upvotes": self.get_upvotes(x),
            }
        )

class IndieHackerContentProvider(InternetContentProvider):
    """Provides internet content from the front page of IndieHackers."""

    def get_base_website(self) -> str:
        return "https://www.indiehackers.com"

    def get_content_id(self) -> ContentLocation:
        return ContentLocation.INDIE_HACKERS_POPULAR

    def get_content(self, page: bs4.BeautifulSoup) -> List[InternetContent]:
        content_list = page.find(
            "div", class_="posts-section__posts"
            )
        items = content_list.find_all(
                class_="feed-item--post"
            )
        return list(map(lambda x: self.convert_item_post(x), items))

    def get_timestamp(self, x:bs4.Tag) -> datetime:
        post_date = x.find("a", class_="feed-item__date")

        if not post_date:
            return datetime.now()

        # April 29 at 5:18 PM
        published = post_date.get("title")
        timestamp = datetime.strptime(published, "%B %d at %I:%M %p")

        # Indie hacker timestamp assumes it is current year
        return timestamp.replace(year= timestamp.now().year)


    def convert_item_post(self, x: bs4.Tag) -> Dict[str, object]:
        title_link = x.find("a", class_="feed-item__title-link")
        upvote_span = x.find("span", class_="feed-item__likes-count")
        comment_span = x.find("span", class_="reply-count__full-count")

        content = {
            # Expected innerHtml ~= "18 comments"
            "comments": int(comment_span.get_text().split(" ")[0]),
            "upvotes": int(upvote_span.get_text())
        }

        url = self.get_base_website() + title_link.get('href')

        return InternetContent(
            str(url),
            self.get_timestamp(x),
            title_link.get_text().strip(),
            url,
            self.get_content_id(),
            content
        )

class HackerNewsContentProvider(InternetContentProvider):
    """Provides internet content from Y combinator's news hompage, HackerNews"""

    def get_base_website(self) -> str:
        return "https://news.ycombinator.com"

    def get_content_id(self) -> ContentLocation:
        return ContentLocation.HACKER_NEWS_NEWS

    def get_content(self, page: bs4.BeautifulSoup) -> List[InternetContent]:
        """Get content iterable, process individually and return as InternetContent"""
        content_list = page.find("table", class_="itemlist").find_all("tr")
        i = 0
        entries = []

        # Ignore last two lines, they are just extra padding <tr> elements
        while i<len(content_list)-2:
            main_line = content_list[i]
            score_metadata = content_list[i+1]
                       # Third element is a spacer <tr>
            i+=3

            entries.append(self.convert_item_post(main_line, score_metadata))

        return entries

    def convert_item_post(self, main_line: bs4.Tag, score_metadata: bs4.Tag) -> Dict[str, object]:
        """ Converts a single post from HackerNews.

        main_line: Table row line contains the link and title of the post.
        score_metadata:
            Example: `95 points by atomiomi 12 hours ago | hide | 71 comments`
        """
        title_link = main_line.find("a", class_="titlelink")

        content = {
            "upvotes": self.get_upvotes(score_metadata),
            "comments": self.get_comment_count(score_metadata),
        }

        url = title_link.get('href')
        if url[:8] == "item?id=":
            url = f"{self.get_base_website()}/{url}"

        return InternetContent(
            str(url),
            self.get_timestamp(score_metadata),
            title_link.get_text().strip(),
            url,
            self.get_content_id(),
            content
        )

    def get_timestamp(self, score_metadata: bs4.Tag) -> datetime:
        """Get timestamp from metadata line"""
        age_span = score_metadata.find("span", class_="age")

        if not age_span:
            return datetime.now()

        time = age_span.get("title")

        # Expected key title="2022-04-27T09:28:57"
        return datetime.fromisoformat(time)

    def get_upvotes(self, score_metadata: bs4.Tag) -> int:
        """Get upvotes from metadata line"""
        upvote_span = score_metadata.find("span", class_="score")
        if upvote_span:
            # Expected innerHtml ~= "415 points"
            return int(upvote_span.get_text().split(" ")[0])
        return 0

    def get_comment_count(self, score_metadata: bs4.Tag) -> int:
        """Get number of comments from metadata line. If no comments, the element will not exist."""
        links = score_metadata.find_all("a")
        if len(links) == 4:
            comments = links[-1].get_text()
            if "comments" not in comments:
                return 0

            # Expected innerHtml ~= "289 comments"
            return int(comments.split("\xa0")[0])

        return 0