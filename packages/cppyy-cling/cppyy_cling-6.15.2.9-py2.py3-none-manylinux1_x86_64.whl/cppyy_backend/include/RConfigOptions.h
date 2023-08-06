#ifndef ROOT_RConfigOptions
#define ROOT_RConfigOptions

#define R__CONFIGUREOPTIONS   "ZLIB_INCLUDE_DIR=/root/cppyy-dev/cppyy-backend/cling/src/builtins/zlib ZLIB_INCLUDE_DIRS=/root/cppyy-dev/cppyy-backend/cling/src/builtins/zlib ZLIB_LIBRARIES=ZLIB::ZLIB ZLIB_LIBRARY=$<TARGET_FILE:ZLIB> xxHash_INCLUDE_DIR=/root/cppyy-dev/cppyy-backend/cling/src/builtins/xxhash xxHash_INCLUDE_DIRS=/root/cppyy-dev/cppyy-backend/cling/src/builtins/xxhash xxHash_LIBRARIES=xxHash::xxHash xxHash_LIBRARY=$<TARGET_FILE:xxhash> "
#define R__CONFIGUREFEATURES  " builtin_llvm builtin_clang builtin_pcre builtin_xxhash builtin_zlib cling cxx11 explicitlink thread"

#endif
