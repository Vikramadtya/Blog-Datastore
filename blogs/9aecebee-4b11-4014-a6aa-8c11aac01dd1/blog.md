Tar bundles multiple files into a single archive file, and can optionally compress them in Linux systems.

# Compress
To compress a file or directory


```shell
tar -cvf archive_file_name.tar <location-to-the-directory-or-file>
```

the options used in the above command are 


- `-c` for creating a new archive
- `-v` to show the detailed output of the process.
- `-f` to specify the archive file.

to compress the archive using gzip use the option `-z` so the archive will be a `.tar.gz` file

```shell
tar -cvfz compressed_archive_file_name.tar.gz <location-to-the-directory-or-file>
```

> some other **gzip** (`-z`) alternative to compress the archive are **bzip2* (`-j`) and  **xz** (`-J`)

# Extract
To compress a file or directory


```shell
tar -C <location-to-the-directory-where-to-uncompress> -xvf archive_file_name.tar
```

the options used in the above command are

- `x` Extract files from an archive.
- `-v` to show the detailed output of the process.
- `-f` to specify the archive file.

# List the contents 
To see the files in an archive

```shell
tar -tvf compressed_file_name.tar
```


> For a compressed archive provide the valid `-z` or `-j` or `-J` option