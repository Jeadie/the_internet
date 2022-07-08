cd once-a-day/

# Make sure we don't deploy a local build.
if ! grep -q "const isLocal = false" src/index.tsx; then
    echo "isLocal=true... change to isLocal=false in index.tsx"
    exit 1
fi 

npm run build
cd -
./upload_build.sh


# Create invalidation on `--force`
if [ $1 == "--force" ]; then
    echo "[INFO] - Creating an AWS CDN validation" 
    aws cloudfront create-invalidation --distribution-id $(aws cloudfront list-distributions --query 'DistributionList.Items[0].Id' | sed 's/"//g') --paths /
fi
