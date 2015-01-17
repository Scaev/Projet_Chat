from django.conf.urls import patterns, url
urlpatterns = patterns('discussion.views',
                           url(r'^conversations/(?P<pseudo_utilisateur>\w+)$', 'conversations'),
                           url(r'^connexion$', 'connexion'),
                           url(r'^inscription$', 'inscription'),
                           url(r'^changement$', 'changement'),
                           url(r'^conversations/(?P<pseudo_utilisateur>\w+)/creation_conversation$','creation_conversation'),
                           url(r'^conversations/(?P<pseudo_utilisateur>\w+)/(?P<id_conversation>\d+)/quitter_conversation$','quitter_conversation'),
                           url(r'^conversations/(?P<pseudo_utilisateur>\w+)/(?P<id_conversation>\d+)/ajout_ami_conversation$','ajout_ami_conversation'),
                           url(r'^discussion/(?P<id_discussion>\w+)$', 'discussion'),
                       )
