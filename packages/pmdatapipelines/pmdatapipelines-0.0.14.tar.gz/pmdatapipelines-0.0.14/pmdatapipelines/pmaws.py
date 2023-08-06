import boto3
from botocore.exceptions import ClientError

def parse_s3_event(event):

	try:
		s3_event = event['Records'][0]['s3']
		s3_key = unquote(s3_event['object']['key'])
		s3_bucket_name = s3_event['bucket']['name']
		return { 'type': 's3_event', 's3_key': s3_key, 's3_bucket_name': s3_bucket_name }
	except:
		if 's3_key' in event and 's3_bucket_name' in event:
			s3_key = event['s3_key']
			s3_bucket_name = event['s3_bucket_name']
			return { 'type': 'manual_event', 's3_key': s3_key, 's3_bucket_name': s3_bucket_name }
		else:
			raise KeyError('did not find s3_key and s3_bucket_name in event')


def upload_transformed_data_to_s3(b_io_buffer, source_s3_key, source_s3_bucket_name):

	target_s3_key = s3key.replace("raw", "transformed")
	target_s3_bucket_name = source_s3_bucket_name
	b_io_buffer.seek(0)
	try:
		target_bucket.upload_fileobj(b_io_buffer, target_s3_key)
		return 'success'
	except ClientError as e:
		raise Exception(e.response['Error']['Code'])


def upload_converted_data_to_s3(b_io_buffer, source_s3_key, source_s3_bucket_name):

	target_s3_key = s3key.replace("transformed", "queryable")
	target_s3_bucket_name = source_s3_bucket_name
	b_io_buffer.seek(0)
	try:
		target_bucket.upload_fileobj(b_io_buffer, target_key)
		return 'success'
	except ClientError as e:
		raise Exception(e.response['Error']['Code'])


def add_partitions(s3_key, s3_bucket_name, table_name, database_name):

	s3_key_parts = s3_key.split('/')
	s3_key_location = '/'.join(s3_key_parts[:-1])
	partitions = []
	for part in s3_key_parts:
		if '=' in part:
			partitions.append(part.split('='))
	athena_query = '''
	ALTER TABLE {} ADD
	'''.format(table_name)
	partitions_string = ''
	for key, value in partitions:
		partitions_string += '{} = \'{}\', '.format(key, value)
	partitions_string = partitions_string[:-2]
	athena_query += 'PARTITION (' + partitions_string + ')' + '\n'
	athena_query += 'LOCATION \'s3://{}/{}\''.format(s3_bucket_name, s3_key_location)
	athena_query += ';'
	athena_client = boto3.client('athena')
	response = athena_client.start_query_execution(
		QueryString = athena_query,
		QueryExecutionContext={
			"Database": database_name
		},
		ResultConfiguration = {
			"OutputLocation": "s3://{}/athena_output".format(s3_bucket_name)
		}
	)
	
	return response