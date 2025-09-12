## RipaurionIA - API Documentation

# Overview

RipaurionIA is a web application built using FastAPI. It is designed to check if a given website is a fishing site.

# Installation and Setup

1. Clone the repository:
```bash
   git clone [repository_url]
    cd RipaurionIA
```
2. Create a virtual environment:
```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```
3. Build the Docker image:
```bash
   docker build -t ripaurionia .
```
4. Run the Docker container:
```bash
    docker run -d -p 8000:8000 ripaurionia
```
(Remove -d if you want to see logs in the terminal) 
