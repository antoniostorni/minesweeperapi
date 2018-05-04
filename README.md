# Minesweeper

A minesweeper API game developed using Django and Django Rest Framework in 5 hours

Current endpoints

grids/
GET: Return the list of grids
Creates, updates or delete: POST, PUT, DELETE

grids/grid_id/
GET: Returns the squares for grid grid_id


grids/grid_id/squares/x/y/explore
GET: Explores square x,y from grid_id and then returns the squares for grid

Django admin site is enabled in /admin/

# Installing and running a dev server

pip install -r requirements.txt

python manage.py migrate

python manage.py runserver