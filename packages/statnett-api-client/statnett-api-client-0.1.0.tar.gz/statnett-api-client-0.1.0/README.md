# Statnett API Client

Client presents methods for reading real-time Nordic power balance data provided 
by the Norwegian Transmission System Operator ([statnett.no](https://www.statnett.no/)). 

The full list of topics accessible via Statnett REST API can be seen [here](http://driftsdata.statnett.no/restapi).

Client supports reading of the following data:

* [Nordic Power Balance](https://www.statnett.no/en/for-stakeholders-in-the-power-industry/data-from-the-power-system/#nordic-power-balance)
* [Nordic Power Flow](https://www.statnett.no/en/for-stakeholders-in-the-power-industry/data-from-the-power-system/#nordic-power-flow)

## Installation

To install the Client, simply use pip:

```
$ pip install statnett_api_client
``` 

## Client initialization

Firstly, you need to initialize the client. By default, it will return data in json format. 
You can specify `fmt` parameter to receive data as pandas dataframe. 

```python
from statnett_api_client import Client

# this client will return json array
client = Client()
# this client will return pandas dataframe
client = Client(fmt='pandas')
# this client will return pandas dataframe with datetime index
client = Client(fmt='pandas', date2index=True)
```

By default, the time is in UTC. To add a column with Central European Time (CET), 
you need to specify `time_cet` parameter.

```python
client = Client(fmt='pandas', time_cet=True)
```

## Reading data

After you have set the client, you can read data from supported topics.

```python
# read power flow 
flow = client.get('flow')
# read power balance
balance = client.get('balance')
```

## License

The Client is released under [MIT License](https://github.com/viktorsapozhok/statnett-api-client/blob/master/LICENSE). 
