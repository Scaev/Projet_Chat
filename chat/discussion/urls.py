from django.conf.urls import patterns, url
urlpatterns = patterns('discussion.views',
                           url(r'^conversations/(?P<pseudo_utilisateur>\w+)$', 'conversations'),
                           url(r'^connexion$', 'connexion'),
                           url(r'^inscription$', 'inscription'),
                           url(r'^accueil$', 'accueil'),
                           #url(r'^creation_conversation/(?P<pseudo_utilisateur>\w+)$','creation_conversation'),
                       )
