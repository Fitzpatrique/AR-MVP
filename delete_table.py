import boto3
import key_config as keys

dynamodb = boto3.resource('dynamodb', aws_access_key_id=keys.ACCESS_KEY_ID, aws_secret_access_key=keys.ACCESS_SECRET_KEY, region_name='eu-west-2')

usertable = dynamodb.Table('users')
vendortable = dynamodb.Table('vendors')
carttable = dynamodb.Table('carts')
ordertable = dynamodb.Table('orders')
collectiontable = dynamodb.Table('collections')
categorytable = dynamodb.Table('categories')
producttable = dynamodb.Table('products')
wishlisttable = dynamodb.Table('wishlists')

usertable.delete()
vendortable.delete()
carttable.delete()
ordertable.delete()
collectiontable.delete()
categorytable.delete()
producttable.delete()
wishlisttable.delete()