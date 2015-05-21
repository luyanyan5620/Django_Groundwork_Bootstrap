from django.core.management.base import BaseCommand, CommandError
from django.db import models
from .placeholders import *
import os
import traceback
    
class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('app')
        parser.add_argument('models')

    def handle(self, *args, **options):
        "Usage : manage.py groundwork <app> <model>"
        app_arg = options['app']
        models_arg = options['models']

        PROJECT_ROOT = os.getcwd() 
        TEMPLATE_DIR = os.path.join ( PROJECT_ROOT , 'templates')

        PROJECT_NAME = PROJECT_ROOT.replace("\\", "/").split('/')[-1]
	
        try:
            app = app_arg #args[0] # App name is the first parameter
            model_names = models_arg.split(",") #args[1:] # Models which need to be scaffolded will follow
            model_instances = [ models.get_model(app, x) for x in model_names ]

            # url config
            urls = URL_IMPORTS

            # Generate CRUD urls for each model
            for model_instance in model_instances:
                urls += URL_CRUD_CONFIG % {'model':model_instance._meta.object_name.lower(), 'modelClass': model_instance._meta.object_name } 

            urls += URL_END

            # write to urls.py
            f = open( os.path.join (PROJECT_ROOT , app, 'urls.py') , 'w')
            f.write(urls)
            f.close()
            
            # append to root urlconf
            f = open( os.path.join (PROJECT_ROOT , PROJECT_NAME, 'urls.py') , 'a')
            f.write( "\nurlpatterns += patterns ('',\n (r'^%(app)s/', include('%(app)s.urls')),\n)\n" % {'app': app } )
            f.close()



            # forms
            forms_content = FORMS_IMPORTS
            for model_instance in model_instances:
                forms_content += FORMS_MODELFORM_CONFIG % { 'modelClass' : model_instance._meta.object_name }

            formspath = os.path.join (PROJECT_ROOT, app, 'forms.py')
            f = open( formspath , 'w')
            f.write(forms_content)
            f.close()


            # views
            views_content = VIEWS_IMPORTS

            for model_instance in model_instances:
                views_content += VIEWS_CREATE 
                views_content += VIEWS_LIST
                views_content += VIEWS_VIEW
                views_content += VIEWS_UPDATE
                views_content += VIEWS_DEL
                
                views_content = views_content %  {'model':model_instance._meta.object_name.lower(), 'modelClass': model_instance._meta.object_name, 'app': app } 

            # write to views.py
            viewspath = os.path.join (PROJECT_ROOT, app, 'views.py')
            f = open( viewspath, 'w')
            f.write(views_content)
            f.close()


            # Templates
            
            template_dir = os.path.join(TEMPLATE_DIR, app )
            if not os.path.exists(template_dir):
                os.makedirs(template_dir)
            
            print("Generate base template? [Y/N]?")
            yn = input()
            if yn.lower() == 'y':
                f = open(os.path.join(TEMPLATE_DIR, 'base.html') , 'w')
                f.write(TEMPLATES_BASE)
                f.close()
                
            for model_instance in model_instances:
                f = open(os.path.join( TEMPLATE_DIR, app, 'create_%s.html' % (model_instance._meta.object_name.lower()) ) ,'w')
                f.write(TEMPLATES_CREATE  %  { 'modelClass' : model_instance._meta.object_name } )
                f.close()
                
                f = open(os.path.join( TEMPLATE_DIR, app, 'list_%s.html' % (model_instance._meta.object_name.lower()) ) ,'w')
                f.write(TEMPLATES_LIST  %  { 'modelClass' : model_instance._meta.object_name ,'model' : model_instance._meta.object_name.lower(), 'app' : app} )
                f.close()
                
                f = open(os.path.join( TEMPLATE_DIR, app, 'edit_%s.html' % (model_instance._meta.object_name.lower()) ) ,'w') 
                f.write(TEMPLATES_EDIT  %  { 'modelClass' : model_instance._meta.object_name } )
                f.close()
                
                f = open(os.path.join( TEMPLATE_DIR, app, 'view_%s.html' % (model_instance._meta.object_name.lower()) ) , 'w')
                f.write(TEMPLATES_VIEW  %  { 'modelClass' : model_instance._meta.object_name,  'model' : model_instance._meta.object_name.lower()} )
                f.close()

            # settings
            f = open(os.path.join(PROJECT_ROOT, PROJECT_NAME, 'settings.py'), 'a')
            if 'TEMPLATE_DIRS' in open(os.path.join(PROJECT_ROOT, PROJECT_NAME, 'settings.py'), 'r').read():
                f.write( "\nTEMPLATE_DIRS += (os.path.join(  os.path.dirname(__file__), '../templates') ,)\n")
            else:
                f.write( "\nTEMPLATE_DIRS = (os.path.join(  os.path.dirname(__file__), '../templates') ,)\n")
            f.close()

            # Template Tags
            TEMPLATE_TAGS_DIR = os.path.join (PROJECT_ROOT , app, 'templatetags')
            if not os.path.exists(TEMPLATE_TAGS_DIR):
                os.makedirs(TEMPLATE_TAGS_DIR)
            f = open(os.path.join(TEMPLATE_TAGS_DIR, 'getattribute.py'), 'w')
            f.write(TEMPLATE_TAGS)
            f.close()
                
        except:
            traceback.print_exc()
            print("Usage : manage.py groundwork <app> <model>")

