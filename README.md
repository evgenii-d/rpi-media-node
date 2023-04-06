# RPi Media Node

## Node API

### Machine Control

| Endpoints  | HTTP Method | Description |
| ------------- | ------------- | ------------- |
| <http://localhost:5000/machine-control> | POST | Execute system command (Reboot, Shutdown) |

### Media Files

| Endpoints  | HTTP Method | Description |
| ------------- | ------------- | ------------- |
| <http://localhost:5000/media-files> | GET | Return list of media files |
| <http://localhost:5000/media-files/add> | POST | Upload files |
| <http://localhost:5000/media-files/delete> | DELETE | Delete files |
| <http://localhost:5000/media-files/size> | GET | Return size of "files" directory |
| <http://localhost:5000/media-files/playlists> | GET | Returns avalible playlists |
| <http://localhost:5000/media-files/playlists/add> | POST | Create playlist |
| <http://localhost:5000/media-files/playlists/delete> | DELETE | Remove playlist |
| <http://localhost:5000/media-files/playlists/content/id> | GET | Return playlist content |
| <http://localhost:5000/media-files/playlists/content/id> | PUT | Update playlist content |
| <http://localhost:5000/media-files/playlists/default> | GET | Get default playlist |
| <http://localhost:5000/media-files/playlists/default> | POST | Set default playlist |

### Media Player

| Endpoints  | HTTP Method | Description |
| ------------- | ------------- | ------------- |
| <http://localhost:5000/media-player/settings> | GET | Get player state |
| <http://localhost:5000/media-player/settings> | POST | Set player state |
| <http://localhost:5000/media-player/control> | POST | Execute player commands |
| <http://localhost:5000/media-player/state> | GET | Update player settings |
| <http://localhost:5000/media-player/state> | POST | Update player settings |

### Node Details

| Endpoints  | HTTP Method | Description |
| ------------- | ------------- | ------------- |
| <http://localhost:5000/node-details/hostname> | GET | Get hostname |
| <http://localhost:5000/node-details/name> | GET | Get node name |
| <http://localhost:5000/node-details/name> | POST | Set node name |

### Web Browser

| Endpoints  | HTTP Method | Description |
| ------------- | ------------- | ------------- |
| <http://localhost:5000/web-browser/url> | GET | Get Web Browser startup URL |
| <http://localhost:5000/web-browser/url> | POST | Set Web Browser startup URL |
| <http://localhost:5000/web-browser/state> | GET | Get Web Browser state |
| <http://localhost:5000/web-browser/state> | POST | Set Web Browser state |

### Web Server

| Endpoints  | HTTP Method | Description |
| ------------- | ------------- | ------------- |
| <http://localhost:5000/web-server/archive> | GET | Get Web Browser startup URL |
| <http://localhost:5000/web-server/archive> | POST | Set Web Browser startup URL |
| <http://localhost:5000/web-server/state> | GET | Return zip archive |
| <http://localhost:5000/web-server/state> | POST | Upload zip archive |
