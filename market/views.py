from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import requests
import environ

env = environ.Env()
environ.Env.read_env()

# Create your views here.
def live(request):

	API_KEY = env('API_KEY')

	url = "https://api-football-beta.p.rapidapi.com/fixtures"# fixtures live

	querystring = {"live":"all"}

	headers = {
		"X-RapidAPI-Key": API_KEY,
		"X-RapidAPI-Host": "api-football-beta.p.rapidapi.com"
	}

	response = requests.get(url, headers=headers, params=querystring)

	data = response.json()

	#fixtures = data['response'][0:len(data['response'])-1]
	#print(data)

	"""
	for i in range(0, data['results']):

		response = data['response'][i]

		for y in range(0, response['fixture']):
			response = response['fixture'][y]
			print(response)
	"""
	responses = data['response']

	page = request.GET.get('page', 1)
	paginator = Paginator(responses, 1)

	try:
		responses = paginator.page(page)
	except PageNotInteger:
		responses = paginator.page(1)
	except EmptyPage:
		responses = paginator.page(paginator.num_pages)		
	
	return render(
		request=request,
		template_name='market/live.html',
		context={'responses': responses}
	)


def team_details(request, pk):

	API_KEY = env('API_KEY')
	fixture = pk

	url = "https://api-football-beta.p.rapidapi.com/teams"# fixtures live

	querystring = {"id":fixture}

	headers = {
		"X-RapidAPI-Key": API_KEY,
		"X-RapidAPI-Host": "api-football-beta.p.rapidapi.com"
	}

	response = requests.get(url, headers=headers, params=querystring)

	data = response.json()

	#fixtures = data['response'][0:len(data['response'])-1]
	#print(data)

	"""
	for i in range(0, data['results']):

		response = data['response'][i]

		for y in range(0, response['fixture']):
			response = response['fixture'][y]
			print(response)
	"""
	responses = data['response']
	return render(
		request=request,
		template_name='market/team.html',
		context={'responses': responses}
	)

