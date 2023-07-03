from django.urls import path
from .views import CandidateAPIView, JobdescriptionAPIView, LanguageAPIView, RegisterAPI,LoginAPI,RepresentativesAPIView, VendorAPIView,SentMailView,OtpVerification,ResetPasswordview


urlpatterns = [
    path('register', RegisterAPI.as_view()),
    path('login', LoginAPI.as_view(), name='login'),
    path('SentMailView', SentMailView.as_view(), name="sentmail"),
    path('ResetPasswordview', ResetPasswordview.as_view()),
    path('otp', OtpVerification.as_view()),
    path('vendor', VendorAPIView.as_view(), name='vendor'),
    path('represent',RepresentativesAPIView.as_view(),name = 'represent'),
    # path('represent/<int:pk>/',RepresentativesAPIView.as_view(),name = 'represent'),
    path('language', LanguageAPIView.as_view(), name='language'),
    path('candidate', CandidateAPIView.as_view(), name='candidate'),
    path('jobdescription', JobdescriptionAPIView.as_view(), name='jobdescription'),

]