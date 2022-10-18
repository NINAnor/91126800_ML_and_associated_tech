# Filesystem

A **filesystem** (or filesystem) is the way in which files are named and where they are placed logically for **storage** and **retrieval**. Without a file system, stored information wouldn't be isolated into individual files and would be difficult to identify and retrieve. As data capacities increase, the organization and accessibility of individual files are becoming even more important in data storage. [^1].

```mermaid

graph TB;

A[Project folder] --> B[Camera trap pictures]
A --> C[Code]
A --> D[Report.doc]
B --> E[Pictures of deer]
B --> F[Pictures of birds]
C --> G[myscript.py]
```



## Pyfilesystem: a filesystem abstraction for Python

A filesystem abstraction allows you to work with files and directories in archives, memory, the cloud etc. as easily as your local drive. **It makes your code agnostic to where the data is stored**.

**[Pyfilesystem](https://www.pyfilesystem.org/)** is a filesystem abstraction **for Python**. This means that in your python code you can fully replace the use of `os` with **Pyfilesystem**. 

Suppose the data is stored on `NIRD` in the project folder `/folder/my_data` but I want to process the data on `SAGA` to benefit from optimal computational resources. To access the data on `NIRD` I would make the following change to my code:


First, a connection to `NIRD` must be established. The connection to `NIRD` is done using the `ssh` protocol.

```python
connection_string = "ssh://bencretois:PASSWORD@nird.sigma2.no"


def doConnection(connection_string):

    myfs = fs.open_fs(connection_string)
    return myfs


my_filesystem = doConnection(connection_string)
```

Now that the connection is established we can list the files in `/folder/my_data`:


```python
def walk_audio(filesystem, input_path):
    # Get all files in directory with os.walk
    walker = filesystem.walk(input_path, filter=['*.wav', '*.mp3'])
    for path, dirs, flist in walker:
        for f in flist:
            yield fs.path.combine(path, f.name)


all_files = walk_audio(my_filesystem, "/folder/my_data")
```

Now that the object `all_files` has been created, it is possible to use the files locally.


--- 

[^1] Definition on [Techtarget](https://www.techtarget.com/searchstorage/definition/file-system)