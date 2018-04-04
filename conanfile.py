from conans import ConanFile, CMake, tools
import shutil
import os
import platform

class LlvmConan(ConanFile):
    name = 'llvm'

    source_version = '3.3'
    package_version = '5'
    version = '%s-%s' % (source_version, package_version)

    build_requires = 'vuoutils/1.1@vuo/stable'
    settings = 'os', 'compiler', 'build_type', 'arch'
    url = 'https://github.com/vuo/conan-llvm'
    license = 'http://releases.llvm.org/%s/LICENSE.TXT' % source_version
    description = 'A collection of modular and reusable compiler and toolchain technologies'
    source_dir  = 'llvm-%s.src' % source_version
    build_dir = '_build'
    install_dir = '_install'
    exports_sources = '*.patch'
    libs = {
        'LLVMAnalysis': 0,
        'LLVMArchive': 0,
        'LLVMAsmParser': 0,
        'LLVMAsmPrinter': 0,
        'LLVMBitReader': 0,
        'LLVMBitWriter': 0,
        'LLVMCodeGen': 0,
        'LLVMCore': 0,
        'LLVMDebugInfo': 0,
        'LLVMExecutionEngine': 0,
        'LLVMIRReader': 0,
        'LLVMInstCombine': 0,
        'LLVMInstrumentation': 0,
        'LLVMInterpreter': 0,
        'LLVMJIT': 0,
        'LLVMLinker': 0,
        'LLVMMC': 0,
        'LLVMMCDisassembler': 0,
        'LLVMMCJIT': 0,
        'LLVMMCParser': 0,
        'LLVMObjCARCOpts': 0,
        'LLVMObject': 0,
        'LLVMOption': 0,
        'LLVMRuntimeDyld': 0,
        'LLVMScalarOpts': 0,
        'LLVMSelectionDAG': 0,
        'LLVMSupport': 0,
        'LLVMTableGen': 0,
        'LLVMTarget': 0,
        'LLVMTransformUtils': 0,
        'LLVMVectorize': 0,
        'LLVMX86AsmParser': 0,
        'LLVMX86AsmPrinter': 0,
        'LLVMX86CodeGen': 0,
        'LLVMX86Desc': 0,
        'LLVMX86Disassembler': 0,
        'LLVMX86Info': 0,
        'LLVMX86Utils': 0,
        'LLVMipa': 0,
        'LLVMipo': 0,
        'LTO': 0,
        'c++': 0,
        'clang': 0,
        'clangARCMigrate': 0,
        'clangAST': 0,
        'clangASTMatchers': 0,
        'clangAnalysis': 0,
        'clangBasic': 0,
        'clangCodeGen': 0,
        'clangDriver': 0,
        'clangEdit': 0,
        'clangFormat': 0,
        'clangFrontend': 0,
        'clangFrontendTool': 0,
        'clangLex': 0,
        'clangParse': 0,
        'clangRewriteCore': 0,
        'clangRewriteFrontend': 0,
        'clangSema': 0,
        'clangSerialization': 0,
        'clangStaticAnalyzerCheckers': 0,
        'clangStaticAnalyzerCore': 0,
        'clangStaticAnalyzerFrontend': 0,
        'clangTooling': 0,
    }
    executables = [
        'clang',
        'clang++',
        'llvm-link',
    ]

    def requirements(self):
        if platform.system() == 'Linux':
            self.requires('patchelf/0.10pre-1@vuo/stable')
        elif platform.system() != 'Darwin':
            raise Exception('Unknown platform "%s"' % platform.system())

    def source(self):
        tools.get('http://llvm.org/releases/%s/llvm-%s.src.tar.gz' % (self.source_version, self.source_version),
                  sha256='68766b1e70d05a25e2f502e997a3cb3937187a3296595cf6e0977d5cd6727578')

        tools.get('http://llvm.org/releases/%s/cfe-%s.src.tar.gz' % (self.source_version, self.source_version),
                  sha256='b1b55de4ab3a57d3e0331a83e0284610191c77d924e3446498d9113d08dfb996')
        shutil.move('cfe-%s.src' % self.source_version, '%s/tools/clang' % self.source_dir)

        tools.get('http://llvm.org/releases/%s/libcxx-%s.src.tar.gz' % (self.source_version, self.source_version),
                  sha256='c403ed18d2992719c794cdd760dc87a948b62a7c2a07beb39eb984dfeb1679f1')
        shutil.move('libcxx-%s.src' % self.source_version, '%s/projects/libcxx' % self.source_dir)

        # https://b33p.net/kosada/node/7848#comment-32297
        tools.patch(patch_file='disable-unused-intrinsics.patch', base_path=self.source_dir)

        if platform.system() == 'Linux':
            tools.patch(patch_file='linux-offsetof.patch', base_path=self.source_dir)
            tools.replace_in_file('%s/cmake/config-ix.cmake' % self.source_dir,
                'check_include_file(sanitizer/msan_interface.h HAVE_SANITIZER_MSAN_INTERFACE_H)',
                '')

        self.run('mv %s/LICENSE.TXT %s/%s.txt' % (self.source_dir, self.source_dir, self.name))
        self.run('mv %s/include/llvm/Support/LICENSE.TXT %s/%s-systemsupport.txt' % (self.source_dir, self.source_dir, self.name))
        self.run('mv %s/tools/clang/LICENSE.TXT %s/clang.txt' % (self.source_dir, self.source_dir))

    def build(self):
        import VuoUtils
        tools.mkdir(self.build_dir)
        with tools.chdir(self.build_dir):
            cmake = CMake(self)

            cmake.definitions['CMAKE_BUILD_TYPE'] = 'Release'
            cmake.definitions['CMAKE_C_FLAGS'] = '-O3 -march=x86-64'
            cmake.definitions['CMAKE_CXX_FLAGS'] = cmake.definitions['CMAKE_C_FLAGS'] + ' -std=c++11 -stdlib=libc++'
            cmake.definitions['CMAKE_SHARED_LINKER_FLAGS'] = '-stdlib=libc++'
            cmake.definitions['CMAKE_STATIC_LINKER_FLAGS'] = '-stdlib=libc++'
            cmake.definitions['CMAKE_INSTALL_PREFIX'] = '%s/../%s' % (os.getcwd(), self.install_dir)

            cmake.definitions['BUILD_SHARED_LIBS'] = 'ON'
            cmake.definitions['CLANG_BUILD_EXAMPLES'] = 'OFF'
            cmake.definitions['CLANG_INCLUDE_TESTS'] = 'OFF'
            cmake.definitions['LLVM_BUILD_32_BITS'] = 'OFF'
            cmake.definitions['LLVM_BUILD_EXAMPLES'] = 'OFF'
            cmake.definitions['LLVM_BUILD_RUNTIME'] = 'ON'
            cmake.definitions['LLVM_BUILD_TESTS'] = 'OFF'
            cmake.definitions['LLVM_BUILD_TOOLS'] = 'ON'
            cmake.definitions['LLVM_ENABLE_ASSERTIONS'] = 'ON'
            cmake.definitions['LLVM_ENABLE_BACKTRACES'] = 'OFF'
            cmake.definitions['LLVM_ENABLE_FFI'] = 'OFF'
            cmake.definitions['LLVM_ENABLE_PEDANTIC'] = 'ON'
            cmake.definitions['LLVM_ENABLE_PIC'] = 'ON'
            cmake.definitions['LLVM_ENABLE_THREADS'] = 'ON'
            cmake.definitions['LLVM_ENABLE_TIMESTAMPS'] = 'ON'
            cmake.definitions['LLVM_ENABLE_WARNINGS'] = 'ON'
            cmake.definitions['LLVM_ENABLE_WERROR'] = 'OFF'
            cmake.definitions['LLVM_ENABLE_LIBCXX'] = 'ON'
            cmake.definitions['LLVM_EXPERIMENTAL_TARGETS_TO_BUILD'] = ''
            cmake.definitions['LLVM_EXTERNAL_CLANG_BUILD'] = 'ON'
            cmake.definitions['LLVM_INCLUDE_EXAMPLES'] = 'OFF'
            cmake.definitions['LLVM_INCLUDE_RUNTIME'] = 'OFF'
            cmake.definitions['LLVM_INCLUDE_TESTS'] = 'OFF'
            cmake.definitions['LLVM_INCLUDE_TOOLS'] = 'ON'
            cmake.definitions['LLVM_LIT_ARGS'] = '-sv'
            cmake.definitions['LLVM_TARGETS_TO_BUILD'] = 'X86'
            cmake.definitions['LLVM_TARGET_ARCH'] = 'host'
            cmake.definitions['LLVM_USE_FOLDERS'] = 'ON'
            cmake.definitions['LLVM_USE_INTEL_JITEVENTS'] = 'OFF'
            cmake.definitions['LLVM_USE_OPROFILE'] = 'OFF'

            if platform.system() == 'Darwin':
                cmake.definitions['CMAKE_C_FLAGS'] += ' -mmacosx-version-min=10.10'
                cmake.definitions['CMAKE_CXX_FLAGS'] += ' -mmacosx-version-min=10.10'
                cmake.definitions['CMAKE_C_COMPILER']   = '/usr/bin/clang'
                cmake.definitions['CMAKE_CXX_COMPILER'] = '/usr/bin/clang++'
                cmake.definitions['CMAKE_OSX_ARCHITECTURES'] = 'x86_64'
                cmake.definitions['CMAKE_OSX_DEPLOYMENT_TARGET'] = '10.10'
            elif platform.system() == 'Linux':
                cmake.definitions['CMAKE_C_COMPILER']   = '/usr/bin/clang-5.0'
                cmake.definitions['CMAKE_CXX_COMPILER'] = '/usr/bin/clang++-5.0'
                cmake.definitions['PYTHON_EXECUTABLE'] = '/usr/bin/python2'

            # Build LLVM and Clang.
            cmake.configure(source_dir='../%s' % self.source_dir,
                            build_dir='.')
            cmake.build()
            cmake.install()

            # Build libc++.
            libcxx_build_dir = 'libcxx'
            tools.mkdir(libcxx_build_dir)
            with tools.chdir(libcxx_build_dir):
                if platform.system() == 'Darwin':
                    cmake.definitions['CMAKE_SHARED_LINKER_FLAGS'] += ' /usr/lib/libc++abi.dylib'
                    cmake.definitions['CMAKE_STATIC_LINKER_FLAGS'] += ' /usr/lib/libc++abi.dylib'
                cmake.configure(source_dir='../../%s/projects/libcxx' % self.source_dir,
                                build_dir='.')
                cmake.build()
                cmake.install()

        with tools.chdir(self.install_dir):
            with tools.chdir('bin'):
                if platform.system() == 'Darwin':
                    self.run('rm clang')
                    self.run('mv clang-3.3 clang')
            with tools.chdir('lib'):
                if platform.system() == 'Darwin':
                    self.run('rm libclang.dylib')
                    self.run('mv libclang.3.3.dylib libclang.dylib')
                    self.run('rm libc++.dylib')
                    self.run('mv libc++.1.0.dylib libc++.dylib')
                self.output.info(self.libs)
                VuoUtils.fixLibs(self.libs, self.deps_cpp_info, False)

            with tools.chdir('bin'):
                VuoUtils.fixExecutables(self.executables, self.libs, self.deps_cpp_info, False)

    def package(self):
        if platform.system() == 'Darwin':
            libext = 'dylib'
        elif platform.system() == 'Linux':
            libext = 'so'

        self.copy('*', src='%s/include'  % self.install_dir, dst='include')

        for f in list(self.libs.keys()):
            self.copy('lib%s.%s' % (f, libext), src='%s/lib' % self.install_dir, dst='lib')
        # Yes, these are include files that need to be copied to the lib folder.
        self.copy('*', src='%s/lib/clang/%s/include' % (self.install_dir, self.source_version), dst='lib/clang/%s/include' % self.source_version)

        for f in self.executables:
            self.copy(f, src='%s/bin' % self.install_dir, dst='bin', symlinks=True)

        self.copy('%s.txt' % self.name, src=self.source_dir, dst='license')
        self.copy('%s-systemsupport.txt' % self.name, src=self.source_dir, dst='license')
        self.copy('clang.txt', src=self.source_dir, dst='license')

    def package_info(self):
        self.cpp_info.libs = list(self.libs.keys())
        if platform.system() == 'Darwin':
            self.cpp_info.libs += ['/usr/lib/libc++abi.dylib', '/usr/lib/libSystem.dylib']
            self.cpp_info.sharedlinkflags = ['-L/usr/lib']

        self.cpp_info.includedirs = ['include', 'include/c++/v1/']
