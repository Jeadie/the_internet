package main

import (
	"context"
	"fmt"
	"github.com/aws/aws-sdk-go-v2/feature/dynamodb/expression"
	"log"
	"time"

	"github.com/aws/aws-sdk-go-v2/config"
	"github.com/aws/aws-sdk-go-v2/feature/dynamodb/attributevalue"
	"github.com/aws/aws-sdk-go-v2/service/dynamodb"
)

type InternetContent struct {
	URL       string `json:"url"`       // Hash key
	Timestamp int    `json:"timestamp"` // Sort key

	Location       string  `json:"location"`
	Title          string  `json:"title"`
	Description    string  `json:"description"`
	MainCategory   string  `json:"mainCategory"`
	Upvotes        int     `json:"upvotes"`
	Comments       int     `json:"comments"`
	ImageSourceURL string `json:"imageSourceUrl"`
}

var dao *dynamodb.Client

func GetDao(ctx context.Context) *dynamodb.Client {
	if dao != nil {
		return dao
	}

	cfg, err := config.LoadDefaultConfig(ctx, config.WithRegion("us-east-1") )
	if err != nil {
		panic(err)
	}

	dao = dynamodb.NewFromConfig(cfg)
	return dao
}

func GetInternetContentFromToday(ctx context.Context) []InternetContent {
	dao := GetDao(ctx)
	var content []InternetContent

	expr, err := expression.NewBuilder().WithFilter(
		// TODO: change to nano
		expression.Name("timestamp").GreaterThanEqual(expression.Value(time.Now().Add(-7 * 24 * time.Hour).Unix()))).Build()

	if err != nil {
		fmt.Println(err.Error())
		return content
	}
	table := "InternetContent"
	q, err := dao.Scan(ctx, &dynamodb.ScanInput{
		ExpressionAttributeNames:  expr.Names(),
		ExpressionAttributeValues: expr.Values(),
		FilterExpression:          expr.Filter(),
		ProjectionExpression:      expr.Projection(),
		TableName:                 &table,
	})

	if err != nil {
		fmt.Println(err)
		return content
	}
	fmt.Println("Query: ", q)

	err = attributevalue.UnmarshalListOfMaps(q.Items, &content)
	if err != nil {
		log.Println(fmt.Sprintf("failed to unmarshal Dynamodb Scan Items, %v", err))
		return content
	}

	return content

}
