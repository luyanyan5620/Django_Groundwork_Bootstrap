# Django_Groundwork_Bootstrap


A Django tool to help you generate CRUD code on your Django project.

---

**1:How to install**

you can git clone this tool-app ([github address][1]) to your Django project root floder.

edit your project's **settings.py**,add 'bootstrap3' and 'django-groundwork',just like:

    INSTALLED_APPS = (
    #
    #
    'bootstrap3',
    #blog or others#
    'django-groundwork',
    #
    
    )

now you can use this command:

     python manage.py help

to check out this tools has been add in your project,if you see:

       [django-groundwork]
        groundwork
        placeholders

Congratulations! you can use this funny tool now.


----------


**2: How to get fun**

 - add your app-name to INSTALLED_APPS(settings.py)
 - add your model to your APP floder
 - use this command:
 
    python manage.py groundwork APP-name [Model-name,Model-name,...]

eg: 

    python manage.py groundwork blog Subject,Article

it will help you gererate some boring code:
app:
    *forms.py
    urls.py
    views.py
    templatetags/*
project:
    *template/*.html*

**3:others**

this tools base on Django-groundwork ([github address][2]),Thanks to the Author.

this tools support python3 and Django(test in 1.8),add bootstrap support to make page looks fine.

this tools create a template-tag to help you get dynamic attribue from dynamic object in the page.

so Enjoy it!


  [1]: https://github.com/lianzhengkun/Django_Groundwork_Bootstrap.git
  [2]: https://github.com/madhusudancs/django-groundwork
