FROM python:3.8
RUN mkdir -p /home/src/app
ADD requirements.txt /home/src/app
RUN pip install -r /home/src/app/requirements.txt
ADD main.py /home/src/app
ADD run.sh /home/src/app
ADD /app /home/src/app/app
RUN chmod +x /home/src/app/run.sh
ENV FLASK_APP /home/src/app/app/__init__.py
CMD /home/src/app/run.sh
