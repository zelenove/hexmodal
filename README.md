### Prereqs:
- This project requires UV, which can be installed by following the instructions at: https://docs.astral.sh/uv/getting-started/installation/
- Install deps: `uv sync`

### Getting started:
- Run migrations: `uv run manage.py migrate`
- Create a user: `uv run manage.py createsuperuser`
- Run server: `uv run manage.py runserver`
- To get a token run the following in a Python shell:
  ```
  from rest_framework.authtoken.models import Token
  from django.contrib.auth.models import User
  
  user = User.objects.get(username="youruser")
  token, _ = Token.objects.get_or_create(user=user)
  
  print(token.key)
  ```
  Then use the following header for requests: `Authorization: Token <token>`