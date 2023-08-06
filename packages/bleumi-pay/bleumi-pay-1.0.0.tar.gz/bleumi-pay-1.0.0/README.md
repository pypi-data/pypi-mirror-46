# Bleumi Pay SDK for Python

The Bleumi Pay SDK is a one-stop shop to help you integrate stablecoin payments (on Ethereum & Stellar Networks) into your business or application. The SDK bundles [Bleumi Pay API](https://pay.bleumi.com/docs/#introduction) into one SDK to ease implementation and support.

bleumi-pay-sdk-python is a Python library that provides an interface between your Python application and [Bleumi Pay API](https://pay.bleumi.com/docs/#introduction). This tutorial covers the basics, including examples, needed to use the SDK.

## Getting Started

### Pre-requisites

#### Development Environment

Python 2.7 and 3.4+

#### Obtain An API Key

Bleumi Pay SDK uses API keys to authenticate requests. You can obtain an API key through the [Bleumi Pay developer portal](https://pay.bleumi.com/app/).

### Install Package
### pip install

If the python package is hosted on Github, you can install directly from Github

```sh
pip install git+https://github.com/bleumi/bleumi-pay-sdk-python.git
```
(you may need to run `pip` with root permission: `sudo pip install git+https://github.com/bleumi/bleumi-pay-sdk-python.git`)

Then import the package:
```python
import bleumi_pay 
```

### Setuptools

Install via [Setuptools](http://pypi.python.org/pypi/setuptools).

```sh
python setup.py install --user
```
(or `sudo python setup.py install` to install the package for all users)

Then import the package:
```python
import bleumi_pay
```

### Run Sample Code

The following code funds a Stellar Address (targetAddress) with 10,000 tokens on the test network.

Note: Please ensure the targetAddress meets the Minimum Account Balance & Trustline requirements before running this sample code. For details, please visit [How to establish Stellar Trustline documentation](http://pay.bleumi.com/wp-content/uploads/2019/05/trustline_stellar.pdf).

```python
from __future__ import print_function
import time
import bleumi_pay
from bleumi_pay.rest import ApiException
from pprint import pprint

# Configure API key authorization: ApiKeyAuth
configuration = bleumi_pay.Configuration()
configuration.api_key['x-api-key'] = '<Your API Key>' # Replace <Your API Key> with your actual API key


# create an instance of the API class
api_instance = bleumi_pay.DevelopmentApi(bleumi_pay.ApiClient(configuration))
addr = '<STELLAR ADDRESS>'; # String | Replace <STELLAR ADDRESS> with an actual Stellar Network Address 
issuer = 'GDWEVA6U7ZUKAWERV336BIQ7T3UNLLKSF4ENFK3GZ3Q35ZSU7SWH6AYV' # StellarAddress of Asset Issuer (Test)

try:
    # Fund Stellar test addresses with 10,000 tokens
    api_instance.friendbot(addr, issuer)
except ApiException as e:
    print("Exception when calling DevelopmentApi->friendbot: %s\n" % e)
```

Use the Stellar Laboratory's [Endpoint Explorer](https://www.stellar.org/laboratory/#explorer?resource=accounts&endpoint=single&network=test) or the following URL to check the balance of the target address.

```
https://horizon-testnet.stellar.org/accounts/<targetAddress>
```

More examples can be found under each method in [SDK Classes](README.md#sdk-classes) section.

## SDK Classes

Class | Method | HTTP request | Description
------------ | ------------- | ------------- | -------------
PaygPaymentsApi | [**create_payment**](docs/PaygPaymentsApi.md#create_payment) | **POST** /v1/payment/payg/{id} | Create a payment request.
PaygPaymentsApi | [**update_payment**](docs/PaygPaymentsApi.md#update_payment) | **PUT** /v1/payment/payg/{id} | Update a payment request.
PaygPaymentsApi | [**get_payment**](docs/PaygPaymentsApi.md#get_payment) | **GET** /v1/payment/payg/{id} | Retrieves a specific payment request.
PaygPaymentsApi | [**list_payments**](docs/PaygPaymentsApi.md#list_payments) | **GET** /v1/payments/payg | Retrieves all PAYG payment requests.
PaygPaymentsApi | [**cancel_payment**](docs/PaygPaymentsApi.md#cancel_payment) | **POST** /v1/payment/payg/{id}/cancel | Cancels a specific payment. Any amount received will be refunded (minus charges) to the address specified in fromAddress.
PaygPaymentsApi | [**settle_payment**](docs/PaygPaymentsApi.md#settle_payment) | **POST** /v1/payment/payg/{id}/settle | Settle a specific payment which has been partially paid. Current balance (minus charges) will be sent to the address specified in toAddress.
PaygPaymentsApi | [**extend_payment**](docs/PaygPaymentsApi.md#extend_payment) | **POST** /v1/payment/payg/{id}/extend | Enable processing for a payment for 7 days from date of invocation
GasApi | [**estimate_gas**](docs/GasApi.md#estimate_gas) | **GET** /v1/gas/estimate | Provides an estimate of the Ethereum Network Fee for an ERC20 Token.
DevelopmentApi | [**friendbot**](docs/DevelopmentApi.md#friendbot) | **GET** /v1/friendbot | Provides 10,000 tokens to any Stellar address on the test network.


## Documentation For Models

 - [Address](docs/Address.md)
 - [BadRequest](docs/BadRequest.md)
 - [ERC20PaymentAddress](docs/ERC20PaymentAddress.md)
 - [ERC20Token](docs/ERC20Token.md)
 - [EstimatedGas](docs/EstimatedGas.md)
 - [EthAddress](docs/EthAddress.md)
 - [EthNetwork](docs/EthNetwork.md)
 - [PaginatedPayments](docs/PaginatedPayments.md)
 - [Payment](docs/Payment.md)
 - [PaymentAddress](docs/PaymentAddress.md)
 - [PaymentCreateInput](docs/PaymentCreateInput.md)
 - [PaymentStatus](docs/PaymentStatus.md)
 - [PaymentUpdateInput](docs/PaymentUpdateInput.md)
 - [StellarAddress](docs/StellarAddress.md)
 - [StellarMemo](docs/StellarMemo.md)
 - [StellarNetwork](docs/StellarNetwork.md)
 - [StellarPaymentAddress](docs/StellarPaymentAddress.md)
 - [StellarToken](docs/StellarToken.md)
 - [Token](docs/Token.md)
 - [Transfer](docs/Transfer.md)

## Limitations

 - [Bleumi Pay API Limits](https://pay.bleumi.com/docs/#api-limits)


## License

Copyright 2019 Bleumi, Inc.

Code licensed under the [MIT License](docs/MITLicense.md). 



