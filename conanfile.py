from conans import ConanFile, CMake, tools
import shutil
import os
import platform

class LlvmConan(ConanFile):
    name = 'llvm'

    source_version = '5.0.2'
    source_version_major_minor = '5.0'
    package_version = '0'
    version = '%s-%s' % (source_version, package_version)

    build_requires = 'vuoutils/1.2@vuo/stable'
    settings = 'os', 'compiler', 'build_type', 'arch'
    url = 'https://github.com/vuo/conan-llvm'
    license = 'http://releases.llvm.org/%s/LICENSE.TXT' % source_version
    description = 'A collection of modular and reusable compiler and toolchain technologies'
    source_dir  = 'llvm-%s.src' % source_version
    build_dir = '_build'
    install_dir = '_install'
    llvm_dylib_base = 'LLVM-%s' % source_version_major_minor
    llvm_dylib = 'lib%s.dylib' % llvm_dylib_base
    exports_sources = '*.patch'
    libs = {
        'LLVMAArch64AsmParser': source_version_major_minor,
        'LLVMAArch64AsmPrinter': source_version_major_minor,
        'LLVMAArch64CodeGen': source_version_major_minor,
        'LLVMAArch64Desc': source_version_major_minor,
        'LLVMAArch64Disassembler': source_version_major_minor,
        'LLVMAArch64Info': source_version_major_minor,
        'LLVMAArch64Utils': source_version_major_minor,
        'LLVMAnalysis': source_version_major_minor,
        'LLVMAsmParser': source_version_major_minor,
        'LLVMAsmPrinter': source_version_major_minor,
        'LLVMBinaryFormat': source_version_major_minor,
        'LLVMBitReader': source_version_major_minor,
        'LLVMBitWriter': source_version_major_minor,
        'LLVMCodeGen': source_version_major_minor,
        'LLVMCore': source_version_major_minor,
        'LLVMCoroutines': source_version_major_minor,
        'LLVMCoverage': source_version_major_minor,
        'LLVMDebugInfoCodeView': source_version_major_minor,
        'LLVMDebugInfoDWARF': source_version_major_minor,
        'LLVMDebugInfoMSF': source_version_major_minor,
        'LLVMDebugInfoPDB': source_version_major_minor,
        'LLVMDemangle': source_version_major_minor,
        'LLVMExecutionEngine': source_version_major_minor,
        'LLVMGlobalISel': source_version_major_minor,
        'LLVMIRReader': source_version_major_minor,
        'LLVMInstCombine': source_version_major_minor,
        'LLVMInstrumentation': source_version_major_minor,
        'LLVMInterpreter': source_version_major_minor,
        'LLVMLTO': source_version_major_minor,
        'LLVMLibDriver': source_version_major_minor,
        'LLVMLinker': source_version_major_minor,
        'LLVMMC': source_version_major_minor,
        'LLVMMCDisassembler': source_version_major_minor,
        'LLVMMCJIT': source_version_major_minor,
        'LLVMMCParser': source_version_major_minor,
        'LLVMMIRParser': source_version_major_minor,
        'LLVMObjCARCOpts': source_version_major_minor,
        'LLVMObject': source_version_major_minor,
        'LLVMOption': source_version_major_minor,
        'LLVMOrcJIT': source_version_major_minor,
        'LLVMPasses': source_version_major_minor,
        'LLVMProfileData': source_version_major_minor,
        'LLVMRuntimeDyld': source_version_major_minor,
        'LLVMScalarOpts': source_version_major_minor,
        'LLVMSelectionDAG': source_version_major_minor,
        'LLVMSupport': source_version_major_minor,
        'LLVMTableGen': source_version_major_minor,
        'LLVMTarget': source_version_major_minor,
        'LLVMTransformUtils': source_version_major_minor,
        'LLVMVectorize': source_version_major_minor,
        'LLVMX86AsmParser': source_version_major_minor,
        'LLVMX86AsmPrinter': source_version_major_minor,
        'LLVMX86CodeGen': source_version_major_minor,
        'LLVMX86Desc': source_version_major_minor,
        'LLVMX86Disassembler': source_version_major_minor,
        'LLVMX86Info': source_version_major_minor,
        'LLVMX86Utils': source_version_major_minor,
        'LLVMipo': source_version_major_minor,
        'LTO': source_version_major_minor,
        'c++': source_version_major_minor,
        'clang': source_version_major_minor,
        'clangARCMigrate': source_version_major_minor,
        'clangAST': source_version_major_minor,
        'clangASTMatchers': source_version_major_minor,
        'clangAnalysis': source_version_major_minor,
        'clangBasic': source_version_major_minor,
        'clangCodeGen': source_version_major_minor,
        'clangDriver': source_version_major_minor,
        'clangEdit': source_version_major_minor,
        'clangFormat': source_version_major_minor,
        'clangFrontend': source_version_major_minor,
        'clangFrontendTool': source_version_major_minor,
        'clangIndex': source_version_major_minor,
        'clangLex': source_version_major_minor,
        'clangParse': source_version_major_minor,
        'clangRewrite': source_version_major_minor,
        'clangRewriteFrontend': source_version_major_minor,
        'clangSema': source_version_major_minor,
        'clangSerialization': source_version_major_minor,
        'clangStaticAnalyzerCheckers': source_version_major_minor,
        'clangStaticAnalyzerCore': source_version_major_minor,
        'clangStaticAnalyzerFrontend': source_version_major_minor,
        'clangTooling': source_version_major_minor,
        'clangToolingCore': source_version_major_minor,
    }
    executables = [
        'bugpoint',
        'clang',
        'clang++',
        'clang-check',
        'clang-format',
        'llc',
        'lli',
        'llvm-ar',
        'llvm-as',
        'llvm-bcanalyzer',
        'llvm-config',
        'llvm-cov',
        'llvm-diff',
        'llvm-dis',
        'llvm-dwarfdump',
        'llvm-extract',
        'llvm-link',
        'llvm-mc',
        'llvm-mcmarkup',
        'llvm-nm',
        'llvm-objdump',
        'llvm-ranlib',
        'llvm-readobj',
        'llvm-rtdyld',
        'llvm-size',
        'llvm-stress',
        'llvm-symbolizer',
        'llvm-tblgen',
        'opt',
    ]

    def requirements(self):
        if platform.system() == 'Linux':
            self.requires('patchelf/0.10pre-1@vuo/stable')
        elif platform.system() != 'Darwin':
            raise Exception('Unknown platform "%s"' % platform.system())

    def build_requirements(self):
        if platform.system() == 'Darwin':
            self.build_requires('macos-sdk/10.11-0@vuo/stable')

    def source(self):
        tools.get('https://releases.llvm.org/%s/llvm-%s.src.tar.xz' % (self.source_version, self.source_version),
                  sha256='d522eda97835a9c75f0b88ddc81437e5edbb87dc2740686cb8647763855c2b3c')

        tools.get('https://releases.llvm.org/%s/cfe-%s.src.tar.xz' % (self.source_version, self.source_version),
                  sha256='fa9ce9724abdb68f166deea0af1f71ca0dfa9af8f7e1261f2cae63c280282800')
        shutil.move('cfe-%s.src' % self.source_version, '%s/tools/clang' % self.source_dir)

        tools.get('https://releases.llvm.org/%s/libcxx-%s.src.tar.xz' % (self.source_version, self.source_version),
                  sha256='6edf88e913175536e1182058753fff2365e388e017a9ec7427feb9929c52e298')
        shutil.move('libcxx-%s.src' % self.source_version, '%s/projects/libcxx' % self.source_dir)

        tools.get('https://releases.llvm.org/%s/compiler-rt-%s.src.tar.xz' % (self.source_version, self.source_version),
                  sha256='3efe9ddf3f69e0c0a45cde57ee93911f36f3ab5f2a7f6ab8c8efb3db9b24ed46')
        shutil.move('compiler-rt-%s.src' % self.source_version, '%s/projects/compiler-rt' % self.source_dir)

        if platform.system() == 'Linux':
            tools.patch(patch_file='linux-offsetof.patch', base_path=self.source_dir)

        self.run('cp %s/LICENSE.TXT %s/%s.txt' % (self.source_dir, self.source_dir, self.name))
        self.run('cp %s/include/llvm/Support/LICENSE.TXT %s/%s-systemsupport.txt' % (self.source_dir, self.source_dir, self.name))
        self.run('cp %s/tools/clang/LICENSE.TXT %s/clang.txt' % (self.source_dir, self.source_dir))

    def build(self):
        import VuoUtils
        tools.mkdir(self.build_dir)
        with tools.chdir(self.build_dir):
            cmake = CMake(self)

            cmake.definitions['CMAKE_BUILD_TYPE'] = 'Release'
            cmake.definitions['CMAKE_C_FLAGS'] = '-O3 -march=x86-64'
            cmake.definitions['CMAKE_CXX_FLAGS'] = cmake.definitions['CMAKE_C_FLAGS'] + ' -std=c++11 -stdlib=libc++'
            cmake.definitions['CMAKE_INSTALL_PREFIX'] = '%s/../%s' % (os.getcwd(), self.install_dir)

            cmake.definitions['BUILD_CLANG_FORMAT_VS_PLUGIN'] = 'OFF'
            cmake.definitions['BUILD_SHARED_LIBS'] = 'ON'
            cmake.definitions['CLANG_BUILD_EXAMPLES'] = 'OFF'
            cmake.definitions['CLANG_DEFAULT_OPENMP_RUNTIME'] = 'libgomp'
            cmake.definitions['CLANG_ENABLE_ARCMT'] = 'ON'
            cmake.definitions['CLANG_ENABLE_STATIC_ANALYZER'] = 'ON'
            cmake.definitions['CLANG_INCLUDE_DOCS'] = 'OFF'
            cmake.definitions['CLANG_INCLUDE_TESTS'] = 'OFF'
            cmake.definitions['CLANG_PLUGIN_SUPPORT'] = 'OFF'
            cmake.definitions['LLVM_BUILD_32_BITS'] = 'OFF'
            cmake.definitions['LLVM_BUILD_EXAMPLES'] = 'OFF'
            cmake.definitions['LLVM_BUILD_RUNTIME'] = 'ON'
            cmake.definitions['LLVM_BUILD_TESTS'] = 'OFF'
            cmake.definitions['LLVM_BUILD_TOOLS'] = 'ON'
            cmake.definitions['LLVM_ENABLE_ASSERTIONS'] = 'ON'
            cmake.definitions['LLVM_ENABLE_BACKTRACES'] = 'OFF'
            cmake.definitions['LLVM_ENABLE_DOXYGEN'] = 'OFF'
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
            cmake.definitions['LLVM_INCLUDE_DOCS'] = 'OFF'
            cmake.definitions['LLVM_INCLUDE_EXAMPLES'] = 'OFF'
            cmake.definitions['LLVM_INCLUDE_GO_TESTS'] = 'OFF'
            cmake.definitions['LLVM_INCLUDE_TESTS'] = 'ON'
            cmake.definitions['LLVM_INCLUDE_TOOLS'] = 'ON'
            cmake.definitions['LLVM_LIT_ARGS'] = '-sv'
            cmake.definitions['LLVM_TARGETS_TO_BUILD'] = 'X86;AArch64'
            cmake.definitions['LLVM_TARGET_ARCH'] = 'host'
            cmake.definitions['LLVM_USE_FOLDERS'] = 'ON'
            cmake.definitions['LLVM_USE_INTEL_JITEVENTS'] = 'OFF'
            cmake.definitions['LLVM_USE_OPROFILE'] = 'OFF'

            if platform.system() == 'Darwin':
                cmake.definitions['CMAKE_C_FLAGS'] += ' -mmacosx-version-min=10.11'
                cmake.definitions['CMAKE_CXX_FLAGS'] += ' -mmacosx-version-min=10.11'
                cmake.definitions['CMAKE_C_COMPILER']   = '/usr/bin/clang'
                cmake.definitions['CMAKE_CXX_COMPILER'] = '/usr/bin/clang++'
                cmake.definitions['CMAKE_OSX_ARCHITECTURES'] = 'x86_64'
                cmake.definitions['CMAKE_OSX_DEPLOYMENT_TARGET'] = '10.11'
                cmake.definitions['CMAKE_OSX_SYSROOT'] = self.deps_cpp_info['macos-sdk'].rootpath
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
                cmake.configure(source_dir='../../%s/projects/libcxx' % self.source_dir,
                                build_dir='.')
                cmake.build()
                cmake.install()

        with tools.chdir(self.install_dir):
            with tools.chdir('bin'):
                self.run('rm clang')
                self.run('mv clang-%s clang' % self.source_version_major_minor)
            with tools.chdir('lib'):
                if platform.system() == 'Darwin':
                    self.run('rm libc++.dylib')
                    self.run('mv libc++.1.0.dylib libc++.dylib')
                elif platform.system() == 'Linux':
                    self.run('rm libclang.so')
                    self.run('mv libclang.so.%s libclang.so' % self.source_version_major_minor)
                    self.run('rm libc++.so')
                    self.run('mv libc++.so.1.0 libc++.so')
                VuoUtils.fixLibs(self.libs, self.deps_cpp_info)

            with tools.chdir('bin'):
                VuoUtils.fixExecutables(self.executables, self.libs, self.deps_cpp_info)

            if platform.system() == 'Linux':
                patchelf = self.deps_cpp_info['patchelf'].rootpath + '/bin/patchelf'
                self.run('%s --set-rpath "\$ORIGIN/../lib" bin/clang' % patchelf)
                self.run('%s --set-rpath "\$ORIGIN/../lib" bin/llvm-link' % patchelf)

    def package(self):
        if platform.system() == 'Darwin':
            libext = 'dylib'
        elif platform.system() == 'Linux':
            libext = 'so'

        self.copy('*', src='%s/include'  % self.install_dir, dst='include')

        for f in list(self.libs.keys()):
            self.copy('lib%s.%s' % (f, libext), src='%s/lib' % self.install_dir, dst='lib')
        self.copy('*', src='%s/lib/clang/%s/lib/darwin' % (self.install_dir, self.source_version), dst='lib/clang/%s/lib/darwin' % self.source_version)
        # Yes, these are include files that need to be copied to the lib folder.
        self.copy('*', src='%s/lib/clang/%s/include' % (self.install_dir, self.source_version), dst='lib/clang/%s/include' % self.source_version)

        for f in self.executables:
            self.copy(f, src='%s/bin' % self.install_dir, dst='bin', symlinks=True)

        self.copy('%s.txt' % self.name, src=self.source_dir, dst='license')
        self.copy('%s-systemsupport.txt' % self.name, src=self.source_dir, dst='license')
        self.copy('clang.txt', src=self.source_dir, dst='license')

    def package_info(self):
        self.cpp_info.libs = list(self.libs.keys())
        self.cpp_info.includedirs = ['include', 'include/c++/v1/']
