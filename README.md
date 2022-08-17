# Social Network with Django

A four-part tutorial series from [Real Python](https://realpython.com/django-social-network-1/) in which we will build a social network with Django. This will help us in strengthening our understanding of relationships between Django models and show how we can use forms so that our users can interact with our app and with each other. We will be using the Bulma CSS Framework in order to make our side look good!

## Full Project Implementation Steps

We will implement the project in a series of steps spread out over four parts.

🎈 **Part1: Models and Relationships**

* Step 1: Set Up the Base Project
* Step 2: Extend the Django User Model
* Step 3: Implement a Post-Save Hook

✨ **Part 2: Templates and Front-End Styling**

* Step 4: Create a Base Template with Bulma
* Step 5: List All user profiles
* Step 6: Access Individual Profile Pages

🎉 **Part 3: Follows and Dweets**

* Step 7: Follow and Unfollow Other Profiles
* Step 8: Create the Back-End Logic For Dweets
* Step 9: Display Dweets on the Front End

🎁 **Part 4: Forms and Submissions**

* Step 10: Submit Dweets Through a Django Form
* Step 11: Prevent Double Submissions and Handle Errors
* Step 12: Improve the Front-End User Experience

## Part 1

### Objectives

* [ ] - Implement **one-to-one** and **many-to-many** relationships between Django **models**
* [ ] - Extend the **Django user model** with a custom `Profile` model
* [ ] - Customize the **Django admin interface**.

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

## [TBC] - Part 2 : Building a Django Front End with Bulma
