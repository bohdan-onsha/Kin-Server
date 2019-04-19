import kin
import pprint

print('First we will create our KinClient object, and direct it to our test environment')
async with kin.KinClient(kin.TEST_ENVIRONMENT) as client:
    print('\nEnvironment: ')
    print(client.environment)


