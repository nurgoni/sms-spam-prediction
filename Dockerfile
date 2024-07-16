# use python 3.12 as the base image
FROM python:3.10

# set the working directory in the container
WORKDIR /app

# copy requirements.txt file into container
COPY requirements/main.txt ./

# install necessary dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    libssl-dev \
    libffi-dev \
    python3-dev \
    python3-pip \
    python3-nltk

# install python dependencies
RUN pip install --no-cache-dir -r main.txt 

# install nltk data
RUN python -c "import nltk; nltk.download('wordnet'); nltk.download('stopwords')"

# copy the rest of application code into container
COPY . .

# expose the port number that FastAPI will use (default is 8000)
EXPOSE 8000

# Define environment variable
ENV NAME World

# command to run the FastAPI application with uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]