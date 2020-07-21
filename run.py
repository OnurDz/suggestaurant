from suggestaurant import app
from suggestaurant.models import User
if __name__ == '__main__':
    print(User.query.all())
    app.run(debug=True)