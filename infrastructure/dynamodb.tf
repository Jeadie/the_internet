
resource "aws_dynamodb_table_item" "my_profile" {
    table_name = aws_dynamodb_table.internet_content.name
    hash_key   = aws_dynamodb_table.internet_content.hash_key
    range_key = aws_dynamodb_table.internet_content.range_key

    item = <<ITEM
{
    "location": {"S": "Github"},
    "title": {"S": "Jack Eadie"},
    "description": {"S": "Software engineer at Amazon. Giving people groceries."},
    "mainCategory": {"S": "Profile"},
    "timestamp": {"N": "1654067172097"},
    "upvotes": {"N": "4"},
    "comments": {"N": "6"},
    "imageSourceUrl": {"S": "https://avatars.githubusercontent.com/u/23766767?v=4"},
    "url": {"S": "https://github.com/Jeadie"}
}
    ITEM
}

resource "aws_dynamodb_table" "internet_content" {
    name = "InternetContent"

    read_capacity  = 5
    write_capacity = 5
    hash_key       = "url"
    range_key      = "timestamp"

    attribute {
        name = "url"
        type = "S"
    }

    attribute {
      name = "timestamp"
      type = "N"
    }

    #  ttl {
    #     enabled = true 
    #     attribute_name = "expiresOn" 
    # }
}