#include <stdio.h>

#define __STDC_CONSTANT_MACROS
#define __STDC_FORMAT_MACROS
#define __STDC_LIMIT_MACROS
#include <clang/Basic/Version.h>

int main()
{
	std::string v = clang::getClangFullVersion();
	printf("%s\n", v.c_str());
	return 0;
}
