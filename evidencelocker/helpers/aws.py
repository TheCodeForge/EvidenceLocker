import boto3

from os import remove
from io import BytesIO
from evidencelocker.__main__ import app

#set up AWS connection
S3 = boto3.client(
	"s3",
	aws_access_key_id=app.config["AWS_ACCESS_KEY_ID"],
	aws_secret_access_key=app.config["AWS_SECRET_ACCESS_KEY"]
	)

def s3_upload_file(name, file):

	tempname=name.replace("/","_")

	file.save(tempname)

	S3.upload_file(
		name,
		Bucket=app.config["S3_BUCKET_NAME"],
		Key=name,
		ExtraArgs={
			"ContentType":"image/png",
			"StorageClass":"INTELLIGENT_TIERING"
			}
		)

	remove(tempname)

def s3_download_file(name):

	with BytesIO() as f:
		S3.download_fileobj(
			app.config["S3_BUCKET_NAME"],
			name,
			f
			)
		f.seek(0)
		return f.read()