Fork the repo! AT the top right corner

    download the zipcode
    extract zip to intended folder  I RECOMMENT NAMING IT Video-App..
    
    open terminal on the directory(folder)
    type the following command:
        1. python -m venv virtualEnv
        2. python pip install django
        3. python pip install pillow
        
     After installing this tree pakages and you're still on project folder:
        type the following to the terminal
            1. python manage.py runserver
    


All HTML code are in the TEMPLATES folder is optional but already configured,
    another directory form html codes will require additional configuration from the backend

CSS and JAVASCRIPT code should be the STATIC folder
    if you like to seperate your static files you create folders in STATIC folder
    like e.g /css/style.css or even /js/script.js
    
Additionally
  the "{% for loop %} {% endfor %}" and co are 'jinger templating engine!"
  basically its just linked with python for rendering backend responses

BACKEND URLS
  1. homepage => {% url 'index' %} 
        returning all posts that are liked, shared, followered-author by ' login user '
