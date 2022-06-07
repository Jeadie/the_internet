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


# Typeshare
See https://typeshare.co. For an example user `philmorle`, if we get their slug and userID, we can get a nice JSON of their writings.
```
curl -X POST -H "Content-Type: application/json" \
    -d '{"userID":"XnozsQmTb4WYE690QdkWuerjtei1","slug":"philmorle","next":null}' \
    https://typeshare.co/api/library/sortPosts
```