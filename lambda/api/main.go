package main

import (
	"context"
	"encoding/json"
	"fmt"

	"github.com/aws/aws-lambda-go/events"
	"github.com/aws/aws-lambda-go/lambda"
)

type PostEvent struct {
	content []InternetContent `json:"content"`
}

func handler(ctx context.Context, request events.APIGatewayProxyRequest) (events.APIGatewayProxyResponse, error) {
	switch request.HTTPMethod {
	case "GET":
		return handleGet(ctx, request)

	case "POST":
		return handlePost(ctx, request)
	}
	return events.APIGatewayProxyResponse{StatusCode: 400}, fmt.Errorf("unsupported HTTP method %s. Supported methods: GET, POST", request.HTTPMethod)
}

func handlePost(ctx context.Context, request events.APIGatewayProxyRequest) (events.APIGatewayProxyResponse, error) {
	p := PostEvent{}
	err := json.Unmarshal([]byte(request.Body), &p)
	if err != nil {
		return events.APIGatewayProxyResponse{Body: fmt.Errorf("invalid POST payload: %w", err).Error(), StatusCode: 500}, err
	}

	err = PostInternetContentFromToday(ctx, p.content)
	if err != nil {
		return events.APIGatewayProxyResponse{
			Body:       fmt.Errorf("could not save content. Error: %w", err).Error(),
			StatusCode: 500,
		}, err
	}
	return events.APIGatewayProxyResponse{Body: "OK", StatusCode: 200}, nil
}

func handleGet(ctx context.Context, request events.APIGatewayProxyRequest) (events.APIGatewayProxyResponse, error) {
	content, err := GetInternetContentFromToday(ctx)
	if err != nil {
		return events.APIGatewayProxyResponse{
			Body:       fmt.Errorf("could not get content from DynamoDB. Error: %w", err).Error(),
			StatusCode: 500,
		}, err
	}

	body, err := json.Marshal(content)
	var statusCode int
	if err != nil {
		statusCode = 200
	} else {
		statusCode = 500
	}

	return events.APIGatewayProxyResponse{Body: string(body), StatusCode: statusCode}, err
}

func main() {
	lambda.Start(handler)
}
