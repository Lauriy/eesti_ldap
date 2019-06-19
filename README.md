# Running

```bash
docker-compose up
```

# Create superuser

```bash
docker exec -it eesti-ldap sh
python manage.py createsuperuser
```

# Run tests

```bash
docker exec -it eesti-ldap sh
pytest
```

# Trivia

- Celery needs hard restarts if you're changing tasks, doesn't refresh like dev Django.

- Running a single test test verbose:
    ```bash 
    pytest -k test_parse_ldap_result -slv
    ```
    
- python-ldap for venv on Windows:
  https://www.lfd.uci.edu/~gohlke/pythonlibs/#python-ldap