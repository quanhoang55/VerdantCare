# Init project

```zsh
mkdir -p backend frontend docs
touch README.md
cd backend
uv init .
uv venv
uv add "fastapi[standard]" pydantic-settings httpx uvicorn
mkdir -p app/{api,core,models,schemas,services}
mkdir -p app/api/endpoint/v1
touch main.py
touch app/api/endpoint/__init__.py app/__init__.py app/main.py app/core/config.py .env .env.example
cd ..

cd frontend
bun create vite . --template react-ts
bun install

<!-- bun add -d tailwindcss @tailwindcss/vite -->
cd ..

```
