from dataclasses import dataclass
from datetime import datetime
from enum import Enum, auto
from typing import Dict, List

import bs4
import requests

from .models import ContentLocation

class ContentId(Enum):
    IndieHacker_PopularPosts = auto()
    HackerNews_News          = auto() 

    def _generate_next_value_(name, start, count, last_values):
        return name

    def all():
        return [ContentId.IndieHacker_PopularPosts, ContentId.HackerNews_News]


@dataclass
class InternetContent:
    id: str
    timestamp: datetime
    title: str
    url: str
    content_type: ContentId
    content: Dict[str, object]


def get_internet_content()-> List[InternetContent]:
    result = []
    for c in [HackerNewsContentProvider(), IndieHackerContentProvider()]:
        resp = requests.get(c.getBaseWebsite())
        if resp.status_code != 200:

            continue

        soup = bs4.BeautifulSoup(resp.content, "html.parser")
        result.extend(c.getContent(soup))
    return result


class InternetContentProvider(object):
    """ Provides a uniform interface for internet content to be collected from different locations."""

    def getBaseWebsite(self) -> str:
        """ Returns the website to GET that contains the internet content."""
        pass

    def getContentId(self) -> str:
        """Returns the id for the content provider. Should not depend on the underlying content
        (i.e may relate to the sub-characteristics of a website, but not the specific content.
        """
        pass

    def getContent(self, page: bs4.BeautifulSoup) -> List[InternetContent]:
        """Parses the internet content from a website, as a BeautifulSoup object, and returns a list
        of individual content payloads. An individiual payload represents a single consumable piece
        of content. 

        getContent is intended to isolate all the awkward, hard-coded random logic required in web 
        scraping specific websites.
        """
        pass


class IndieHackerContentProvider(InternetContentProvider):

    def getBaseWebsite(self) -> str:
        return "https://www.indiehackers.com"

    def getContentId(self) -> ContentId:
        return ContentLocation.INDIE_HACKERS_POPULAR

    def getContent(self, page: bs4.BeautifulSoup) -> List[InternetContent]:
        contentList = page.find(
            "div", class_="posts-section__posts"
            )
        items = contentList.find_all(
                class_="feed-item--post"
            )
        return list(map(lambda x: self.convertItemPost(x), items))

    def getTimestamp(self, x:bs4.Tag) -> datetime:
        post_date = x.find("a", class_="feed-item__date")

        if not post_date:
            return datetime.now()

        # April 29 at 5:18 PM
        published = post_date.get("title")
        timestamp = datetime.strptime(published, "%B %d at %I:%M %p")

        # Indie hacker timestamp assumes it is current year
        return timestamp.replace(year= timestamp.now().year)


    def convertItemPost(self, x: bs4.Tag) -> Dict[str, object]:
        title_link = x.find("a", class_="feed-item__title-link")
        upvote_span = x.find("span", class_="feed-item__likes-count")
        comment_span = x.find("span", class_="reply-count__full-count")

        content = {
            # Expected innerHtml ~= "18 comments"
            "comments": int(comment_span.get_text().split(" ")[0]),
            "upvotes": int(upvote_span.get_text())
        }

        url = self.getBaseWebsite() + title_link.get('href')

        return InternetContent(
            str(hash(url)),
            self.getTimestamp(x),
            title_link.get_text().strip(),
            url,
            self.getContentId(),
            content
        )


class HackerNewsContentProvider(InternetContentProvider):

    def getBaseWebsite(self) -> str:
        return "https://news.ycombinator.com"

    def getContentId(self) -> str:
        return ContentLocation.HACKER_NEWS_NEWS

    def getContent(self, page: bs4.BeautifulSoup) -> List[InternetContent]:
        contentList = page.find("table", class_="itemlist").find_all("tr")
        i = 0
        entries = []

        # Ignore last two lines, they are just extra padding <tr> elements
        while i<len(contentList)-2:
            main_line = contentList[i]
            score_metadata = contentList[i+1]
            
            # Third element is a spacer <tr>
            i+=3

            entries.append(self.convertItemPost(main_line, score_metadata))

        return entries
        
    def convertItemPost(self, main_line: bs4.Tag, score_metadata: bs4.Tag) -> Dict[str, object]:
        """ Converts a single post from HackerNews.

        main_line: Table row line contains the link and title of the post.
        score_metadata: 
            Example: `95 points by atomiomi 12 hours ago | hide | 71 comments`
        """
        title_link = main_line.find("a", class_="titlelink")

        content = {
            "upvotes": self.getUpvotes(score_metadata),
            "comments": self.getCommentCount(score_metadata),
        }

        url = title_link.get('href')

        return InternetContent(
            str(hash(url)),
            self.getTimestamp(score_metadata),
            title_link.get_text().strip(),
            url,
            self.getContentId(),
            content
        )

    def getTimestamp(self, score_metadata: bs4.Tag) -> datetime:
        age_span = score_metadata.find("span", class_="age")

        if not age_span:
            return datetime.now()

        time = age_span.get("title")

        # Expected key title="2022-04-27T09:28:57"
        return datetime.fromisoformat(time)

    def getUpvotes(self, score_metadata: bs4.Tag) -> int:
        upvote_span = score_metadata.find("span", class_="score")
        if upvote_span:
            # Expected innerHtml ~= "415 points"
            return int(upvote_span.get_text().split(" ")[0])
        else:
            return 0 

    def getCommentCount(self, score_metadata: bs4.Tag) -> int:
        links = score_metadata.find_all("a")
        if len(links) == 4:        
            comments = links[-1].get_text()
            if "comments" not in comments:
                return 0

            # Expected innerHtml ~= "289 comments"
            return int(comments.split("\xa0")[0])
        else:
            return 0