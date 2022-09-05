# Social Network with Django

A four-part tutorial series from [Real Python](https://realpython.com/django-social-network-1/) in which we will build a social network with Django. This will help us in strengthening our understanding of relationships between Django models and show how we can use forms so that our users can interact with our app and with each other. We will be using the Bulma CSS Framework in order to make our side look good!

## Full Project Implementation Steps

We will implement the project in a series of steps spread out over four parts.

🎈 **[Part 1: Models and Relationships](#part-1-models-and-relationships)**

* [Step 1: Set Up the Base Project](#setting-up-the-base-project)
* [Step 2: Extend the Django User Model](#extending-the-django-user-model)
* [Step 3: Implement a Post-Save Hook](#implement-a-post-save-hook)

✨ **[Part 2: Templates and Front-End Styling](#part-2--building-a-django-front-end-with-bulma)**

* [Step 4: Create a Base Template with Bulma](#create-a-base-template-with-bulma)
* [Step 5: List All user profiles](#step-5-listing-all-user-profiles-on-the-front-end-of-our-django-app)
* [Step 6: Access Individual Profile Pages](#step-6-access-individual-profile-pages)

🎉**[Part 3: Follows and Dweets](#part-3---build-and-handle-post-requests-in-django)**

* [Step 7: Follow and Unfollow Other Profiles](#step-7-follow-and-unfollow-other-profiles)
* [Step 8: Create the Back-End Logic For Dweets](#step-8---create-the-back-end-logic-for-dweets)
* [Step 9: Display Dweets on the Front End](#step-9-display-dweets-on-the-front-end)

🎁 **[Part 4: Forms and Submissions](#part-04---build-and-submit-html-forms-with-django)**

* [Step 10: Submit Dweets Through a Django Form](#step-10---submit-dweets-using-django-forms)
* [Step 11: Prevent Double Submissions and Handle Errors](#step-11---prevent-double-submissions-and-handle-errors)
* [Step 12: Improve the Front-End User Experience](#step-12---improve-the-front-end-user-experience)

✍ **[Next Steps](#next-steps)**

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

#### Adding Buttons to our Profiles

```[html]
<div class="column">

    <div class="block">
        <h1 class="title is-1">
            {{profile.user.username|upper}}'s Dweets
        </h1>
    </div>
    <div class="buttons has-addons">
        <button class="button is-success">Follow</button>
        <button class="button is-danger">Unfollow</button>
    </div>

</div>
```

We could add some distinction in our buttons, wherein we could gray out the irrelevant button so that the relevant action will be more apparent for our users. Bulma should render our buttons grayed-out if we add an HTML class called `is-static`.

We can apply the class depending on whether or not the logged-in user is already following the profile that they're viewing.

### Handling POST Requests in Django Code Logic

```[html]
    <form method="post">
        {% csrf_token %}
        <div class="buttons has-addons">
            {% if profile in user.profile.follows.all %}
                <button class="button is-success is-static">Follow</button>
                <button class="button is-danger" name="follow" value="unfollow">
                    Unfollow
                </button>
            {% else %}
                <button class="button is-success" name="follow" value="follow">
                    Follow
                </button>
                <button class="button is-danger is-static">Unfollow</button>
            {% endif %}
        </div>
    </form>
</div>
```

We have a few essential changes to our template by updating our `profile.html` source code:

* We have wrapped our two 'Follow' and 'Unfollow' buttons in an HTML `<form>` element and added the HTML attribute `method` with the value `"post"` to clarify that we'll send data with this form.
* We added a [CSRF token](https://docs.djangoproject.com/en/3.2/ref/csrf/) that Django conveniently provides. We need to add this for security reasons if we want to allow our users to submit forms in our Django app.
* We added two HTML attributes to both `<button>` elements:

1. [name](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/button#attr-name) defines what key we'll use to access the value in our view function. We set this key to `"follow"` for both buttons.
2. [value](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/button#attr-value) defines what value the form will send to our view function under the key name defined in `name` when we press one of the buttons.

```[python]
# dwitter/views.py

# ...

def profile(request, pk):
    profile = Profile.objects.get(pk=pk)
    if request.method == "POST":
        current_user_profile = request.user.profile
        data = request.POST
        action = data.get("follow")
        if action == "follow":
            current_user_profile.follows.add(profile)
        elif action == "unfollow":
            current_user_profile.follows.remove(profile)
        current_user_profile.save()
    return render(request, "dwitter/profile.html", {"profile": profile})
```

Based from our code update above in `views.py`:

* We introduce a conditional check to see whether the incoming request to our Django view function is an HTTP POST request. This will only be the case if someone submitting the form on profile.html by clicking either the *Follow* or *Unfollow* button.
* We have used the user attribute from Django's `request` object, which refers to the currently logged-in user, to access that user's `.profile` object and assign it to `current_user_profile`
* We get the user-submitted data from the `request.POST` dictionary and store it in `data`. Django puts data in `request.POST` when a user submits a form with the attribute `method="post"`.
* We have retrieved the submitted value by accessing the data at the key `"follow"`, which we have defined in our template with the `name` HTML attribute on our `<button>` elements.
* We use `.save()` on our `current_user_profile` to propagate the changes to `.follows` back to the database.

**NOTE**: Just in case we haven't created profiles for you and for our existing users may run into an `RelatedObjectDoesNotExist` error when performing the POST request. In order to prevent this error, we can verify that our user has a profile in our `profile` view:

```[python]
# dwitter/views.py

# ...

def profile(request, pk):
    if not hasattr(request.user, 'profile'):
        missing_profile = Profile(user=request.user)
        missing_profile.save()

    profile = Profile.objects.get(pk=pk)
    if request.method == "POST":
        current_user_profile = request.user.profile
        data = request.POST
        action = data.get("follow")
        if action == "follow":
            current_user_profile.follows.add(profile)
        elif action == "unfollow":
            current_user_profile.follows.remove(profile)
        current_user_profile.save()
    return render(request, "dwitter/profile.html", {"profile": profile})
```

When we call the `profile` view, we first check whether `request.user` contains `profile` with [hasattr](https://docs.python.org/3/library/functions.html#hasattr). If the profile is missing, then we create a profile for our user before proceeding.

With this updates so far, we have fully connected the follow and unfollow back-end logic with the front end. We added an HTML `<form>` element and two buttons in `profile.html`. We have also implemented the code logic in `profile()` that translates the button presses into changes that affect our database.

### Step 8 - Create the Back-end Logic for Dweets

**NOTE**: The type of content that our users post could have been anything! Our focus was only on the connections between users of our app. Now we're getting specific. If we wanted to allow a different form of content in our social network, we'd need to branch off in another direction at this point.

#### Making the Model

```[python]
class Dweet(models.Model):
    user = models.ForeignKey(
        User, related_name="dweets", on_delete=models.DO_NOTHING
    )
    body = models.CharField(max_length=140)
    created_at = models.DateTimeField(auto_now_add=True)
```

Our `Dweet` model needs only 3 fields:

1. **user**: We define the model to be in a foreign jey relationship, which means that each dweet will be associated with a user. We also pass `"dweets"` to `related_name`, which allows us to access the dweet objects from the user side of the relationship through `.dweets`. Finally, we specify the orphaned dweets should stick around by setting `on_delete` to `models.DO_NOTHING`
2. **body**: Defines our content type and we have set a character field limit to a maximum length of 140 characters.
3. **created_at**: The final field of our new model records the date and time when the text-based message is submitted. Setting `auto_now_add` to `True` on a `DateTimeField` object ensures that this value gets automatically updated when a user submits a sweet.

```[python]
(social) C:\Users\Clarence Vinzcent\Real-World-Python\Django-Projects\Django-Social-Network-App>py manage.py makemigrations && migrate
Migrations for 'dwitter':
  dwitter\migrations\0002_dweet.py
    - Create model Dweet
'migrate' is not recognized as an internal or external command,
operable program or batch file.

(social) C:\Users\Clarence Vinzcent\Real-World-Python\Django-Projects\Django-Social-Network-App>py manage.py migrate
Operations to perform:
  Apply all migrations: admin, auth, contenttypes, dwitter, sessions
Running migrations:
  Applying dwitter.0002_dweet... OK
```

#### Adding Dweets Through the Admin Interface

In our dweets functionality, we would be testing the functionality of creating dweets through our admin interface. We are going to register our new `Dweet` model in our admin interface.

```[python]
...
from .models import Profile

...

admin.site.register(Dweet)
```

**NOTE** : We need to assign an existing user object to the sweet that we want to create.

After creating our `dweets`, *Dweet object (1)* isn't an exceedingly descriptive name for the submitted dweet.

```[pytohn]
class Dweet(models.Model):
    user = models.ForeignKey(
        User, related_name="dweets", on_delete=models.DO_NOTHING
    )
    body = models.CharField(max_length=140)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return (
            f"{self.User} "
            f"({self.created_at:%Y-%m-%d %H:%M}): "
            f"{self.body[:30]}..."
        )
```

**NOTE** : We should create a couple of dweets and assign them to different users of our app. We have created at least 3 users and that they all have a few example dweets so that we can see which dweets show up when we follow or unfollow profiles.

As a conclusion to this step, we created a new model for the text content of our Django social network, registered it in our admin interface, and improved how Django displays the objects. In the next section, we'll add the code to tell Django to show these dweets on the front end of our web app.

### Step 9: Display Dweets on the Front End

#### Displaying Personal Dweets on Each Profile Page

The name that we defined in our `Dweet` model gives us reverse access to the associated `User` Model.

```[python]
profile.user.dweets
```

```[html]
  <div class="content">
        {% for dweet in profile.user.dweets.all %}
            <div class="box">
                {{ dweet.body }}
                <span class="is-small has-text-grey-light">
                    ({{ dweet.created at }})
                </span>
            </div>
        {% endfor %}
    </div>
```

The iteration works after stepping through our model relationships, and we can view the dweets of the current user in a pleasant way thanks to Bulma's Stylesheet!

We're still missing a way to display a feed of all the dweets of all the profiles we follow. We implement this functionality by updating our dashboard view.

#### Create a Dashboard View

On our dashboard, we want to be able to do two things:

1. Read all dweets from the profiles we follow.
2. Submit a dweet.

```[html]
{% comment %} dwitter/templates/dwitter/dashboard.html {% endcomment %}

{% for followed in user.profile.follows.all %}
    {% for dweet in followed.user.dweets.all %}
        <li>{{dweet.user.username}} ({{ dweet.created_at }}): {{ dweet.body }}</li>
    {% endfor %}
{% endfor %}
```

Before we proceed any further by applying Bulma's styling, it's worth to revisit first the model relationships that we're chaining together in our Django template:

* We dive into the `user` object that Django sends with every POST or GET request. It refers to the logged-in user, currently our admin user. With `.profile`, we access the profile of our admin user, which we set up when we extended the Django User Model. The profile has an attribute called `.follows` that holds a collection of all the user profiles that this profile follows. Finally, with `.all`, we access an iterable of that collection.
* We nest another `for` loop into the previous one. Here, we access `followed` to get at each user profile that the currently logged-in user follows.
* We now have access to each dweet in `dweet`. We will use that to pick out the information we want from each text-based message and assemble this information in a single HTML list item.

Time to buff up `dashboard.html` so that it fits with the design of the rest of our social network!

```[html]
{% comment %} dwitter/templates/dwitter/dashboard.html {% endcomment %}

{% extends 'base.html' %}

{% block content %}

<div class="column">

    {% for followed in user.profile.follows.all %}
        {% for dweet in followed.user.dweets.all %}
            <div class="box">
                {{ dweet.body }}
                <span class="is-small has-text-grey-ligt">
                    ({{ dweet.created_at }}) by {{ dweet.user.username }}
                </span>
            </div>
        {% endfor %}
    {% endfor %}

</div>

{% endblock content %}
```

By extending our base template and adding some styling through Bulma's CSS classes, we have created an attractive dashboard page that shows our feed displaying all the dweets of all the profiles we follow. Each user will see their own personal feed of dweets, based on which profiles they follow.

To wrap-up this step, we added a new dashboard template that displays a personal feed of dweets, and we also added code to `profile.html` that shows each user's dweets on their profile page.

### Conclusion Part 03

In the process of building this project, we have learned how to:

* Create the **front-end interface** to **follow and unfollow** profiles
* Submit and handle a **POST request** in Django using **buttons**
* Set up the **model** for our text-based content
* Build **styled templates** to display content on the front end
* Use intricate **model relationships** in template code

## Part 04 - Build and submit HTML Forms with Django

In the fourth part of the tutorial series, we'll learn how to:

* Create and render **Django forms** from our `Dweet` model
* **Prevent double submissions** and **display helpful error messages**
* **Interlink** pages of our app using **dynamic URLs**
* **Refactor** a view function
* Using **`QuerySet`** **field lookups** to **filter** our data on the back end

### Step 10 - Submit Dweets Using Django Forms

In this specific tutorial series, we decided early on to handle usr creation in our Django admin. Our tiny social network is invite-only, and we're the one who decides to create user accounts.

**NOTE**: Feel free to expand on this with [Django's user management system](https://realpython.com/django-user-management/) and build the necessary templates by following the linked tutorial.

Once we have our users get into our social network app, we'll want to give them the opportunity to create content.

#### Create a Text Input Form

We'll learn how to create HTML forms using a **Django Form**.

```[python]
# ./dwitter/forms.py

from django import forms
from .models import Dweet


class DweetForm(forms.ModelForm):
    body = forms.CharField(required=True)

    class Meta:
        model = Dweet
        exclude = ("user",)
```

Creating forms like the code snippet above relies heavily on abstractions set up by Django, which means that we need to define very little by ourselves to get a working form.

* We have created a [`Meta` options](https://docs.djangoproject.com/en/3.2/topics/db/models/#meta-options) class in `DweetForm`. This options class allows us to pass any information that isn't a field to our form class.
* We need to define which model `ModelForm` should take its information from. Because we want to make a form that allows users to create dweets, `Dweet` is the right choice here.
* By adding the name of the model field that we want to exclude to the `exclude` tuple, we ensure that Django will omit it when creating the form.

We want to make the dweet submissions as user-friendly as possible. Users can only dweet on our social network when they're logged in, and they can only create dweets for themselves. Therefore, *we don't need to explicitly pass which user is sending a dweet inside the form*.

**NOTE**: Associating a dweet to a user is necessary, but we'll handle that in the back end instead.

#### Render the Form in Your Template

```[python]
# ./dwitter/views.py

from django.shortcuts import render

from .forms import DweetForm
from .models import Profile


# Create your views here.
def dashboard(request):
    form = DweetForm()
    return render(request, "dwitter/dashboard.html", {"form": form})
...
```

```[html]
<!-- dwitter/templates/dwitter/dashboard.html -->

{% extends 'base.html' %}

{% block content %}

<div class="column">

    {% for followed in user.profile.follows.all %}
        {% for dweet in followed.user.dweets.all %}
            <div class="box">
                {{ dweet.body }}
                <span class="is-small has-text-grey-ligt">
                    ({{ dweet.created_at }}) by {{ dweet.user.username }}
                </span>
            </div>
        {% endfor %}
    {% endfor %}

</div>

<div class="column is-one-third">
    {{ form.as_p }}
</div>

{% endblock content %}
```

We can improve the display of our Django form by adding customizations through a **widget** to `forms.CharField` in `forms.py`.

```[python]
# ./dwitter/forms.py

from django import forms
from .models import Dweet


class DweetForm(forms.ModelForm):
    body = forms.CharField(
        required=True,
        widget=forms.widgets.Textarea(
            attrs={
                "placeholder": "Dweet something...",
                "class": "textarea is-primary is-medium",
            }
        ),
        label="",
    )

    class Meta:
        model = Dweet
        exclude = ("user",)
```

By adding a [Django widget](https://docs.djangoproject.com/en/3.2/ref/forms/widgets/) to `CharField`, we get to control how the HTML input element will be represented:

* We choose the type of input element that Django should use and set it to Textarea. The `Textarea` widget will render as an [HTML `<textarea>` element](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/textarea), which offeres more space for our users to enter their dweets.
* We set the `label` to an empty string (""), which removes the *Body* text that previously showed up due to a Django default setting that renders the name of a form field as its label.

#### Make Form Submissions Possible

To create a functional form that allows POST requests, we'll also need to define the HTTP method accordingly:

```[html]
<!-- dwitter/templates/dwitter/dashboard.html -->

{% extends 'base.html' %}

{% block content %}

<div class="column">

    {% for followed in user.profile.follows.all %}
        {% for dweet in followed.user.dweets.all %}
            <div class="box">
                {{ dweet.body }}
                <span class="is-small has-text-grey-ligt">
                    ({{ dweet.created_at }}) by {{ dweet.user.username }}
                </span>
            </div>
        {% endfor %}
    {% endfor %}

</div>

<div class="column is-one-third">
    <form method="post">
        {% csrf_token %}
        {{ form.as_p }}
        <button class="button is-primary is-fullwidth is-medium mt-5"
                type="submit">
            Dweet
        </button>
    </form>
</div>

{% endblock content %}
```

With another incremental update to our HTML code, we completed the front-end setup of our dweet submission form:

* We wrapped the form code in an HTML `<form>` element with `method` set to `"post"` because we want to send the user-submitted messages via a POST request.

What happens when we click the *Dweet* button? Not much, because we haven't set up any code logic to complement our front-end code yet. Here's the submit functionality shown in our `views.py`:

```[python]
# ./dwitter/views.py

from django.shortcuts import render

from .forms import DweetForm
from .models import Profile


# Create your views here.
def dashboard(request):
    if request.method == "POST":
        form = DweetForm(request.POST)
        if form.is_valid():
            dweet = form.save(commit=False)
            dweet.user = request.user
            dweet.save()
    form = DweetForm()
    return render(request, "dwitter/dashboard.html", {"form": form})
```

With some additions to `dashboard()`, we make if possible for our view to handle the submitted data and create new dweets in our database. We have one issue that we need to address. If we write a dweet and submit it now, it gets added and if we reload the page after submitting, the same dweet will get added again!

#### Step 11 - Prevent Double Submissions and Handle Errors

After posting a dweet, Django sends another POST request with the same data and creates another entry in our database if *we reload the page*. Django will keep making duplicate dweets as often as we keep reloading. We don't want that to happen!

#### Prevent Double Submissions

To avoid double dweet submissions, we'll have to **prevent our app from keeping the request data around**, so that a *reload* won't have a change to resubmit the data. We can do just that by using a [Django Redirect](https://realpython.com/django-redirects/):

```[python]
from django.shortcuts import render
from django.shortcuts import redirect

from .forms import DweetForm
from .models import Profile


# Create your views here.
def dashboard(request):
    if request.method == "POST":
        form = DweetForm(request.POST)
        if form.is_valid():
            dweet = form.save(commit=False)
            dweet.user = request.user
            dweet.save()
            return redirect("dwitter:dashboard")
    form = DweetForm()
    return render(request, "dwitter/dashboard.html", {"form": form})
```

When we have imported `redirect()`, we're sending a GET request, which means that any number of page reloads will only ever show the dweets that already exist instead of creating an army of cloned dweets.

We set up our redirect path by referencing the `app_name` variable and the name keyword argument of a `path()`, which we have defined in our URL configuration:

* **"dwitter"** is the `app_name` variable that describes the namespace of our app. We can find it before the colon (:) in the string argument passed to `redirect()`
* **"dashboard"** is the value of the `name` keyword argument for the `path()` entry that points to `dashboard()`. We need to add it after the colon (:) in string argument passed to `redirect()`

```[python]
# dwitter/urls.py

from django.urls import path

from .views import dashboard
from .views import profile_list
from .views import profile

app_name = "dwitter"

urlpatterns = [
    path("", dashboard, name="dashboard"),
    ...
]
```

With `urls.py` set up as shown above, we can use `redirect()` to point our users back to their dashboard page with a GET request after successfully processing the POST request from their form submission.

When we don't give a proper error message to our users that our dweet has already gone beyond the 140 character limit, then the text we have already entered has already disappeared as well. Better to make this user experience better for our users by notifying them about what they did wrong and keeping the text they entered!

#### Handle Submission Errors

We could use the Django forms rendered with `{{ form.as_p }}` to display error messages that get sent along with the form object without needing to add any code. These error messages can improve the user experience significantly.

Why we can't see error messages? We take another look at `dashboard()`:

```[python]
from django.shortcuts import render
from django.shortcuts import redirect

from .forms import DweetForm
from .models import Profile


# Create your views here.
def dashboard(request):
    if request.method == "POST":
        form = DweetForm(request.POST)
        if form.is_valid():
            dweet = form.save(commit=False)
            dweet.user = request.user
            dweet.save()
            return redirect("dwitter:dashboard")
    form = DweetForm()
    return render(request, "dwitter/dashboard.html", {"form": form})
```

We can see that we're creating one of two different `DweetForm` objects, either [a bound or an unbound form](https://docs.djangoproject.com/en/3.2/ref/forms/api/#ref-forms-api-bound-unbound). Inspecting the code above:

* If our function gets called from a POST request, we instantiate `DweetForm` with the data that came along with the request. Django creates a **bound form** that hass access to data and can get validated.
* If our page gets called with a GET request, we're instantiating an **unbound form** that doesn't have any data associated with it.

We should validate the bound form, and if the validation passes, the dweet gets written to our database. However, if a user adds to many characters, then our form validation fails, and the code in our conditional statement doesn't get executed. Our `dashboard()` view function jumps to overwrite `form` with an empty unbound `DweetForm` object. Since we overwrote the bound form that held the information about the validation error with an unbound form, Django won't display any of the validation errors that occured.

In order to send the bound form to the template if a validation error orccurs:

```[python]
from django.shortcuts import render
from django.shortcuts import redirect

from .forms import DweetForm
from .models import Profile


# Create your views here.
def dashboard(request):
    form = DweetForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            dweet = form.save(commit=False)
            dweet.user = request.user
            dweet.save()
            return redirect("dwitter:dashboard")
    return render(request, "dwitter/dashboard.html", {"form": form})
```

**NOTE** : Python Boolean `or` operator is a **short-circuit** operator. This means that it only evaluates the second argument if the first one if `False`, or falsy.

* **POST request**: IF we call `dashboard()` with a POST request that includes any data, the `request.POST` [`QueryDict`](https://docs.djangoproject.com/en/3.2/ref/request-response/#django.http.QueryDict) will contain our form submission data. The `request.POST` object now has a **truthy** value, and Python will short-circuit the `or` operator to return the value of `request.POST`. This way, we'll pass the form content as an argument when instantiating `DweetForm`, as we did previously with `form = DweetForm(request.POST)`.
* **GET request**: If we call `dashboard()` with a GET request, `request.POST` will be empty, which is a **falsy** value. Python will continue evaluating the `or` expression and return the second value, `None`. Therefore, Django will instantiate `DweetForm` as an unbound form object, like we previously did with `form = DweetForm()`.

The advantage of this setup is that we now pass the bound form to our template even when the form validation fails, which allows Django's `{{ form.as_p }}` to render a descriptive error message for our users out of the box:

**NOTE**: We didn't need to add any HTML to our template to make this change. Django knows how to render form submission errors when they get sent along in a bound form object inside the {{ form.is_p }} tag.

The best thing about this certain change is that we're passing the bound form object that retains the text data that our user entered in the form. No data is lost, and they can use the helpful suggestions to edit their dweet and submit it to the database successfully.

#### Step 12 - Improve the Front-End User Experience

#### Improving the Navigation

Our social network has 3 different pages that our users might want to visit at different times:

1. The empty URL path (/) points to the dashboard page.
2. The `/profile_list` URL path points to the list of profiles.
3. The `/profile/<int>` URL path points to a specific user's profile page.

We will be adding two buttons in our `dashboard.html` that will allow our users to navifate to different pages in our app:

1. The profile list page
2. Their personal profile page

#### Sorting the Dweets

There are a couple of ways that we could sort the dweets, and a few places where we could do that, namely:

1. In our model
2. In our view function
3. In our template

Our take on handling the sorting of the user's dweets from latest to oldest, wherein we specify the ordering option in our `Dweet` model class that orders our list of queries from its most recent to its oldest dweet.

```[python]
# ./dwitter/models.py

class Dweet(models.Model):
    user = models.ForeignKey(
        User, related_name="dweets", on_delete=models.DO_NOTHING
    )
    body = models.CharField(max_length=140)
    created_at = models.DateTimeField(auto_now_add=True)


    # We can set our ordering in our model class.
    # This will be the default ordering for the object, for use
    # when obtaining lists of objects. 
    class Meta:
        ordering = ['-created_at']


    def __str__(self):
        return (
            f"{self.user} "
            f"({self.created_at:%Y-%m-%d %H:%M}): "
            f"{self.body[:30]}..."
        )
```

In our view functions, we can use Django ORM calls with modifiers to get precisely the dweets we're looking for. We will fetch all the dweets from all the profiles that a user follows right inside our view function. Then we'll sort them by date and time and pass a new sorted iterable named dweet to our template.

```[python]
# ./dwitter/views.py

from django.shortcuts import render
from django.shortcuts import redirect

from .forms import DweetForm
from .models import Profile
from .models import Dweet


# Create your views here.
def dashboard(request):
    form = DweetForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            dweet = form.save(commit=False)
            dweet.user = request.user
            dweet.save()
            return redirect("dwitter:dashboard")

    followed_dweets = Dweet.objects.filter(
        user__profile__in=request.user.profile.follows.all()
    ).order_by("-created_at")
    return render(
        request, 
        "dwitter/dashboard.html", 
        {"form": form, "dweets": followed_dweets},
    )
```

Some key Django concepts based from our code snippet above:

* In our `user__profile__in`, this signifies that our Django ORM syntax for the main part of a SQL WHERE clause. We can follow through database relations with a double-underscore syntax (__) specific to Django ORM. We write `user__profile__in` to access the profile of a user and see whether that profile is in a collection that we'll pass as thevalue to our field lookup keyword argument.

We can now update the template in `dashboard.html` to reflect these changes and reduce the amount of code logic that we need to write in our template, effectively getting rid of our nested for loop:

```[html]
<!-- dwitter/templates/dwitter/dashboard.html -->

{% extends 'base.html' %}

{% block content %}

<div class="column">

    {% for dweet in dweets  %}
        <div class="box">
            {{ dweet.body }}
            <span class="is-small has-text-grey-ligt">
                ({{ dweet.created_at }}) by {{ dweet.user.username }}
            </span>
        </div>
    {% endfor %}

</div>
```

We've made the pre-selected and pre-sorted dweets available to our template under the name `dweets`. Now we can iterate over that `QuerySet` object with a single `for` loop and access the dweets attributes without needing to step through any model relationships in our template.

### conclusion Part 04

In the process of building this project, we've learned how to:

* Build a **Django Project** from start to finish.
* Implement `OneToOne` and `ForeignKey` relationships between Django **models**
* Extend the Django **user model** with a custom `Profile` model
* Customize the **Django admin** interface
* Integrate **Bulma CSS** to **style** our app.

## Next Steps

We can keep improving our Django social network to add functionality and make it even more impressive. Here are some ideas to take our Social Media Project to the next level:

* **Implement User Authentication**: Allow new users to sign up through the front end of our web app by following the steps outlined in [Get Started with Django Part 2: Django User Management](https://realpython.com/django-user-management/)
* **Deploying our Dwitter Project**: Put our web app online for the whole world to see by [hosting our Django project on Heroku](https://realpython.com/django-hosting-on-heroku/)
* **Get social!**: Invite our friends to join our Django social network, and start dweeting thoughts to one another.
* **Adding a delete dweet functionality**

## Django User Management

Some notes that are important to remember when dealing with Django User Management!

* When testing the Password Reset functionality of your Django App, running a local live server that accepts email messages is the way to go. Run the following command in your terminal:

```[python]
py -m smtpd -n -c DebuggingServer localhost:1025
```

Sample email message generated after sending into the local host (using **cvinzreyes@gmail.com**)

```[python]
---------- MESSAGE FOLLOWS ----------
b'Content-Type: text/plain; charset="utf-8"'
b'MIME-Version: 1.0'
b'Content-Transfer-Encoding: 8bit'
b'Subject: Password reset on 127.0.0.1:8000'
b'From: webmaster@localhost'
b'To: cvinzreyes@gmail.com'
b'Date: Sun, 04 Sep 2022 16:19:35 -0000'
b'Message-ID: <166230837534.24728.896738955454107603@LAPTOP-SS9A7TBK>'
b'X-Peer: ::1'
b''
b''
b"You're receiving this email because you requested a password reset for your user account at 127.0.0.1:8000."
b''
b'Please go to the following page and choose a new password:'
b''
b'http://127.0.0.1:8000/reset/MQ/bb94wn-a1c59d17588d7f231c210243e399e599/'
b''
b'Your username, in case you\xe2\x80\x99ve forgotten: admin'
b''
b'Thanks for using our site!'
b''
b'The 127.0.0.1:8000 team'
b''
------------ END MESSAGE ------------
```

After creating your `password_reset_confirm` and `password_reset_complete` forms, make sure to click on the email link that was being send to the test server just like the sample below:

```[python]
---------- MESSAGE FOLLOWS ----------
...
b'http://127.0.0.1:8000/reset/MQ/bba1ca-1cbe8629fddadd7950596420f68ba3f7/'
b''
b'Your username, in case you\xe2\x80\x99ve forgotten: admin'
b''
b'Thanks for using our site!'
b''
b'The 127.0.0.1:8000 team'
b''
------------ END MESSAGE ------------
```

**NOTE**: Django provides a [lot of variables and important security reminders](https://docs.djangoproject.com/en/3.0/topics/auth/default/#django.contrib.auth.views.PasswordResetView) in the email template context that you can use to compose your own messages:
