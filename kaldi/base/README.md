# Kaldi Base Docker

Contains the `Dockerfile` to build the `kaldi-base` image required by the `kaldi-worker` and `decode-worker`. It might take a while until this image is built (> 30 minutes), so the mentioned workers use the prebuilt `th-nuernberg/kaldi-base` image from Docker Hub.

As this repository is private, a Docker Hub account is required and access has to be granted ([contact](mailto:***REMOVED***)).


## Build Image

The following command builds the Dockerfile from the current directory.
```bash
docker build . -t <name> [--squash]
```
 - The name `<name>` of the image should equal the repository name (e.g. `<username>/kaldi-base`).
 - The option `--squash` reduces the image size by diffing all layers into a new one.  
 This is an [experimental feature](https://github.com/docker/docker-ce/blob/master/components/cli/experimental/README.md) and not enabled by default so far (docker engine 18.09).

For the `kaldi-base` image the command looks like this:
```bash
docker build . -t kaldi-base --squash
```
