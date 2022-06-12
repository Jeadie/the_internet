
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