from django.urls import path
from . import views

app_name = 'realtime'

urlpatterns = [
    # Dashboard - main entry point
    path('', views.dashboard, name='dashboard'),
    path('dashboard/', views.dashboard, name='dashboard'),
    
    # Session management
    path('create-session/', views.create_session, name='create_session'),
    path('live-shopping/<uuid:room_name>/', views.live_shopping_room, name='live_shopping_room'),
    path('room/<uuid:room_name>/', views.shopping_room, name='shopping_room'),  # Legacy compatibility
    path('join/<uuid:session_id>/', views.join_session, name='join_session'),
    path('end/<uuid:session_id>/', views.end_session, name='end_session'),
    path('leave/<uuid:session_id>/', views.leave_session, name='leave_session'),
    
    # Browse and explore
    path('browse-sessions/', views.browse_sessions, name='browse_sessions'),
    
    # API endpoints
    path('api/session/<uuid:session_id>/', views.session_details_api, name='session_details_api'),
    path('test-websocket/', views.test_websocket, name='test_websocket'),
]