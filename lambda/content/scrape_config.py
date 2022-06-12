from dataclasses import dataclass
from typing import Dict, List

from scrapers import ContentLocations, AFRInternetContentProvider, RedditChannelContentProvider, ProductHuntContentProvider, HackerNewsContentProvider, IndieHackerContentProvider

@dataclass
class ContentProviderConfig:
    location: ContentLocations
    default_page: bool
    subtypes: List[str]

class ScrapeConfig(object):
    default_config: List[ContentProviderConfig] = [
        ContentProviderConfig(ContentLocations.AFR, True, ["Front Page", "technology", "markets", "politics", "world", "opinion", "street-talk"]),
        ContentProviderConfig(ContentLocations.Reddit, False, ["technology", "australia", "worldnews"]),
        ContentProviderConfig(ContentLocations.ProductHunt, True, []),
        ContentProviderConfig(ContentLocations.IndieHackers, True, []),
        ContentProviderConfig(ContentLocations.HackerNews, True, []),
    ]

    location_map: Dict[ContentLocations, type] = {
        ContentLocations.AFR: AFRInternetContentProvider,
        ContentLocations.Reddit: RedditChannelContentProvider,
        ContentLocations.ProductHunt: ProductHuntContentProvider,
        ContentLocations.IndieHackers: IndieHackerContentProvider,
        ContentLocations.HackerNews: HackerNewsContentProvider
    }

    @classmethod
    def get_content_providers(config: Dict[ContentLocations, List[str]] = default_config) -> List[ContentLocations]:
        """ Get config """
        providers = []
        for location_config in  ScrapeConfig.default_config:
            if location_config.default_page:
                providers.append(ScrapeConfig.location_map[location_config.location]())

            providers.extend([ScrapeConfig.location_map[location_config.location](v) for v in location_config.subtypes])
        return providers

if __name__ == "__main__":
    print(ScrapeConfig.get_content_providers())