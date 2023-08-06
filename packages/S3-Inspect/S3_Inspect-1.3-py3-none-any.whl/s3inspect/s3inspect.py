import uuid
import boto3
from datetime import datetime
from dateutil.tz import tzutc


class S3Inspect():

    def __init__(self, args):
        self.s3_client = boto3.client('s3')
        # self.s3_client = s3_client
        self.args = args
        self.report = {}
        self.report.setdefault('Regions',{})


    @staticmethod
    def _create_bucket_name(bucket_prefix):
        # The generated bucket name must be between 3 and 63 chars long
        return ''.join([bucket_prefix, str(uuid.uuid4())])

    def _create_bucket(self, bucket_prefix, s3_connection):
        session = boto3.session.Session()
        current_region = session.region_name
        bucket_name = self._create_bucket_name(bucket_prefix)
        bucket_response = s3_connection.create_bucket(
            Bucket=bucket_name,
            CreateBucketConfiguration={
            'LocationConstraint': current_region})
        print(bucket_name, current_region)
        return bucket_name, bucket_response


    def _get_cost_and_usage(self, args):
        client = boto3.client('ce')
        response = client.get_cost_and_usage(TimePeriod=args.timeperiod,Granularity=args.granularity, Metrics=args.metrics)
        return response
    # def _read_s3_buckets(self, s3_connection):
    #     return s3_connection.buckets.all()

    def _list_buckets(self):
        list_buckets = self.s3_client.list_buckets()
        return  list_buckets['Buckets']

    def _show_bucket_details(self, args):
        file_count = 0
        total_size = 0
        try:

            print("------------------------------------------------------------------")
            print("S3 Bucket Inspection Report:")
            if args.groubyregion:
                for bucket_region in self.report['Regions'].keys():
                    print("------------------------------------------------------------------")
                    print("Bucket Region: {}".format(bucket_region))
                    print("------------------------------------------------------------------")
                    for bucket in self.report['Regions'][bucket_region]['Buckets'].keys():
                        print("\t------------------------------------------------------------------")
                        print("\tBucket Name: {}".format(bucket))
                        print("\t------------------------------------------------------------------")
                        print("\tBucket Creation Date: {}".format(self.report['Regions'][bucket_region]['Buckets'][bucket]['CreationDate']))
                        print("\tRecent File Modification Date (Bucket): {}".format(
                                    self.report['Regions'][bucket_region]['Buckets'][bucket]['RECENT_FILE_MODIFICATION_DATE']))
                        if args.groubystoragetype:
                            for storage_class in self.report['Regions'][bucket_region]['Buckets'][bucket]['StorageClasses'].keys():
                                print("\t\t------------------------------------------------------------------")
                                print ("\t\tStorage Class: {}".format(storage_class))
                                print("\t\t------------------------------------------------------------------")
                                print("\t\tTotal Files: {}".format(self.report['Regions'][bucket_region]['Buckets'][bucket]['StorageClasses'][storage_class]['File_Count']))
                                self._print_total_size(self.report['Regions'][bucket_region]['Buckets'][bucket]['StorageClasses'][storage_class]['Total_Size'], indent="\t\t")
                                print("\t\tModification Date (storage type): {}".format(self.report['Regions'][bucket_region]['Buckets'][bucket]['StorageClasses'][storage_class]['Modified_Date']))

                        else:
                            file_count = 0
                            total_size = 0
                            for storage_class in self.report['Regions'][bucket_region]['Buckets'][bucket]['StorageClasses'].keys():
                                file_count += self.report['Regions'][bucket_region]['Buckets'][bucket]['StorageClasses'][storage_class]['File_Count']
                                total_size += self.report['Regions'][bucket_region]['Buckets'][bucket]['StorageClasses'][storage_class]['Total_Size']
                            print("\tTotal Files: {}".format(file_count))
                            self._print_total_size(total_size, indent="\t")
            else:
                for bucket_region in self.report['Regions'].keys():
                    for bucket in self.report['Regions'][bucket_region]['Buckets'].keys():
                        print("------------------------------------------------------------------")
                        print("Bucket Name: {}".format(bucket))
                        print("------------------------------------------------------------------")
                        print("Bucket Creation Date: {}".format(self.report['Regions'][bucket_region]['Buckets'][bucket]['CreationDate']))
                        print("Recent File Modification Date (Bucket): {}".format(
                                    self.report['Regions'][bucket_region]['Buckets'][bucket]['RECENT_FILE_MODIFICATION_DATE']))
                        if args.groubystoragetype:
                            for storage_class in self.report['Regions'][bucket_region]['Buckets'][bucket]['StorageClasses'].keys():
                                print("\t------------------------------------------------------------------")
                                print ("\tStorage Class: {}".format(storage_class))
                                print("\t------------------------------------------------------------------")
                                print("\tTotal Files: {}".format(self.report['Regions'][bucket_region]['Buckets'][bucket]['StorageClasses'][storage_class]['File_Count']))
                                self._print_total_size(self.report['Regions'][bucket_region]['Buckets'][bucket]['StorageClasses'][storage_class]['Total_Size'], indent="\t")
                                print("\tModification Date (storage type): {}".format(self.report['Regions'][bucket_region]['Buckets'][bucket]['StorageClasses'][storage_class]['Modified_Date']))

                        else:
                            file_count = 0
                            total_size = 0
                            for storage_class in self.report['Regions'][bucket_region]['Buckets'][bucket]['StorageClasses'].keys():
                                file_count += self.report['Regions'][bucket_region]['Buckets'][bucket]['StorageClasses'][storage_class]['File_Count']
                                total_size += self.report['Regions'][bucket_region]['Buckets'][bucket]['StorageClasses'][storage_class]['Total_Size']
                            print("Total Files: {}".format(file_count))
                            self._print_total_size(total_size, indent="")
        except Exception as e:
            print ("Exception {} Occured while creating Report.. ".format(e))




        # print(self.report)
        # if args.groubystoragetype:
        #     for storage_class in self.report['Regions'][bucket_region]['Buckets'][bucket]['StorageClasses'].keys():
        #         print ("Storage Class: {}".format(storage_class))
        #         # print (self.report['Regions'][bucket_region]['Buckets'][bucket]['StorageClasses'][storage_class])
        #         print("\tTotal Files: {}".format(self.report['Regions'][bucket_region]['Buckets'][bucket]['StorageClasses'][storage_class]['File_Count']))
        #         self._print_total_size(self.report['Regions'][bucket_region]['Buckets'][bucket]['StorageClasses'][storage_class]['Total_Size'], indent="\t")
        #         print("\tModification Date (storage type)".format(self.report['Regions'][bucket_region]['Buckets'][bucket]['StorageClasses'][storage_class]['Modified_Date']))
        # else:
        #     for storage_class in self.report['Regions'][bucket_region]['Buckets'][bucket]['StorageClasses'].keys():
        #         file_count += self.report['Regions'][bucket_region]['Buckets'][bucket]['StorageClasses'][storage_class]['File_Count']
        #         total_size += self.report['Regions'][bucket_region]['Buckets'][bucket]['StorageClasses'][storage_class]['Total_Size']




    def _print_total_size(self, total_size, indent=""):
        if self.args.unit == 'b':
            print (indent + 'Total Files Size = %.3f B' % (total_size))
        elif self.args.unit == 'kb':
            print (indent + 'Total Files Size = %.3f KB' % (total_size/1024))
        elif self.args.unit == 'mb':
            print (indent + 'Total Files Size = %.3f MB' % (total_size/1024/1024))
        elif self.args.unit == 'gb':
            print (indent + 'Total Files Size = %.3f GB' % (total_size/1024/1024/1024))
        else:
            print (indent + "Warning: Unknown <unit> : {}".format(self.args.unit))
            print (indent + 'Total Files Size = %.3f B' % (total_size))

    def _get_bucket_location(self, Bucket):
        return self.s3_client.get_bucket_location(Bucket=Bucket)['LocationConstraint']


    def _get_matching_s3_keys(self, bucket, bucket_region, maxkeys=None, prefix=None ):
        """
        Generate the keys in an S3 bucket.

        :param bucket: Name of the S3 bucket.
        :param maxkeys: Maximum Keys to fetch. Default = 1000
        :param prefix: Only fetch keys that start with this prefix (optional).
        """

        # s3 = boto3.client('s3')

        s3 = self.s3_client
        kwargs = {'Bucket': bucket}
        get_last_modified = lambda obj: int(obj['LastModified'].strftime('%s'))
        # tzlocal = tz.tzoffset('utc',0)
        recent_date = datetime(1970,1,1,tzinfo=tzutc())
        # self.report.setdefault('StorageClasses',{})
        #

        # If the prefix is a single string (not a tuple of strings), we can
        # do the filtering directly in the S3 API.
        if isinstance(prefix, str):
            kwargs['Prefix'] = prefix

        if isinstance(maxkeys, int):
            kwargs['MaxKeys'] = maxkeys

        while True:

            # The S3 API response is a large blob of metadata.
            # 'Contents' contains information about the listed objects.
            resp = s3.list_objects_v2(**kwargs)

            if resp['KeyCount'] >= 1:
                contents = sorted(resp['Contents'], key=get_last_modified, reverse=True)
                last_modified_date = contents[0]['LastModified']

                if recent_date < last_modified_date:
                    recent_date = last_modified_date

                for obj in contents:
                    # print (obj)
                    key = obj['Key']
                    size = obj['Size']
                    storage_class = obj['StorageClass']
                    # self.report['Regions'][bucket_region]['Buckets'][bucket]['StorageClasses'].setdefault(storage_class, {'Total_Size':0, 'File_Count':0, 'Modified_Date':None})


                    modified_date_sc = obj['LastModified']
                    self.report['Regions'][bucket_region]['Buckets'][bucket].setdefault('StorageClasses', {})
                    self.report['Regions'][bucket_region]['Buckets'][bucket]['StorageClasses'].setdefault(storage_class,{})
                    self.report['Regions'][bucket_region]['Buckets'][bucket]['StorageClasses'][storage_class].setdefault('Modified_Date',None)

                    if self.report['Regions'][bucket_region]['Buckets'][bucket]['StorageClasses'][storage_class]['Modified_Date'] is None or \
                                self.report['Regions'][bucket_region]['Buckets'][bucket]['StorageClasses'][storage_class]['Modified_Date'] < modified_date_sc:
                        self.report['Regions'][bucket_region]['Buckets'][bucket]['StorageClasses'][storage_class]['Modified_Date'] = modified_date_sc


                    if key.startswith(prefix):
                        # print (key, size, storage_class, modified_date)
                        # print(obj)
                        yield key, size, storage_class
            else:
                raise Exception("No Keys found matching S3 Bucket filter... Exiting")

            # The S3 API is paginated, returning up to 1000 keys at a time.
            # Pass the continuation token into the next response, until we
            # reach the final page (when this field is missing).
            try:
                kwargs['ContinuationToken'] = resp['NextContinuationToken']
            except KeyError:
                # print("recent_date: {}".format(recent_date))
                self.report['Regions'][bucket_region]['Buckets'][bucket].setdefault('RECENT_FILE_MODIFICATION_DATE', recent_date)
                # self.report['RECENT_FILE_MODIFICATION_DATE'] =  recent_date
                return
