# Python Directchannel

DirectChannel Mentor API Client

## Overview

Questa libreria permette di interfacciarsi con gli endpoint del WS di Mentor Direct Channel. 
La documentazione degli endpoint e' reperibile qui:
http://dc.directchannel.it/mentor/supporto/default.aspx

### Requisiti

E' necessario avere installati i seguenti pacchetti

- python (2.7, 3.4, 3.5)
- requests (2.18.1)

### Installazione

Per installare la libreria e' sufficiente digitare:

        pip install python-directchannel

Quick start
-----------

Dopo aver installato la libreria e' possibile inizializzare l'oggetto DirectChannel e invocare i metodi per interrogare gli endpoint.

```python
    from pydirectchannel import DirectChannel
    d = DirectChannel(env="YOURENV", application="YOURAPPLICATION",
                     token="YOURTOKEN",
                     user="YOURUSER")
    d.wsc_table('tipiAnagrafica')
```

Per accedere all'ambiente di test e' possibile specificare test=True al costruttore dell'oggetto

```python
    from pydirectchannel import DirectChannel
    d = DirectChannel(env="YOURENV", application="YOURAPPLICATION",
                     token="YOURTOKEN",
                     user="YOURUSER", test=True)
```

## Available endpoints

1. wsc_table

2. wsc_save_donor

3. wsc_save_donation

4. wsc_save_product

5. wsc_save_regular

6. wsc_save_activity

7. wsc_save_privacy

8. wsc_get_children


## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details