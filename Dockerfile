FROM python:3.9.7
WORKDIR /app
COPY tp1.py /app
COPY requirement.txt /app
RUN python -m pip install -r requirement.txt
CMD python tp1.py