from django.urls import path
from . import views



urlpatterns = [
    path('stream/<int:pk>/', views.get_streaming_video, name='stream'),
    path('examples/', views.examples, name='examples'),
    path('checks_path/', views.getting_checks),
    path('send_money/', views.send_coins_page),
    path('send_stars/', views.send_stars_page, name='stars'),
    path('success/<str:status>', views.status_sending),
    path('error/<str:status>', views.error_wallet),
    path('<int:pk>/', views.VideoDetailView.as_view(), name='videomain'),
    path('', views.get_list_video, name='home'),
    path('seedance', views.get_list_dance, name='seedance'),
    path('profile/<username>/', views.Profile, name="profile"),
    path('profile/<username>/follow/<option>', views.follow, name="follow"),
    path('send_request/<int:user_id>/', views.send_request, name='send_request'),
    path('respond_request/<int:request_id>/<str:action>/', views.respond_request, name='respond_request'),
    path('profile/<username>/wallet/', views.wallet_user),
    path('user/<username>', views.ViewProfile, name='edit'),
    path('edit/<int:pk>/', views.Edite.as_view(), name='edit_profile'),
    path('create_video/', views.video_create, name='create'),
    path('createmusic/', views.video_create_music, name='createmusic'),
    path('audiocut/', views.audio_create, name='audiocut'),
    path('reels/', views.reels_create, name='reels'),
    path('blackwhite/', views.blackwhite, name='blackwhite'),
    path('slowing/', views.slowing, name='slowing'),
    path('speedup/', views.speedup, name='speed'),
    path('images/', views.zip_image, name='zip_image'),
    path('render/', views.render_video, name='render'),
    path('render1/', views.render_vid, name='render2'),
    path('error1/', views.verifyprofile, name='error1'),
    path('loading/', views.process_data),
    path('loading1/', views.process_data1),
    path('loading2/', views.process_data2),
    path('loading3/', views.process_data3),
    path('loading4/', views.process_data4),
    path('loading5/', views.process_data5),
    path('loading6/', views.process_data6),
    path('loading7/', views.process_data7),
    path('loading8/', views.process_data8),
    #path('loading9/', views.process_data9),
    path('loading10/', views.process_data10),
    path('rerender/', views.re_rend_video),
    path('rerender1/', views.re_rend_video1),
    path('rerender2/', views.re_rend_video2),
    path('rerender3/', views.re_rend_video3),
    path('rerender4/', views.re_rend_video4),
    path('rerender5/', views.re_rend_video5),
    path('rerender6/', views.re_rend_video6),
    path('rerender7/', views.re_rend_video7),
    path('rerender8/', views.re_rend_video8, name='rerender8'),
    path('rerender9/', views.re_rend_video9, name='rerender9'),
    path('rerender10/', views.re_rend_video10, name='rerender10'),
    path('slideshow/', views.slideshow, name='slideshow'),
    path('videoshow/', views.videoshow, name='videoshow'),
    path('update/<int:pk>', views.UpdateCreateView.as_view(), name='update'),
    path('delete/<int:pk>', views.delete_video_v, name='delete'),
    path('delete1/<int:pk>', views.delete_video_w, name='deletemusic'),
    path('download/<int:pk>/', views.download_video_v, name='download'),
    path('download1/<int:pk>/', views.download_video_w, name='downloadvideo'),
    path('download2/<int:pk>/', views.download_audio_w, name='downloadaudio'),
    path('download3/<int:pk>/', views.download_video_z, name='downloadvideo2'),
    path('download4/<int:pk>/', views.download_images, name='zip_image1'),
    path('download5/<int:pk>/', views.download_blackwhite, name='blackwhite'),
    path('download6/<int:pk>/', views.download_slowing, name='slowing'),
    path('download7/<int:pk>/', views.download_render, name='ren'),
    path('download8/<int:pk>/', views.download_render1, name='renders'),
    path('download9/<int:pk>/', views.download_slide_w, name='downloadslide'),
    path('download10/<int:pk>/', views.download_slide_f, name='downloadslide1'),
    path('download11/<int:pk>/', views.download_speed, name='speed'),
    path('download12/<int:pk>/', views.download_video_f, name='downloadvideo1'),
    path('login/', views.MyprojectLoginView.as_view(), name='login'),
    path('register/', views.RegisterUserView.as_view(), name='register'),
    path('logout/', views.MyprojectLogoutView.as_view(), name='logout'),
    path('video/<int:pk>/like/', views.AddLike.as_view(), name='like'),
    path('video/<int:pk>/dislike/', views.AddDislike.as_view(), name='dislike'),
    path('handle-request/', views.handle_request, name='handle_request'),
]
