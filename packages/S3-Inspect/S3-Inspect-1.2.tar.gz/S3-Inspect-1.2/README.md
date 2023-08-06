# aws-devops-challenge

### Getting Started
1. Get the AWS API Key and Secret
2. Place create a folder ~/.aws/
`mkdir -p ~/.aws/`
3. Create `credentials` file inside `~/.aws/` folder
`vi ~/.aws/credentials`.
The contents of the file should look like this:
```
[default]
aws_access_key_id = YOUR_ACCESS_KEY_ID
aws_secret_access_key = YOUR_SECRET_ACCESS_KEY
```

4. (Optional)You can choose to create `~/.aws/config` file to select your default region:
```
touch ~/.aws/config
[default]
region = YOUR_PREFERRED_REGION
```

5. (Optional) Note: It is recommended but not required to create a python environment using:
`python3 -m venv YOUR_PYTHON_ENV_NAME`
`source YOUR_PYTHON_ENV_NAME/bin/activate`

6. Install `s3-inspect` using the following:
```
pip install s3-inspect
```

7. Running the python package

`python -m s3inspect -h`
```
usage: __main__.py [-h] [-u {b,kb,mb,gb}] [-p PREFIX] [-gs] [-gr] [-gc]
                   [--timeperiod TIMEPERIOD] [--granularity GRANULARITY]
                   [--metrics METRICS] [-l]
                   regex

Inspect S3 Bucket

positional arguments:
  regex                 Regex Support for Buckets list)

optional arguments:
  -h, --help            show this help message and exit
  -u {b,kb,mb,gb}, --unit {b,kb,mb,gb}
                        Return files sizes in these units: b (bytes), kb
                        (kilobytes), mb (megabytes), gb (gigabytes)
  -p PREFIX, --prefix PREFIX
                        Add prefix for the keys. Example: images/
  -gs, --groubystoragetype
                        When this is set information is grouped by Storage
                        Type
  -gr, --groubyregion   When this is set information is grouped by Region Type
  -gc, --getcost        When this is set cost report is returned Type
  --timeperiod TIMEPERIOD
                        Example: '{"Start":"2019-01-01","End":"2019-05-20"}'
  --granularity GRANULARITY
                        Example: MONTHLY
  --metrics METRICS     Example: 'BlendedCost UNBLENDED_COST AMORTIZED_COST'
  -l, --list            Displays a list of available S3 Buckets in account

```
### Examples

- Following is to use only `regex` for bucket name


```
$ python s3inspect test*

------------------------------------------------------------------
S3 Bucket Inspection Report:
------------------------------------------------------------------
Bucket Name: tests32424312341234
------------------------------------------------------------------
Bucket Creation Date: 2019-05-21 08:04:15+00:00
Recent File Modification Date (Bucket): 2019-05-21 08:08:38+00:00
Total Files: 3
Total Files Size = 0.003 MB
```

-  The following is an example to get Cost Summary in Json format
`time python s3inspect -gc  --granularity MONTHLY --metrics 'BlendedCost' --timeperiod '{"Start":"2019-01-01","End":"2019-05-20"}' test*`
