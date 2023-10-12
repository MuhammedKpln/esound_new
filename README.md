# Migrate from YouTube Music to another service.

## Supported clients as for now:

- ESound

## Installation

```bash
git clone https://github.com/muhammedkpln/youtube-migrator.git

cd youtube-migrator

poetry install

python src/main.py
```

## Connect your YouTube Music

There is two way if you want to connect your YouTube account. The connection is handled by `ytmusicapi` library. You can read more about it in [ytmusicapi docs](https://ytmusicapi.readthedocs.io/en/stable/index.html)

### First way:

Connection with OAuth:

```bash
python src/main.py -o
```

You can read more about [second way here](https://ytmusicapi.readthedocs.io/en/stable/setup/browser.html)

```
Yt2Esound is Open Source software open to development.
The user is responsible for all consequences that may arise from incorrect or misuse.
Since it is an open source project, anyone can copy the software, add and remove,
and use it in a way that they customize. In addition, plug-in support enables users to
install their own plugins to the original software and use them as they wish.
Usage is entirely the user's responsibility, yt2esound is an
infrastructure only. Just as the operating system is not responsible
for the work done with the programs that are installed later, yt2esound
is not responsible for the usage purpose and method of the users.
Marketing yt2esound for money, making it available or having any material value
ıt is strictly forbidden to offer it for sale with anything. All legal investigations that may arise
the user is responsible.

```
