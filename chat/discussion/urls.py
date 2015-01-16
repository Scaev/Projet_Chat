from django.conf.urls import patterns, url
urlpatterns = patterns('discussion.views',
                           url(r'^conversations/(?P<pseudo_utilisateur>\w+)$', 'conversations'),
                           url(r'^connexion$', 'connexion'),
                           url(r'^inscription$', 'inscription'),
                           url(r'^accueil$', 'accueil'),
                           url(r'^conversations/(?P<pseudo_utilisateur>\w+)/creation_conversation$','creation_conversation'),
                           url(r'^discussion/(?P<id_discussion>\w+)$', 'discussion'),
                       )
