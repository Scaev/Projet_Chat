from django.conf.urls import patterns, url
urlpatterns = patterns('discussion.views',
                           url(r'^connexion$', 'connexion'),
                           url(r'^inscription$', 'inscription'),
                            url(r'^accueil$', 'accueil'),
                       
                       
                       )