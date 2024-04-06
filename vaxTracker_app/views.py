from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import DoctorModel, FamilyMemberModel, FamilyModel, UserModel
from django.contrib.auth.hashers import make_password
import uuid
import requests

def index(request):
    doctors = DoctorModel.objects.all()
    families = FamilyModel.objects.all()
    total_families = FamilyModel.objects.count()
    total_vaccinated_people = FamilyMemberModel.objects.filter(vaccination_status=True).count()
    total_vaccinated_people = total_vaccinated_people - 1
    total_doctors = DoctorModel.objects.count()
    total_adults = FamilyMemberModel.objects.filter(age__gt=18).count()
    total_infants = FamilyMemberModel.objects.filter(age__lte=2).count()
    total_unvaccinated_people = (total_adults + total_infants) - total_vaccinated_people
    context = {
        'total_families': total_families,
        'total_vaccinated_people': total_vaccinated_people,
        'total_unvaccinated_people': total_unvaccinated_people,
        'total_doctors': total_doctors,
        'doctors': doctors, 
        'families':families,
        'total_adults': total_adults,
        'total_infants': total_infants,
    }

    return render(request, 'index.html', context)

def elements(request):
    return render(request, 'element.html')


def add_doctors(request): 
    if request.method == 'POST': 
        password = make_password(request.POST.get('password'))
        email = request.POST.get('email')
        role = request.POST.get('role')
        name = request.POST.get('name') 
        username = request.POST.get('name') 
        phone_number = request.POST.get('phone_number') 
        address = request.POST.get('address') 
        post = request.POST.get('post') 
        specialization = request.POST.get('specialization') 

        try:
            user = UserModel.objects.create(
                username = username,
                password=password,
                email=email,
                role=role
            )

            doctor = DoctorModel.objects.create(
                name=name,
                phone_number=phone_number,
                address=address,
                post=post,
                specialization=specialization
            )
            doctor.save()

            user.save()

            messages.success(request, 'Doctor added successfully!')
            return redirect('/')
        except Exception as e:
            messages.error(request, f'Doctor Added!')
            return redirect('/')
    else:
        return render(request, 'add-doctors.html')




def add_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')
        role = request.POST.get('role')

        user = UserModel.objects.create(
            username=username,
            password=password,
            email=email,
            role=role
        )
        user.save()

        return redirect('/')
    else:
        return render(request, 'add_user.html')


def add_family(request):
    doctors = DoctorModel.objects.all()

    if request.method == 'POST':
        address = request.POST.get('address')
        doctor_assigned = request.POST.get('doctor_assigned')
        total_people = request.POST.get('totalMembers')

        # Create a FamilyModel instance
        family = FamilyModel.objects.create(
            address=address,
            doctor_assigned=doctor_assigned,
            total_people=total_people,
            total_vaccinated=0,
            total_adults=0,
            total_infants=0
        )

        # Create JSON payload
        payload = {
            'address': family.address,
            'doctor_assigned': family.doctor_assigned,
            'total_people': family.total_people,
            'total_vaccinated': family.total_vaccinated,
            'total_adults': family.total_adults,
            'total_infants': family.total_infants
        }

        # Send data to endpoint with custom header
        endpoint = "your api endpoint"
        headers = {
            'Content-Type': 'application/json',
            'X-Cassandra-Token': 'your_cassandra_token_here'  # Replace 'your_cassandra_token_here' with your actual token
        }
        
        try:
            response = requests.post(endpoint, json=payload, headers=headers)
            response.raise_for_status()  # Raise exception for HTTP errors
            messages.success(request, "Family Added successfully! Please add the members now!")
            return redirect('add-family-members', family_id=family.house_id)
        except requests.exceptions.RequestException as e:
            messages.error(request, f"Failed to send data to endpoint: {e}")
            return redirect('add-family')

    context = {'doctors': doctors}
    return render(request, 'add-family.html', context)


def add_family_members(request, family_id):
    family = get_object_or_404(FamilyModel, house_id=family_id)

    if request.method == 'POST':
        member_name = request.POST.get('member_name')
        member_age = request.POST.get('member_age')
        member_gender = request.POST.get('member_gender')
        member_vaccination_status = request.POST.get('member_vaccination_status')
        member_vaccine_received = request.POST.get('member_vaccine_received')

        FamilyMemberModel.objects.create(
            house_id=family_id,
            name=member_name,
            age=member_age,
            gender=member_gender,
            vaccination_status=member_vaccination_status,
            vaccine_received=member_vaccine_received
        )

        messages.success(request, "Family member added successfully!")
        return redirect('add-family-members', family_id=family.house_id)

    members = FamilyMemberModel.objects.filter(house_id=family_id)
    context = {'family': family, 'members': members}
    return render(request, 'add-family-members.html', context)


def delete_member(request, member_id):
    member = FamilyMemberModel.objects.get(member_id=member_id)
    member.delete()
    messages.success(request, 'Member deleted successfully!')
    return redirect('add-family-members', family_id=member.house_id)

def delete_doctor(request, user_id):
    doctor = UserModel.objects.get(user_id=user_id)
    doctor.delete()
    messages.success(request, 'Doctor deleted successfully!')
    return redirect('/')

def edit_member(request, member_id):
    family = FamilyModel.objects.all()
    member = FamilyMemberModel.objects.get(member_id=member_id)

    if request.method == 'POST':
        member.name = request.POST.get('member_name')
        member.gender = request.POST.get('member_gender')
        member.age = request.POST.get('member_age')
        member.vaccination_status = 'on' if request.POST.get('member_vaccination_status') == 'on' else 'off'
        member.vaccine_received = request.POST.get('member_vaccine_received')

        member.save()
        messages.success(request, "Member Edited Successfully!")
        return redirect('/')

    return render(request, 'edit-member.html', {'member': member, 'family': family})

def delete_family(request, family_id):
    family = FamilyModel.objects.get(house_id=family_id)
    family.delete()
    messages.success(request, 'Family deleted successfully!')
    return redirect('/') 

def edit_family(request, family_id):
    family = FamilyModel.objects.get(house_id=family_id)
    doctors = DoctorModel.objects.all()

    if request.method == 'POST':
        family.address = request.POST.get('address')
        family.doctor_assigned = request.POST.get('doctor_assigned')
        family.total_people = request.POST.get('totalMembers')
        family.total_vaccinated=0
        family.total_adults=0
        family.total_infants=0

        family.save()
        messages.success(request, "Member Edited Successfully!")
        return redirect('/')

    return render(request, 'edit-family.html', {'family': family, 'doctors': doctors})