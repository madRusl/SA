# SA

##installation

generate secret key:
```python
python3 -c 'import os; print(os.urandom(24).hex())'
```

replace secret_key in dockerfile env

run compose
```docker
docker-compose up -d --build
```

create db with tables and data
```docker
docker exec -ti flask python fixture.py
```
