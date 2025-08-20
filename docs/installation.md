# Installation Guide

Choose one of the methods below to get started.

## Source code

```bash
git clone https://github.com/Miras3210/codejam-laudatory-larkspurs.git
cd codejam-laudatory-larkspurs
python -m venv .venv

# Windows
.venv\Scripts\activate
# Linux / macOS
source .venv/bin/activate

pip install --upgrade pip
pip install .
python build.py --serve --port 8000
```

Open [http://localhost:8000](http://localhost:8000).

## Dev Install

```bash
pip install --upgrade pip
pip install --group dev
```

## Docker

```bash
docker build -t good-image-terminal:latest .
docker run --rm --name good-image-terminal -e PORT=8000 -p 8000:8000 good-image-terminal:latest
```

Then visit [http://localhost:8000](http://localhost:8000).
