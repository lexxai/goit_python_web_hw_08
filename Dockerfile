# Docker-команда FROM вказує базовий образ контейнера
# Наш базовий образ - це Linux з попередньо встановленим python-3.11
# FROM python:3.11
FROM python:3.11

# Встановимо змінну середовища

ENV APP_HOME /app 

# Встановимо робочу директорію всередині контейнера
WORKDIR $APP_HOME

# Скопіюємо інші файли в робочу директорію контейнера
COPY . .
COPY .config/config_docker.ini .config/config.ini
COPY run.sh run.sh 
COPY migrations/ migrations/
COPY src/ src/
COPY requirements.txt requirements.txt

# Встановимо залежності всередині контейнера
# RUN pip install -r requirements.txt 
# RUN pip wheel --no-cache-dir --no-deps --wheel-dir /app/wheels -r requirements.txt
RUN pip install -r requirements.txt 

CMD ./run.sh 

# CMD bash

#CMD ["python", "-u", "src/main.py"]

# Запустимо наш застосунок всередині контейнера
# ENTRYPOINT [ "python", "src/main.py" ]

