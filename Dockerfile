FROM public.ecr.aws/lambda/python:3.9
COPY ./app ./app
COPY ./requirements.txt ./requirements.txt
RUN pip install -r ./requirements.txt
CMD ["app.main.handler"]