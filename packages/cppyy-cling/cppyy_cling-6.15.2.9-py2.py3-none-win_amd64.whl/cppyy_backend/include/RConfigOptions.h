#ifndef ROOT_RConfigOptions
#define ROOT_RConfigOptions

#define R__CONFIGUREOPTIONS   "CMAKE_CXX_STANDARD_LIBRARIES=kernel32.lib user32.lib gdi32.lib winspool.lib shell32.lib ole32.lib oleaut32.lib uuid.lib comdlg32.lib advapi32.lib CMAKE_C_STANDARD_LIBRARIES=kernel32.lib user32.lib gdi32.lib winspool.lib shell32.lib ole32.lib oleaut32.lib uuid.lib comdlg32.lib advapi32.lib ZLIB_INCLUDE_DIR=C:/Users/wlav/Test/cppyy-backend/cling/src/builtins/zlib ZLIB_INCLUDE_DIRS=C:/Users/wlav/Test/cppyy-backend/cling/src/builtins/zlib ZLIB_LIBRARIES=ZLIB::ZLIB ZLIB_LIBRARY=$<TARGET_FILE:ZLIB> xxHash_INCLUDE_DIR=C:/Users/wlav/Test/cppyy-backend/cling/src/builtins/xxhash xxHash_INCLUDE_DIRS=C:/Users/wlav/Test/cppyy-backend/cling/src/builtins/xxhash xxHash_LIBRARIES=xxHash::xxHash xxHash_LIBRARY=$<TARGET_FILE:xxhash> "
#define R__CONFIGUREFEATURES  " builtin_freetype builtin_llvm builtin_clang builtin_pcre builtin_xxhash builtin_zlib cling cxx14 explicitlink thread"

#endif
