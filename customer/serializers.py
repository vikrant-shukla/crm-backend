from rest_framework import serializers
from customer.models import  Candidate, Followup, Jobdescription, Language, Otp, Selected, UserTable, Representatives, Vendor
from django.contrib.auth.hashers import make_password
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
import re


class UserTableSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserTable
        fields = ['email', 'password', 'firstname', 'lastname']

    def create(self, validated_data):
        validated_data['email'] = validated_data['email'].lower()
        validated_data['password'] = make_password(validated_data['password'])
        return super(UserTableSerializer, self).create(validated_data)

    def validate(self,data):
        firstname=data.get('firstname')
        lastname=data.get('lastname')
        email=data.get('email')
        password=data.get('password')
        if not re.match(r'^[A-Za-z]{1,30}$', firstname):
            raise serializers.ValidationError("enter valid name")
        if not re.match(r'^[A-Za-z]{1,30}$', lastname):
            raise serializers.ValidationError('Enter a valid name')
        if not re.match(r'^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$', email):
            raise serializers.ValidationError('Enter a email.')
        if not re.match(r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$", password):
            raise serializers.ValidationError('Password must contain 8 character and one uppercase,one lowercase and one special symbol')
        return data
    
class AuthTokenSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        attrs['password'] = attrs.get('password')
        attrs = super().validate(attrs)
        return attrs
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['email'] = user.email
        return token

class SetNewPasswordSerializer(serializers.Serializer):
    password = serializers.CharField(min_length=6, max_length=20)
    email = serializers.EmailField()
    class Meta:
        model = Otp
        fields = '__all__'
        
    def validate_email(self, email):
        user_instance = UserTable.objects.get(email=email)
        print(user_instance.email)
        if Otp.objects.filter(email_id=user_instance.pk).exists():
            if Otp.objects.get(email_id=user_instance.pk):
                return email
        else:
            return serializers.ValidationError('Email does not matched')
        
    def validate(self,data):        
        password=data.get('password')
        if not re.match(r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$", password):
            raise serializers.ValidationError('Password must contain 8 character and one uppercase,one lowercase and one special symbol')
        return data
    
    
class VendorSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Vendor
        fields = '__all__'
    
    def validate(self,data):
        company_name=data.get('company_name')
        address=data.get('address')
        nda=data.get('nda')
        nda_reason=data.get('nda_reason')
        followup_reason=data.get('followup_reason')
        Followup_duration=data.get('Followup_duration')
        
        if not re.match(r'^[A-Za-z ]{1,50}$', company_name):
            raise serializers.ValidationError("enter valid company name")
        if not re.match(r'^[A-Za-z0-9\s\-\.\,\/\ ]+$', address):
            raise serializers.ValidationError('Enter a valid address')
        if not re.match(r'^[A-Za-z ]{1,100}$', nda):
            raise serializers.ValidationError("reason must be character")
        if not re.match(r'^[A-Za-z ]{1,100}$', nda_reason):
            raise serializers.ValidationError("reason must be character")
        if not re.match(r'^[A-Za-z  ]{1,500}$', followup_reason):
            raise serializers.ValidationError(" f reason must be character")
        if not re.match(r'^[A-Za-z0-9 ]{1,50}$', Followup_duration):
            raise serializers.ValidationError("fd reason must be character or number")
        return data

class RepresentativesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Representatives
        fields = '__all__'

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['company'] = VendorSerializer(instance.company).data
        return response
    
    def validate(self,data):
        firstname=data.get('firstname')
        lastname=data.get('lastname')
        email=data.get('email')
        contact_no=data.get('contact_no')       
        if not re.match(r'^[A-Za-z]{1,30}$', firstname):
            raise serializers.ValidationError("enter valid name")
        if not re.match(r'^[A-Za-z]{1,30}$', lastname):
            raise serializers.ValidationError("enter valid name")
        if not re.match(r'^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$', email):
            raise serializers.ValidationError('Enter a correct email.')
        if not re.match(r'^[6789]\d{9}$', contact_no):
            raise serializers.ValidationError("enter valid mobile number")
        
                        
        return data
    
class LanguageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Language
        fields = '__all__'
    
    def validate(self,data):
        language=data.get('language')
        if not re.match(r'^[A-Za-z+\.\+\#]{1,30}$', language):
            raise serializers.ValidationError("enter correct language name")
        return data
        
class CandidateSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Candidate
        fields = '__all__'
    
    def validate(self,data):
        Candidatename=data.get('Candidatename')
        if not re.match(r'^[A-Za-z ]{1,30}$', Candidatename):
            raise serializers.ValidationError("enter valid Candidatename")
        return data

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['language'] = LanguageSerializer(instance.language).data
        return response
    
class  FollowupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Followup
        fields = '__all__'
    def validate(self,data):
        status=data.get('status')
        if not re.match(r'^[A-Za-z ]{1,30}$', status):
            raise serializers.ValidationError("enter valid status")
        return data

class JobdescriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Jobdescription
        fields = '__all__'

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['candidate'] = CandidateSerializer(instance.candidate).data
        response['status'] = FollowupSerializer(instance.status).data
        return response
    
    def validate(self,data):
        description=data.get('description')
        
        if not re.match(r'^[A-Za-z ]{1,500}$', description):
            raise serializers.ValidationError("enter valid description")
        
        return data
        
            
class  SelectedSerializer(serializers.ModelSerializer):
    # shows = JobdescriptionSerializer(read_only=True, many=False)
    class Meta:
        model = Selected
        fields = '__all__'
        
    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['candiadte_details'] = JobdescriptionSerializer(instance.candidate_details).data
        return response
    
    def validate(self,data):
        project_name=data.get('project_name')
        project_duration=data.get('project_duration')
        working_person=data.get('working_person')
        extend_status=data.get('extend_status')
        extend_period=data.get('extend_period')
        if not re.match(r'^[A-Za-z ]{1,30}$', project_name):
            raise serializers.ValidationError("enter correct name")
        if not re.match(r'^[A-Za-z0-9 ]{1,30}$', project_duration):
            raise serializers.ValidationError("enter correct duration")
        if not re.match(r'^[A-Za-z ]{1,30}$', working_person):
            raise serializers.ValidationError("enter valid name")
        if not re.match(r'^[A-Za-z]{1,30}$', extend_status):
            raise serializers.ValidationError("enter correct status")
        if not re.match(r'^[A-Za-z0-9 ]{1,30}$', extend_period):
            raise serializers.ValidationError("enter valid period")
        
        return data
        
         
class OtpVerificationSerializer(serializers.ModelSerializer):
    otp = serializers.CharField(min_length=6, max_length=6)
    email = serializers.EmailField()

    class Meta:
        model = Otp
        fields = '__all__'

    def validate_otp(self, otp):
        if otp:
            if Otp.objects.filter(otp=otp).exists():
                user_instance = UserTable.objects.get(email=self.instance["email"].lower())
                if Otp.objects.get(email=user_instance.pk):
                    return otp
                raise serializers.ValidationError('OTP does not matched')
            raise serializers.ValidationError('OTP does not exits.')
        raise serializers.ValidationError('Please generate Otp again!!!')
