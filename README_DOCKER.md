- Construire l'image :

  docker-compose build

- Lancer les services en arrière-plan :

  docker-compose up -d

- Récupérer les logs :

  docker-compose logs -f

- Exécuter une commande dans le conteneur web :

  docker-compose exec web bash

- Si collectstatic n'a pas été exécuté automatiquement :

  docker-compose exec web python manage.py collectstatic --noinput
