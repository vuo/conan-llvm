from conans import ConanFile
import os
import platform

class LlvmTestConan(ConanFile):
    generators = 'qbs'

    def build(self):
        self.run('qbs -f "%s"' % self.source_folder)

    def imports(self):
        self.copy('*', src='bin', dst='bin')
        self.copy('*', src='lib', dst='lib')

    def test(self):
        if platform.system() == 'Darwin':
            libext = 'dylib'
        elif platform.system() == 'Linux':
            libext = 'so'
        elif platform.system() == 'Windows':
            libext = 'dll'

        self.run('qbs run -f "%s"' % self.source_folder)

        # Ensure we only link to system libraries.
        for f in [
            'bin/clang',
            'bin/clang++',
            'bin/llvm-link',
        ]:
            self.output.info('Checking %s...' % f)
            if platform.system() == 'Darwin':
                self.run('! (otool -L ' + f + ' | tail +2 | egrep -v "^\s*(/usr/lib/|/System/|@rpath/)")')
                self.run('! (otool -L ' + f + ' | fgrep "libstdc++")')
                self.run('! (otool -l ' + f + ' | grep -A2 LC_RPATH | cut -d"(" -f1 | grep "\s*path" | egrep -v "^\s*path @(executable|loader)_path/")')
            elif platform.system() == 'Linux':
                self.run('! (ldd ' + f + ' | grep -v "^lib/" | grep "/" | egrep -v "(\s(/lib64/|(/usr)?/lib/x86_64-linux-gnu/)|test_package/build)")')
                self.run('! (ldd ' + f + ' | fgrep "libstdc++")')

        libs = self.deps_cpp_info['llvm'].libs
        libs.remove('c++abi')
        for f in libs:
            self.output.info('Checking %s...' % f)
            if platform.system() == 'Darwin':
                self.run('! (otool -L lib/lib' + f + '.dylib | tail +2 | egrep -v "^\s*(/usr/lib/|/System/|@rpath/)")')
                self.run('! (otool -L lib/lib' + f + '.dylib | fgrep "libstdc++")')
                self.run('! (otool -l lib/lib' + f + '.dylib | grep -A2 LC_RPATH | cut -d"(" -f1 | grep "\s*path" | egrep -v "^\s*path @(executable|loader)_path")')
            elif platform.system() == 'Linux':
                self.run('! (ldd lib/lib' + f + '.so | grep -v "^lib/" | grep "/" | egrep -v "(\s(/lib64/|(/usr)?/lib/x86_64-linux-gnu/)|test_package/build)")')
                self.run('! (ldd lib/lib' + f + '.so | fgrep "libstdc++")')
