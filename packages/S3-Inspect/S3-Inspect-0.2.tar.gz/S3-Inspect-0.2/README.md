# aws-devops-challenge
touch ~/.aws/credentials
[default]
aws_access_key_id = YOUR_ACCESS_KEY_ID
aws_secret_access_key = YOUR_SECRET_ACCESS_KEY
touch ~/.aws/config
[default]
region = YOUR_PREFERRED_REGION


time python s3inspect -gc  --granularity MONTHLY --metrics 'BlendedCost' --timeperiod '{"Start":"2019-01-01","End":"2019-05-20"}' test*
