On macOS use the command `lsof -i` with the port number to find out what is running on a specific port.

```shell
sudo lsof -i :<PortNumber>
```

> This will work for linux as well ;) 

### Kill the process running on a specific port 
use the `kill` command with the -9 option and the port PID number to kill a process


```shell
kill -9 <PID>
```