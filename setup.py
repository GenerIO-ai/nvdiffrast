# Copyright (c) 2020, NVIDIA CORPORATION. All rights reserved.

import os

import setuptools

try:
    from torch.utils.cpp_extension import BuildExtension, CUDAExtension
except ImportError:
    print("\n\n" + "*" * 70)
    print("ERROR! Cannot compile nvdiffrast CUDA extension. Please ensure that:\n")
    print("1. You have PyTorch installed")
    print("2. You run 'pip install' with --no-build-isolation flag")
    print("*" * 70 + "\n\n")
    raise SystemExit(1)


setuptools.setup(
    name="nvdiffrast",
    version="0.4.0",
    packages=setuptools.find_packages(
        include=["nvdiffrast", "nvdiffrast.torch"],
        exclude=["nvdiffrast.common*"],
    ),
    install_requires=["numpy"],
    ext_modules=[
        CUDAExtension(
            "_nvdiffrast_c",
            sources=[
                "csrc/common/antialias.cu",
                "csrc/common/common.cpp",
                "csrc/common/cudaraster/impl/Buffer.cpp",
                "csrc/common/cudaraster/impl/CudaRaster.cpp",
                "csrc/common/cudaraster/impl/RasterImpl.cpp",
                "csrc/common/cudaraster/impl/RasterImpl_kernel.cu",
                "csrc/common/interpolate.cu",
                "csrc/common/rasterize.cu",
                "csrc/common/texture.cpp",
                "csrc/common/texture_kernel.cu",
                "csrc/torch/torch_antialias.cpp",
                "csrc/torch/torch_bindings.cpp",
                "csrc/torch/torch_interpolate.cpp",
                "csrc/torch/torch_rasterize.cpp",
                "csrc/torch/torch_texture.cpp",
            ],
            extra_compile_args={
                "cxx": ["-DNVDR_TORCH"]
                + (["/wd4067", "/wd4624", "/wd4996"] if os.name == "nt" else []),
                "nvcc": ["-DNVDR_TORCH", "-lineinfo"],
            },
        )
    ],
    cmdclass={"build_ext": BuildExtension},
)