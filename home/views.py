from django.contrib.auth import get_user_model, authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.shortcuts import render, HttpResponse, redirect

from property.models import Property
from general.models import Contact, Testimonial
from account.models import Response, Subscription,User

User = get_user_model()

# Create your views here.

def index (request):
    testimonials = Testimonial.objects.all()
    context = {
        "testimonials": testimonials,
    }
    return render(request, 'index.html', context)

def about(request):
    return render(request, 'about1.html')

def conditions(request):
    return render(request, 'conditions.html')


def contact(request):
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        message = request.POST.get('message')
        contact = Contact(name=name, email=email, phone=phone, message=message)
        contact.save()
        messages.success(request, "Your message has been sent successfully")
        return redirect('contact')
    return render(request, 'contact1.html')

def gallery_details(request, uuid):
    try:
        prop = Property.objects.get(uuid=uuid)
        return render(request, 'gallery_details.html', {"prop": prop})
    except Exception as e:
        print(e)
        return HttpResponse("Something went wrong")
    

def gallery_detailsgirls(request):
    return render(request, 'gallery_detailsfor girls.html')

def ownerquery(request, uuid):
    try:
        prop = Property.objects.get(uuid=uuid)
        if prop:
            context = {
                "name": prop.user.name,
                "phone": prop.user.phone_number,
            }
    except:
        return HttpResponse("Something went wrong")
    return render(request, 'owner_pohone_form.html', context)

@login_required
def ownerremainings(request):
    return render(request, 'owner_remaining.html')

def Register(request):
    if request.method=='POST':
        if request.POST.get('fname')=="":
            return render (request,"register.html",{'error':'Please Enter your first_name'})
        elif request.POST.get('lname')=="":
            return render (request,"register.html",{'error':'Please Enter your last_name'})
        elif request.POST.get('email')=="":
            return render (request,"register.html",{'error':'Please Enter your email'}) 
        elif request.POST.get('phone')=="":
            return render (request,"register.html",{'error':'Invalid Contact Number'})
        elif request.POST.get('password')=="":
            return render (request,"register.html",{'error':'Please enter your Password'})
        elif request.POST.get('cpassword')=="":
            return render (request,"register.html",{'error':'Please enter your Confirm password'})
        first_name=request.POST.get('fname')
        last_name=request.POST.get('lname')
        email=request.POST.get('email')
        phone_number=request.POST.get('phone')
        password=request.POST.get('password')
        cpassword=request.POST.get('cpassword')
        property_type = request.POST.get('property_type')
        value={
            'fname':first_name,
            'lname':last_name,
            'email':email,
            'phone':phone_number,
        }

        if password==cpassword:
            # new = User(first_name=first_name, email=email, last_name=last_name, phone_number=phone_number,
            #         password=password,cpassword=cpassword)
            user = User.objects.create_user(username=email, email=email, password=password)
            user.save()
            user.first_name = first_name
            user.last_name = last_name
            user.phone_number = phone_number
            user.save()
            property = Property(user=user, property_ad_type=property_type)
            property.save()
            return redirect("ursroom_Details", uuid=property.uuid)
            
        else:
            data= {   
                    'values':value,
                  }
            messages.error(request, "Please Password & Confirm Password not Match")
            return render(request,'register.html',data)

    return render(request,'register.html')

def ownerdetails(request):
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        property_type = request.POST.get('property_type')
        try:
            user = User.objects.create_user(username=email, email=email, phone=phone)
            user.save()
            user.name = name
            user.phone_number = phone
            user.save()
            property = Property(user=user, property_ad_type=property_type)
            property.save()
            return redirect("ursroom_Details", uuid=property.uuid)
        except Exception as e:
            messages.error(request, "Property with this email id already exists! Please use another email.")
    return render(request, 'owner-detail-part.html')

def privacy(request):
    return render(request, 'policy.html')

def propertypost(request):
    return render(request, 'property-post.html')

