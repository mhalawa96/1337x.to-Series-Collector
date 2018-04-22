#!/usr/bin/python3
import os
import sys
import argparse
from urllib.parse import urlparse
import requests
from bs4 import BeautifulSoup


def main():
    # Settings Commandline args
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "url", help="Series Url e.g. https://1337x.to/series/series_name/")
    parser.add_argument("--out", help="output Directory",
                        default=os.path.dirname(os.path.realpath(__file__)))
    args = parser.parse_args()

    # Check the Domain
    domain = Get_Domain(args.url)
    if "1337x" in domain:
        os.chdir(args.out)
        req = requests.get(args.url)
        # Get the status Code: req.status_code
        if req.status_code == 200 :
            page_content = BeautifulSoup(req.content, "html5lib")

            # Extract Series Name and Create a Dir with it's name
            info = page_content.find("div", {"class": "movie-info"})
            movie_title = info.find("h3").find("a").text.strip('!@#$')
            # series_dir is the Series Directory
            series_dir = os.path.join(args.out, movie_title)
            if not os.path.exists(movie_title):
                os.makedirs(movie_title)
            os.chdir(series_dir)
            seasons_links = get_seasons(page_content, domain)
            # Iterate Through ALL Seasons !
            for season_number, season_link in enumerate(seasons_links):
                print(
                    "<----------------- Downloading Season {} ----------------->".format(season_number+1))
                # Creating Dir for each season by name
                os.chdir(series_dir)
                dir_name = os.path.join(
                    series_dir, "Season {}".format(season_number+1))
                if not os.path.exists(dir_name):
                    os.makedirs(dir_name)
                os.chdir(dir_name)
                for episode_link, episode_name in Get_Episodes(season_link, domain):
                    episode_torrent_link = Extract_Episode_Torrent(
                        episode_link)
                    if episode_torrent_link:
                        url = episode_torrent_link
                        filename = os.path.join(
                            dir_name, episode_name+".torrent")
                        # Check if the file Already Exist !
                        if not os.path.exists(filename):
                            Download(url, filename)
                            print("[{}]: Downloaded".format(episode_name))
                        else:
                            print("[{}]: Already Exist !".format(
                                episode_name))
                    else:
                        eprint("[{}]: Failed Please Check: {}".format(
                            episode_name, episode_link))
        print("<----------------- Finished Successfully ! ----------------->")
    else:
        eprint("collector doesn't recongnize the domain, please double sure the url")


def get_seasons(pg_content, domain):
    seasons = pg_content.find("div", {"class": "seasons"})
    # Extract Links
    if seasons is not None:
        # get all anchor tags in the page
        links = seasons.find_all("a")
        # extract attributes from the link
        for link in links:
            yield domain+link.get("href")
    else:
        print("Nothing found !")
        exit(0)


def Get_Episodes(season, domain):
    req = requests.get(season)
    if(req.status_code == 200):
        seasonContent = BeautifulSoup(req.content, "html5lib")
        Episodes = seasonContent.find_all("table")
        # Break if there is no Episodes
        for Episode in Episodes:
            # return link for each episode
            Link = domain + \
                Episode.find("td", {"class", "name"}).find("a").get("href")
            Name = Episode.find("td", {"class", "name"}).text
            # return the name of the Episode and the Link
            yield Link, Name


def Extract_Episode_Torrent(episode):
    req = requests.get(episode)
    if(req.status_code == 200):
        page_content = BeautifulSoup(req.content, "html5lib")
        link_list = page_content.find("ul", {"class", "dropdown-menu"})
        if link_list is not None:
            torrent_links = link_list.find_all("a", {"class": "btn"})
            for torrent_link in torrent_links:
                if torrent_link.get("href").endswith(".torrent"):
                    return torrent_link.get("href")
                else:
                    return None
        else:
            return None


def Download(url, filename):
   # open in binary mode
    with open(filename, "wb") as file:
        # get request
        response = requests.get(url)
        # write to file
        file.write(response.content)


def Get_Domain(url):
    parsed_uri = urlparse(url)
    domain = '{uri.scheme}://{uri.netloc}'.format(uri=parsed_uri)
    return domain


def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)


if __name__ == "__main__":
    main()
