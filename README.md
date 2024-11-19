##  data.labs

Simple site with information with NURE university links (Google Meet, Zoom, etc.) for lessons.

### Installation
To install dependencies run:
    
    pip install -r requirements.txt

After that, you need to create a `.env` file with the `DJANGO_SECRET_KEY`, `MONGO_CLUSTER_SECRET` variables.
Optionally, you can set the `DEBUG` variable to `true` to enable debug mode:

    DJANGO_SECRET_KEY="SECRET_KEY"
    MONGO_CLUSTER_SECRET="mongodb+srv://username:password@localhost/test?retryWrites=true&w=majority"
    DEBUG=true

### Usage
To run the server, run:

    python manage.py runserver

After that, you can access the site at `http://localhost:8000/`
Please notice, that it's not recommended to run the server using the `runserver` command in production environment.
Instead, read the deployment guideline [here](https://docs.djangoproject.com/en/5.1/howto/deployment/).