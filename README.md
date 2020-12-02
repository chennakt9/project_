# Mini - Face


```
Run
>python server.py

Run
>python 1_client.py

User name : test1
Password : pass1
```

For running on mininet

Open a terminal on Ubuntu

Run
```
>sudo tree_topo_manual.py
```
Then
```
mininet> xterm h1 h2 h3 h4
```

On xterm h4, run ``` python server.py ```

On xterms h1,h2,h3 run ``` python 1_client.py ``` , ``` python 2_client.py ``` , ``` python 3_client.py ``` respectively

