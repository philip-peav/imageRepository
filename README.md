# Image Repo 
This is a web application developed in Python using the Flask web framework. The application communicates with a MySQL Database using the `flask-sqlalchemy` library to handle user authentication as well as basic create, read, and delete operations for posts.

## Project Setup
In order to get started with the project, the repo will need to be cloned to your local system. 

After this is complete, we will need to install all of the dependencies specified within the '**_requirements.txt_**' file. This can be done by opening up the command line in the project directory and running the following (assuming Python is already installed with the PIP package manager):
### `pip install -r .\requirements.txt`

While still in the project directory in the command line, the development server must be launched by running the '**_run.py_**' file:
### `python .\run.py`

After this is complete, the user can access the image repo in a web browser by opening [http://localhost:5000](http://localhost:5000).

The image repo is ready to be used!

## Using the Image Repo
To begin using the site, the user can head to the top right of the page to create an account after which they can proceed to login. 

After logging in, the user can use the navigation bar to visit the home page (posts from all users will be visible here), create a post (post an image), view their account details (username, email, all posts), and logout.

Posts can only be deleted by the user who has posted the image. In order to delete a post, the user must click on the post which will take them to another page. Here, the user will be allowed to delete the post, removing it from the database and the home page.

## Design Decisions
There were several design decisions that were made throughout the development of this project.

One such decision was to use a local file system to store images instead of storing the images in the database. Instead, the database would contain the path to the images in the filesystem, greatly reducing the load on the database. This is especially important when considering scalability, as the increase in traffic for the site would mean an exponential increase on the memory usage for the database had the images been stored in the database.

Another design decision was to package the project rather than to run it as a single large file. There were many advantages to this decision, such as simplifying the program by modularizing different segments of the code based on their role (such as authentication, form data collection, etc.), minimizing interdependency between modules and circular import issues, and allowing code to be reused when needed with ease.

### That is all for this project, thank you! :)
