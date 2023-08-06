
####To install 
```
pip install ohmylamb  
```

####To Configure

To configure define team name, application name and environment name in app.ini file.
```
echo "[app]" >> app.ini
echo "name = adl-common-pytools" >> app.ini
echo "team = adl-dse" >> app.ini
echo "env = dev" >> app.ini

```

####To import into code add following
```
from ohmylamb import ohmylamb as oml

```

####Configuration handling
Configuration management has been split into three areas.

- Application configuration. This comes from aap.ini file. This configuration can be accessed using following code.
    ```
    

    ```

