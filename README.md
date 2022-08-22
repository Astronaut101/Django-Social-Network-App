# Social Network with Django

A four-part tutorial series from [Real Python](https://realpython.com/django-social-network-1/) in which we will build a social network with Django. This will help us in strengthening our understanding of relationships between Django models and show how we can use forms so that our users can interact with our app and with each other. We will be using the Bulma CSS Framework in order to make our side look good!

## Full Project Implementation Steps

We will implement the project in a series of steps spread out over four parts.

🎈 **[Part 1: Models and Relationships](#part-1-models-and-relationships)**

* Step 1: Set Up the Base Project
* Step 2: Extend the Django User Model
* Step 3: Implement a Post-Save Hook

✨ **[Part 2: Templates and Front-End Styling](#part-2--building-a-django-front-end-with-bulma)**

* Step 4: Create a Base Template with Bulma
* Step 5: List All user profiles
* Step 6: Access Individual Profile Pages

🎉TBC **[Part 3: Follows and Dweets](#part-3---build-and-handle-post-requests-in-django)**

* Step 7: Follow and Unfollow Other Profiles
* Step 8: Create the Back-End Logic For Dweets
* Step 9: Display Dweets on the Front End

🎁 **Part 4: Forms and Submissions**

* Step 10: Submit Dweets Through a Django Form
* Step 11: Prevent Double Submissions and Handle Errors
* Step 12: Improve the Front-End User Experience

## Part 1: Models and Relationships

### Objectives

* [x] - Implement **one-to-one** and **many-to-many** relationships between Django **models**
* [x] - Extend the **Django user model** with a custom `Profile` model
* [x] - Customize the **Django admin interface**.

### Project Planning

What do we need for a social network? In its most basic form, we need two things:

1. **User-to-user connections** that allow people to connect with one another.
2. **Content creation and display functionality** so that our users can create output for their connected users to view.

### Profiles for User-to-User connections

How we can implement connections in Django models? First, we'll jot down what a basic version of these connections could look like.

1. You'll have multiple users in our social network
2. They need to know about each other so that they can decide whom they want to follow

Here a couple of assumptions that expand on the two cornerstones mentioned above:

* Our users will be able to either follow or not follow another user.
* If they follow someone, they'll see that user's content. If they don't, they won't.
* Our users can follow a person without being followed back. Relationships in our social network can be **asymmetrical**, meaning that a user can follow someone and see their content without the reverse being true.
* Our users need to be aware of **who exists** so that they know whom they can follow.
* Users should also be aware of **who follows them**
* In our app's most basic form, users won't have many extra features available to them. We won't implement a way to block people, and there won't be a way to directly respond to content that someone else posted.

Essentially, our social network app is a repository of short-form blogs or RSS feeds that users can either subscribe to or not.

### Text-Based Content

In addition to establishing relationships between  users, our platform also needs a way for users to create and share content. The content could be anything. It could include images, text, videos, webcomics, and more.

In our project, we're building a social network that handles limited-character text-based messages, similar to Twitter. Because you'll make it using the Django web Framework, it'll carry the fashionable name **Dwitter**.

In our Dwitter network, we will need a model for storing the text-based messages that users can create, which we'll refer to as **dweets**. We'll record only three pieces of information about each dweet:

1. **Who** wrote it.
2. **What** the message says.
3. **When** the user wrote it.

For our Dweet, it connects to our Dweet table through a one-to-many relationship. This type of relationship means that one user can have many dweets and each dweet belongs to exactly one user.

We can also see the different fields in the table that correspond to the information that we want to collect about each dweet:

1. **user**: holds information about who wrote the message.
2. **body**: holds the text content of the message.
3. **created_at**: holds the date and time when the user posted the message

The `created_at` field is grayed out in the ER diagram because we won't allow our users to edit this themselves! Django will automatically fill the field whenever a user submits a new message.

**NOTE**: Our goal is to create a basic social network implementation that fulfills the criteria we previously brainstormed. We can always make it more complex later on.

We will also need a way for our users to create content and view the content that they and others in their network have created. For the convenience of our users, we'll have to do some of the following tasks to set up the front end:

* Provide a form for submitting content
* Create views to handle these submissions
* Build templates to display existing content
* Make it look decent

### Setting up the Base Project

#### Creating a Virtual Environment and Installing Django

```[python]
C:\Users\creyes24\Real-World-Python\django-projects\django_social_network>py -m venv .venv --prompt="social"

C:\Users\creyes24\Real-World-Python\django-projects\django_social_network>".venv\Scripts\activate"

(social) C:\Users\creyes24\Real-World-Python\django-projects\django_social_network>pip install django==3.2.5
```

#### Creating a Django Project and App

```[python]
(social) C:\Users\creyes24\Real-World-Python\django-projects\django_social_network>django-admin startproject social .

(social) C:\Users\creyes24\Real-World-Python\django-projects\django_social_network>py manage.py startapp dwitter
```

#### Customizing the Dhango Admin Interface

Django built-in admin interface tool is a powerful tool for managing our application, and we'll use it to handle user creation and management in this Dwitter project.

**NOTE**: We won't implement any user-facing registration functionality in this project. However, we can add this functionality later by following the Real Python Tutorial on **[Django user management](https://realpython.com/django-user-management/)**

We will be setting Django's default SQLite database and create a superuser so we can log in to the Django Admin Portal:

```[python]
(social) C:\Users\creyes24\Real-World-Python\django-projects\django_social_network>py manage.py migrate
Operations to perform:
  Apply all migrations: admin, auth, contenttypes, sessions
Running migrations:
  Applying contenttypes.0001_initial... OK
  Applying auth.0001_initial... OK
  Applying admin.0001_initial... OK
  Applying admin.0002_logentry_remove_auto_add... OK
  Applying admin.0003_logentry_add_action_flag_choices... OK
  Applying contenttypes.0002_remove_content_type_name... OK
  Applying auth.0002_alter_permission_name_max_length... OK
  Applying auth.0003_alter_user_email_max_length... OK
  Applying auth.0004_alter_user_username_opts... OK
  Applying auth.0005_alter_user_last_login_null... OK
  Applying auth.0006_require_contenttypes_0002... OK
  Applying auth.0007_alter_validators_add_error_messages... OK
  Applying auth.0008_alter_user_username_max_length... OK
  Applying auth.0009_alter_user_last_name_max_length... OK
  Applying auth.0010_alter_group_name_max_length... OK
  Applying auth.0011_update_proxy_permissions... OK
  Applying auth.0012_alter_user_first_name_max_length... OK
  Applying sessions.0001_initial... OK

(social) C:\Users\creyes24\Real-World-Python\django-projects\django_social_network>py manage.py createsuperuser
Username (leave blank to use 'creyes24'): admin
Email address: cvinzreyes@gmail.com
Password:
Password (again):
Superuser created successfully.
```

We can now run our Django development server:

```[python]
(social) C:\Users\creyes24\Real-World-Python\django-projects\django_social_network>py manage.py runserver
Watching for file changes with StatReloader
Performing system checks...

System check identified no issues (0 silenced).
August 17, 2022 - 00:13:39
Django version 3.2.5, using settings 'social.settings'
Starting development server at http://127.0.0.1:8000/
Quit the server with CTRL-BREAK.
```

In order to simplify our admin, there a few things we can cut down on:

1. We won't use Django's Groups, so we can remove it from our admin view altogether.
2. The most basic way to create a user in Django is by passing just a username. We can remove all the other fields from the Users model display as well.

We will be unregistering our `Group` model, which removes the model from our admin interface:

```[python]
# ./dwitter/admin.py
from django.contrib import admin
from django.contrib.auth.models import Group

# Register your models here.
admin.site.unregister(Group)
```

Next, we will change the fields displayed in the admin section of Django's built-in `User` model. To do this, we need to first unregister it since the model comes registered by default. Then, we can re-register the default `User` model to limit which fields the Django admin should display.

```[python]
# ./dwitter/admin.py
from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.models import User


# Register your models here.
class UserAdmin(admin.ModelAdmin):
    model = User
    # Only display the "username"  field
    fields = ["username"]


admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.unregister(Group)
```

#### Create Users for Our App

**NOTE**: Only use these user accounts for development purposes. Setting a user account without defining any password or any additional information is not secure.

### Extending the Django User Model

We need a way to hold information about the users of our app. If we started from the very beginning, we'd have to build an entirely new user model for that. Instead, we're going to use the built-in Django `User` model to rely on Django's well-tested implementation so that we can avoid reinventing the authentication wheel.

However, we'll also need additional functionality that the default `User` model doesn't cover: **How can one user follow another user?** We'll need a way to connect users to other users.

A great way to keep capitalizing on Django's built-in capacities for user management, while adding our specific customizations, is to [extend the User model](https://docs.djangoproject.com/en/3.2/topics/auth/customizing/#extending-the-existing-user-model)

**NOTE**: We'll see the term **extend** used when talking about inheritance. In the Django community, **extending the User model** refers to other ways of customizing the built-in `User` model that don't involve inheritance.

#### Create Profile Model

We'll extend Django's built-in `User` model by using a one-to-one relationship with a small and focused new model, `Profile`. We'll build this `Profile` from scratch. The `Profile` model will keep track of the additional information that we want to collect about each user.

**What do you need in addition to the user information that the Django `User` model already includes?**

1. **Whom they follow**
2. **Who follows them**
3. **Which dweets they wrote**

**POSSIBLE FEATURE ADD**: Adding more details to the `Profile` model

The `Profile` model only contains information that our users create `after` they already have a user account, which allows you to let Django handle the sign-up and authentication process. This is one of the suggested ways for [extending the existing `User` model](https://docs.djangoproject.com/en/3.2/topics/auth/customizing/#extending-the-existing-user-model)

Our `Profile` model should record the user's connections to other user profiles. The ER diagram states that the `Profile` model connects to itself through the `follows` many-to-many relationship.

Once we have our `Profile` set up, we need to rerun Django's database commands to propagate the model updates to our database:

```[python]
(social) $ python manage.py makemigrations
(social) $ python manage.py migrate
```

Running `makemigrations` creates a migration file that registers the changes to our database, and `migrate` applies the changes to the database.

We now have all of the functionality that we need to create profiles and follow other profiles. However, having `User` and `Profile` displayed in two separate places when they're so tightly connected and minimally informative might seem inconvenient.

#### Display Profile Information Within the USer Admin Page

We will customize our User Admin Page by adding an [admin inline](https://docs.djangoproject.com/en/3.0/ref/contrib/admin/#inlinemodeladmin-objects), which allows us to edit both in one area.

```[pytho]
from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.models import User

from .models import Profile

# Register your models here.
class ProfileInline(admin.StackedInline):
    model = Profile

class UserAdmin(admin.ModelAdmin):
    model = User
    # Only display the "username"  field
    fields = ["username"]
    inlines = [ProfileInline]


admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.unregister(Group)
# Removing the register Profile site
# admin.site.register(Profile)
```

**NOTE**: `inlines` is a list that can take multiple entries, but in this case, we only want to add one.

However, after combining our User and Profile model in an Inline fashion, our profile names are currently hard to interpret. How should we know that _Profile object (1)_ is the user profile of _admin?_.

In order to solve that dilemma, we would update our `./dwitter/models.py` and add a `.__str__()` method to `Profile`:

```[python]
from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    follows = models.ManyToManyField(
        "self",
        related_name="followed_by",
        symmetrical=False,
        blank=True
    )
    
    def __str__(self):
        return self.user.username
```

We have overloaded the default `.__str__()` method so that it returns the value of username from the associated instance of the user model.

We want to also have one user be associated with the profile with them, we can setup in Django to do this task for us. Every time we create a new user, Django should create the fitting user profile automatically as well.

### Implement a Post-Save Hook

#### Coordinate Users and Profiles with a Signal

We can associate a new profile with a user automatically when the user creates it by using the [Django Signals](https://docs.djangoproject.com/en/3.2/topics/signals/)

**NOTE**: The Django docs mentions that the best place to put our signals is in a `signals.py` submodule of our app. However, this requires us to make additional changes in our app configuration. Since we only need to build out a single signal for this tutorial, we're keeping it in `models.py`

We can implement this functionality wit the help of `post_save`, which will call the `create_profile` function object every time our code executes the user model's `.save()`. Note that `create_profile()` is a top-level function that we define outside of `Profile`:

```[python]
# ./dwitter/models.py
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save


# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    follows = models.ManyToManyField(
        "self",
        related_name="followed_by",
        symmetrical=False,
        blank=True
    )
    
    def __str__(self):
        return self.user.username
    
    
def create_profile(sender, instance, created, **kwargs):
    if created:
        user_profile = Profile(user=instance)
        user_profile.save()
        

# Create a profile for each new user.
post_save.connect(create_profile, sender=User)
```

Based from the code snippet above:

* We have added `post_save` from the `django.db.models.signals import post_save`
* We have written a new function called `create_profile` that used `created`, which `post_save` provides, to decide whether to create a new `Profile` instance. Our code will only continue if the post-save signal indicates that Django created the user object successfully.

The implementation of a post-save signal creates a new profile for each new user. We automatically associate one with the other by passing the newly created user to the `Profile` constructor.

**NOTE**: When a post-save is triggered, it returns multiple variables, so we're catching the variables that we don't need right now with `**kwargs` in the function definition of `create_profile()`.

We could end it here with a sparkling clean and empty profile for each new user. However, we'll automatically ad the user's own profile to the list of profiles they follow, so each user will also see the dweets they wrote themselves.

#### Add Functionality Through Error-Driven Development

```[python]
ValueError at /admin/auth/user/add/

"<Profile: Test_user_05>" needs to have a value for field "id" before this many-to-many relationship can be used.
```

In this error message above,  Django tells us that a `User` instance first needs to exist in our database so that we can use `.set()` to add an instance to `follows`. That's an actionable tip!

```[python]
TypeError at /admin/auth/user/add/

'User' object is not iterable
```

Let's explore on Django's docs on many-to-many relationships:

Relation sets can be set to:

```[python]
# ./dwitter/models.py
...
def create_profile(sender, instance, created, **kwargs):
    if created:
        # We want to follow our own profile to see our own musings and rediculousness
        # user_profile = Profile(user=instance, follows=[instance])
        
        user_profile = Profile(user=instance)
        user_profile.save()
        user_profile.follows.set([instance])
        user_profile.save()
```

It seems like `.set()` really requires an iterable input, which Django tried to tell us in the error message.

```[python]
TypeError at /admin/auth/user/add/

Field 'id' expected a number but got <User: ColdRamen>.
```

Based from the error message above, Django is telling us that it got a `User` object but expected an `id` field instead. We have set up profiles to follow other profiles, yet Django is only looking for the `Profile` object's `.id`.

After extending our `User` model, we can access a user's profile through a user instance with `.profile` and then step deeper into the object to get `.id`:

```[python]
# dwitter/models.py
...
def create_profile(sender, instance, created, **kwargs):
    if created:
        # We want to follow our own profile to see our own musings and rediculousness
        # user_profile = Profile(user=instance, follows=[instance])
        
        user_profile = Profile(user=instance)
        user_profile.save()
        user_profile.follows.set([instance.profile.id])
        user_profile.save()
```

**[Django's Many-to-Many Relationship docs](https://docs.djangoproject.com/en/dev/topics/db/examples/many_to_many/)**

We can implement the alternative solution, which is using `.add()`, instead of using the `.set()` method:

```[python]
def create_profile(sender, instance, created, **kwargs):
    if created:
        # We want to follow our own profile to see our own musings and rediculousness
        # user_profile = Profile(user=instance, follows=[instance])
        
        user_profile = Profile(user=instance)
        user_profile.save()
        
        # Implementation 01: Using .set() for adding single objects to many-to-many relationships
        # user_profile.follows.set([instance.profile.id])
        
        # Implementation 02: Using .add() for adding single objects to many-to-many relationships
        user_profile.follows.add(instance.profile)
        user_profile.save()
```

According to the Django docs, we don't need to pass a `.id()`, but we can pass the whole object instead. This means that it'll be more  efficient to use `.add()` instead of `.set()`. Also, since it has the same effect and is more descriptive, we can pass `instance.profile` directly instead of using `.id`.

### Refactoring our Code using a Decorator

It's better to register signals by using a decorator, in which Django comes with a `receiver` decorator.

```[python]
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    follows = models.ManyToManyField(
        "self",
        related_name="followed_by",
        symmetrical=False,
        blank=True
    )
    
    def __str__(self):
        return self.user.username
 
    
# Create a profile for each new user.
@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        # We want to follow our own profile to see our own musings and rediculousness
        # user_profile = Profile(user=instance, follows=[instance])
        
        user_profile = Profile(user=instance)
        user_profile.save()
        
        # Implementation 01: Using .set() for adding single objects to many-to-many relationships
        # user_profile.follows.set([instance.profile.id])
        
        # Implementation 02: Using .add() for adding single objects to many-to-many relationships
        user_profile.follows.add(instance.profile)
        user_profile.save()
        
# Previous method without using the decorator @receiver
# post_save.connect(create_profile, sender=User)
```

To summarize, we have implemented the mode relationships between our users and our Django social network profiles! Every time we create a new user, they'll also receive a user profile and immediately follow their own profile.

**NOTE**: We can set up the front-end authentication through Django's built-in user management system later on, and we won't need to make any changes in the back end for the functionality to keep working as expected.

### Conclusion to Part 1

* Implemented **one-to-one** and **many-to-many** relationships between Django **models**
* Extend the Django **user model** with a custom `Profile` model
* Customize the `Django admin` interface

## Part 2 : Building a Django Front End with Bulma

### Objectives Part 2

* Integrate **Bulma CSS** and **style** our app
* Use **template inheritace** to reduce repetition
* Structure Django templates in a **folder hierarchy**
* Build **routing and view functions**
* **Interlink** pages of our app using **dynamic URLs**

### Project Overview Part 2

* [x] - Step 4 : Creating a Base Template with Bulma
* [ ] - Step 5 : List All user Profiles
* [ ] - Step 6 : Access Individual Profile Pages

### Create a Base Template with Bulma

**NOTE**: Having a fundamental understanding of how we can make our website projects look decent without too much effort goes a long way.

#### Create a Base Template

```[html]
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF=8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="with=device-width, initial-scale=1.0">
    <title>Dwitter</title>
</head>
<body>
    <section>
        <h1>Dwitter</h1>
        <p>Your tiny social network built with Django</p>
    </section>
    <div>
        {% block content %}

        {% endblock content %}
    </div>
</body>
</html>
```

#### View Your Base Template

To make Django render and display our base template, we'll need to set up URL routing and a view function. We now open our primary `urls.py` file in the management app that we called `social`, then route requests that point to the base URL forward to our `dwitter` app:

```[python]
from django.contrib import admin
from django.urls import path
from django.urls import include


urlpatterns = [
    path("", include("dwitter.urls")),
    path('admin/', admin.site.urls),
]
```

Later, we'll change the code in the respective file above to distribute incoming requests further.

**NOTE**: By default, Django apps don't come with their own `urls.py` files. However, it's best to create a URL configuration for each app in our Django project and [include them in our main URLconf](https://docs.djangoproject.com/en/3.2/topics/http/urls/#including-other-urlconfs). For each new app, we'll need to create a new `urls.py` file.

After we have created our `dwitter/urls.py`, we can now add the necessary functional code. This time, without needing to handle the `/admin` route. Catch the incoming request to the base URL that gets redirected to this file and send it to a new function called `dashboard`

```[python]
# dwitter/urls.py

from django.urls import path
from .views import dashboard

app_name = "dwitter"

urlpatterns = [
    path("", dashboard, name="dashboard"),
]
```

We will be running through a helpful error message that tells all about what we are missing:

```[python]
ImportError: cannot import name 'dashboard' from 'dwitter.views' (C:\Users\creyes24\Real-World-Python\django-projects\django_social_network\dwitter\views.py)
```

Next stop would be to create the `dashboard()` function in `views.py` in order for the main project folder to be linking to your app url.

```[python]
# ./dwitter/views.py

from django.shortcuts import render

# Create your views here.
def dashboard(request):
    return render(request, "base.html")
```

With the `dashboard()`, we're pointing the incoming request to `base.html` and telling Django to render that template.

```[python]
(social) C:\Users\creyes24\Real-World-Python\django-projects\django_social_network>py manage.py runserver
Watching for file changes with StatReloader
Performing system checks...

System check identified no issues (0 silenced).
August 18, 2022 - 21:53:17
Django version 3.2.5, using settings 'social.settings'
Starting development server at http://127.0.0.1:8000/
Quit the server with CTRL-BREAK.
```

#### Adding a Bulma CSS to our Base Template

We will use the CSS framework [Bulma](https://bulma.io/) to handle the CSS rules for us. We will make the Bulma CSS stylesheet available to all of our templates. A quick way to do it is by adding a link to the stylesheet file, which is hosted on a [content delivery network (CDN)](https://en.wikipedia.org/wiki/Content_delivery_network), to our base template's `<head>` element:

```[html]
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF=8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="with=device-width, initial-scale=1.0">
    <!-- Adding our Bulma CSS Framework -->
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bulma@0.9.4/css/bulma.min.css">
    <title>Dwitter</title>
</head>
<body>
    <section>
        <h1>Dwitter</h1>
        <p>Your tiny social network built with Django</p>
    </section>
    <div>
        {% block content %}

        {% endblock content %}
    </div>
</body>
</html>
```

We are now going to continue to improve the look of our page by employing pre-made classes defined in our stylesheet.

```[html]
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF=8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="with=device-width, initial-scale=1.0">
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bulma@0.9.4/css/bulma.min.css">
    <title>Dwitter</title>
</head>
<body>
    <section class="hero is-small is-primary mb-4">
        <div class="hero-body">
            <h1 class="title is-1">Dwitter</h1>
            <p class="subtitle is-4">Your tiny social network built with Django</p>
        </div>
    </section>

    <div class="container">
        <div class="columns">
            {% block content %}

            {% endblock content %}
        </div>
    </div>
</body>
</html>
```

### Step 5: Listing all User Profiles on the Front End of Our Django App

At this point, we can inherit from our base template, which links our style scaffolding through Bulma. We will follow the flow of a request through the Django Web framework and write the code that we'll need piece by piece.

#### Write the routes and code logic

| Topic          | File Location              |
|----------------|----------------------------|
| Routing        | urls.py                    |
| Logic          | views.py                   |
| Representation | html files in `templates/` |

We will next pick-up requests that go through `/profile_list` in `dwitter/urls.py` and take it from there:

```[python]
from django.urls import path

from .views import dashboard
from .views import profile_list

app_name = "dwitter"

urlpatterns = [
    path("", dashboard, name="dashboard"),
    path("profile_list/", profile_list, name="profile_list")
]

```

From our code snippet above, we're telling Djnago that we want to route requests that come to `/profile_list` to view the function called `profile_list()`.

**NOTE**: The names of our **URL slug and the view function don't need to match**, but it **makes sense to name them the same to keep our code clearer and more straightforward to debug**.

Next, we will add the `profile_list()` function to our `dwitter/views.py` file:

```[python]
# ./dwitter/views.py

from django.shortcuts import render

from .models import Profile


# Create your views here.
def dashboard(request):
    return render(request, "base.html")

def profile_list(request):
    profiles = Profile.objects.exclude(user=request.user)
    return render(request, "dwitter/profile_list.html", {"profiles": profiles})
```

From the code snippet above, we're defining the view function that'll handle all requests to the `/profile_list` URL slug:

* We have used Django's Object-Relational Mapper (ORM) to [retrieve objects](https://docs.djangoproject.com/en/3.2/topics/db/queries/#retrieving-objects) from our profile table and store them in `profiles`. We want to get all user profiles except for our own, which we can accomplish with [`.exclude()`](https://docs.djangoproject.com/en/3.2/ref/models/querysets/#exclude)

* When we return a call to `render()`, we pass a string for the template we want to render a context dictionary that contains `profiles`.

In short, we have fetched all user profiles except for our own from our database and send that information onwards to a template with the path `dwitter/profile_list.html`

#### Write the Profile List Template

**NOTE**: The reason why we're creating this second `dwitter/` folder is to avoid complications with templates from other apps we might  add to our project in the future. Learn more about [Django's Double-Folder Structure](https://www.youtube.com/watch?v=bydSXmg5GR8). **Don't forget to naviate through the `/profile_list` domain of your web app to check if profile_list.html is working.

```[html]
<!-- dwitter/templates/dwitter/profile_list.html -->

{% for profile in profiles %}

<div>
    <p>{{ profile.user.username }}</p>
    <p>@{{ profile.user.username|lower }}</p>
</div>

{% endfor %}
```

Now it's time to add more Bulma-specific HTML structure and classes to improve the look and feel of our profile pages.

```[html]
<!-- dwitter/templates/dwitter/profile_list.html -->

{% extends 'base.html' %}

{% block content %}

<div class="column">

{% for profile in profiles %}

    <div class="block">
        <div class="card">
            <a href="#">
                <div class="card-content">
                    <div class="media">
                        <div class="media-left">
                            <figure class="image is-48x48">
                                <img src="https://bulma.io/images/placeholders/96x96.png"
                                     alt="Placeholder image">
                            </figure>
                        </div>
                        <div class="media-content">
                            <p class="title is-4">
                                {{ profile.user.username }}
                            </p>
                            <p class="subtitle is-6">
                                @{{ profile.user.username|lower }}
                            </p>
                        </div>
                    </div>
                </div>
            </a>
        </div>
    </div>

{% endfor %}

</div>

{% endblock content %}
```

To make the updates happen accordingly, we start by extending `base.html` and wrapping our site-specific HTML into the `{% block content %}` tag. This structure allows Django to insert the child template's content into our base template's HTML structure.

We've also implemented the HTML structure for a [Bulma Card](https://bulma.io/documentation/components/card/#) to improve how the profile information for each user appears on our page.

**NOTE** - when navigating to the `<your_local_host>/profile_list`, make sure that you are logged-in with your admin account or in a Production server, logged in as a valid user.

### Step 6: Access Individual Profile Pages

#### Building a Profile Page Template

```[python]
# dwitter/urls.py

from django.urls import path

from .views import dashboard
from .views import profile_list
from .views import profile

app_name = "dwitter"

urlpatterns = [
    path("", dashboard, name="dashboard"),
    path("profile_list/", profile_list, name="profile_list"),
    path("profile/<int:pk>", profile, name="profile"),
]
```

With `<int:pk>`, we're indicating that any URL request that goes to `profile/` followed by an integer number should be funneled to the `profile()` view function in `dwitter/views.py`

The `profile()` function takes both Django's `request` object as well as an integer, `pk`. We use `pk` in a call to our database, which allows us to pick a specific profile by its primary key ID. Finally, we return another call to `render()`. Finally, we return another call to `render()` and instruct Django to send the gathered profile object to a template named `dwitter/profile.html`

**NOTE**: In our tutorial series, we're keeping the names and locations of our template files consistent with the structure that's used in the tutorial on [Django User Management](https://realpython.com/django-user-management/). This would help us have a helpful resource to help us implement a proper front-end facing authentication flow for the Django project.

Since we have also implemented the `follows` field in our back-end code logic, which means that we can now display all the profiles that a user is following:

```[html]
<!-- dwitter/templates/dwitter/profile.html -->

<ul>
{% for following in profile.follows.all %}
    <li>{{ following }}</li>
{% endfor %}
</ul>
```

The following code snippet above describes the following:

* **profile** - the variable that we're passing in our context dictionary to `render()` in `profile()`. It holds the information that we pulled from our database about a user profile.

* **.follows** - gives us access to the `ManyRelatedManager` object, which holds all the user profiles that the current profile follows.

* **.all** - fetches all those user profile instances and allows us to iterate over them.

#### Exercise - Add Follower List

Try to display the list of all the profiles that follow the user whose profile page you're on.

**Answer:**

```[html]
<!-- dwitter/templates/dwitter/profile.html -->

<ul>
{% for following in profile.follows.all %}
    <li>{{ following }}</li>
{% endfor %}
</ul>

<ul>
{% for followers in profile.followed_by.all %}
    <li>{{ followers }}</li>
{% endfor %}
</ul>
```

The `related_name` value that we have passed in our `Profile` model of `models.ManyToManyField()`, we're setting the name that we can use to refer to **connected objects in the reverse direction**.

**NOTE**: Keep in mind that we set the user-to-user relationships as asymmetrical, which means that a user can follow someone else's profile without them following that user.

It's highly encouraged that you write your own version of how you want your profile pages to look. But for now, we will follow the Real Python author's html design that uses Bulma's [columns](https://bulma.io/documentation/columns/), [blocks](https://bulma.io/documentation/elements/block/), and [titles](https://bulma.io/documentation/elements/title/):

```[html]
<!-- dwitter/templates/dwitter/profile.html -->

{% extends 'base.html' %}

{% block content %}

<div class="column">

    <div class="block">
        <h1 class="title is-1">
            {{profile.user.username|upper}}'s Dweets
        </h1>
    </div>

</div>

<div class="column is-one-third">

    <div class="block">
        <a href="#">
            <button class="button is-dark is-outlined is-fullwidth">
                All Profiles
            </button>
        </a>
    </div>

    <div class="block">
        <h3 class="title is-4">
            {{profile.user.username}} follows:
        </h3>
        <div class="content">
            <ul>
            {% for following in profile.follows.all %}
                <li>
                    <a href="#">
                        {{ following }}
                    </a>
                </li>
            {% endfor %}
            </ul>
        </div>
    </div>

    <div class="block">
        <h3 class="title is-4">
            {{profile.user.username}} follows:
        </h3>
        <div class="content">
            <ul>
            {% for followers in profile.followed_by.all %}
                <li>
                    <a href="#">
                        {{ followers }}
                    </a>
                </li>
            {% endfor %}
            </ul>
        </div>
    </div>

</div>

{% endblock content %}
```

If we go to `http://127.0.0.1:8000/profile/1`, for example, then we can access a profile page on our localhost. The downside for the IDs is that we need to keep on guessing the ID of a user profile if we want to see the actual user's profile page. That's why we need to link the profile pages from our profile list page.

### Link the Profile Pages

We will now add a link to the profile pages for each profile displayed in `profile_list.html`

**NOTE**: If we want to learn more about dynamic linking in Django and the URL template tag, you can watch the lesson about URL Linking using `app_name`, `path names`, and `arguments`

We will replace all the '#' symbols from our `<a>` tags with `{% url %}` tag that links to individual profile page:

```[html]
<!-- dwitter/templates/dwitter/profile_list.html -->

{% extends 'base.html' %}

{% block content %}

<div class="column">

{% for profile in profiles %}

    <div class="block">
        <div class="card">
            <a href="{% url 'dwitter:profile' profile.id %}">
                <div class="card-content">
                    <div class="media">
                        <div class="media-left">
                            <figure class="image is-48x48">
                                <img src="https://bulma.io/images/placeholders/96x96.png"
                                     alt="Placeholder image">
                            </figure>
                        </div>
                        <div class="media-content">
                            <p class="title is-4">
                                {{ profile.user.username }}
                            </p>
                            <p class="subtitle is-6">
                                @{{ profile.user.username|lower }}
                            </p>
                        </div>
                    </div>
                </div>
            </a>
        </div>
    </div>

{% endfor %}

</div>

{% endblock content %}
```

Based from the code block above, when we update the `href` attribute in this way, we link to the `path()` call with the name `profile` in our `dwtter` app's **namespace** and pass the `.id` value of each profile as an argument:

* **{% url %}** : The URL template tag in Django allows you to create dynamic links to different endpoints of your web app.

* **`dwitter.profile`** : This part of the template tag defines the namespace of our app (`dwitter`) and the path name (`profile`) that we want our link to redirect to.

* **`profile.id`**

We need to navigate as well to the overall profile list. To round off the user experience, we will also add a `{% url %}` tag to the `href` attribute of the link containing the button in our profile page view so that it links back to the profile list:

```[html]
<!-- dwitter/templates/dwitter/profile.html -->

<div class="block">
    <a href="{% url 'dwitter:profile_list' %}">
        <button class="button is-dark is-outlined is-fullwidth">
            All Profiles
        </button>
    </a>
</div>
```

#### Exercise : Linking our Connections

```[html]
...
<div class="block">
        <h3 class="title is-4">
            {{profile.user.username}} follows:
        </h3>
        <div class="content">
            <ul>
            {% for following in profile.follows.all %}
                <li>
                    <a href="{% url 'dwitter:profile' following.id %}">
                        {{ following }}
                    </a>
                </li>
            {% endfor %}
            </ul>
        </div>
    </div>

    <div class="block">
        <h3 class="title is-4">
            {{profile.user.username}} followed by:
        </h3>
        <div class="content">
            <ul>
            {% for followers in profile.followed_by.all %}
                <li>
                    <a href="{% url 'dwitter:profile' followers.id %}">
                        {{ followers }}
                    </a>
                </li>
            {% endfor %}
            </ul>
        </div>
    </div>
```

To recap, we added two `{% url %}` tags to `profile.html`. Both of them follow the same structure:

* **Namespace**: The namespace `dwitter:profile` allows Django to redirect to `profile()` in views.py
* **Argument**: The argument, which is either `following.id` or `followers.id`, will be passed on to `profile()`, which uses it to pull the user profile from the database.

### Conclusion

We have learned how to:

* Integrate **Bulma CSS** to **style** our app
* Use **template inheritance8** to reduce repetition
* Structure Django templates in a **folder hierarchy**
* Build **routing** and **view functions**
* **Interlink** pages of our app using **dynamic URLs**.

## Part 3 - Build and Handle POST Requests in Django

Objectives for the third part of our tutorial series, we will learn how to:

* Create the **front-end interface** to let users **follow** and **unfollow** profiles.
* Submit and **handle a POST request** in Django using buttons.
* Set up the model for our text-based content.
* **Build styled templates** to display content on the front end.
* Use intricate **model relationships** in template code.

### Step 7: Follow and Unfollow Other Profiles

#### [TBC] - Adding Buttons to our Profiles
 