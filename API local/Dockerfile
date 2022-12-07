# 
FROM python:3.10.8

# 
WORKDIR /code

# 
COPY ./requirements.txt /code/requirements.txt

# 
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# 
COPY ./sismos /code/app

# 
CMD ["uvicorn", "sismos.main:app", "--host", "0.0.0.0", "--port", "80"]