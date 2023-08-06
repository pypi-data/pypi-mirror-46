# NeterraProxy
This is a Python version of the [neterra proxy](https://github.com/sgloutnikov/NeterraProxy) java app written by @sgloutnikov.

## What?
NeterraProxy is an on-demand m3u8 playlist/playback daemon for Neterra.tv, running on Python (2.7.x).

## Why?
Have the freedom to watch on your desired IPTV player or TV (Perfect Player, Kodi IPTV Simple, Android Live Channels, GSE Smart IPTV Player, etc). Play links issued by Neterra expire after 12 hours to prevent abuse. Traditional playlist generators need to be run again in order to generate new links. This is not the case for NeterraProxy.

## How?
NeterraProxy generates a specialized playlist that points to itself rather than Neterra. When NeterraProxy receives a playback request it determines the context of the request and responds with a 301 redirect to a valid corresponding Neterra play link. It automatically re-authenticates if the session has expired.

## Electronic Program Guide (EPG)
The application has a built-in scheduler that downloads an XMLTV file with the program guides for the most of the offered by Neterra.tv channels. The scheduler runs every 4 hours. Please note that the application does not perform the download on start - you need to keep it running for 4 hours. The xmltv file is downloaded in the specified data directory (see the section Instructions).

## Instructions
1) Install the Python package **pip install neterraproxy**. 
2) Start the application with **python -m neterraproxy *your Nettera.tv username* *your Netter.tv password* *the proxy data directory***
    * Active subscription for Nettera.tv is required for the provided above user.
    * The script data directory is used to store the proxy log file and the xmltv epg file.
3) Leave the proxy application running. **Ctrl + C** will terminate NeterraProxy.
4) Use the following URL to connect NeterraProxy with your favorite IPTV player:
    * Playlist URL: http://localhost:8080/playlist.m3u8
    * EPG URL: http://localhost:8080/epg.xml

## Run as Linux Service
1) Install the package as per the instruction above
2) Download the netteraproxy.service unit file from [here](https://github.com/ananchev/neterraproxy/blob/master/neterraproxy.service)
3) Edit the file and provide your username, password and data directory in the line **Environment='ARGUMENTS=-m neterraproxy *neterra_username* *neterra_password* *data_directory*'**
4) Copy the unit file in __/lib/systemd/system__
5) Start the service with **sudo systemctl start neterraproxy.service**
6) Check the status with **sudo systemctl status neterraproxy.service** and verify the proxy functions properly 
7) Enable the service to start with the OS **sudo systemctl enable neterraproxy.service**

## Acknowledgements
@sgloutnikov for his Java proxy and the answers to my stupid during the development of the Python version
[Kodi Fan Forum BG](https://kodibg.org/forum/) for collecting and hosting the XMLTV EPG file 
