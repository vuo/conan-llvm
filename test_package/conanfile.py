from conans import ConanFile
import os
import platform

class LlvmTestConan(ConanFile):
    generators = 'qbs'

    def requirements(self):
        if platform.system() == 'Darwin':
            self.requires('ld64/242-2@vuo/stable')
        elif platform.system() != 'Linux':
            raise Exception('Unknown platform "%s"' % platform.system())

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

        self.run('qbs run -f "%s"' % self.source_folder)

        # Ensure we only link to system libraries.
        for f in [
            'bin/clang',
            'bin/clang++',
            'bin/llvm-link',
            'lib/libLLVM-3.3.%s' % libext,
        ]:
            self.output.info('Checking %s…' % f)
            if platform.system() == 'Darwin':
                self.run('! (otool -L ' + f + ' | tail +3 | egrep -v "^\s*(/usr/lib/|/System/)")')
                self.run('! (otool -l ' + f + ' | grep -A2 LC_RPATH | cut -d"(" -f1 | grep "\s*path" | egrep -v "^\s*path @(executable|loader)_path/")')
            elif platform.system() == 'Linux':
                self.run('! (ldd ' + f + ' | grep -v "^lib/" | grep "/" | egrep -v "(\s(/lib64/|(/usr)?/lib/x86_64-linux-gnu/)|test_package/build)")')
