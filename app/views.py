from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from .models import Department, Course, Uploader, Resource, Comment
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth import login as django_login
from django.contrib.auth import logout as django_logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages

# Create your views here.


def index(request):
    departments = Department.objects.all()
    params = {'departments': departments}
    return render(request, 'app/index.html', params)


def dept(request, DName):

    departments = Department.objects.all()
    params = {'departments': departments}

    department = Department.objects.filter(DName=DName)[0]
    courses = Course.objects.filter(DCode=department.DCode)

    crs = False

    if(courses):
        crs = True
    else:
        crs = False

    return render(request, 'app/department.html', {'department': department, 'courses': courses, 'departments': departments, 'crs': crs})


def Crs(request, CCode):

    departments = Department.objects.all()
    params = {'departments': departments}

    course = Course.objects.filter(CCode=CCode)
    resources = Resource.objects.filter(CCode=CCode)

    rs = True

    if(resources):
        rs = True
    else:
        rs = False

    return render(request, 'app/course.html', {'course': course[0], 'resources': resources, 'departments': departments, 'rs': rs})


def signup(request):
    if (request.method == 'POST'):

        username = request.POST['username']
        firstname = request.POST['firstname']
        lastname = request.POST['lastname']
        email = request.POST['email']
        password = request.POST['password']
        cnfpassword = request.POST['cnfpassword']

        users = User.objects.filter(username=username)

        f = 0

        if(users):
            f = 1

        emails = User.objects.filter(email=email)

        if(emails):
            f = 2

        if cnfpassword == password:

            if(f == 0):

                user = User.objects.create_user(username, email, password)
                user.firstname = firstname
                user.lastname = lastname
                user.save()

                django_login(request, user)

                messages.success(request, 'Successfully Logged In')
                return redirect("/")

            elif(f == 1):

                messages.error(
                    request, 'Username already exists please enter a different username')
                return redirect("/")

            else:
                messages.error(
                    request, 'Email already registered Please enter a different Email Address')
                return redirect("/")

        else:
            messages.error(
                request, 'Password and Confirm Password Fields should match')
            return redirect("/")


def login(request):
    if (request.method == 'POST'):
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)

        if user:
            django_login(request, user)
            messages.success(request, 'Successfully Logged In')
        else:
            messages.error(
                request, 'Wrong username or password')

        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required
def logout(request):

    django_logout(request)
    messages.success(request, "Successfully Logged Out")
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def uploader(request, CCode):
    if request.method == "POST":

        rname = request.POST['rname']
        rdes = request.POST['rdes']
        username = request.POST['username']
        password = request.POST['password']

        user = request.user

        if user.is_authenticated:

            if username == user.username:

                user = authenticate(username=username, password=password)

                if user:

                    course = Course.objects.filter(CCode=CCode)[0]

                    uploader = Uploader.objects.filter(UName=username)

                    if uploader:

                        resource = Resource(RName=rname, RDes=rdes, CCode=course,
                                            UNumber=uploader[0], filepath=request.FILES['file1'])

                        resource.save()

                    else:
                        upload = Uploader(UName=username)
                        upload.save()

                        resource = Resource(RName=rname, RDes=rdes, CCode=course,
                                            UNumber=upload, filepath=request.FILES['file1'])

                        resource.save()

                    messages.success(request, "Resource Successfully Uploaded")

                    return redirect(request.META.get('HTTP_REFERER'))

                else:
                    messages.error(
                        request, 'Wrong password')

                    return redirect(request.META.get('HTTP_REFERER'))
            else:
                messages.error(
                    request, 'Please Enter Valid Username')
                return redirect(request.META.get('HTTP_REFERER'))

        else:
            messages.error(
                request, 'First Login to Upload Resource')
            return redirect(request.META.get('HTTP_REFERER'))


def contact(request):

    departments = Department.objects.all()

    return render(request, 'app/contact.html', {'departments': departments})


def feedback(request):
    if request.method == "POST":

        Name = request.POST['name']
        Email = request.POST['email']
        Subject = request.POST['subject']
        Feedback = request.POST['feedback']

        comment = Comment(Name=Name, Email=Email,
                          Subject=Subject, Feedback=Feedback)

        comment.save()

        messages.success(request, "FeedBack Submitted")

        return redirect(request.META.get('HTTP_REFERER'))
