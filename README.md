# 1337x.to Series Collector 
### Description
This script is able to download torrent files from 1337x.to and Organize it into  Directories according to seasons.

### System requirements
---
`Python3`

### Installation
---

1- Linux
* `cd ~/Downloads`
*  `git clone https://github.com/mhalawa96/1337x.to-Series-Collector.git && cd 1337x.to-Series-Collector`
*  `pip install -r requirements.txt`
* Now you can run script: `python3 1337x.py` or `./1337x.py`
 > [Optional]  include the script into system commands.

 * `sudo cp 1337x.py /usr/local/bin/`
 * `sudo ln -s /usr/local/bin/1337x.py /usr/bin/1337x`

Usage: `python3 1337x.py <url>`

### Examples
---

1- Download 'Game of Thrones' Torrent Files.

`python3 1337x.py https://1337x.to/series/game-of-thrones/`
> By default downloads will be in the same directory as the script.

2- Download into another Directory of your choice:

`python3 1337x.py --out=/home/${USER}/Downloads https://1337x.to/series/game-of-thrones/`
 
 
### Options:
```
    -h --help                Show this screen
    --out                    Save into another Directory
```


### Features
---

* Download the torrents with highest seeding score.
* Organize the torrent files into directories according to season

### License
---

[MIT]( 1337x.to-Series-Collector/LICENSE )

### Author Mail
---

[mhalawa.work@gmail.com](mailto:mhalawa.work@gmail.com)
