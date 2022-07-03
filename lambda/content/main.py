from typing import Dict, List
from dynamo import batch_put_results
from lambda.content.scrapers import InternetContent
from scrape_config import ScrapeConfig
from scrapers import get_all_internet_content
from api_news import NewsApi



def handler(event, context):
    # {'version': '0', 'id': '28433b70-41cb-18df-0714-58133645ca18', 'detail-type': 'Scheduled Event', 'source': 'aws.events', 'account': '383495223751', 'time': '2022-06-08T05:56:38Z', 'region': 'us-east-1', 'resources': ['arn:aws:events:us-east-1:383495223751:rule/web-scrape-cron-job'], 'detail': {}}
    # LambdaContext([aws_request_id=756a73d7-e00a-48d5-8354-c1cf5a36607f,log_group_name=/aws/lambda/content-scraper,log_stream_name=2022/06/08/[$LATEST]79907da73e7444e5b913d21f90b89f8c,function_name=content-scraper,memory_limit_in_mb=128,function_version=$LATEST,invoked_function_arn=arn:aws:lambda:us-east-1:383495223751:function:content-scraper,client_context=None,identity=CognitoIdentity([cognito_identity_id=None,cognito_identity_pool_id=None])])

    # Web scraping
    content_providers = ScrapeConfig.get_content_providers()
    result = get_all_internet_content(content_providers)

    counts = calculate_content_counts(result)
    print(counts)
    
    batch_put_results(result)


    # NewsAPI batch_put_results(NewsApi().get_content())
    api = NewsApi()
    result = api.get_content()
    batch_put_results(result)

    return {
        'statusCode' : 200,
        'body': "Hello World",
    }

def calculate_content_counts(content: List[InternetContent]) -> Dict[str, int]:
    counts = dict([(x.content_type , 0) for x in content])
    for c in content:
        counts[c.content_type]+=1
    return counts
