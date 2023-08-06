# ypc : youtube_playlist_converter

This python utility allows the conversion of spotify/deezer/text playlists to youtube urls or audio/video files.

It supports spotify and deezer playlist urls, as well as a list of terms to search (see below for some examples). 

It also supports files containing a list of spotify and deezer playlist urls or a list of terms to search (one by line). Unfortunately, a mix of several type is not supported at this moment (spotify and deezer playlists urls in the same file for example).

If you want to extract spotify playlists, you need to set up a valid config.ini file with your spotify api client id and secret (go to https://developer.spotify.com/dashboard/login to create your own spotify application) and place it in the ~/.config/ypc/ directory (see the config_sample.ini file as an example).

## Installation

```
pip install ypc
```

## Installation in a virtualenv

```
git clone https://github.com/dbeley/ypc
cd ypc
pipenv install '-e .'
```

## Usage

### Help

Use ypc with the -h flag to see all the available options :

```
ypc -h
```

### Examples

#### Simple Examples

Download audio files for several songs :

```
ypc "u2 one,xtc general and majors,debussy la mer" -a
```

Download videos for several deezer playlists using the name "deezer_export" as export folder :

```
ypc DEEZER_PLAYLIST_URL1,DEEZER_PLAYLIST_URL2 -v -n deezer_export
```

Download audio and video for each spotify playlists in the file spotify_playlists.txt (one by line) using the name "spotify_export" as export folder :

```
ypc spotify_playlists.txt -a -v -n spotify_export
```

The main ypc arguments you want are -a (download audio), -v (download video) and -n (set the name of the export folder).

You can set the medias (an url, a list of search terms, a file containing spotify playlist urls, etc.) to download without any argument and ypc will guess which kind of media it is, or use explicit argument, as shown in the examples below.

#### With a spotify url

Download the audio of a spotify playlist :

```
ypc SPOTIFY_PLAYLIST_URL -a
ypc -su SPOTIFY_PLAYLIST_URL -a
```

#### With a deezer url

Download the video founds on youtube from a file containing deezer playlists (one by line) :

```
ypc deezer_list_playlists.txt -v
ypc -df deezer_list_playlists.txt -v
```

#### With a csv file

Given a file sample_file.csv :

```
artist1 - title1
artist1 - title2
artist2 - title1
any search term
```

Download the audio files for the tracks/search terms in the sample csv file above :

```
ypc sample_file.csv -a
ypc -f sample_file.csv -a
```

Download the video files for the tracks/search terms in the sample csv file above :

```
ypc sample_file.csv -v
ypc -f sample_file.csv -v
```
