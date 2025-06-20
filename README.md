# 🌿 CesiZen – Application Web de Détente

**CesiZen** est une application web développée avec **Django** et **Tailwind CSS**, permettant aux utilisateurs de consulter des activités de détente, de les ajouter en favoris (s’ils sont connectés), et aux modérateurs de gérer l’ensemble du contenu et des utilisateurs.

---

## 🚀 Fonctionnalités

- Consultation publique des activités et informations de bien-être
- Système d’authentification pour utilisateurs
- Ajout de favoris (utilisateurs connectés)
- Interface d’administration complète pour modérateurs
- API REST sécurisée avec jetons
- Design moderne avec Tailwind CSS
- Rafraîchissement automatique avec `django-browser-reload`

---

## ⚙️ Stack technique

- Backend : Django (Python)
- Frontend : Tailwind CSS (via CLI)
- API : Django REST Framework + Token Auth
- Autres : django-browser-reload, corsheaders

---

## 📦 Installation

### 1. Cloner le projet

```bash
git clone https://github.com/toncompte/cesizen.git
cd cesizen
```

### 2. Créer un environnement virtuel

```bash
python -m venv env
# Windows
env\Scripts\activate
# macOS/Linux
source env/bin/activate
```

### 3. Installer les dépendances Python

```bash
pip install -r requirements.txt
```

---

## 🎨 Configuration de Tailwind CSS

### 1. Installer les dépendances Node.js

> Assurez-vous d’avoir Node.js installé :  
> https://nodejs.org/

Dans le dossier `frontend` (ou celui où se trouve `tailwind.config.js`) :

```bash
npm install
```

### 2. Lancer Tailwind CSS en mode développement

```bash
npx tailwindcss -i ./static/src/input.css -o ./static/css/style.css --watch
```

---

## 🛠️ Config Django (extrait `settings.py`)

```python
INSTALLED_APPS = [
    ...
    'django_browser_reload',
    'rest_framework',
    'rest_framework.authtoken',
    'corsheaders',
    ...
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    ...
]

CORS_ALLOW_ALL_ORIGINS = True  # pour développement
```

---

## 🗃️ Migrer la base de données + Superuser

```bash
python manage.py migrate
python manage.py createsuperuser
```

---

## 🚀 Lancer l’application

- Serveur Django :
  ```bash
  python manage.py runserver
  ```

- Watcher Tailwind (dans un autre terminal) :
  ```bash
  npx tailwindcss -i ./static/src/input.css -o ./static/css/style.css --watch
  ```

---

## ❓ Aide rapide

| Problème                          | Solution                                          |
|----------------------------------|---------------------------------------------------|
| Pas de CSS visible               | Vérifier le watcher Tailwind (`--watch`)          |
| `npm` non reconnu                | Installer Node.js                                 |
| API REST inaccessible            | Vérifier `rest_framework` et CORS configurés      |
| `ModuleNotFoundError`            | Activer l’environnement virtuel Python            |

---

## 👨‍💻 Auteur

Projet réalisé par **Alexis Fernandes** dans le cadre du cursus **CESI** – 2025.
