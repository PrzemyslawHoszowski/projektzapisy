from django.conf.urls.defaults import *

# to tree/list_view and description, pass by GET:
# format=json - returns data as json
# format=html - returns data rendered with template, not using the base template
# by default, they return a fully rendered page

urlpatterns = patterns('',
    url(r'^$',              'fereol.grade.poll.views.default',                name='grade-default'),
   
    url(r'^prepare_grade$', 'fereol.grade.ticket_create.views.prepare_grade', name='grade-prepare-grade'),
    url(r'^enable_grade$',  'fereol.grade.poll.views.enable_grade',           name='grade-enable-grade'),
    url(r'^disable_grade$', 'fereol.grade.poll.views.disable_grade',          name='grade-disable-grade'),
    
    url(r'^grade_logout$',  'fereol.grade.poll.views.grade_logout',           name='grade-logout'),
    
    (r'^poll/',   include('fereol.grade.poll.urls')),
    (r'^ticket/', include('fereol.grade.ticket_create.urls')),

    url(r'declaration$',  'declaration', name='grade-poll-show'),
)