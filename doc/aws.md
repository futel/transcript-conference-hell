# AWS deployment

# Setup

To be done once.

## Create AWS user

Use the AWS IAM ("Identity and Access Management") web console.

Create AWS user
- user details
 - name transcript-conference-hell
- set permissions
 - user groups s3-writers
   - this has s3-get-put-delete, s3 list-bucket-content

Update .env with the attributes of the user:
- AWS_ACCESS_KEY_ID
- AWS_SECRET_ACCESS_KEY

XXX

(the permissions and groups are probably not needed?)
description: transcript-conference-hell actions
permissions policies:
- s3-get-put-delete
- s3 list-bucket-content
groups:
- s3-writers

## Create transcript-conference-hell S3 bucket

Use the S3 web console.

type: general purpose
name: transcript-conference-hell
aws region: us-west-2
object ownership: acls disabled
block public access settings: block all public access off

XXX I edited this in the console, not accurate anymore?

Update permissions and add a bucket policy. Use the ARN of the created transcript-conference-hell user.

```
{
	"Version": "2012-10-17",
	"Statement": [
		{
			"Sid": "statement1",
			"Effect": "Allow",
			"Principal": {
				"AWS": "arn:aws:iam::168594572693:user/transcript-conference-hell"
			},
			"Action": "*",
			"Resource": [
                 "arn:aws:s3:::transcript-conference-hell/*",
                 "arn:aws:s3:::transcript-conference-hell"
            ]
		},
		{
			"Sid": "statement2",
			"Effect": "Allow",
			"Principal": {
				"AWS": "*"
			},
			"Action": "s3:GetObject",
			"Resource": "arn:aws:s3:::transcript-conference-hell/*"
		}
	]
}
```