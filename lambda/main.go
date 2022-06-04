package main

import (
	"context"
	"encoding/json"
	"fmt"

	"github.com/aws/aws-lambda-go/events"
	"github.com/aws/aws-lambda-go/lambda"
)

type PostEvent struct {
	Url   string `json:"url"`
	Title string `json:"title"`
}

func handler(ctx context.Context, request events.APIGatewayProxyRequest) (events.APIGatewayProxyResponse, error) {
	ApiResponse := events.APIGatewayProxyResponse{}
	switch request.HTTPMethod {
	case "GET":
		name := request.QueryStringParameters["name"]
		if name != "" {
			ApiResponse = events.APIGatewayProxyResponse{Body: "Hey " + name + " welcome! ", StatusCode: 200}
		} else {
			ApiResponse = events.APIGatewayProxyResponse{Body: "Error: What is your name?", StatusCode: 500}
		}

	case "POST":
		p := PostEvent{}

		err := json.Unmarshal([]byte(request.Body), &p)
		if err != nil {
			body := "Error: Invalid JSON payload ||| " + fmt.Sprint(err) + " Body Obtained" + "||||" + request.Body
			ApiResponse = events.APIGatewayProxyResponse{Body: body, StatusCode: 500}
		} else {
			ApiResponse = events.APIGatewayProxyResponse{Body: request.Body, StatusCode: 200}
		}
	}

	return ApiResponse, nil
}

func main() {
	lambda.Start(handler)
}
