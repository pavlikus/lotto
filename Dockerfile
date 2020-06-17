FROM kubler/python3

COPY lotto.py game.py ./

ENTRYPOINT ["python", "lotto.py"]
