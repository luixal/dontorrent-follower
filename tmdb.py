import requests
from rich import print

def get_episodes_info(tv_show_id: str, season_number=0, api_key='eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiIyNmQwMmJjNzI1NmFiNTU0NTVlZWRmZTQ0OGIwNjZlMCIsInN1YiI6IjY1NDkyODFiMWFjMjkyN2IzMDI4Yzc1OCIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.ajbtVAIhcYNyF-7ZS8Aj1nmS4MjHXh82ymuSlcW2FE8'):
  headers = { 'Authorization': f'Bearer {api_key}' }
  response = requests.get(f'https://api.themoviedb.org/3/tv/{tv_show_id}?language=en-US', headers=headers)
  data = response.json()
  # finding right season:
  season = ''
  for _season in data['seasons']:
    if (_season['season_number'] == season_number):
      season = _season
      break
  # build result object:
  result = {
    'title': data['name'],
    'season_name': season['name'],
    'episode_count': season['episode_count'],
    'rating': season['vote_average'],
    'rating_tv_show': data['vote_average']
  }
  # print(data)
  return result

# print(get_episodes_info('62852', 7))