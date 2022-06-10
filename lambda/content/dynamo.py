from cmath import e
import json
from typing import Dict, List, Union

import boto3
from botocore.exceptions import ClientError

from scrapers import InternetContent

# https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/WorkingWithItems.html#WorkingWithItems.BatchOperations
MAXIMUM_BATCH_SIZE_PUT_OPERATOR = 25
MAXIMUM_BATCH_SIZE_GET_OPERATOR = 100

def batch_put_results(content: List[InternetContent], n=MAXIMUM_BATCH_SIZE_PUT_OPERATOR):
    """Sends batched PUT requests, of size n, to the InternetContent table."""
    batched_internet_content = [content[i * n:(i + 1) * n] for i in range((len(content) + n - 1) // n )]
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table("InternetContent")
    for batch in batched_internet_content:
        # TODO: More common error is `content` has duplicates
        try:
            put_results(table, batch)
        except ClientError as e:
            print(e)


def put_results(table, content: List[InternetContent]):
    """Sends a batch PUT request of InternetContent to the InternetContent DynamoDb table."""
    with table.batch_writer() as writer:
        for c in content:
            writer.put_item(Item=convert_internet_content(c))

def convert_internet_content(c: InternetContent) -> Dict[str, Union[str, int]]:
    """ Convert an InternetContent object to a DynamoDB-friendly item."""
    return {
        "timestamp" : int(c.timestamp.timestamp()),
        "title" : c.title,
        "url" : c.url,
        "description": c.content.get("description", None),
        "location": c.content_type,
        "additional_fields" : json.dumps(c.content),
        "upvotes": c.content.get("upvotes", 0),
        "comments": c.content.get("comments", 0),
        "imageSourceUrl": c.content.get("img", ""),
    }
