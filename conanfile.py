from conans import ConanFile, tools, AutoToolsBuildEnvironment
import shutil
import os

class LlvmConan(ConanFile):
    name = 'llvm'

    source_version = '3.4.2'
    source_version_major_minor = '3.4'
    package_version = '1'
    version = '%s-%s' % (source_version, package_version)

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

    def source(self):
        tools.get('http://llvm.org/releases/%s/llvm-%s.src.tar.gz' % (self.source_version, self.source_version),
                  sha256='17038d47069ad0700c063caed76f0c7259628b0e79651ce2b540d506f2f1efd7')
        tools.get('http://llvm.org/releases/%s/cfe-%s.src.tar.gz' % (self.source_version, self.source_version),
                  sha256='5ba6f5772f8d00f445209356a7daf83c5bca2da5acd10de517ad2359ae95bc10')
        shutil.move('cfe-%s.src' % self.source_version, '%s/tools/clang' % self.source_dir)

        # https://b33p.net/kosada/node/7848#comment-32297
        tools.patch(patch_file='disable-unused-intrinsics.patch', base_path=self.source_dir)

    def build(self):
        tools.mkdir(self.build_dir)
        with tools.chdir(self.build_dir):
            autotools = AutoToolsBuildEnvironment(self)
            autotools.flags.append('-march=x86-64')
            # gcc-4.2 says `error: Unknown value '10.10' of -mmacosx-version-min`, so extend back to 10.9
            autotools.flags.append('-mmacosx-version-min=10.9')
            autotools.link_flags.append('-Wl,-macosx_version_min,10.9')
            env_vars = {
                'CC' : '/usr/bin/clang',
                'CXX': '/usr/bin/clang++',
            }
            with tools.environment_append(env_vars):
                autotools.configure(configure_dir='../%s' % self.source_dir,
                                    args=['--quiet',
                                          '--enable-shared',
                                          '--disable-static'
                                          '--enable-cxx11',
                                          '--disable-jit',
                                          '--disable-docs',
                                          '--enable-optimized',
                                          '--with-optimize-option=-O3',
                                          '--disable-bindings',
                                          '--enable-targets=x86_64',
                                          '--prefix=%s/../%s' % (os.getcwd(), self.install_dir)])
                autotools.make(args=['install'])
                with tools.chdir('tools/clang'):
                    autotools.make(args=['install'])
        with tools.chdir(self.install_dir):
            self.run('install_name_tool -id @rpath/%s lib/%s' % (self.llvm_dylib, self.llvm_dylib))
            self.run('install_name_tool -id @rpath/libLTO.dylib lib/libLTO.dylib')
            self.run('install_name_tool -change @executable_path/../lib/%s @rpath/%s lib/libLTO.dylib' % (self.llvm_dylib, self.llvm_dylib))

    def package(self):
        self.copy('*', src='%s/include/llvm'  % self.install_dir, dst='include/llvm')
        self.copy('*', src='%s/include/llvm-c'% self.install_dir, dst='include/llvm-c')
        self.copy('*', src='%s/include/clang' % self.install_dir, dst='include/clang')

        self.copy(self.llvm_dylib,       src='%s/lib' % self.install_dir, dst='lib')
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