def ursLocationDetails(request, uuid):
    try:
        prop = Property.objects.get(uuid=uuid)
        if prop:
            if request.method == "POST":
                city = request.POST.get('city')
                locality = request.POST.get('locality')
                landmark = request.POST.get('landmark')
                pg_name = request.POST.get('pg_name')
                available_date = request.POST.get('available_date')
                pg_available_for = request.POST.get('pg_available_for')
                preferred_tenants = request.POST.get('preferred_tenants')
                latitude = request.POST.get('latitude')
                longitude = request.POST.get('longitude')
                food_included = True if request.POST.get('food_included') else False
                food_included_details = []
                gate_closing_time = request.POST.get('gate_closing_time')
                pg_other_details = []
                pg_other_rules = request.POST.get('pg_other_rules').strip()
                if request.POST.get('food_included_breakfast') == "on":
                    food_included_details.append('Breakfast')
                if request.POST.get('food_included_lunch') == "on":
                    food_included_details.append('Lunch')
                if request.POST.get('food_included_dinner') == "on":
                    food_included_details.append('Dinner')
                if request.POST.get('pg_other_details_smoking') == "on": 
                    pg_other_details.append('No Smoking')
                if request.POST.get('pg_other_details_guardian') == "on":
                    pg_other_details.append('No Guardian')
                if request.POST.get('pg_other_details_drinking') == "on":
                    pg_other_details.append('No Drinking')
                if request.POST.get('pg_other_details_girls_entry') == "on":
                    pg_other_details.append("No Girls Entry")
                if request.POST.get('pg_other_details_non_veg') == "on":
                    pg_other_details.append("No Non-Veg")
                prop.city = city
                prop.locality = locality
                prop.landmark = landmark
                prop.pg_name = pg_name
                prop.pg_available_for = pg_available_for
                prop.preferred_tenants = preferred_tenants
                prop.available_date = available_date
                prop.food_included = food_included
                prop.food_included_details = food_included_details
                prop.gate_closing_time = gate_closing_time if gate_closing_time else None
                prop.pg_other_details = pg_other_details
                prop.pg_other_rules = pg_other_rules
                if latitude != "":
                    prop.latitude = latitude
                if longitude != "":
                    prop.longitude = longitude
                prop.save()
                return redirect("ursroom_aminities_details", uuid=prop.uuid)
            elif request.method == "GET":
                return render(request, 'URS location details.html', {"prop": prop})
            return render(request, 'URS location details.html')
        else:
            return HttpResponse("Something went wrong")
    except Exception as e:
        print(e)
        return HttpResponse("Something went wrong!!!!")

