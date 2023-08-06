"""
    Example of usage.
    To run do in the command line: s3inspect -h

    The tool must return the following information
        Bucket name - Done
        Creation date (of the bucket) - Done
        Number of files - Done
        Total size of files - Done
        Last modified date (most recent file of a bucket) - Done
        And the most important of all, how much does it cost
    The following options should be supported
        Ability to get the size results in bytes, KB, MB, ... - Done
        Organize the information by storage type (Standard, IA, RR) - Done
        Filter the results in a list of buckets (bonus point for regex support)
        Ability to group information by regions - Done
    Some additional features that could be useful (optional)
        It would be nice to support prefix in the bucket filter
        (e.g.: s3://mybucket/Folder/SubFolder/log*).
        It may also be useful to organize the results according to the
        encryption type, get additional buckets information (life cycle,
        cross-region replication, etc.) or take into account the previous
        file versions in the count + size calculation.

        Some statistics to check the percentage of space used by a bucket,
        or any other good ideas you could have, are more than welcome.


"""
import sys
import json
from s3inspect import S3Inspect
import argparse
import boto3
import datetime
import re
def main():
    # import pdb;pdb.set_trace()
    parser = argparse.ArgumentParser(description='Inspect S3 Bucket')


    parser.add_argument('-u', '--unit', type=str,
                       default='mb', choices=['b','kb','mb','gb'],
                       help='Return files sizes in these units: b (bytes), \
                            kb (kilobytes), mb (megabytes), gb (gigabytes)'
                        )
    parser.add_argument('regex', type=str,
                       help='Regex Support for Buckets list)'
                        )

    parser.add_argument('-p', '--prefix', type=str,
                       default='',
                       help='Add prefix for the keys. Example: \
                            images/'
                        )
    parser.add_argument('-gs', '--groubystoragetype', action='store_true',
                       help='When this is set information is grouped by Storage\
                       Type'
                        )
    parser.add_argument('-gr', '--groubyregion', action='store_true',
                       help='When this is set information is grouped by Region\
                       Type'
                        )

    parser.add_argument('-gc', '--getcost', action='store_true',
                       help='When this is set cost report is returned\
                       Type'
                        )
    parser.add_argument('--timeperiod', type=str,
                        help="Example: '{\"Start\":\"2019-01-01\",\"End\":\"2019-05-20\"}'"
                        )
    parser.add_argument('--granularity', type=str,
                        help="Example: MONTHLY"
                        )
    parser.add_argument('--metrics', type=str,
                        help="Example: 'BlendedCost UNBLENDED_COST AMORTIZED_COST'"
                        )
    # parser.add_argument('-s', '--suffix', type=str,
    #                    default='',
    #                    help='Add suffix for the keys. Example: \
    #                         .jpg'
    #                     )
    parser.add_argument('-l', '--list', action='store_true',
                       help='Displays a list of available S3 Buckets in account'
                        )
    # parser.add_argument('bucket_name', type=str,
    #                    help='Name of the bucket to inspect')


    args = parser.parse_args()


    s = S3Inspect(args)
    total_size = 0
    file_count = 0
    filtered_bucket_list = []
    bucket_found = False

    bucket_list = s._list_buckets()


    if args.list:
        print("------------------------------------------------------------------")
        print("List of All buckets in account")
        print("Bucket Name\t\t\t|\t\t CreationDate")
        for bucket in bucket_list:
            print("{}\t\t\t|\t\t\t {}".format(bucket['Name'], bucket['CreationDate']))
    elif args.getcost:
        args.timeperiod=json.loads(args.timeperiod)
        args.metrics = args.metrics.split()

        cost_report = s._get_cost_and_usage(args)

        print(cost_report)
    elif args.regex is not None:
        # r = re.compile(args.regex)
        for buckets in bucket_list:
            if re.match(args.regex, buckets['Name']):
                filtered_bucket_list.append({'Name':buckets['Name'], 'CreationDate': buckets['CreationDate']})
                bucket_found = True
        if bucket_found:
            for buckets in filtered_bucket_list:
                try:
                    bucket_region = s._get_bucket_location(Bucket=buckets['Name'])
                    s.report['Regions'].setdefault(bucket_region,{})
                    s.report['Regions'][bucket_region].setdefault('Buckets', {})
                    s.report['Regions'][bucket_region]['Buckets'].setdefault(buckets['Name'], {})
                    s.report['Regions'][bucket_region]['Buckets'][buckets['Name']].setdefault('CreationDate', buckets['CreationDate'])
                    total_size = 0
                    file_count = 0
                    try:
                        for key, size, storage_class in \
                                s._get_matching_s3_keys(
                                        bucket=buckets['Name'],
                                        bucket_region=bucket_region,
                                            # maxkeys=2,
                                            prefix=args.prefix):

                            total_size += size
                            file_count += 1
                            s.report['Regions'][bucket_region]['Buckets'][buckets['Name']]['StorageClasses'][storage_class].setdefault('Total_Size', total_size)
                            s.report['Regions'][bucket_region]['Buckets'][buckets['Name']]['StorageClasses'][storage_class].setdefault('File_Count', file_count)
                        s.report['Regions'][bucket_region]['Buckets'][buckets['Name']]['StorageClasses'][storage_class]['Total_Size'] = total_size
                        s.report['Regions'][bucket_region]['Buckets'][buckets['Name']]['StorageClasses'][storage_class]['File_Count'] = file_count


                    except Exception as e:
                        print ("Failed to fetch keys in S3 Bucket Regex Requested: {}".format(args.regex))
                        print (e)
                except Exception as e:
                    print ("WARNING: Cannot read bucket: {}...Continuing".format(buckets['Name']))
                    print (e)

            s._show_bucket_details(args)

        else:
            print("------------------------------------------------------------------")
            print("No Buckets found with matching Regex: {}. \
                    \nPlease choose from the available bucket list. Using: \
                    \n\t-l or --list option Or \
                    \n\t-h or --help for more options \
                    ".format(args.regex))
            print("------------------------------------------------------------------")
if __name__== "__main__":
    main()
