# Utiliser une image Python officielle
FROM python:3.10-slim

# Définir les variables d'environnement
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV FLASK_APP=app.py
ENV FLASK_ENV=production

# Créer un utilisateur non-root
RUN adduser --disabled-password --gecos '' appuser


# Installer les dépendances système
RUN apt-get update && apt-get install -y \
    postgresql-client \
    gcc \
    python3-dev \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copier les fichiers de requirements depuis le dossier de l'app
COPY flask/requirements.txt .

# Installer les dépendances Python
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir --retries 10 -r requirements.txt

# Copier tout le code de l'application
COPY flask/ .


# Passer à l'utilisateur non-root
USER appuser

# Exposer le port Flask
EXPOSE 5000

# Script de démarrage avec gestion de la base de données
CMD ["python", "app.py"]

