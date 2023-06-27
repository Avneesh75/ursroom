from django.urls import path
from home import views


urlpatterns = [
    path('', views.index, name='home'),
    path('about', views.about, name='about'),
    path('terms-and-conditions', views.conditions, name='conditions'),
    path('contact', views.contact, name='contact'),
    path('gallery-details/<str:uuid>', views.gallery_details, name='gallery_details'),
    path('gallery-details-girls', views.gallery_detailsgirls, name='gallery_detailsgirls'),
    path('owner-phone-form/<str:uuid>', views.ownerquery, name='owner_pohone_form'),
    path('owner-remainings', views.ownerremainings, name='owner_remainings'),
    path('owner-details', views.ownerdetails, name='owner_details'),
    path('privacy', views.privacy, name='privacy'),
    path('property-post', views.propertypost, name='property-post'),
    path('urs-location-details/<str:uuid>', views.ursLocationDetails, name='ursLocationDetails'),
    path('ursroom-details/<str:uuid>', views.ursroom_Details, name='ursroom_Details'),
    path('ursroom-details-share', views.ursroom_details_share, name='ursrooms_details_share'),
    path('ursroom-boys', views.ursroom_boys, name='ursroom_boys'),
    path('ursroom-girls', views.ursroom_girls, name='ursroom_girl'),
    path('ursroom-professional', views.ursroom_professional, name='ursroom_professional'),
    path('ursroom-student', views.ursroom_student, name="ursroom_student"),
    path("ursroom-aminities-details/<str:uuid>", views.ursroom_aminities_details, name="ursroom_aminities_details"),
    path("ursroom-personal-details", views.ursroom_personal_details, name="ursroom_personal_details"),
    path("ursroom-room-user-login", views.ursroom_room_user_login, name="ursroom_room_user_login"),
    path("ursroom-room-user-profile", views.ursroom_room_user_profile, name="ursroom_room_user_profile"),
    path("ursroom-room-user-subscription", views.ursroom_room_user_subscription, name="ursroom_room_user_subscription"),
    path("store-response", views.store_response, name="store_response"),
    path("logout", views.user_logout, name="logout"),
    path("register",views.Register,name='register'),
    #path("user_login",views.UserLogin,name='user_login')
]