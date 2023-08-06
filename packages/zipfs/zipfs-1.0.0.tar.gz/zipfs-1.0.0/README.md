# zipf

CLI tool to directly zip several files/folders or an existing folder

Mare a zip from list of files/folders with or without specifying the archive name ("%Y_%m_%d-%H_%M_%S.zip" if not precised) or from an existing folder


# installation
```sh
with pip:
sudo pip3 install zipfs

with yay:
yay -a zipf

with yaourt:
yaourt -a zipf
```

# compatibility
python >= 3


# usage
<pre>
<b>zipf / zipper</b> [<b>F_PATH_01 F_PATH_02 ...</b>] [<b>ARCHIVE_NAME</b>]
<b>options:</b>
<!-- -->         <b>-h, --help</b>        show this help message and exit
</pre>


# examples
for **help**:<br/>
```sh
zipf -h
or
rt --help
```

<br/>make a zip archive from 3 files:<br/>
```sh
zipf titi/toto.jpg titi/tutu.jpg tata.txt
```
giving the **2019_05_15-17_25_44.zip** archive<br/><br/>

make a zip archive from 2 files and one folder with specifying the archive name (work):<br/>
```sh
zipf titi/toto.jpg titi/ tata.txt work
```
giving the **work.zip** archive