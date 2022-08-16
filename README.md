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

### [TBC] Extending the Django User Model
