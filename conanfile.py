from conans import ConanFile, tools, AutoToolsBuildEnvironment
import shutil
import os

class LlvmConan(ConanFile):
    name = 'llvm'

    source_version = '3.2'
    package_version = '2'
    version = '%s-%s' % (source_version, package_version)

    settings = 'os', 'compiler', 'build_type', 'arch'
    url = 'https://github.com/vuo/conan-llvm'
    license = 'http://releases.llvm.org/3.2/LICENSE.TXT'
    description = 'A collection of modular and reusable compiler and toolchain technologies'
    source_dir  = 'llvm-%s.src' % source_version
    build_dir = '_build'
    install_dir = '_install'
    llvm_dylib_base = 'LLVM-%ssvn' % source_version
    llvm_dylib = 'lib%s.dylib' % llvm_dylib_base

    def source(self):
        tools.get('http://llvm.org/releases/%s/llvm-%s.src.tar.gz' % (self.source_version, self.source_version),
                  sha256='125090c4d26740f1d5e9838477c931ed7d9ad70d599ba265f46f3a42cb066343')
        tools.get('http://llvm.org/releases/%s/clang-%s.src.tar.gz' % (self.source_version, self.source_version),
                  sha256='2aaaf03f7c0f6b16fe97ecc81247dc2bf2d4bec7620a77cc74670b7e07ff5658')
        shutil.move('clang-%s.src' % self.source_version, '%s/tools/clang' % self.source_dir)

        tools.download('https://b33p.net/sites/default/files/llvm-disable-unused-intrinsics_1.patch', 'llvm-disable-unused-intrinsics_1.patch')
        tools.check_sha256('llvm-disable-unused-intrinsics_1.patch', 'f5a5f89e3eb4160a43f224451473d21dc542eb89f6b541b7c6f8b29dca23156d')
        tools.patch(patch_file='llvm-disable-unused-intrinsics_1.patch', base_path=self.source_dir)
            
    def build(self):
        tools.mkdir(self.build_dir)
        with tools.chdir(self.build_dir):
            autotools = AutoToolsBuildEnvironment(self)
            autotools.flags.append('-march=x86-64')
            autotools.flags.append('-mmacosx-version-min=10.10')
            autotools.link_flags.append('-Wl,-macosx_version_min,10.10')
            env_vars = {
                'CC' : '/usr/bin/clang',
                'CXX': '/usr/bin/clang++',
            }
            with tools.environment_append(env_vars):
                autotools.configure(configure_dir='../%s' % self.source_dir,
                                    args=['--quiet',
                                          '--enable-shared',
                                          '--disable-static',
                                          '--enable-optimized',

                                          # When built with clang-900.0.39.2:
                                          # -Oz =  9M clang, 11M libLLVM*.dylib
                                          # -O3 = 14M clang, 14M libLLVM*.dylib
                                          # I haven't measured the performance difference yet, so I'm using the smaller one.
                                          '--with-optimize-option=-Oz',

                                          '--disable-bindings',
                                          '--enable-targets=host',
                                          '--prefix=%s/../%s' % (os.getcwd(), self.install_dir)])
                autotools.make(args=['install'])
                with tools.chdir('tools/clang'):
                    autotools.make(args=['install'])
        with tools.chdir(self.install_dir):
            self.run('install_name_tool -id @rpath/%s lib/%s' % (self.llvm_dylib, self.llvm_dylib))
            self.run('install_name_tool -id @rpath/libprofile_rt.dylib lib/libprofile_rt.dylib')
            self.run('install_name_tool -id @rpath/libLTO.dylib lib/libLTO.dylib')
            self.run('install_name_tool -change @executable_path/../lib/%s @rpath/%s lib/libLTO.dylib' % (self.llvm_dylib, self.llvm_dylib))

    def package(self):
        self.copy('*',             src='%s/include/llvm'         %  self.install_dir,                       dst='include/llvm')
        self.copy('*',             src='%s/include/clang'        %  self.install_dir,                       dst='include/clang')

        self.copy(self.llvm_dylib,       src='%s/lib' % self.install_dir, dst='lib')
        self.copy('libprofile_rt.dylib', src='%s/lib' % self.install_dir, dst='lib')
        self.copy('libLTO.dylib',        src='%s/lib' % self.install_dir, dst='lib')
        # Yes, these are include files that need to be copied to the lib folder.
        self.copy('*',                   src='%s/lib/clang/%s/include' % (self.install_dir, self.source_version), dst='lib/clang/%s/include' % self.source_version)

        # There's also a clang dylib, but we need to use symbols which the dylib doesn't reexport, so we use the static libraries.
        self.copy('libclang*.a',   src='%s/lib' % self.install_dir, dst='lib')

        self.copy('llvm-link',     src='%s/bin' % self.install_dir, dst='bin')
        self.copy('clang',         src='%s/bin' % self.install_dir, dst='bin')
        self.copy('clang++',       src='%s/bin' % self.install_dir, dst='bin', symlinks=True)

    def package_info(self):
        self.cpp_info.libs = [
            self.llvm_dylib_base,
            'clangAnalysis',
            'clangAST',
            'clangBasic',
            'clangCodeGen',
            'clangDriver',
            'clangEdit',
            'clangFrontend',
            'clangLex',
            'clangParse',
            'clangSema',
            'clangSerialization',
        ]
