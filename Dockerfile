FROM python:3.11-slim-buster
LABEL version = 1.0
LABEL description = "local image with backend"
ENV HOME_APP=/home/app
WORKDIR $HOME_APP
COPY ./requirements.txt $HOME_APP
RUN pip install --no-cache-dir -r requirements.txt && rm -f .requirements.txt


#COPY ./cogs $HOME_APP/cogs
#COPY ./models $HOME_APP/models
#COPY ./sql_queries $HOME_APP/sql_queries
#COPY ./tasks $HOME_APP/tasks
#COPY ./bot.py $HOME_APP
#COPY moduls.py /.$HOME_APP

# RUN sed -i 's/\r$//g' .$HOME_APP/bot.py && chmod +x $HOME_APP/bot.py
# CMD [ "python", "bot.py" ]
