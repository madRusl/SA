#### docker
###### generate secret key:
```python
python3 -c 'import os; print(os.urandom(24).hex())'
```

###### replace secret_key value in docker-compose

###### run compose
```docker
docker-compose up -d --build
```

###### create db with tables and data
```docker
docker exec -ti flask python fixture.py
```

###### for test purpose
```bash
curl -X POST -d @/tmp/hardware_data.xml  -H "Accept: application/xml"  -H "Content-Type: application/xml" http://127.0.0.1:5000/api/hardware?ip_addr=$(ipconfig getifaddr en0)

curl -X POST -d @/tmp/sys_data.xml  -H "Accept: application/xml"  -H "Content-Type: application/xml" "http://127.0.0.1:5000/api/system?serialnumber=$(system_profiler SPHardwareDataType | awk '/Serial/ {print $4}')&userlist=$(dscl . list /Users | grep -vE '_|root|root8|admin|nobody|daemon|Guest')"

curl -X POST -d @/tmp/app_data.xml  -H 'Accept: application/xml'  -H 'Content-Type: application/xml' http://127.0.0.1:5000/api/applications?serialnumber=$(system_profiler SPHardwareDataType | awk '/Serial/ {print $4}')
```

#### ansible
install ansible and in hosts file set values for:
```
ansible_user=
ansible_ssh_pass=
ansible_ssh_private_key_file=
```
###### and run
```
ansible-playbook playbook.yml -i hosts -l all
```
