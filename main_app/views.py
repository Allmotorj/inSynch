from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.views.generic.edit import CreateView, UpdateView
from .models import Song



# Define the home view
def home(request):
  return render(request, 'home.html')

@login_required
def about(request):
  return render(request, 'about.html')

class SongCreate(CreateView):
  model = Song
  fields = ['name', 'band', 'mood']
  
  
  def form_valid(self, form):
    form.instance.posted_by = self.request.user
    # return super().form_valid(form)
    return redirect('mood', mood=form.instance.mood)

def songs_mood(request, mood):
  songs = Song.objects.filter(mood=mood)
  print(songs)
  return render(request, 'index.html', { 'songs': songs , 'mood': mood })

class SongUpdate(UpdateView):
  model = Song
  fields = ['name', 'band', 'mood']


def accounts(request):
  return render(request, 'registration/login.html')

def signup(request):
  error_message = ''
  if request.method == 'POST':
    # This is how to create a 'user' form object
    # that includes the data from the browser
    form = UserCreationForm(request.POST)
    if form.is_valid():
      # This will add the user to the database
      user = form.save()
      # This is how we log a user in via code
      login(request, user)
      return redirect('about')
    else:
      error_message = 'Invalid sign up - try again!'
  # A bad POST or a GET request, so render signup.html with an empty form
  form = UserCreationForm()
  context = {'form': form, 'error_message': error_message}
  return render(request, 'registration/signup.html', context)    