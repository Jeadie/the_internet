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
			body := "Error: Invalid JSON payload ||| " + fmt.Sprint(err) + " Body Obtained" + "||||" + request.Body
			ApiResponse = events.APIGatewayProxyResponse{Body: body, StatusCode: 500}
		} else {
			body := "title: " + fmt.Sprint(p.Title) + " url: " + fmt.Sprint(p.Url)
			ApiResponse = events.APIGatewayProxyResponse{Body: body, StatusCode: 200}
		}
	}

	return ApiResponse, nil
}

func main() {
	lambda.Start(handler)
}
