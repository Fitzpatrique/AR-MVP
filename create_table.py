import boto3
import key_config as keys

dynamodb = boto3.resource('dynamodb', aws_access_key_id=keys.ACCESS_KEY_ID, aws_secret_access_key=keys.ACCESS_SECRET_KEY, region_name='eu-west-2')

# Create the Users DynamoDB table.

usertable = dynamodb.create_table(
    TableName='users',
    KeySchema=[
        {
            'AttributeName': 'email',
            'KeyType': 'HASH'
        }
         
    ],
    AttributeDefinitions=[
             {
            'AttributeName': 'email',
            'AttributeType': 'S'
        } 
    ],
    ProvisionedThroughput={
        'ReadCapacityUnits': 5,
        'WriteCapacityUnits': 5
    }
)

# Wait until the table exists.
usertable.meta.client.get_waiter('table_exists').wait(TableName='users')

# Create the Vendors DynamoDB table.

vendortable = dynamodb.create_table(
    TableName='vendors',
    KeySchema=[
        {
            'AttributeName': 'email',
            'KeyType': 'HASH'
        }
         
    ],
    AttributeDefinitions=[
             {
            'AttributeName': 'email',
            'AttributeType': 'S'
        } 
    ],
    ProvisionedThroughput={
        'ReadCapacityUnits': 5,
        'WriteCapacityUnits': 5
    }
)

# Wait until the table exists.
vendortable.meta.client.get_waiter('table_exists').wait(TableName='vendors')

# Create the Products DynamoDB table.

producttable = dynamodb.create_table(
    TableName='products',
    KeySchema=[
        {
            'AttributeName': 'producttitle',
            'KeyType': 'HASH'
        }
         
    ],
    AttributeDefinitions=[
             {
            'AttributeName': 'producttitle',
            'AttributeType': 'S'
        } 
    ],
    ProvisionedThroughput={
        'ReadCapacityUnits': 5,
        'WriteCapacityUnits': 5
    }
)

# Wait until the table exists.
producttable.meta.client.get_waiter('table_exists').wait(TableName='products')

# Create the Wishlist DynamoDB table.

wishlisttable = dynamodb.create_table(
    TableName='wishlists',
    KeySchema=[
        {
            'AttributeName': 'producttitle',
            'KeyType': 'HASH'
        }
         
    ],
    AttributeDefinitions=[
             {
            'AttributeName': 'producttitle',
            'AttributeType': 'S'
        } 
    ],
    ProvisionedThroughput={
        'ReadCapacityUnits': 5,
        'WriteCapacityUnits': 5
    }
)

# Wait until the table exists.
wishlisttable.meta.client.get_waiter('table_exists').wait(TableName='wishlists')

# Create the Carts DynamoDB table.

carttable = dynamodb.create_table(
    TableName='carts',
    KeySchema=[
        {
            'AttributeName': 'cartid',
            'KeyType': 'HASH'
        },
		{
            'AttributeName': 'email',
            'KeyType': 'RANGE'
        }
         
    ],
    AttributeDefinitions=[
             {
            'AttributeName': 'cartid',
            'AttributeType': 'S'
        },
		{
            'AttributeName': 'email',
            'AttributeType': 'S'
        }, 
    ],
    ProvisionedThroughput={
        'ReadCapacityUnits': 5,
        'WriteCapacityUnits': 5
    }
)

# Wait until the table exists.
carttable.meta.client.get_waiter('table_exists').wait(TableName='carts')

# Create the Collections DynamoDB table.

collectiontable = dynamodb.create_table(
    TableName='collections',
    KeySchema=[
        {
            'AttributeName': 'collectiontitle',
            'KeyType': 'HASH'
        }
         
    ],
    AttributeDefinitions=[
             {
            'AttributeName': 'collectiontitle',
            'AttributeType': 'S'
        } 
    ],
    ProvisionedThroughput={
        'ReadCapacityUnits': 5,
        'WriteCapacityUnits': 5
    }
)

# Wait until the table exists.
collectiontable.meta.client.get_waiter('table_exists').wait(TableName='collections')

# Create the Categories DynamoDB table.

categorytable = dynamodb.create_table(
    TableName='categories',
    KeySchema=[
        {
            'AttributeName': 'categorytitle',
            'KeyType': 'HASH'
        }
         
    ],
    AttributeDefinitions=[
             {
            'AttributeName': 'categorytitle',
            'AttributeType': 'S'
        } 
    ],
    ProvisionedThroughput={
        'ReadCapacityUnits': 5,
        'WriteCapacityUnits': 5
    }
)

# Wait until the table exists.
categorytable.meta.client.get_waiter('table_exists').wait(TableName='categories')

# Create the Orders DynamoDB table.

ordertable = dynamodb.create_table(
    TableName='orders',
    KeySchema=[
        {
            'AttributeName': 'reference',
            'KeyType': 'HASH'
        }
         
    ],
    AttributeDefinitions=[
             {
            'AttributeName': 'reference',
            'AttributeType': 'S'
        } 
    ],
    ProvisionedThroughput={
        'ReadCapacityUnits': 5,
        'WriteCapacityUnits': 5
    }
)

# Wait until the table exists.
ordertable.meta.client.get_waiter('table_exists').wait(TableName='orders')



# Print out some data about the tables.
print(usertable.item_count,vendortable.item_count,producttable.item_count,wishlisttable.item_count,carttable.item_count,collectiontable.item_count,categorytable.item_count,ordertable.item_count)