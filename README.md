# pgibbs-toy-model
[Birch] implementation of the toy model (Andrieu, 2010)
with `sigma_x=10.0` and `sigma_y=1.0`.

## Download and install birch

Build and install
```
birch build
birch install
```

The configurations for the experiments can be found in the folder `config`. The script `run_simulation.sh` runs all the experiments.

## docker
The docker image `rsrsl/birch-debian` with Birch pre-installed can be found on [Dockerhub]:

```
docker pull rsrsl/birch-debian
docker run --tty --interactive rsrsl/birch-debian
```



[Dockerhub]:https://hub.docker.com/r/rsrsl/birch-debian
[Birch]:https://birch-lang.org/