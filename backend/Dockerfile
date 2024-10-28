FROM python:3.9

WORKDIR /backend

COPY backend/requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY backend /backend
RUN ls
EXPOSE 5000
CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]