def ursroom_Details(request, uuid):
    try:
        prop = Property.objects.get(uuid=uuid)
        if prop:
            if request.method == "POST":
                single_room = True if request.POST.get('single_room') == "on" else False
                double_room = True if request.POST.get('double_room') == "on" else False
                triple_room = True if request.POST.get('triple_room') == "on" else False
                four_room = True if request.POST.get('four_room') == "on" else False
                single_room_expected_rent = int(request.POST.get('single_room_expected_rent')) if request.POST.get('single_room_expected_rent') else 0
                double_room_expected_rent = int(request.POST.get('double_room_expected_rent')) if request.POST.get('double_room_expected_rent') else 0
                triple_room_expected_rent = int(request.POST.get('triple_room_expected_rent')) if request.POST.get('triple_room_expected_rent') else 0
                four_room_expected_rent = int(request.POST.get('four_room_expected_rent')) if request.POST.get('four_room_expected_rent') else 0
                single_room_deposit_rent = int(request.POST.get('single_room_deposit_rent')) if request.POST.get('single_room_deposit_rent') else 0
                double_room_deposit_rent = int(request.POST.get('double_room_deposit_rent')) if request.POST.get('double_room_deposit_rent') else 0
                triple_room_deposit_rent = int(request.POST.get('triple_room_deposit_rent')) if request.POST.get('triple_room_deposit_rent') else 0
                four_room_deposit_rent = int(request.POST.get('four_room_deposit_rent')) if request.POST.get('four_room_deposit_rent') else 0
                single_room_extra_features = []
                double_room_extra_features = []
                triple_room_extra_features = []
                four_room_extra_features = []
                if request.POST.get('single_room_cupboard') == "on":
                    single_room_extra_features.append("Cupboard")
                if request.POST.get('single_room_tv') == "on":
                    single_room_extra_features.append("TV")
                if request.POST.get('single_room_bedding') == "on":
                    single_room_extra_features.append("Bedding")
                if request.POST.get('single_room_ac') == "on":
                    single_room_extra_features.append("AC")
                if request.POST.get('single_room_geyser') == "on":
                    single_room_extra_features.append("Geyser")
                if request.POST.get('single_room_attached_bathroom') == "on":
                    single_room_extra_features.append("Attached Bathroom")
                if request.POST.get('double_room_cupboard') == "on":
                    double_room_extra_features.append("Cupboard")
                if request.POST.get('double_room_tv') == "on":
                    double_room_extra_features.append("TV")
                if request.POST.get('double_room_bedding') == "on":
                    double_room_extra_features.append("Bedding")
                if request.POST.get('double_room_ac') == "on":
                    double_room_extra_features.append("AC")
                if request.POST.get('double_room_geyser') == "on":
                    double_room_extra_features.append("Geyser")
                if request.POST.get('double_room_attached_bathroom') == "on":
                    double_room_extra_features.append("Attached Bathroom")
                if request.POST.get('triple_room_cupboard') == "on":
                    triple_room_extra_features.append("Cupboard")
                if request.POST.get('triple_room_tv') == "on":
                    triple_room_extra_features.append("TV")
                if request.POST.get('triple_room_bedding') == "on":
                    triple_room_extra_features.append("Bedding")
                if request.POST.get('triple_room_ac') == "on":
                    triple_room_extra_features.append("AC")
                if request.POST.get('triple_room_geyser') == "on":
                    triple_room_extra_features.append("Geyser")
                if request.POST.get('triple_room_attached_bathroom') == "on":
                    triple_room_extra_features.append("Attached Bathroom")
                if request.POST.get('four_room_cupboard') == "on":
                    four_room_extra_features.append("Cupboard")
                if request.POST.get('four_room_tv') == "on":
                    four_room_extra_features.append("TV")
                if request.POST.get('four_room_bedding') == "on":
                    four_room_extra_features.append("Bedding")
                if request.POST.get('four_room_ac') == "on":
                    four_room_extra_features.append("AC")
                if request.POST.get('four_room_geyser') == "on":
                    four_room_extra_features.append("Geyser")
                if request.POST.get('four_room_attached_bathroom') == "on":
                    four_room_extra_features.append("Attached Bathroom")
                prop.single_room = single_room
                prop.double_room = double_room
                prop.triple_room = triple_room
                prop.four_room = four_room
                prop.single_room_expected_rent = single_room_expected_rent
                prop.double_room_expected_rent = double_room_expected_rent
                prop.triple_room_expected_rent = triple_room_expected_rent
                prop.four_room_expected_rent = four_room_expected_rent
                prop.single_room_deposit_rent = single_room_deposit_rent
                prop.double_room_deposit_rent = double_room_deposit_rent
                prop.triple_room_deposit_rent = triple_room_deposit_rent
                prop.four_room_deposit_rent = four_room_deposit_rent
                prop.single_room_extra_features = single_room_extra_features
                prop.double_room_extra_features = double_room_extra_features
                prop.triple_room_extra_features = triple_room_extra_features
                prop.four_room_extra_features = four_room_extra_features
                prop.save()
                return redirect("ursLocationDetails", uuid=prop.uuid)
            elif request.method == "GET":
                return render(request, 'URS room details.html', {"prop": prop})
            return render(request, 'URS room details.html')
        else:
            return HttpResponse("Something went wrong")
    except Exception as e:
        print(e)
        return HttpResponse("Something went wrong!!!!")

