import yaml
import re
import requests
from datetime import datetime
from bs4 import BeautifulSoup
from tmdb import get_episodes_info
from rich.console import Console
from rich.table import Table

def parsePage(url, min_episode=0):
  # load and parse html page:
  response = ''
  try:
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    print('Parsing ' + soup.title.text + '...')
    # get data from episodes table:
    _title = soup.title.text.split('Descargar')[1].split('-')[0].strip()
    data = { 'episodes': [] }
    table = soup.find('table', attrs={'class': 'table'})
    table_body = table.find('tbody')
    rows = table_body.find_all('tr')
    for row in rows:
      try:
        cols = row.find_all('td')
        _season, _episode = re.findall(r'\d+', cols[0].text)
        data['season'] = int(_season)
        # get details and add to data only if episode is new:
        if int(_episode) > min_episode:
          row_data = { 'title': _title}
          row_data['season'] = int(_season)
          row_data['episode'] = int(_episode)
          row_data['download_url'] = 'https:' + cols[1].find('a')['href']
          row_data['date'] = datetime.fromisoformat(cols[2].text)
          data['episodes'].append(row_data)
      except:
        print('WARNING: Error parsing row: ' + row.find_all('td')[0].text)
    return data
  except:
    print(f'ERROR downloading page :: {url}')


def load_config(filename='data.yaml'):
  with open(filename, 'r') as yamlfile:
    data = yaml.load(yamlfile, Loader=yaml.FullLoader)
    return data

def save_config(new_config, filename='data.yaml'):
  with open(filename, 'w') as yamlfile:
    data = yaml.dump(new_config, yamlfile)
    print('Data file updated')

def download_file(url, path="./"):
  filename = url.split("/")[-1]
  print('\tDownlading torrent file' + filename + "...")
  r = requests.get(url, allow_redirects=True)
  open(path + "/" + filename, 'wb').write(r.content)

def getRatingString(season_rating, tv_show_rating):
  # star emojis:
  rating_stars = '[bold yellow]'
  for i in range(int(season_rating/2)):
    rating_stars += ':star:'
  rating_stars += '[/bold yellow]'
  # full string:
  return f'{rating_stars} {"{:.1f}".format(season_rating)} - {"{:.1f}".format(tv_show_rating)}'

def addTableRow(table, input, tv_show_info, status):
  return table.add_row(input['url'], tv_show_info['title'], tv_show_info['season_name'], str(input['min_episode']), str(tv_show_info['episode_count']), getRatingString(tv_show_info["rating"], tv_show_info["rating_tv_show"]), status)


input_data = load_config()

console = Console()
table = Table(show_header=True, header_style="bold cyan")
table.add_column("URL")
table.add_column("Title")
table.add_column("Season")
table.add_column("Min.Episode", justify="right")
table.add_column("Total", justify="right")
table.add_column("Rating", justify="right")
table.add_column("Status")


with console.status("[bold green]Looking for new episodes...", spinner="arrow3") as status:
  for i in range(len(input_data['pages'])):
    input = input_data['pages'][i]
    output_data = parsePage(input['url'], input['min_episode'])
    if output_data:
      tv_show_info = get_episodes_info(input['tmdb_id'], output_data['season'])
      if not output_data['episodes']:
        # print('Todo al día')
        status = 'Up to date'
        if (input['min_episode'] == tv_show_info['episode_count']):
          status = '[bold green]COMPLETED![/bold green]'
        # rating_stars = '[bold yellow]'
        # for i in range(int(tv_show_info['rating']/2)):
        #   rating_stars += ':star:'
        # rating_stars += '[/bold yellow]'
        # table.add_row(input['url'], tv_show_info['title'], tv_show_info['season_name'], str(input['min_episode']), str(tv_show_info['episode_count']), getRatingString(tv_show_info["rating"], tv_show_info["rating_tv_show"]), status)
        addTableRow(table, input, tv_show_info, status)
      else:
        last_episode = 0
        _new_episodes = []
        for output in output_data['episodes']:
          last_episode = output['episode']
          print(f'{output["title"]} {output["season"]}x{output["episode"]}')
          _new_episodes.append(f' {output["season"]}x{output["episode"]}')
          download_file(output['download_url'], input_data['download_path'])
        addTableRow(table, input, tv_show_info, f'[bold]{", ".join(_new_episodes)}[/bold]')
        input_data['pages'][i]['min_episode'] = last_episode
        save_config(input_data)

print()
print('Summary:')
console.print(table)