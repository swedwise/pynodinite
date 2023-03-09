# PyNodinite

A series of `logging.Handler`-implementations producing 
[Nodinite JSON Log Events](https://docs.nodinite.com/Documentation/CoreServices?doc=/Log%20API/Features/Log%20Event/Json%20Formatted)
and sending these to one of the supported [intermediary storages]().

https://docs.nodinite.com/Documentation/LoggingAndMonitoring/Apache%20Camel%20-%20Logging#move-logged-events-using-the-nodinite-pickup-service

## Installation
 
```shell
pip install pynodinite
```

The default installation enables the use of File/Disk storage and Direct LogAPI transfer handlers only

There are several options to install additional packages for the specific intermediary storage 
that you want to use:

- `pip install pynodinite[activemq]` - Installs packages to send to ActiveMQ queues
- `pip install pynodinite[eventhub]` - Installs packages to send to Azure Event Hub
- `pip install pynodinite[msmq]` - Installs packages to send to Microsoft Message Queues
- `pip install pynodinite[postgresql]` - Installs packages to send to PostgreSQL database
- `pip install pynodinite[servicebus]` - Installs packages to send to Azure Service Bus
- `pip install pynodinite[sqlserver]` - Installs packages to send to Microsoft SQL Server database
  - Installs `pyodbc`