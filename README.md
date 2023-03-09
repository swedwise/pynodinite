# PyNodinite

[![Hatch project](https://img.shields.io/badge/%F0%9F%A5%9A-Hatch-4051b5.svg)](https://github.com/pypa/hatch)
[![Test module](https://github.com/swedwise/pynodinite/actions/workflows/test.yml/badge.svg)](https://github.com/swedwise/pynodinite/actions/workflows/test.yml)

A series of `logging.Handler`-implementations producing 
[Nodinite JSON Log Events](https://docs.nodinite.com/Documentation/CoreServices?doc=/Log%20API/Features/Log%20Event/Json%20Formatted)
and sending these to one of the supported [intermediary storages](https://docs.nodinite.com/Documentation/LoggingAndMonitoring%2FPickup%20LogEvents%20Service?doc=/Overview#fa-ballot-check-features).

## Installation

```shell
pip install git+https://github.com/swedwise/pynodinite.git
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