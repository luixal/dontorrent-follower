# dontorrent-follower
Simple python script to follow and download torrents files for your series from DonTorrent site

This script goes through the pages from DonTorrent's site (no link, domain changes along time) you configure in a file (`data.yaml`). It downlads new episodes each time you run it. And that's it.

This script in not related at all with DonTorrent or any of its members nor mantainers.

## Configuration file
The file is called `data.yaml` and an example is provided in this repo:

```yaml
download_path: /mnt/vault/transmission/torrents
pages:
- min_episode: 17
  tmdb_id: '202102'
  url: https://dontorrent.cymru/serie/103845/103845/Quantum-Leap-1-Temporada-720p
- min_episode: 6
  tmdb_id: '134095'
  url: https://dontorrent.cymru/serie/105152/105152/Asesinato-En-El-Fin-Del-Mundo-1-Temporada-720p
- min_episode: 5
  tmdb_id: '87917'
  url: https://dontorrent.cymru/serie/105290/105293/Para-toda-la-humanidad-4-Temporada-720p
- min_episode: 3
  tmdb_id: '95480'
  url: https://dontorrent.cymru/serie/105547/105547/Slow-Horses-3-Temporada-720p
```

You can see a fields description in this table:

| Field | Description |
| ----- | ----------- |
| download_path | The path to the directoy where you want the `.torrent` files to be downloaded. i.e: transmission torrents directory :) |
| pages | An array of objects that represent a series page (see next table) |

Each page in `pages` must have this fields:

| Field | Description |
| ----- | ----------- |
| min_episode | Only episodes later than this one are downloaded |
| tmdb_id | The ID of the series in [The Movie DB](https://www.themoviedb.org/) page |
| url | URL to the series page in DonTorrent's site |

## How to run it
You can run it by just running python main file, like this:

```sh
python main.py
```

You can also activate python's virtual env and run it:

```sh
source ./bin/activate
python main.py
```
