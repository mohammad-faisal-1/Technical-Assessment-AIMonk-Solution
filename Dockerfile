FROM python:3.8
WORKDIR C:\Users\Shahid\Desktop\Technical Assessment (AIMonk)\ui_backend\app
COPY . .
RUN pip install fastapi requests
EXPOSE 5000
CMD ["python", "app.py"]
