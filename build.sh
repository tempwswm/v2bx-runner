#!/bin/bash
export V2BX_VERSION="v0.3.8" &&\
export BUILD_IMG_TAG="registry.cluster.local/v2bx:${V2BX_VERSION}_v1" &&\
echo "Building image $BUILD_IMG_TAG" &&\
podman build -t $BUILD_IMG_TAG . --build-arg V2BX_VERSION=$V2BX_VERSION &&\
podman save -o image.tar $BUILD_IMG_TAG &&\
k3s ctr -n k8s.io i import image.tar &&\
rm image.tar