def ursroom_details_share(request):
    city = request.GET.get('city')
    preferred_tenants = request.GET.get('preferred_tenants')
    pg_name = request.GET.get('pg_name')
    occupancy = request.GET.get('occupancy')
    gender = request.GET.get('gender')
    budget = request.GET.get('budget')
    tenants = request.GET.get('tenants')
    food = request.GET.get('food')
    for_whom = "All PGs"
    single_room = True if occupancy == "single_room" else False
    double_room = True if occupancy == "double_room" else False
    triple_room = True if occupancy == "triple_room" else False
    four_room = True if occupancy == "four_room" else False

    if city and not preferred_tenants and not pg_name:
        prop = Property.objects.filter(city=city, active=True)
        for_whom = city
    elif not city and preferred_tenants and not pg_name:
        prop = Property.objects.filter(preferred_tenants=preferred_tenants, active=True)
        for_whom = preferred_tenants
    elif not city and not preferred_tenants and pg_name:
        prop = Property.objects.filter(
            Q(city__icontains=pg_name) |
            Q(locality__icontains=pg_name) |
            Q(landmark__icontains=pg_name) |
            Q(pg_name__icontains=pg_name),
            active=True
        )
        for_whom = pg_name
    elif city and not preferred_tenants and pg_name:
        prop = Property.objects.filter(
            Q(city__icontains=pg_name) |
            Q(locality__icontains=pg_name) |
            Q(landmark__icontains=pg_name) |
            Q(pg_name__icontains=pg_name),
            city=city,
            active=True)
        for_whom = pg_name + " in " + city
    else:
        prop = Property.objects.filter(active=True)

    if occupancy is not None:
        if single_room:
            prop = prop.filter(single_room=True)
        elif double_room:
            prop = prop.filter(double_room=True)
        elif triple_room:
            prop = prop.filter(triple_room=True)
        elif four_room:
            prop = prop.filter(four_room=True)
    if gender is not None:
        prop = prop.filter(pg_available_for=gender)
    if tenants is not None:
        prop = prop.filter(preferred_tenants=tenants)
    if budget is not None:
        budget = int(budget)
        res = Property.objects.none()
        for pr in prop:
            if pr.min_amount["amount"] <= budget:
                res = res | Property.objects.filter(uuid=pr.uuid)
        prop = res
    if food is not None:
        res = Property.objects.none()
        for pr in prop:
            if food in pr.food_included_details:
                res = res | Property.objects.filter(uuid=pr.uuid)
        prop = res
    prop = prop.order_by(
        '-user__subscription__price',
        '-created_at'
    )
    return render(request, 'URS room details share.html', {'properties': prop, "for_whom": for_whom})

def ursroom_boys(request):
    return render(request, 'URS room for boy.html')

def ursroom_girls(request):
    return render(request, 'URS room for girl.html')

def ursroom_professional(request):
    return render(request, 'URS room for professional.html')

def ursroom_student(request):
    return render(request, 'URS room for student.html')

