import os
import mutagen
import json
import hashlib

FILETYPES = ("flac", "mp3", "ogg")
MUSIC_DIR = "res/Music/"

song_database = {}
artist_database = {}
album_database = {}
picture_database = {}


def write_db(database, file_name: str):
    json_object = json.dumps(database, indent=4)
    with open(file_name, "w") as out_file:
        out_file.write(json_object)


def create_databases():
    for root, dirnames, filenames in os.walk(MUSIC_DIR):
        for filename in filenames:
            if filename.endswith(FILETYPES):
                file_path = os.path.join(root, filename)
                metadata = mutagen.File(file_path)

                artist_name = metadata.get("artist")[0]
                album_artist_name = metadata.get("albumartist")[0]
                album_name = metadata.get("album")[0]

                file_path_hash = hashlib.md5(file_path.encode()).hexdigest()
                artist_name_hash = hashlib.md5(artist_name.encode()).hexdigest()
                album_artist_name_hash = hashlib.md5(
                    album_artist_name.encode()
                ).hexdigest()
                album_name_hash = hashlib.md5(album_name.encode()).hexdigest()

                song_database.setdefault(
                    file_path_hash,
                    {
                        "title": metadata.get("title")[0],
                        "artist": artist_name_hash,
                        "album": album_name_hash,
                        "path": file_path,
                    },
                )

                artist_database.setdefault(
                    artist_name_hash,
                    {
                        "name": artist_name,
                    },
                )

                album_database.setdefault(
                    album_name_hash,
                    {
                        "name": album_name,
                        "artist": album_artist_name_hash,
                        "date": metadata.get("date"),
                        "label": metadata.get("label"),
                        "catalog": metadata.get("catalognumber"),
                    },
                )

    write_db(song_database, "song.json")
    write_db(album_database, "album.json")
    write_db(artist_database, "artist.json")


if __name__ == "__main__":
    create_databases()

    song = song_database["8cf68a8d67c625c1b45aefb435e953d4"]
    song_album_id = song.get("album")
    song_artist_id = song.get("artist")
    album = album_database[song_album_id]
    album_artist_id = album.get("artist")
    artist = artist_database[song_artist_id]
    album_artist = artist_database[album_artist_id]
    print(song, album, artist, album_artist)

    print(f"Title: {song.get('title')}")
    print(f"Album: {album['name']}")
    print(f"Artist: {artist['name']}")
    print(f"Album Artist: {album_artist['name']}")
    print(f'Date: {album.get("date")}')
    print(f"Label: {album.get('label')}")
    print(f"Catalog No.: {album.get('catalog')}")
