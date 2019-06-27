generate secret key:
```python
python3 -c 'import os; print(os.urandom(24).hex())'
```

replace secret_key value in docker-compose

run compose
```docker
docker-compose up -d --build
```

create db with tables and data
```docker
docker exec -ti flask python fixture.py
```
