# Test Driven Development To-Do List

## Configuration, Build and Deployment
### Prerequsities:
- [Docker](https://www.docker.com/)
- [AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/install-cliv2.html)
- Python 3.10+ and `pip`
- An active AWS EC2 instance
- Your ssh private key `.pem` file for ec2 access

### Clone the repo
```
git clone https://github.com/SzymonIwaniuk/tdd_todo_app
cd tdd_todo_app
```

### Setup enviroment
In the project root
```bash
touch .env
```
Add the following
```bash
export EMAIL_PASSWORD="your_smtp_email_password"
```
Setup python venv
```
python -m venv .venv
source .venv/bin/activate
```
Install dependencies
```
pip install -r requirements.txt
```
In src/superlists/settings.py update:
```python
EMAIL_HOST = "smtp.gmail.com"
EMAIL_HOST_USER = "your_email@gmail.com"
EMAIL_HOST_PASSWORD = os.environ.get("EMAIL_PASSWORD")
EMAIL_PORT = 587
EMAIL_USE_TLS = True
```

### Database migrations
Run the following
```
python src/manage.py makemigrations
python src/manage.py migrate
```

### FTs configuration
Edit src/functional_tests/container_commands.py
```python
USER = "ubuntu"  # based on your ec2 ami
PEM_KEY_PATH = os.path.expanduser("/absolute/path/to/your/private_key_file.pem")
```

### Run with docker
To build and run the app using docker (by defalut on localhost:8888)
```
source .env
docker compose up
```

### Ansible configuration
Open infra/ansible.cfg and set:
```ini
private_key_file = /absolute/path/to/your/private_key_file.pem
remote_user = ubuntu  # or ec2-user depending on ami
```
Open infra/aws_ec2.yml and set
```yaml
regions:
  - region-of-your-ec2
tag:Name: your-ec2-instance-name
```






