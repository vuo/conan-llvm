from conans import ConanFile
import os

class LlvmTestConan(ConanFile):
    requires = 'ld64/242-2@vuo/stable'
    generators = 'qbs'

    def build(self):
        self.run('qbs -f "%s"' % self.source_folder)

    def imports(self):
        self.copy('*',       src='bin', dst='bin')
        self.copy('*.dylib', src='lib', dst='lib')
        self.copy('clang/*', src='lib', dst='lib')

    def test(self):
        self.run('qbs run')

        # Ensure we only link to system libraries.
        for f in [
            'bin/clang',
            'bin/clang++',
            'bin/llvm-link',
            'lib/libLLVM-3.3.dylib',
        ]:
            self.run('! (otool -L ' + f + ' | tail +3 | egrep -v "^\s*(/usr/lib/|/System/)")')
            self.run('! (otool -l ' + f + ' | grep -A2 LC_RPATH | cut -d"(" -f1 | grep "\s*path" | egrep -v "^\s*path @(executable|loader)_path/")')
