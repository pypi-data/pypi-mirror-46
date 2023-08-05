# realtime-aws-secretsmngr

This package will provide a class called RealTimeAwsSecretsMngr.

## Usage

```python
secretsmngr = RealTimeAwsSecretsMngr(region="us-east-2",secretId="XXX",apiId="XXXX")
  def callback(secret):
      print(secret)
  secretsmngr.subscribe(callback)

```
