# Copyright 2018-present PIO Plus <contact@pioplus.com>
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""
mbed framework

Fork of Mbed OS for GAP8 by GreenWaves Technologies

https://github.com/GreenWaves-Technologies/mbed-os
"""

from os.path import isdir, join

Import("env")

platform = env.PioPlatform()
SDK_DIR = platform.get_package_dir("platformio-wch583m-sdk")
FRAMEWORK_DIR = join(SDK_DIR, "src")
TOOLCHAIN_DIR = platform.get_package_dir("toolchain-riscv-pulp")
assert SDK_DIR and isdir(SDK_DIR)
assert FRAMEWORK_DIR and isdir(FRAMEWORK_DIR)
assert TOOLCHAIN_DIR and isdir(TOOLCHAIN_DIR)


def get_toolchain_version():
    version = platform.get_package_version("toolchain-riscv-pulp")
    version = version.split(".")[1]
    version = version.replace('0', '.')
    return version


board_config = env.BoardConfig()

toolchain_version = get_toolchain_version()
target_path = join(FRAMEWORK_DIR, "targets",
                   "TARGET_%s" % board_config.get("build.target"))
variant = board_config.get("build.variant")
variant_path = join(target_path, "TARGET_%s" % variant)

env.Append(
    CCFLAGS=[
        "-Os",
        "-Wall",
        "-Wextra",
        "-Wno-unused-parameter",
        "-Wno-unused-function",
        "-Wno-unused-variable",
        "-Wno-deprecated-declarations",
        "-ffunction-sections",
        "-fdata-sections",
        "-mPE=8",
        "-mFC=1",
        "-Wno-missing-field-initializers",
        "-Wno-unused-but-set-variable",
        "-fmessage-length=0",
        "-fno-exceptions",
        "-fno-builtin",
        "-funsigned-char",
        "-fno-delete-null-pointer-checks",
        "-fomit-frame-pointer",
        ("-include", join(target_path, "mbed_config.h")),
        "-march=%s" % board_config.get("build.march")
    ],

    CFLAGS=["-std=gnu99"],

    CXXFLAGS=[
        "-std=gnu++98",
        "-fno-rtti",
        "-Wvla"
    ],

    CPPDEFINES=[
        # DEVICE_FLAGS
        ("DEVICE_SPI_ASYNCH", 1),
        ("DEVICE_SPI", 1),
        ("DEVICE_SERIAL", 1),
        ("DEVICE_SERIAL_ASYNCH", 1),
        ("DEVICE_HYPERBUS_ASYNCH", 1),
        ("DEVICE_HYPERBUS", 1),
        ("DEVICE_STDIO_MESSAGES", 1),
        ("DEVICE_SLEEP", 1),
        ("DEVICE_PORTIN", 1),
        ("DEVICE_PORTOUT", 1),
        ("DEVICE_PORTINOUT", 1),
        ("DEVICE_I2C", 1),
        ("DEVICE_I2C_ASYNCH", 1),
        ("DEVICE_I2S", 1),
        ("DEVICE_RTC", 1),
        ("DEVICE_INTERRUPTIN", 1),
        ("DEVICE_PWMOUT", 1),

        # FEATURE_FLAGS
        ("FEATURE_CLUSTER", 1),

        # MBED_FLAGS
        ("__MBED__", 1),
        "TOOLCHAIN_GCC_RISCV",
        "TOOLCHAIN_GCC"
    ],

    CPPPATH=[
        variant_path,
        join(variant_path, "StdPeriphDriver"),
        join(FRAMEWORK_DIR),
        join(FRAMEWORK_DIR, "RVMSIS"),
        join(FRAMEWORK_DIR, "Ble"),
        join(FRAMEWORK_DIR, "StdPeriphDriver"),
        join(target_path, "libs", "newlib", "extra", "stdio", "tinyprintf"),
        join(target_path, "api")
    ],

    LINKFLAGS=[
        "-nostartfiles",
        "-Wl,--gc-sections",
        "-Wl,--wrap,main",
        "-Wl,--wrap,_malloc_r",
        "-Wl,--wrap,_free_r",
        "-Wl,--wrap,_realloc_r",
        "-Wl,--wrap,_memalign_r",
        "-Wl,--wrap,_calloc_r",
        "-Wl,--wrap,atexit",
        "-Wl,-n",
        join(TOOLCHAIN_DIR, "lib", "gcc", "riscv32-unknown-elf",
             toolchain_version, "crtbegin.o"),
        join(TOOLCHAIN_DIR, "lib", "gcc", "riscv32-unknown-elf",
             toolchain_version, "crti.o"),
        join(TOOLCHAIN_DIR, "lib", "gcc", "riscv32-unknown-elf",
             toolchain_version, "crtn.o"),
        join(TOOLCHAIN_DIR, "lib", "gcc", "riscv32-unknown-elf",
             toolchain_version, "crtend.o")
    ],

    LIBPATH=[
        join(target_path, "libs"),
        join(target_path, "libs", "newlib"),
        join(target_path, "TARGET_%s" % variant, "device", "ld")
    ],

    LIBS=["c", "m", "gcc", "-lstdc++"]
)

env.Append(ASFLAGS=env.get("CCFLAGS", [])[:])

#
# Target: Build Core files from framework
#

env.BuildSources(
    join("$BUILD_DIR", "StdPeriphDriver"),
    join(FRAMEWORK_DIR, "StdPeriphDriver", "StdPeriphDriver")
)

env.BuildSources(
    join("$BUILD_DIR", "StdPeriphDriver"),
    join(FRAMEWORK_DIR, "StdPeriphDriver", "StdPeriphDriver"),
    src_filter="+<*> -<TOOLCHAIN_IAR>"
)
