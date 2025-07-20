from django.http import HttpResponse
from django.shortcuts import redirect

def unauthenticated_user(view_func):
	def wrapper_func(request, *args, **kwargs):
		if request.user.is_authenticated:
			return redirect('home')
		else:
			return view_func(request, *args, **kwargs)

	return wrapper_func

def allowed_users(allowed_roles=[]):
	def decorator(view_func):
		def wrapper_func(request, *args, **kwargs):

			group = None
			if request.user.groups.exists():
				group = request.user.groups.all()[0].name

			if group in allowed_roles:
				print ('létező és elfogadott group')
				print(group)
				print(allowed_roles)
				return view_func(request, *args, **kwargs)
			else:
				return HttpResponse('Nincs engedélye az oldal megtekintéséhez!')
		return wrapper_func
	return decorator

def vezetoi(view_func):
	def wrapper_function(request, *args, **kwargs):
		group = None
		if request.user.groups.exists():
			group = request.user.groups.all()[0].name

		if group == 'terapeuta':
			return redirect('guru_lap')

		if group == 'szulo':
			return redirect('szulo_lap')

		if group == 'vezeto':
			return view_func(request, *args, **kwargs)

	return wrapper_function

def emusok(view_func):
	def wrapper_function(request, *args, **kwargs):
		group = None
		if request.user.groups.exists():
			group = request.user.groups.all()[0].name

		if group == 'terapeuta':
			return view_func(request, *args, **kwargs)

		if group == 'szulo':
			return redirect('szulo_lap')

		if group == 'vezeto':
			return view_func(request, *args, **kwargs)

	return wrapper_function