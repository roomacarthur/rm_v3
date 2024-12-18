# How to recover a forgotten superuser username in django


So you open up your project and you can't remeber your useruser name for some reason, and you really don't want to create a new one. We can recover the usperuser name using the Django Shell. 


## Recovering the superuser username. 

So first of all we need to navigate into the shell, This can be done by running the following in your terminal. 

```bash
python manage.py shell
```

Once we are inside the shell we can run a few lines of code to recover usernames relating to accounts that are superusers. 

NOTE: we need to use shift+enter when in the shell to navigate to the next line without submitting the line of code. 

```python
from django.contrib.auth.models import User
superusers = User.objects.filter(is_superuser=True)

for superuser in superusers:
    print(f"Username: {superuser.username}")
```

The above command will return a the username for all users that are flagged as superusers. 


## But wait, what about a forgotten superuser password? 

well that's much easier, we can simply run the following in the terminal, swapping out `superuser_username` with the actual username for the superuser you wish to change the password for. 

```bash
python manage.py changepassword superuser_username
```