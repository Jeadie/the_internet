package main

import (
	"context"
	"strconv"

	"github.com/aws/aws-sdk-go-v2/service/dynamodb/types"

	"github.com/aws/aws-sdk-go-v2/config"
	"github.com/aws/aws-sdk-go-v2/feature/dynamodb/attributevalue"
	"github.com/aws/aws-sdk-go-v2/service/dynamodb"
)

type InternetContent struct {
	URL       string `json:"url"`       // Hash key
	Timestamp int    `json:"timestamp"` // Sort key

	Location       string `json:"location"`
	Title          string `json:"title"`
	Description    string `json:"description"`
	MainCategory   string `json:"mainCategory"`
	Upvotes        int    `json:"upvotes"`
	Comments       int    `json:"comments"`
	ImageSourceURL string `json:"imageSourceUrl"`
}

func (c InternetContent) ToPutRequest() *types.PutRequest {

	return &types.PutRequest{Item: map[string]types.AttributeValue{
		"url":            &types.AttributeValueMemberS{Value: c.URL},
		"timestamp":      &types.AttributeValueMemberN{Value: strconv.Itoa(c.Timestamp)},
		"location":       &types.AttributeValueMemberS{Value: c.Location},
		"title":          &types.AttributeValueMemberS{Value: c.Title},
		"description":    &types.AttributeValueMemberS{Value: c.Description},
		"mainCategory":   &types.AttributeValueMemberS{Value: c.MainCategory},
		"upvotes":        &types.AttributeValueMemberN{Value: strconv.Itoa(c.Upvotes)},
		"comments":       &types.AttributeValueMemberN{Value: strconv.Itoa(c.Comments)},
		"imageSourceUrl": &types.AttributeValueMemberS{Value: c.ImageSourceURL},
	}}
}

var dao *dynamodb.Client

func GetDao(ctx context.Context) *dynamodb.Client {
	if dao != nil {
		return dao
	}

	cfg, err := config.LoadDefaultConfig(ctx, config.WithRegion("us-east-1"))
	if err != nil {
		panic(err)
	}

	dao = dynamodb.NewFromConfig(cfg)
	return dao
}

func PostInternetContentFromToday(ctx context.Context, content []InternetContent) error {
	dao := GetDao(ctx)

	writes := make([]types.WriteRequest, len(content))
	for i, c := range content {
		writes[i] = types.WriteRequest{PutRequest: c.ToPutRequest()}
	}

	_, err := dao.BatchWriteItem(ctx, &dynamodb.BatchWriteItemInput{
		RequestItems: map[string][]types.WriteRequest{
			"InternetContent": writes,
		},
	})
	return err
}

func GetInternetContentFromToday(ctx context.Context) ([]InternetContent, error) {
	var content []InternetContent
	tableName := "InternetContent"

	q, err := GetDao(ctx).Scan(ctx, &dynamodb.ScanInput{
		TableName: &tableName,
	})
	if err != nil {
		return content, err
	}

	err = attributevalue.UnmarshalListOfMaps(q.Items, &content)
	if err != nil {
		return content, err
	}
	return content, nil
}
