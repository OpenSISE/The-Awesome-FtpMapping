# The-Awesome-FtpMapping-script

> A ftpmapping for helping files or foler index with ftp server


## Usage
**It below was generated by ```python ftpmapping.py -h``` command**

```
Usage: ftpmapping.py [options]

Options:
  -h, --help            show this help message and exit
  --path=PATH           the path used to generate the tree [default: /]
  -o FILE, --out=FILE   specify a filename or file to store the generated tree
                        [default: pathname.trees]
  -u USERNAME, --username=USERNAME
                        the username used to connect to the ftp server
                        [default: anonymous]
  -p PASSWORD, --password=PASSWORD
                        the password used to connect to the ftp server
                        [default: anonymous]
  -s SERVER, --server=SERVER
                        the ftp server address
  -t TREETYPE, --type=TREETYPE
                        tree type, leave it default for folder-only.It map and
                        generate the tree contained files when passing 'file'.
                        [default: folder]

```


### Example:
> list folders only ```python ftpmapping.py -u chris -p damnpass -s 172.16.144.202 -t folder --path /```
![example1](http://schoolpot.qiniudn.com/ftpmappingsample1.png)
> list folders and files ```python ftpmapping.py -u chris -p damnpass -s 172.16.144.202 -t file --path / ```
![example2](http://schoolpot.qiniudn.com/ftpmappingsample2.png)