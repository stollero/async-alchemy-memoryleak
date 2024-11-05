# Memoryleak investigation

Reproduce memory leak with async sqlalchemy and blacksheep.

Run application with: `docker compose rm -f && docker compose up --build`

# Load Tests

Using <https://grafana.com/docs/k6/>:

    brew install k6
    k6 run loadtest.js