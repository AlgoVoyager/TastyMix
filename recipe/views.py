from django.shortcuts import *
from .models import *
from django.contrib.auth import authenticate, login,logout
from django.contrib import messages

# Create your views here.
def recipes(request):
    if request.method == "POST":
        print("post request")
        data = request.POST
        user= request.user
        recipe_name = data.get('recipe_name')
        Ingredients = data.get('Ingredients')
        recipe_image = request.FILES.get('recipe_image')
        print(recipe_name, Ingredients, recipe_image)

        Recipe.objects.create(
            user=user,
            recipe_image=recipe_image,
            recipe_name=recipe_name,
            Ingredients=Ingredients,
        )
        return redirect('/recipe')

    queryset = Recipe.objects.all()
    if request.GET.get("search"):
        queryset=queryset.filter(recipe_name__icontains=request.GET.get('search'))

    context = {'recipes': queryset}
    return render(request, "recipe.html", context)

def update_recipe(request,id):
    queryset=Recipe.objects.get(id=id)
    if request.method=="POST":
        data = request.POST
        recipe_name = data.get('recipe_name')
        Ingredients = data.get('Ingredients')
        recipe_image = request.FILES.get('recipe_image')

        queryset.recipe_name=recipe_name
        queryset.Ingredients=Ingredients

        if recipe_image:
            queryset.recipe_image=recipe_image
        queryset.save()
        return redirect('/recipe')

    context={'recipe':queryset}
    return render(request,'update_recipe.html',context)
def delete_recipe(request,id):
    queryset= Recipe.objects.get(id=id)
    queryset.delete()
    return redirect('/recipe')

def index(request):
    return render(request, "index.html")

def profile(request,id):
    print("viewing Profile id : ",id)
    queryset = Recipe.objects.all()
    queryset = queryset.filter(user_id=id)
    if request.GET.get("search"):
        queryset=queryset.filter(recipe_name__icontains=request.GET.get('search'))
    context = {'recipes': queryset}
    return render(request, "profile.html", context)

def auth(request):

    return render(request,'auth.html')


def signin(request):

    if request.method=='POST':
        username= request.POST.get('username')
        password= request.POST.get('password')

        if not User.objects.filter(username=username):
            messages.error(request,"Username Doesn't Exist.")
            return redirect('/auth/')

        user= authenticate(username=username,password=password)

        if user is None:
            messages.error(request,"Username or password Invalid.")
            return redirect('/auth/')
        else:
            login(request,user)
            return redirect('/recipe/')
    return redirect('/auth/')

def signup(request):
    if request.method=="POST":
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email=request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = User.objects.filter(username=username)

        if user.exists():
            messages.add_message(request, messages.WARNING, 'Username Already Exists...')
            return redirect('/auth/')

        user = User.objects.create(
            first_name=first_name,
            last_name=last_name,
            username=username,
            email=email
        )

        user.set_password(password)
        user.save()
        messages.add_message(request, messages.SUCCESS, 'Account Created Succesfully.')
        return redirect('/auth/')
    return render(request,'auth.html')

def signout(request):
    logout(request)
    return redirect('/auth/')