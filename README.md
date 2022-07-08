# The Internet
The entire internet in one place 


## Future places to get content
Below are just rough notes

## Twitter
Basic accounts to add initially
- @naval
- @pketh
- @nntaleb
- @lexfridman
- @pketh
- @GergelyOrosz
- @EricJorgenson


# Typeshare
See https://typeshare.co. For an example user `philmorle`, if we get their slug and userID, we can get a nice JSON of their writings.
```
curl -X POST -H "Content-Type: application/json" \
    -d '{"userID":"XnozsQmTb4WYE690QdkWuerjtei1","slug":"philmorle","next":null}' \
    https://typeshare.co/api/library/sortPosts
```

# AWS Cognito
 - JS [link](https://github.com/aws-amplify/amplify-js/tree/main/packages/amazon-cognito-identity-js)
 - Stripe [subscriptions](https://stripe.com/docs/billing/subscription-resource)

# Things to fix
- Make timestamp of datetime.now() -> date.today() to avoid duplicates.
- Frontend if no DDB data is returned
- Frontend, match items on location (not just location+subtype)
- Mixpanel collect via proxy: https://developer.mixpanel.com/docs/collection-via-a-proxy

hackernoon, stratecherry