def ursroom_aminities_details(request, uuid):
    try:
        prop = Property.objects.get(uuid=uuid)
        if prop:
            if request.method == "POST":
                laundry = True if request.POST.get('laundry') else False
                worden = True if request.POST.get('worden') else False
                room_cleaning = True if request.POST.get('room_cleaning') else False
                parking = request.POST.get('parking')
                pg_amenities = []
                images = request.FILES.getlist('property_images')
                if len(images) == 1:
                    prop.image_1 = images[0]
                elif len(images) == 2:
                    prop.image_1 = images[0]
                    prop.image_2 = images[1]
                elif len(images) == 3:
                    prop.image_1 = images[0]
                    prop.image_2 = images[1]
                    prop.image_3 = images[2]
                elif len(images) == 4:
                    prop.image_1 = images[0]
                    prop.image_2 = images[1]
                    prop.image_3 = images[2]
                    prop.image_4 = images[3]
                elif len(images) == 5:
                    prop.image_1 = images[0]
                    prop.image_2 = images[1]
                    prop.image_3 = images[2]
                    prop.image_4 = images[3]
                    prop.image_5 = images[4]
                elif len(images) == 6:
                    prop.image_1 = images[0]
                    prop.image_2 = images[1]
                    prop.image_3 = images[2]
                    prop.image_4 = images[3]
                    prop.image_5 = images[4]
                    prop.image_6 = images[5]
                elif len(images) == 7:
                    prop.image_1 = images[0]
                    prop.image_2 = images[1]
                    prop.image_3 = images[2]
                    prop.image_4 = images[3]
                    prop.image_5 = images[4]
                    prop.image_6 = images[5]
                    prop.image_7 = images[6]
                elif len(images) == 8:
                    prop.image_1 = images[0]
                    prop.image_2 = images[1]
                    prop.image_3 = images[2]
                    prop.image_4 = images[3]
                    prop.image_5 = images[4]
                    prop.image_6 = images[5]
                    prop.image_7 = images[6]
                    prop.image_8 = images[7]
                elif len(images) == 9:
                    prop.image_1 = images[0]
                    prop.image_2 = images[1]
                    prop.image_3 = images[2]
                    prop.image_4 = images[3]
                    prop.image_5 = images[4]
                    prop.image_6 = images[5]
                    prop.image_7 = images[6]
                    prop.image_8 = images[7]
                    prop.image_9 = images[8]
                property_description = request.POST.get('property_description')
                if request.POST.get('wifi') == "on":
                    pg_amenities.append('wifi')
                if request.POST.get('common_tv') == "on":
                    pg_amenities.append('common tv')
                if request.POST.get('lift') == "on":
                    pg_amenities.append('lift')
                if request.POST.get('power_backup') == "on": 
                    pg_amenities.append('power backup')
                if request.POST.get('mess') == "on":
                    pg_amenities.append('mess')
                if request.POST.get('refrigerator') == "on":
                    pg_amenities.append('refrigerator')
                if request.POST.get('no_girls_entry') == "on":
                    pg_amenities.append("No girls Entry")
                if request.POST.get('no_boys_entry') == "on":
                    pg_amenities.append("No boys Entry")
                if request.POST.get('no_non_veg') == "on":
                    pg_amenities.append("No non-veg")
                prop.laundry = laundry
                prop.worden = worden
                prop.room_cleaning = room_cleaning
                prop.parking = parking
                prop.pg_amenities = pg_amenities
                prop.property_description = property_description
                prop.save()
                return redirect("ursroom_personal_details")
            elif request.method == "GET":
                images = []
                if prop.image_1:
                    images.append(prop.image_1)
                if prop.image_2:
                    images.append(prop.image_2)
                if prop.image_3:
                    images.append(prop.image_3)
                if prop.image_4:
                    images.append(prop.image_4)
                if prop.image_5:
                    images.append(prop.image_5)
                if prop.image_6:
                    images.append(prop.image_6)
                if prop.image_7:
                    images.append(prop.image_7)
                if prop.image_8:
                    images.append(prop.image_8)
                if prop.image_9:
                    images.append(prop.image_9)
                return render(request, 'URS-aminities-details.html', {"prop": prop, "images": images})
            return render(request, 'URS-aminities-details.html')
        else:
            return HttpResponse("Something went wrong")
    except Exception as e:
        print(e)
        return HttpResponse("Something went wrong!!!!")

def ursroom_personal_details(request):
    return render(request, 'URS-Personal-details-submited.html')

def ursroom_room_user_login(request):
    if request.user.is_authenticated:
        return redirect('ursroom_room_user_profile')
    else:
        if request.method == "POST":
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('ursroom_room_user_profile')
            else:
                messages.info(request, 'Username OR password is incorrect')
    return render(request, 'login.html')

def ursroom_room_user_profile(request):
    responses = Response.objects.filter(user=request.user)
    return render(request, 'URS_Room_User_profile.html', {'responses': responses})

def ursroom_room_user_subscription(request):
    subs = Subscription.objects.filter(active=True)
    return render(request, 'URS_Room_User_subscription_package.html', {'subs': subs})


def store_response(request):
    if request.method == "POST":
        data = request.POST
        name = data.get('name')
        email = data.get('email')
        phone = data.get('phone')
        user = data.get('user')
        prop = data.get('prop')
        u = User.objects.get(id=user) 
        p = Property.objects.get(uuid=prop)
        response = Response(name=name, email=email, phone=phone, user=u, property=p)
        response.save()
        u.responses = u.responses - 1
        u.save()
        return redirect('owner_pohone_form', uuid=p.uuid)
    return HttpResponse("Method not allowed", status=405)

def user_logout(request):
    if request.user.is_authenticated:
        logout(request)
        return redirect('home')
