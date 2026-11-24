# 1. Image de base
FROM python:3.12-slim

# 2. Repertoire de travail dans le conteneur
WORKDIR /app

# 3. Installer les dependances (copie d'abord requirements pour profiter du cache)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 4. Copier le code de l'application
COPY . .

# 5. Port de l'application
EXPOSE 5000

# 6. Commande de demarrage
CMD ["python", "run.py"]