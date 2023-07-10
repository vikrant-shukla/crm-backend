from django.db import models
from django.contrib.auth.models import AbstractUser
from customer.manager import CustomManager

class UserTable(AbstractUser):
    username = None
    first_name = None
    last_name = None
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    firstname = models.CharField(max_length=20)
    lastname = models.CharField(max_length=20)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=15)
    object_manager = CustomManager()

    def __str__(self):
        return str(self.email)
    
User_choices = (
    ("yes", "yes"),
    ("no", "no"),
    
)

class Vendor(models.Model):
    company_name = models.CharField(max_length=200, blank = True,null = True)
    address = models.CharField(max_length=300,blank = True, null = True)
    nda = models.CharField(max_length=20, choices=User_choices, default="yes")
    nda_reason = models.CharField(max_length=20, blank = True, null = True)
    nda_attach = models.FileField(upload_to="files", blank=True, null=True)
    previous_followup = models.DateField( blank = True,null = True)
    next_followup = models.DateField( blank = True,null = True)
    followup_reason = models.CharField(max_length=200, blank = True,null = True)
    Followup_duration = models.CharField(max_length=200, blank = True,null = True)


    def __str__(self):
        return str(self.company_name)

class Representatives(models.Model):
    company = models.ForeignKey(Vendor, on_delete=models.CASCADE, null=True)
    firstname = models.CharField(max_length=100)
    lastname = models.CharField(max_length=100)
    email = models.EmailField(unique=True,null=True)
    contact_no = models.CharField(max_length=10)

    def __str__(self):
        return str(self.name)
    
class Language(models.Model):
    language= models.CharField(max_length=100)  

    def __str__(self):
        return str(self.language)
    
class Candidate(models.Model):
    language = models.ForeignKey(Language, on_delete=models.CASCADE, null=True)
    Candidatename = models.CharField(max_length=100)
   
    def __str__(self):
        return str(self.Candidatename)

class Jobdescription(models.Model):
    jd = models.ForeignKey(Candidate, on_delete=models.CASCADE, null=True)
    description = models.CharField(max_length=100,  blank=True, null=True)
   
    def __str__(self):
        return str(self.description)
    
    
    
class Followup(models.Model):
    job_description=models.ForeignKey(Jobdescription,on_delete=models.CASCADE)
    status = models.CharField(max_length=20)
    
    def __str__(self):
        return str(self.job_description)
        
User_choices = (
    ("yes", "yes"),
    ("no", "no"),    
)

class Selected(models.Model):
    follow_up=models.ForeignKey(Followup,on_delete=models.CASCADE)
    project_name=models.CharField(max_length=200)
    DOJ=models.DateField()
    project_duration=models.CharField(max_length=20)
    project_end_date=models.DateField()
    working_person=models.CharField(max_length=20)
    extend_status=models.CharField(max_length=20,choices=User_choices)
    extend_period=models.CharField(max_length=20)
    def __str__(self):
        return str(self.project_name)

class Otp(models.Model):
    email = models.ForeignKey(UserTable, on_delete=models.CASCADE)
    otp = models.IntegerField(default=0, unique=True)
    created_on = models.DateTimeField(auto_now_add=True)
    def __str__(self) -> str:
        return str(self.otp)


