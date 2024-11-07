from django.shortcuts import render, redirect
from .forms import FavoriteLocationForm

def add_favorite_location(request):
    if request.method == 'POST':
        form = FavoriteLocationForm(request.POST)
        if form.is_valid():
            favorite_location = form.save(commit=False)
            favorite_location.user = request.user  # Associate with the logged-in user
            favorite_location.save()
            return redirect('favorites_list')  # Redirect to a list of favorite locations or any other page
    else:
        form = FavoriteLocationForm()
    return render(request, 'favorites/add_favorite_location.html', {'form': form})
