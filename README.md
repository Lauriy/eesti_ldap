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
