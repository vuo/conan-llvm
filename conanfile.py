from conans import ConanFile, tools, AutoToolsBuildEnvironment
import shutil
import os
import platform

class LlvmConan(ConanFile):
    name = 'llvm'

    source_version = '3.3'
    package_version = '3'
    version = '%s-%s' % (source_version, package_version)

    settings = 'os', 'compiler', 'build_type', 'arch'
    url = 'https://github.com/vuo/conan-llvm'
    license = 'http://releases.llvm.org/%s/LICENSE.TXT' % source_version
    description = 'A collection of modular and reusable compiler and toolchain technologies'
    source_dir  = 'llvm-%s.src' % source_version
    build_dir = '_build'
    install_dir = '_install'
    llvm_dylib_base = 'LLVM-%s' % source_version
    exports_sources = '*.patch'
    libs = (llvm_dylib_base, 'profile_rt', 'LTO')

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

        # https://b33p.net/kosada/node/7848#comment-32297
        tools.patch(patch_file='disable-unused-intrinsics.patch', base_path=self.source_dir)

        self.run('mv %s/LICENSE.TXT %s/%s.txt' % (self.source_dir, self.source_dir, self.name))
        self.run('mv %s/include/llvm/Support/LICENSE.TXT %s/%s-systemsupport.txt' % (self.source_dir, self.source_dir, self.name))
        self.run('mv %s/tools/clang/LICENSE.TXT %s/clang.txt' % (self.source_dir, self.source_dir))

    def build(self):
        tools.mkdir(self.build_dir)
        with tools.chdir(self.build_dir):
            autotools = AutoToolsBuildEnvironment(self)
            autotools.flags.append('-march=x86-64')

            if platform.system() == 'Darwin':
                # gcc-4.2 says `error: Unknown value '10.10' of -mmacosx-version-min`, so extend back to 10.9
                autotools.flags.append('-mmacosx-version-min=10.9')
                autotools.link_flags.append('-Wl,-macosx_version_min,10.9')
                env_vars = {
                    'CC' : '/usr/local/Cellar/apple-gcc42/4.2.1-5666.3/bin/gcc-4.2',
                    'CXX': '/usr/local/Cellar/apple-gcc42/4.2.1-5666.3/bin/g++-4.2',
                }
            elif platform.system() == 'Linux':
                env_vars = {
                    'CC' : '/usr/bin/clang-5.0',
                    'CXX': '/usr/bin/clang++-5.0',
                }

            with tools.environment_append(env_vars):
                args = ['--quiet',
                        '--enable-shared',
                        '--disable-static'
                        '--enable-cxx11',
                        '--disable-jit',
                        '--disable-docs',
                        '--enable-optimized',
                        '--with-optimize-option=-O3',
                        '--disable-bindings',
                        '--enable-targets=x86_64',
                        '--prefix=%s/../%s' % (os.getcwd(), self.install_dir)]
                if platform.system() == 'Linux':
                    args.append('--with-python=/usr/bin/python2')

                autotools.configure(configure_dir='../%s' % self.source_dir, args=args)
                autotools.make(args=['install'])
                with tools.chdir('tools/clang'):
                    autotools.make(args=['install'])
        with tools.chdir(self.install_dir):
            if platform.system() == 'Darwin':
                for f in self.libs:
                    self.run('install_name_tool -id @rpath/lib%s.dylib lib/lib%s.dylib' % (f, f))
                self.run('install_name_tool -change @executable_path/../lib/lib%s.dylib @rpath/lib%s.dylib lib/libLTO.dylib' % (self.llvm_dylib_base, self.llvm_dylib_base))
            elif platform.system() == 'Linux':
                patchelf = self.deps_cpp_info['patchelf'].rootpath + '/bin/patchelf'
                for f in self.libs:
                    self.run('%s --set-soname lib%s.so lib/lib%s.so' % (patchelf, f, f))

    def package(self):
        if platform.system() == 'Darwin':
            libext = 'dylib'
        elif platform.system() == 'Linux':
            libext = 'so'

        self.copy('*', src='%s/include/llvm'  % self.install_dir, dst='include/llvm')
        self.copy('*', src='%s/include/llvm-c'% self.install_dir, dst='include/llvm-c')
        self.copy('*', src='%s/include/clang' % self.install_dir, dst='include/clang')

        for f in self.libs:
            self.copy('lib%s.%s' % (f, libext), src='%s/lib' % self.install_dir, dst='lib')
        # Yes, these are include files that need to be copied to the lib folder.
        self.copy('*', src='%s/lib/clang/%s/include' % (self.install_dir, self.source_version), dst='lib/clang/%s/include' % self.source_version)

        # There's also a clang dylib, but we need to use symbols which the dylib doesn't reexport, so we use the static libraries.
        self.copy('libclang*.a',   src='%s/lib' % self.install_dir, dst='lib')

        self.copy('llvm-link',     src='%s/bin' % self.install_dir, dst='bin')
        self.copy('clang',         src='%s/bin' % self.install_dir, dst='bin')
        self.copy('clang++',       src='%s/bin' % self.install_dir, dst='bin', symlinks=True)

        self.copy('%s.txt' % self.name, src=self.source_dir, dst='license')
        self.copy('%s-systemsupport.txt' % self.name, src=self.source_dir, dst='license')
        self.copy('clang.txt', src=self.source_dir, dst='license')

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
