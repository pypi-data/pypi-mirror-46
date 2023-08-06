#ifndef ROOT_RConfigOptions
#define ROOT_RConfigOptions

#define R__CONFIGUREOPTIONS   "Backtrace_INCLUDE_DIR=/usr/include DL_LIBRARY_PATH=/usr/lib/libdl.so LIBCLANG_LIBRARY_VERSION=5.0 LIBXML2_INCLUDE_DIR=/usr/include/libxml2 LIBXML2_LIBRARY=/usr/lib64/libxml2.so LLVM_INCLUDE_EXAMPLES=OFF LLVM_INCLUDE_RUNTIMES=ON LLVM_INCLUDE_TOOLS=ON LLVM_INCLUDE_UTILS=ON PC_LIBXML_INCLUDEDIR=/usr/include PC_LIBXML_INCLUDE_DIRS=/usr/include/libxml2 PC_LIBXML_LIBRARIES=xml2 PC_LIBXML_STATIC_INCLUDE_DIRS=/usr/include/libxml2 ZLIB_INCLUDE_DIR=/home/wlav/cppyy-dev/cppyy-backend/cling/src/builtins/zlib ZLIB_INCLUDE_DIRS=/home/wlav/cppyy-dev/cppyy-backend/cling/src/builtins/zlib ZLIB_LIBRARIES=ZLIB::ZLIB ZLIB_LIBRARY=$<TARGET_FILE:ZLIB> xxHash_INCLUDE_DIR=/home/wlav/cppyy-dev/cppyy-backend/cling/src/builtins/xxhash xxHash_INCLUDE_DIRS=/home/wlav/cppyy-dev/cppyy-backend/cling/src/builtins/xxhash xxHash_LIBRARIES=xxHash::xxHash xxHash_LIBRARY=$<TARGET_FILE:xxhash> "
#define R__CONFIGUREFEATURES  " builtin_llvm builtin_clang builtin_pcre builtin_xxhash builtin_zlib cling cxx17 explicitlink thread"

#endif
