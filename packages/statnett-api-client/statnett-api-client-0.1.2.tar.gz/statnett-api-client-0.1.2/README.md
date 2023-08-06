# Statnett API Client

Client presents methods for reading real-time Nordic power balance data provided 
by the Norwegian Transmission System Operator ([statnett.no](https://www.statnett.no/)). 

The full list of topics accessible via Statnett REST API can be seen [here](http://driftsdata.statnett.no/restapi).

Client supports reading of the following topics:

* [Nordic Power Balance](https://www.statnett.no/en/for-stakeholders-in-the-power-industry/data-from-the-power-system/#nordic-power-balance)
* [Nordic Power Flow](https://www.statnett.no/en/for-stakeholders-in-the-power-industry/data-from-the-power-system/#nordic-power-flow)

## Installation

To install the Client, simply use pip:

```
$ pip install statnett_api_client
``` 

## Basic Usage

```python
from statnett_api_client import Client
# initialize parser
client = Client(fmt='pandas')
# read power flow topic and return pandas dataframe 
flow = client.get('flow')
```

## Client

You can specify the format of returned object when initializing the client. By default, 
it will return data as json array. 

```python
client = Client()
```

To get the data as pandas object, you need to specify `fmt` parameter in constructor.
Specify `date2index` if you want to add dates to dataframe index.

```python
client = Client(fmt='pandas')
client = Client(fmt='pandas', date2index=True)
```

By default, the time is in UTC. To add a column with Central European Time (CET), 
you need to specify `time_cet` parameter.

```python
client = Client(fmt='pandas', time_cet=True)
```

Sometimes it can be useful to add `hour` column to result dataframe. It can be achieved by 
specifying `add_hour` keyword parameter. If `time_cet` is True, then two columns are added, 
`hour_utc` and `hour_cet`.   

```python
client = Client(fmt='pandas', time_cet=True, add_hour=True)
```

## Reading Data

After you have set the client, you can read data from supported topics. 

```python
# Nordic power flow 
flow = client.get('flow')
# Nordic power balance
balance = client.get('balance')
```

## License

The Client is released under [MIT License](https://github.com/viktorsapozhok/statnett-api-client/blob/master/LICENSE). 
