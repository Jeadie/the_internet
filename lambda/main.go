package main

import (
	"context"
	"encoding/json"
	"fmt"
	"github.com/aws/aws-lambda-go/events"
	"github.com/aws/aws-lambda-go/lambda"
)

type PostEvent struct {
	content   []InternetContent `json:"content"`
}

func handler(ctx context.Context, request events.APIGatewayProxyRequest) (events.APIGatewayProxyResponse, error) {

	ApiResponse := events.APIGatewayProxyResponse{}
	switch request.HTTPMethod {
	case "GET":
		content := GetInternetContentFromToday(ctx)
		body, err := json.Marshal(content)

		statusCode := 200
		if err != nil {
			statusCode = 500
		}
		ApiResponse = events.APIGatewayProxyResponse{Body: string(body), StatusCode: statusCode}


	case "POST":
		p := PostEvent{}
		err := json.Unmarshal([]byte(request.Body), &p)
		if err != nil {
			return events.APIGatewayProxyResponse{Body: fmt.Sprintf("Invalid POST payload: %w", err), StatusCode: 500}, nil
		}
		err = PostInternetContentFromToday(ctx, p.content)
		if err != nil {
			return events.APIGatewayProxyResponse{
				Body: fmt.Sprintf("Could not save content. Error: %w", err),
				StatusCode: 500}, nil
		}
		ApiResponse = events.APIGatewayProxyResponse{Body: "OK", StatusCode: 200}
	}

	return ApiResponse, nil
}

func main() {
	lambda.Start(handler)
}

