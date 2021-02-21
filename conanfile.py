from conans import ConanFile, CMake, tools
import shutil
import os
import platform

class LlvmConan(ConanFile):
    name = 'llvm'

    source_version = '5.0.2'
    source_version_major_minor = '5.0'
    package_version = '5'
    version = '%s-%s' % (source_version, package_version)

    build_requires = 'vuoutils/1.2@vuo/stable'
    settings = 'os', 'compiler', 'build_type', 'arch'
    url = 'https://github.com/vuo/conan-llvm'
    license = 'http://releases.llvm.org/%s/LICENSE.TXT' % source_version
    description = 'A collection of modular and reusable compiler and toolchain technologies'
    source_dir  = 'llvm-%s.src' % source_version

    build_llvm_x86_dir = '_build_llvm_x86'
    build_llvm_arm_dir = '_build_llvm_arm'
    build_libcxx_x86_dir = '_build_libcxx_x86'
    build_libcxx_arm_dir = '_build_libcxx_arm'
    install_x86_dir = '_install_x86'
    install_arm_dir = '_install_arm'
    install_universal_dir = '_install_universal'

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
        'LLVMDlltoolDriver': source_version_major_minor,
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
        'LLVMSymbolize': source_version_major_minor,
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
            self.build_requires('macos-sdk/11.0-0@vuo/stable')

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

        # https://reviews.llvm.org/D38141
        tools.patch(patch_file='tsan.patch', base_path=self.source_dir)

        # https://b33p.net/kosada/vuo/vuo/-/issues/18112
        # https://reviews.llvm.org/D47898
        tools.patch(patch_file='mapping-to-a-source-type.patch', base_path=self.source_dir)

        if platform.system() == 'Linux':
            tools.patch(patch_file='linux-offsetof.patch', base_path=self.source_dir)

        self.run('cp %s/LICENSE.TXT %s/%s.txt' % (self.source_dir, self.source_dir, self.name))
        self.run('cp %s/include/llvm/Support/LICENSE.TXT %s/%s-systemsupport.txt' % (self.source_dir, self.source_dir, self.name))
        self.run('cp %s/tools/clang/LICENSE.TXT %s/clang.txt' % (self.source_dir, self.source_dir))

    def build(self):
        cmake = CMake(self)

        cmake.definitions['CMAKE_BUILD_TYPE'] = 'Release'
        cmake.definitions['CMAKE_C_FLAGS'] = '-O3'
        cmake.definitions['CMAKE_CXX_FLAGS'] = cmake.definitions['CMAKE_C_FLAGS'] + ' -stdlib=libc++'
        cmake.definitions['CMAKE_CXX_STANDARD'] = '11'
        cmake.definitions['CMAKE_CXX_STANDARD_REQUIRED'] = 'ON'
        cmake.definitions['BUILD_CLANG_FORMAT_VS_PLUGIN'] = 'OFF'
        cmake.definitions['BUILD_SHARED_LIBS'] = 'ON'
        cmake.definitions['DARWIN_ios_ARCHS'] = ''
        cmake.definitions['DARWIN_iossim_ARCHS'] = ''
        cmake.definitions['COMPILER_RT_ENABLE_IOS'] = 'OFF'
        cmake.definitions['COMPILER_RT_ENABLE_TVOS'] = 'OFF'
        cmake.definitions['COMPILER_RT_ENABLE_WATCHOS'] = 'OFF'
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
        cmake.definitions['LLVM_USE_FOLDERS'] = 'ON'
        cmake.definitions['LLVM_USE_INTEL_JITEVENTS'] = 'OFF'
        cmake.definitions['LLVM_USE_OPROFILE'] = 'OFF'


        self.output.info("=== Build LLVM and Clang to run on x86_64 and generate both x86_64 and arm64 code ===")
        cmake.definitions['CMAKE_C_COMPILER']   = '/usr/bin/clang'
        cmake.definitions['CMAKE_CXX_COMPILER'] = '/usr/bin/clang++'
        cmake.definitions['CMAKE_CROSSCOMPILING'] = 'OFF'
        cmake.definitions['CMAKE_INSTALL_PREFIX'] = '%s/%s' % (os.getcwd(), self.install_x86_dir)
        cmake.definitions['CMAKE_OSX_ARCHITECTURES'] = 'x86_64'
        cmake.definitions['CMAKE_OSX_DEPLOYMENT_TARGET'] = '10.11'
        cmake.definitions['CMAKE_OSX_SYSROOT'] = self.deps_cpp_info['macos-sdk'].rootpath
        cmake.definitions['LLVM_DEFAULT_TARGET_TRIPLE'] = 'x86_64-apple-macos10.11.0'
        cmake.definitions['LLVM_TARGET_ARCH'] = 'host'
        tools.mkdir(self.build_llvm_x86_dir)
        with tools.chdir(self.build_llvm_x86_dir):
            cmake.configure(source_dir='../%s' % self.source_dir,
                            build_dir='.')
            cmake.build()
            cmake.install()


        self.output.info("=== Build libc++ for x86_64 ===")
        tools.mkdir(self.build_libcxx_x86_dir)
        with tools.chdir(self.build_libcxx_x86_dir):
            cmake.configure(source_dir='../%s/projects/libcxx' % self.source_dir,
                            build_dir='.')
            cmake.build()
            cmake.install()


        self.output.info("=== Build LLVM and Clang to run on arm64 and generate both x86_64 and arm64 code ===")
        # https://llvm.org/docs/HowToCrossCompileLLVM.html
        cmake.definitions['CMAKE_C_COMPILER']   = '%s/%s/bin/clang' % (os.getcwd(), self.install_x86_dir)
        cmake.definitions['CMAKE_CXX_COMPILER'] = '%s++' % cmake.definitions['CMAKE_C_COMPILER']
        cmake.definitions['CMAKE_CROSSCOMPILING'] = 'ON'
        cmake.definitions['CMAKE_INSTALL_PREFIX'] = '%s/%s' % (os.getcwd(), self.install_arm_dir)
        cmake.definitions['CMAKE_OSX_ARCHITECTURES'] = 'arm64'
        cmake.definitions['LLVM_DEFAULT_TARGET_TRIPLE'] = 'arm64-apple-macos10.11.0'
        cmake.definitions['LLVM_TARGET_ARCH'] = 'AArch64'
        # tblgen needs to run on the host, so it should be x86 even when cross-compiling for arm.
        cmake.definitions['LLVM_TABLEGEN'] = '%s/%s/bin/llvm-tblgen' % (os.getcwd(), self.build_llvm_x86_dir)
        cmake.definitions['CLANG_TABLEGEN'] = '%s/%s/bin/clang-tblgen' % (os.getcwd(), self.build_llvm_x86_dir)
        flags = ' -target arm64-apple-macos10.11.0'
        cmake.definitions['CMAKE_C_FLAGS'] += flags
        cmake.definitions['CMAKE_CXX_FLAGS'] += flags
        tools.mkdir(self.build_llvm_arm_dir)
        with tools.chdir(self.build_llvm_arm_dir):
            cmake.configure(source_dir='../%s' % self.source_dir,
                            build_dir='.')
            cmake.build()
            cmake.install()


        self.output.info("=== Build libc++ for arm64 ===")
        cmake.definitions['LLVM_CONFIG_PATH'] = '%s/%s/bin/llvm-config' % (os.getcwd(), self.install_x86_dir)
        tools.mkdir(self.build_libcxx_arm_dir)
        with tools.chdir(self.build_libcxx_arm_dir):
            cmake.configure(source_dir='../%s/projects/libcxx' % self.source_dir,
                            build_dir='.')
            cmake.build()
            cmake.install()


    def package(self):
        import VuoUtils
        tools.mkdir(self.install_universal_dir)
        with tools.chdir(self.install_universal_dir):
            tools.mkdir('lib')
            with tools.chdir('lib'):
                self.run('lipo -create ../../%s/lib/libc++.1.0.dylib ../../%s/lib/libc++.1.0.dylib -output libc++.dylib' % (self.install_x86_dir, self.install_arm_dir))
                otherLibs = self.libs.copy()
                del otherLibs['c++']
                for f in otherLibs:
                    self.run('lipo -create ../../%s/lib/lib%s.dylib ../../%s/lib/lib%s.dylib -output lib%s.dylib' % (self.install_x86_dir, f, self.install_arm_dir, f, f))
                VuoUtils.fixLibs(self.libs, self.deps_cpp_info)
                for f in self.libs:
                    self.run('codesign --sign - lib%s.dylib' % f)

            tools.mkdir('bin')
            with tools.chdir('bin'):
                self.run('lipo -create ../../%s/bin/clang-%s ../../%s/bin/clang-%s -output clang' % (
                    self.install_x86_dir, self.source_version_major_minor,
                    self.install_arm_dir, self.source_version_major_minor))
                self.run('ln -s clang clang++')
                otherExecutables = self.executables.copy()
                otherExecutables.remove('clang')
                otherExecutables.remove('clang++')
                for f in otherExecutables:
                    self.run('lipo -create ../../%s/bin/%s ../../%s/bin/%s -output %s' % (
                        self.install_x86_dir, f,
                        self.install_arm_dir, f,
                        f))
                VuoUtils.fixExecutables(self.executables, self.libs, self.deps_cpp_info)

                # Ad-hoc sign everything (except clang++, which is a symlink to clang).
                self.run('codesign --sign - clang')
                for f in otherExecutables:
                    self.run('codesign --sign - %s' % f)

        self.copy('*', src='%s/include'  % self.install_x86_dir, dst='include')
        for f in list(self.libs.keys()):
            self.copy('lib%s.dylib' % f, src='%s/lib' % self.install_universal_dir, dst='lib')
        self.copy('*', src='%s/lib/clang/%s/lib/darwin' % (self.install_x86_dir, self.source_version), dst='lib/clang/%s/lib/darwin' % self.source_version)
        # Yes, these are include files that need to be copied to the lib folder.
        self.copy('*', src='%s/lib/clang/%s/include' % (self.install_x86_dir, self.source_version), dst='lib/clang/%s/include' % self.source_version)

        for f in self.executables:
            self.copy(f, src='%s/bin' % self.install_universal_dir, dst='bin', symlinks=True)

        self.copy('%s.txt' % self.name, src=self.source_dir, dst='license')
        self.copy('%s-systemsupport.txt' % self.name, src=self.source_dir, dst='license')
        self.copy('clang.txt', src=self.source_dir, dst='license')

    def package_info(self):
        self.cpp_info.libs = list(self.libs.keys())
        self.cpp_info.includedirs = ['include', 'include/c++/v1/']
