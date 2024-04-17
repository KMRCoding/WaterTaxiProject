from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    address = models.CharField(max_length=255)
    phone = models.CharField(max_length=15)
    age = models.PositiveIntegerField()
    date_of_birth = models.DateField()
    GENDER_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),
    ]
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)

    def __str__(self):
        return f'{self.user.username} Profile'


class Ticket(models.Model):
    user= models.ForeignKey(User,on_delete=models.CASCADE)
    route = models.CharField(max_length=100, choices=[
        ('san_fernando_pos', 'San Fernando - POS'),
        ('pos_san_fernando', 'POS - San Fernando'),
    ])   
    schedule_date = models.DateField()
    departure_time = models.TimeField()    
    adult_passengers = models.IntegerField()
    teenage_passengers = models.IntegerField()
    infant_passengers = models.IntegerField()
    elderly_passengers = models.IntegerField()
    comments=models.CharField(max_length=255)
    ticket_class = models.CharField(max_length=20, choices=[  #added ticket_class
        ('economy', 'Economy'),
        ('premium', 'Premium'),
    ])
    trip = models.CharField(max_length=20, choices=[  #added ticket_class
        ('one_way', 'One Way'),
        ('return', 'Return'),
    ])

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name} - {self.schedule_date}"
    

class Emergency(models.Model):
    user= models.ForeignKey(User,on_delete=models.CASCADE, null=True)
    route = models.CharField(max_length=100, choices=[
        ('san_fernando_pos', 'San Fernando - POS'),
        ('pos_san_fernando', 'POS - San Fernando'),
    ])
    emergency_type=models.CharField(max_length=100, choices=[
        ('medical', 'Medical Emergency'),
        ('mechanical', 'Mechanical Emergency'),
        ('fire','Fire'),
        ('collision_grounding','Collision or Grounding'),
        ('man_overboard','Man Overboard'),
    ])
    date_occured = models.DateField()
    age = models.IntegerField(null=True)
    GENDER_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),
    ]
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, null=True)
    comments=models.CharField(max_length=255, null=True)

    def __str__(self):
        return f"{self.comments} - {self.date_occured}"
    

    from django.db import models

class Schedule(models.Model):
    DAY_CHOICES = [
        ('Monday', 'Monday'),
        ('Tuesday', 'Tuesday'),
        ('Wednesday', 'Wednesday'),
        ('Thursday', 'Thursday'),
        ('Friday', 'Friday'),
        ('Saturday', 'Saturday'),
        ('Sunday', 'Sunday'),
    ]

    ROUTE_CHOICES = [
        ('san_fernando_pos', 'San Fernando - POS'),
        ('pos_san_fernando', 'POS - San Fernando'),
    ]

    VESSELS = [
        ('carbo_star', 'Carbo Star'),
    ]

    day = models.CharField(max_length=10, choices=DAY_CHOICES)
    route = models.CharField(max_length=20, choices=ROUTE_CHOICES)
    departure_time = models.TimeField()
    vessel = models.CharField(max_length=50, choices=VESSELS)

    def __str__(self):
        return f"{self.get_day_display()} - {self.get_route_display()} - Departure: {self.departure_time} - Vessel: {self.vessel}"

