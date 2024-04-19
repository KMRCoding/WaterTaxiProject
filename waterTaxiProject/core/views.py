from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.models import User
from .models import UserProfile, Ticket, Emergency, Schedule
from django.contrib.auth.decorators import login_required
from datetime import datetime
from django.db.models import Count
from datetime import date
from collections import Counter
from django.db.models import Sum



def signup_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        address = request.POST['address']
        phone = request.POST['phone']
        age = request.POST['age']
        date_of_birth = request.POST['date_of_birth']
        gender = request.POST['gender']
        email = request.POST['email']

        # Create User with first_name and last_name
        user = User.objects.create_user(username=username, password=password, email=email, first_name=first_name, last_name=last_name,)
        
        # Create UserProfile
        UserProfile.objects.create(user=user, address=address, phone=phone, age=age, date_of_birth=date_of_birth, gender=gender)

        # Redirect to login page after successful signup
        return redirect('login')  # Assuming 'login' is the name of your login URL pattern

    return render(request, 'core/SignUp.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        # Authenticate the user
        user = authenticate(request, username=username, password=password)

        if user is not None:
            # User is authenticated, login the user
            result= login(request, user)
            # Redirect to a success page (e.g., home page)
            if user.is_staff:
                return redirect('addschedule')
            else:
                return redirect('home')  # Replace 'home' with your desired URL name
        else:
            # Authentication failed, show error message
            messages.error(request, 'Invalid username or password. Please try again.')
            return redirect('login')  # Redirect back to login page

    return render(request, 'core/Login.html')  # Render the login page template


@login_required
def profile(request):
    user = request.user  # Retrieve the logged-in user object

    # You can access user attributes and related data
    context = {
        'username': user.username,
        'email': user.email,
        'first_name': user.first_name,
        'last_name': user.last_name,
        # Add more user-related data as needed
    }

    return render(request, 'core/profile.html', context)

def index(request):
    user = request.user # Retrieve the logged-in user object

    return render(request, 'core/index.html')

def schedule(request):
    user = request.user # Retrieve the logged-in user object

    schedule_records = Schedule.objects.all()

    # Prepare data for the Tabulator table
    data = []
    for record in schedule_records:
        data.append({
            'day': record.day,
            'route': record.route,
            'departureTime': record.departure_time.strftime('%H:%M'),  # Format time as string
            'vessel': record.vessel
        })

        day={ #added ticket_class library
        'Monday': 'Monday',
        'Tuesday': 'Tuesday',
        'Wednesday': 'Wednesday',
        'Thrursday': 'Thrursday',
        'Friday': 'Friday',        
        'Saturday': 'Saturday',        
        'Sunday': 'Sunday',        
        }
        route={
            'san_fernando_pos': 'San Fernando - POS',
            'pos_san_fernando': 'POS - San Fernando',
        }  
        vessel={
            'carbo_star': 'Carbo Star',
        }
         

    context={'data':data,'day':day,'route':route, 'vessel':vessel,}
    return render(request, 'core/schedule.html', context)

@login_required
def purchaseTicket(request):
    user = request.user # Retrieve the logged-in user object
    if request.method == 'POST':
        route = request.POST['Route']
        schedule_date = request.POST['scheduleDate']
        departure_time = request.POST['DepartureTime']
        ticket_class = request.POST['ticket_class']
        adult_passengers = request.POST['Adults']
        teenage_passengers = request.POST['Teenager']
        infant_passengers = request.POST['Infant']
        elderly_passengers = request.POST['Elderly']
        comments = request.POST['comments']
        trip = request.POST['trip']
        time=datetime.strptime(departure_time, "%I:%M %p").time()
        ticket=Ticket(user=user,route=route,schedule_date=schedule_date,departure_time=time,adult_passengers=adult_passengers,
            teenage_passengers=teenage_passengers,infant_passengers=infant_passengers,elderly_passengers=elderly_passengers,ticket_class=ticket_class,trip=trip, 
            comments=comments)
        ticket.save()
    context = {
        'username': user.username,
        'email': user.email,
        'first_name': user.first_name,
        'last_name': user.last_name,
        # Add more user-related data as needed
    }
    return render(request, 'core/purchaseTicket.html',context)

def fares(request):
    user = request.user # Retrieve the logged-in user object

    return render(request, 'core/fares.html')

def vessels(request):
    user = request.user # Retrieve the logged-in user object

    return render(request, 'core/vessels.html')

def emergency(request):
    user = request.user # Retrieve the logged-in user object
    

    return render(request, 'core/emergency.html')

def emergencyctd(request):
    user = request.user # Retrieve the logged-in user object
    if request.method == 'POST':
        route = request.POST['Route']
        emergency_type= request.POST['emergencyType']
        date_occured = request.POST['dateOccured']
        age = request.POST['age'] or None
        gender = request.POST['gender'] or None
        comments = request.POST['comments']
        emergency_user = user if user.is_authenticated else None
        emergency=Emergency(user=emergency_user, route=route,emergency_type=emergency_type,date_occured=date_occured,age=age,gender=gender,comments=comments)
        emergency.save()
        
    context = {
        'username': user.username,
        
        # Add more user-related data as needed
    }
    if user.is_authenticated:
        context.update({
        'username': user.username,
        'email': user.email,
        'first_name': user.first_name,
        'last_name': user.last_name,
        # Add more user-related data as needed
    })
    
    return render(request, 'core/emergencyctd.html', context)

@login_required
def addschedule(request):
    user = request.user # Retrieve the logged-in user object
    if request.method == 'POST':
        day = request.POST['day']
        route = request.POST['route']
        vessel = request.POST['vessel']
        departure_time = request.POST['DepartureTime']
        time=datetime.strptime(departure_time, "%I:%M %p").time()
        schedule=Schedule( day=day,route=route,vessel=vessel,departure_time=time)
        schedule.save()

    context = {
        'username': user.username,
        'email': user.email,
        'first_name': user.first_name,
        'last_name': user.last_name,
        # Add more user-related data as needed
    }

    return render(request, 'core/addSchedule.html',context)

def viewtickets(request):
    user = request.user # Retrieve the logged-in user object
    
    # Retrieve tickets ordered by 'id' in descending order (newest first)
    tickets = Ticket.objects.order_by('-id')
    routes={
        'san_fernando_pos': 'San Fernando - POS',
        'pos_san_fernando': 'POS - San Fernando',
    }
    ticket_class={ #added ticket_class library
        'economy': 'Economy',
        'premium': 'Premium',
    }
    context = {
        'tickets': tickets,
        'routes':routes,
        'ticket_class':ticket_class, 
    }

    return render(request, 'core/viewTickets.html',context)

def viewemergency(request):
    user = request.user # Retrieve the logged-in user object
    emergencys = Emergency.objects.order_by('-id')
    routes={
        'san_fernando_pos': 'San Fernando - POS',
        'pos_san_fernando': 'POS - San Fernando',
    }
    emergency_type={
        'medical': 'Medical Emergency',
        'mechanical': 'Mechanical Emergency',
        'fire': 'Fire',
        'collision_grounding': 'Collision or Grounding',
        'man_overboard': 'Man Overboard',
    }

    gender={
        'male':'Male',
        'female':'Female',
        'other':'Other',
    }
    context = {
        'emergencys': emergencys,
        'routes':routes,
        'emergency_type':emergency_type,
        'gender':gender,
        # Add more user-related data as needed
    }
    

    return render(request, 'core/viewEmergency.html',context)

def loginRedirect(request):
    user = request.user # Retrieve the logged-in user object
    if user is not None:
        # User is authenticated, login the user
        
        # Redirect to a success page (e.g., home page)
        if user.is_staff:
            return redirect('addschedule')
        else:
            return redirect('index')  # Replace 'home' with your desired URL name
    else:
        # Authentication failed, show error message
        messages.error(request, 'Invalid username or password. Please try again.')
        return redirect('login')  # Redirect back to login page
    
@login_required    
def emerFreqRep(request):
    user = request.user # Retrieve the logged-in user object
    


    return render(request, 'core/emerFreqRep.html' )

def emerFreqRepCtd(request):
    user = request.user # Retrieve the logged-in user object
    context={}
    if request.method == 'POST':
        start_date= request.POST['start_date']
        end_date= request.POST['end_date']

        emergencies_within_range = Emergency.objects.filter(date_occured__gte=start_date, date_occured__lte=end_date)

        # Count occurrences of each emergency type using Django's aggregation
        emergency_counts = emergencies_within_range.values('emergency_type').annotate(count=Count('emergency_type'))

        # Create a Counter object to count occurrences of each emergency type
        type_counter = Counter({emergency['emergency_type']: emergency['count'] for emergency in emergency_counts})

        # Find the most common emergency type
        if type_counter:
            most_common_type = type_counter.most_common(1)[0][0]
        else:
            most_common_type = None  # Return None if no emergencies within the specified date range
        
        route_counts = emergencies_within_range.values('route').annotate(count=Count('route'))

        # Create a Counter object to count occurrences of each emergency type
        route_counter = Counter({emergency['route']: emergency['count'] for emergency in route_counts})

        # Find the most common route
        if route_counter:
            most_common_route = route_counter.most_common(1)[0][0]
        else:
            most_common_route = None  # Return None if no route within the specified date range

        gender_counts={
        'male':0,
        'female':0,
        'other':0,
    }
        for emergency in emergencies_within_range:
            if emergency.gender:
                gender_counts[emergency.gender]+=1 


        # Find the most common gender
        most_common_gender = max(gender_counts, key=gender_counts.get)

        age_ranges = [
        (0, 20),   # 0-20 years
        (21, 40),  # 21-40 years
        (41, 60),  # 41-60 years
        (61, None) # 61+ years
    ]

    # Count occurrences of age ranges
        age_range_counts = []
        for age_range in age_ranges:
            min_age, max_age = age_range
            if max_age:
                age_range_filter = {'age__gte': min_age, 'age__lte': max_age}
            else:
                age_range_filter = {'age__gte': min_age}
            count = emergencies_within_range.filter(**age_range_filter).count()
            age_range_counts.append({'age_range': f"{min_age}-{max_age if max_age else 'above'}", 'count': count})

        most_common_range = None
        max_count = 0

        # Iterate through age range counts to find the most common range
        for age_range in age_range_counts:
            count = age_range['count']
            if count > max_count:
                max_count = count
                most_common_range = age_range['age_range']

        gender={
        'male':'Male',
        'female':'Female',
        'other':'Other',
    }    
        EMERGENCY_TYPE_CHOICES = {
        'medical': 'Medical Emergency',
        'mechanical': 'Mechanical Emergency',
        'fire': 'Fire',
        'collision_grounding': 'Collision or Grounding',
        'man_overboard': 'Man Overboard',
    }
        routes={
        'san_fernando_pos': 'San Fernando - POS',
        'pos_san_fernando': 'POS - San Fernando',
    }
        context = {
        'start_date':start_date,
        'end_date': end_date,
        'most_common_type':EMERGENCY_TYPE_CHOICES[most_common_type] if most_common_type else most_common_type,
        'most_common_route':routes[most_common_route] if most_common_route else most_common_route,
        'most_common_gender':gender[most_common_gender] if most_common_gender else most_common_gender,
        'most_common_range':most_common_range,
        # Add more user-related data as needed
    }
    return render(request, 'core/emerFreqRepCtd.html',context)

@login_required
def revenueReport(request):
    user = request.user # Retrieve the logged-in user object

    return render(request, 'core/revenueReport.html')

def revenueReportCtd(request):
    user = request.user # Retrieve the logged-in user object
    context={}
    if request.method == 'POST':
        start_date= request.POST['start_date']
        end_date= request.POST['end_date']

        Tickets_within_range = Ticket.objects.filter(schedule_date__gte=start_date, schedule_date__lte=end_date)

        ticket_prices = {
        ('economy', 'one_way', 'adult'): 75.00,
        ('economy', 'return', 'adult'): 150.00,
        ('economy', 'one_way', 'teenage'): 50.00,
        ('economy', 'return', 'teenage'): 100.00,
        ('economy', 'one_way', 'infant'): 0.00,
        ('economy', 'return', 'infant'): 0.00,
        ('economy', 'one_way', 'elderly'): 25.00,
        ('economy', 'return', 'elderly'): 50.00,
        ('premium', 'one_way', 'adult'): 150.00,
        ('premium', 'return', 'adult'): 300.00,
        ('premium', 'one_way', 'teenage'): 100.00,
        ('premium', 'return', 'teenage'): 200.00,
        ('premium', 'one_way', 'infant'): 0.00,
        ('premium', 'return', 'infant'): 0.00,
        ('premium', 'one_way', 'elderly'): 150.00,
        ('premium', 'return', 'elderly'): 300.00,
    }

        # Initialize revenue dictionary
        context = {
            'adult': 0,
            'teenage': 0,
            'infant': 0,
            'elderly': 0,
        }

        # Calculate revenue using aggregate function
        for ticket_type, trip_type, passenger_type in ticket_prices:
            price = ticket_prices[(ticket_type, trip_type, passenger_type)]
            field_name = f"{passenger_type}_passengers"
            revenue = Ticket.objects.filter(ticket_class=ticket_type, trip=trip_type).aggregate(
                total_revenue=Sum(field_name)
            )['total_revenue'] or 0
            context[passenger_type] += revenue*price

        context['total']=sum(context.values())
    return render(request, 'core/revenueReportCtd.html', context)

@login_required
def passengerTraffic(request):
    user = request.user # Retrieve the logged-in user object

    return render(request, 'core/passengerTraffic.html')

def passengerTrafficCtd(request):
    user = request.user # Retrieve the logged-in user object
    context={}
    if request.method == 'POST':
        start_date= request.POST['start_date']
        end_date= request.POST['end_date']

        Tickets_within_range = Ticket.objects.filter(schedule_date__gte=start_date, schedule_date__lte=end_date)

        route_counts = Tickets_within_range.values('route').annotate(count=Count('route'))

            # Create a Counter object to count occurrences of each emergency type
        route_counter = Counter({ticket['route']: ticket['count'] for ticket in route_counts})

            # Find the most common route
        if route_counter:
            most_common_route = route_counter.most_common(1)[0][0]
            routes={
            'san_fernando_pos': 'San Fernando - POS',
            'pos_san_fernando': 'POS - San Fernando',
        }
        else:
            most_common_route = None  # Return None if no route within the specified date range

        passenger_counts = {
        'adults': Tickets_within_range.aggregate(total_adults=Sum('adult_passengers'))['total_adults'] or 0,
        'teenagers': Tickets_within_range.aggregate(total_teens=Sum('teenage_passengers'))['total_teens'] or 0,
        'infants': Tickets_within_range.aggregate(total_infants=Sum('infant_passengers'))['total_infants'] or 0,
        'elderly': Tickets_within_range.aggregate(total_elderly=Sum('elderly_passengers'))['total_elderly'] or 0,
    }
        
        passenger_types = {
        'adults': 'Adults',
        'teenagers':'Teenagers',
        'infants': 'Infant',
        'elderly': 'Elderly',
    }

        # Determine the most common passenger type based on counts
        most_common_passenger_type = max(passenger_counts, key=passenger_counts.get) 
        total_passengers = sum(passenger_counts.values())   
            
        context = {
            'start_date':start_date,
            'end_date': end_date,
            'most_common_passenger_type':passenger_types[most_common_passenger_type],
            'total_passengers':total_passengers,
            'most_common_route':routes[most_common_route] if most_common_route else most_common_route,
            
            # Add more user-related data as needed
        }


    return render(request, 'core/passengerTrafficCtd.html',context)


@login_required
def addStaff(request):
    user = request.user # Retrieve the logged-in user object
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        address = request.POST['address']
        phone = request.POST['phone']
        age = request.POST['age']
        date_of_birth = request.POST['date_of_birth']
        gender = request.POST['gender']
        email = request.POST['email']

        # Create User with first_name and last_name
        user = User.objects.create_user(username=username, password=password, email=email, first_name=first_name, last_name=last_name, is_staff=True)
        
        # Create UserProfile
        UserProfile.objects.create(user=user, address=address, phone=phone, age=age, date_of_birth=date_of_birth, gender=gender)

    return render(request, 'core/addStaff.html')

