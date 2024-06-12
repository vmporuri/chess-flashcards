# Chess Flashcards

Flask web app that automatically generates chess flashcards from mistakes in your Lichess games.

## Commands

```bash
# App setup
flask create-db
python -c 'import uuid; print(f"LICHESS_CLIENT_ID=\"{uuid.uuid4()}\"")' >> .env
python -c 'import secrets; print(f"SECRET_KEY=\"{secrets.token_hex()}\"")' >> .env

# Cron tasks
flask session_cleanup
flask refresh-puzzles
```
