#!/bin/sh

alembic upgrade head

python3 -m main.main