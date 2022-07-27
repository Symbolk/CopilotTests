#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright 1995-2022 by Rebecca Ann Heineman becky@burgerbecky.com

# It is released under an MIT Open Source license. Please see LICENSE
# for license details. Yes, you can use it in a
# commercial title without paying anything, just give me a credit.
# Please? It's not like I'm asking you for money!

"""
Sub file for makeprojects.
Handler for Apple Computer XCode projects

@package makeprojects.xcode
This module contains classes needed to generate
project files intended for use by Apple's XCode IDE

@var makeprojects.xcode.TABS
Default tab format for XCode

@var makeprojects.xcode.TEMP_EXE_NAME
Build executable pathname

@var makeprojects.xcode._XCODESAFESET
Valid characters for XCode strings without quoting

@var makeprojects.xcode._PERFORCE_PATH
Path of the perforce executable

@var makeprojects.xcode.SUPPORTED_IDES
Supported IDE codes for the XCode exporter

@var makeprojects.xcode.OBJECT_VERSIONS
Version values

@var makeprojects.xcode.OBJECT_ORDER
Order of XCode objects

@var makeprojects.xcode.FLATTENED_OBJECTS
List of XCode objects that flatten their children

@var makeprojects.xcode.XCBUILD_FLAGS
List of XCBuildConfiguration settings for compilation

@var makeprojects.xcode.FILE_REF_LAST_KNOWN
Dictionary for mapping FileTypes to XCode file types

@var makeprojects.xcode.FILE_REF_DIR
Map of root directories
"""

# pylint: disable=consider-using-f-string
# pylint: disable=useless-object-inheritance
# pylint: disable=too-few-public-methods
# pylint: disable=invalid-name

from __future__ import absolute_import, print_function, unicode_literals

import hashlib
import os
import sys
import operator
import string
from re import compile as re_compile


_PBXPROJFILE_MATCH = re_compile('(?is).*\\.pbxproj\\Z')
_XCODEPROJFILE_MATCH = re_compile('(?is).*\\.xcodeproj\\Z')

_XCODE_SUFFIXES = (
    ('xc3', 3),
    ('xc4', 4),
    ('xc5', 5),
    ('xc6', 6),
    ('xc7', 7),
    ('xc8', 8),
    ('xc9', 9),
    ('x10', 10),
    ('x11', 11),
    ('x12', 12),
    ('x13', 13)
)

# Default tab format for XCode
TABS = '\t'

# Build executable pathname
TEMP_EXE_NAME = '${CONFIGURATION_BUILD_DIR}/${EXECUTABLE_NAME}'

# Valid characters for XCode strings without quoting
_XCODESAFESET = frozenset(string.ascii_letters + string.digits + '_$./')

# Path of the perforce executable
_PERFORCE_PATH = '/opt/local/bin/p4'

# Supported IDE codes for the XCode exporter
SUPPORTED_IDES = (
    IDETypes.xcode3,
    IDETypes.xcode4,
    IDETypes.xcode5,
    IDETypes.xcode6,
    IDETypes.xcode7,
    IDETypes.xcode8,
    IDETypes.xcode9,
    IDETypes.xcode10,
    IDETypes.xcode11,
    IDETypes.xcode12,
    IDETypes.xcode13)

# Tuple of objectVersion, , compatibilityVersion, developmentRegion
OBJECT_VERSIONS = {
    IDETypes.xcode3: ('45', None, 'Xcode 3.1', 'English'),
    IDETypes.xcode4: ('46', '0420', 'Xcode 3.2', 'English'),
    IDETypes.xcode5: ('46', '0510', 'Xcode 3.2', 'English'),
    IDETypes.xcode6: ('47', '0600', 'Xcode 6.3', None),
    IDETypes.xcode7: ('47', '0700', 'Xcode 6.3', None),
    IDETypes.xcode8: ('48', '0800', 'Xcode 8.0', None),
    IDETypes.xcode9: ('50', '0900', 'Xcode 9.3', None),
    IDETypes.xcode10: ('51', '1030', 'Xcode 10.0', None),
    IDETypes.xcode11: ('52', '1100', 'Xcode 11.0', None),
    IDETypes.xcode12: ('53', '1200', 'Xcode 12.0', None),
    IDETypes.xcode13: ('54', '1300', 'Xcode 13.0', None)
}

# This is the order of XCode chunks that match the way
# that XCode outputs them.
OBJECT_ORDER = (
    'PBXAggregateTarget',
    'PBXBuildFile',
    'PBXBuildRule',
    'PBXContainerItemProxy',
    'PBXCopyFilesBuildPhase',
    'PBXFileReference',
    'PBXFrameworksBuildPhase',
    'PBXGroup',
    'PBXNativeTarget',
    'PBXProject',
    'PBXReferenceProxy',
    'PBXResourcesBuildPhase',
    'PBXShellScriptBuildPhase',
    'PBXSourcesBuildPhase',
    'PBXTargetDependency',
    'XCBuildConfiguration',
    'XCConfigurationList'
)

# List of XCode objects that flatten their children
FLATTENED_OBJECTS = (
    'PBXBuildFile',
    'PBXFileReference'
)

# Name / type / default
XCBUILD_FLAGS = (
    # Locations of any sparse SDKs
    ('ADDITIONAL_SDKS', 'string', None),

    # Group permission of deployment
    ('ALTERNATE_GROUP', 'string', None),

    # File permissions of deployment
    ('ALTERNATE_MODE', 'string', None),

    # Owner permission of deployment
    ('ALTERNATE_OWNER', 'string', None),

    # Specific files to apply deployment permissions
    ('ALTERNATE_PERMISSIONS_FILES', 'string', None),

    # Always search user paths in C++
    ('ALWAYS_SEARCH_USER_PATHS', 'boolean', None),

    # Copy Files Build Phase will plist and strings to encoding
    ('APPLY_RULES_IN_COPY_FILES', 'boolean', None),

    # Default CPUs
    ('ARCHS', 'stringarray', None),

    # List of build variants
    ('BUILD_VARIANTS', 'stringarray', None),

    # Name of executable that loads the bundle
    ('BUNDLE_LOADER', 'string', None),

    # Name of the code signing certificate
    ('CODE_SIGN_IDENTITY', 'string', None),

    # Path to property list containing rules for signing
    ('CODE_SIGN_RESOURCE_RULES_PATH', 'string', None),

    # Path for build products
    ('CONFIGURATION_BUILD_DIR', 'string',
     '$(SYMROOT)/$(PRODUCT_NAME)$(SUFFIX)'),

    # Path for temp files
    ('CONFIGURATION_TEMP_DIR', 'string',
     '$(SYMROOT)/$(PRODUCT_NAME)$(SUFFIX)'),

    # Does copying preserve classic mac resource forks?
    ('COPYING_PRESERVES_HFS_DATA', 'boolean', None),

    # Strip debug symbols?
    ('COPY_PHASE_STRIP', 'boolean', None),

    # Numeric project version
    ('CURRENT_PROJECT_VERSION', 'string', None),

    # Strip dead code?
    ('DEAD_CODE_STRIPPING', 'boolean', 'YES'),

    # Type of debug symbols
    ('DEBUG_INFORMATION_FORMAT', 'string', 'dwarf'),

    # Are there valid deployment location settings?
    ('DEPLOYMENT_LOCATION', 'boolean', None),

    # Process deployment files
    ('DEPLOYMENT_POSTPROCESSING', 'boolean', None),

    # Destination root folder for deployment
    ('DSTROOT', 'string', None),

    # Compatible version of the dynamic library
    ('DYLIB_COMPATIBILITY_VERSION', 'string', None),

    # Numeric version of the dynamic library
    ('DYLIB_CURRENT_VERSION', 'string', None),

    # Enable OpenMP
    ('ENABLE_OPENMP_SUPPORT', 'boolean', None),

    # Files and folders to ignore on search.
    ('EXCLUDED_RECURSIVE_SEARCH_PATH_SUBDIRECTORIES', 'string', None),

    # Extension for executables
    ('EXECUTABLE_EXTENSION', 'string', None),

    # Prefix for executables
    ('EXECUTABLE_PREFIX', 'string', None),

    # File with symbols to export
    ('EXPORTED_SYMBOLS_FILE', 'string', None),

    # Array of directories to search for Frameworks
    ('FRAMEWORK_SEARCH_PATHS', 'stringarray', None),

    # Version of the framework being generated
    ('FRAMEWORK_VERSION', 'string', None),

    # PowerPC only, enable altivec
    ('GCC_ALTIVEC_EXTENSIONS', 'boolean', None),

    # Enable vectorization on loops
    ('GCC_AUTO_VECTORIZATION', 'boolean', None),

    # Default 'char' to unsigned if set to true
    ('GCC_CHAR_IS_UNSIGNED_CHAR', 'boolean', None),

    # It true, assume no exceptions on new()
    ('GCC_CHECK_RETURN_VALUE_OF_OPERATOR_NEW', 'boolean', None),

    # Use CodeWarrior inline assembly syntax
    ('GCC_CW_ASM_SYNTAX', 'boolean', 'YES'),

    # Use the latest version of the Objective C++ dialect
    ('GCC_C_LANGUAGE_STANDARD', 'string', 'gnu99'),

    # Sets the level of debugging symbols in the output
    ('GCC_DEBUGGING_SYMBOLS', 'string', None),

    # Set YES for no relocatable code
    ('GCC_DYNAMIC_NO_PIC', 'boolean', 'NO'),
    ('GCC_DYNAMIC_NO_PIC[arch=i386]', 'boolean', 'YES'),
    ('GCC_DYNAMIC_NO_PIC[arch=ppc64]', 'boolean', 'YES'),
    ('GCC_DYNAMIC_NO_PIC[arch=ppc]', 'boolean', 'YES'),

    # Enable the asm keyword
    ('GCC_ENABLE_ASM_KEYWORD', 'boolean', None),

    # Enable built in functions like memcpy().
    ('GCC_ENABLE_BUILTIN_FUNCTIONS', 'boolean', None),

    # Disable CPP Exceptions
    ('GCC_ENABLE_CPP_EXCEPTIONS', 'boolean', 'NO'),

    # Disable CPP RTTI
    ('GCC_ENABLE_CPP_RTTI', 'boolean', 'NO'),

    # Build everything as Objective C++
    ('GCC_INPUT_FILETYPE', 'string', 'sourcecode.cpp.objcpp'),

    # Program flow for profiling.
    ('GCC_INSTRUMENT_PROGRAM_FLOW_ARCS', 'boolean', None),

    # Link with static to dynamic libraries
    ('GCC_LINK_WITH_DYNAMIC_LIBRARIES', 'boolean', None),

    # Enable 64 bit registers for powerpc 64 bit
    ('GCC_MODEL_PPC64', 'boolean', 'NO'),
    ('GCC_MODEL_PPC64[arch=ppc64]', 'boolean', 'YES'),

    # Tune for specific cpu
    ('GCC_MODEL_TUNING', 'string', 'G4'),
    ('GCC_MODEL_TUNING[arch=ppc64]', 'string', 'G5'),

    # Don't share global variables
    ('GCC_NO_COMMON_BLOCKS', 'boolean', None),

    # Call C++ constuctors on objective-c code
    ('GCC_OBJC_CALL_CXX_CDTORS', 'boolean', None),

    # bool takes one byte, not 4
    ('GCC_ONE_BYTE_BOOL', 'boolean', None),

    # Optimizations level
    ('GCC_OPTIMIZATION_LEVEL', 'string', 's'),

    # C++ dialects
    ('GCC_PFE_FILE_C_DIALECTS', 'string', None),

    # Use a precompiled header
    ('GCC_PRECOMPILE_PREFIX_HEADER', 'boolean', None),

    # Name of the precompiled header
    ('GCC_PREFIX_HEADER', 'string', None),

    # Defines
    ('GCC_PREPROCESSOR_DEFINITIONS', 'stringarray', None),

    # Disabled defines
    ('GCC_PREPROCESSOR_DEFINITIONS_NOT_USED_IN_PRECOMPS', 'string', None),

    # Reuse constant strings
    ('GCC_REUSE_STRINGS', 'boolean', None),

    # Shorten enums
    ('GCC_SHORT_ENUMS', 'boolean', None),

    # Use strict aliasing
    ('GCC_STRICT_ALIASING', 'boolean', None),

    # Assume extern symbols are private
    ('GCC_SYMBOLS_PRIVATE_EXTERN', 'boolean', None),

    # Don't emit code to make the static constructors thread safe
    ('GCC_THREADSAFE_STATICS', 'boolean', 'NO'),

    # Causes warnings about missing function prototypes to become errors
    ('GCC_TREAT_IMPLICIT_FUNCTION_DECLARATIONS_AS_ERRORS', 'boolean', None),

    # Non conformant code errors become warnings.
    ('GCC_TREAT_NONCONFORMANT_CODE_ERRORS_AS_WARNINGS', 'boolean', None),

    # Warnings are errors
    ('GCC_TREAT_WARNINGS_AS_ERRORS', 'boolean', None),

    # Enable unrolling loops
    ('GCC_UNROLL_LOOPS', 'boolean', None),

    # Allow native prcompiling support
    ('GCC_USE_GCC3_PFE_SUPPORT', 'boolean', None),

    # Default to using a register for all function calls
    ('GCC_USE_INDIRECT_FUNCTION_CALLS', 'boolean', None),

    # Default to long calls
    ('GCC_USE_REGISTER_FUNCTION_CALLS', 'boolean', None),

    # Allow searching default system include folders.
    ('GCC_USE_STANDARD_INCLUDE_SEARCHING', 'boolean', None),

    # Which compiler to use
    ('GCC_VERSION', 'string', 'com.apple.compilers.llvm.clang.1_0'),

    # Note: com.apple.compilers.llvmgcc42 generates BAD CODE for ppc64 and 4.2
    # doesn't work at all for ppc64. Only gcc 4.0 is safe for ppc64
    # i386 compiler llvmgcc42 has issues with 64 bit code in xcode3
    ('GCC_VERSION[sdk=macosx10.4]', 'string', 'com.apple.compilers.llvmgcc42'),
    ('GCC_VERSION[sdk=macosx10.5]', 'string', 'com.apple.compilers.llvmgcc42'),
    ('GCC_VERSION[sdk=macosx10.5][arch=i386]', 'string', '4.2'),
    ('GCC_VERSION[sdk=macosx10.5][arch=ppc64]', 'string', '4.0'),

    # Warn of 64 bit value become 32 bit automatically
    ('GCC_WARN_64_TO_32_BIT_CONVERSION', 'boolean', 'YES'),

    # Warn about deprecated functions
    ('GCC_WARN_ABOUT_DEPRECATED_FUNCTIONS', 'boolean', None),

    # Warn about invalid use of offsetof()
    ('GCC_WARN_ABOUT_INVALID_OFFSETOF_MACRO', 'boolean', None),

    # Warn about missing ending newline in source code.
    ('GCC_WARN_ABOUT_MISSING_NEWLINE', 'boolean', None),

    # Warn about missing function prototypes
    ('GCC_WARN_ABOUT_MISSING_PROTOTYPES', 'boolean', 'YES'),

    # Warn if the sign of a pointer changed.
    ('GCC_WARN_ABOUT_POINTER_SIGNEDNESS', 'boolean', 'YES'),

    # Warn if return type is missing a value.
    ('GCC_WARN_ABOUT_RETURN_TYPE', 'boolean', 'YES'),

    # Objective-C Warn if required methods are missing in class implementation
    ('GCC_WARN_ALLOW_INCOMPLETE_PROTOCOL', 'boolean', 'YES'),

    # Warn if a switch statement is missing enumeration entries
    ('GCC_WARN_CHECK_SWITCH_STATEMENTS', 'boolean', 'YES'),

    # Warn if Effective C++ violations are present.
    ('GCC_WARN_EFFECTIVE_CPLUSPLUS_VIOLATIONS', 'boolean', None),

    # Warn is macOS stype 'APPL' 4 character constants exist.
    ('GCC_WARN_FOUR_CHARACTER_CONSTANTS', 'boolean', None),

    # Warn if virtual functions become hidden.
    ('GCC_WARN_HIDDEN_VIRTUAL_FUNCTIONS', 'boolean', 'YES'),

    # Disable all warnings.
    ('GCC_WARN_INHIBIT_ALL_WARNINGS', 'boolean', None),

    # Warn if union initializers are not fully bracketed.
    ('GCC_WARN_INITIALIZER_NOT_FULLY_BRACKETED', 'boolean', 'NO'),

    # Warn if parentheses are missing from nested statements.
    ('GCC_WARN_MISSING_PARENTHESES', 'boolean', 'YES'),

    # Warn if a class didn't declare its destructor as virtual if derived.
    ('GCC_WARN_NON_VIRTUAL_DESTRUCTOR', 'boolean', 'YES'),

    # Warn if non-C++ standard keywords are used
    ('GCC_WARN_PEDANTIC', 'boolean', None),

    # Warn if implict type conversions occur.
    ('GCC_WARN_PROTOTYPE_CONVERSION', 'boolean', 'YES'),

    # Warn if a variable becomes shadowed.
    ('GCC_WARN_SHADOW', 'boolean', 'YES'),

    # Warn if signed and unsigned values are compared.
    ('GCC_WARN_SIGN_COMPARE', 'boolean', None),

    # Validate printf() and scanf().
    ('GCC_WARN_TYPECHECK_CALLS_TO_PRINTF', 'boolean', 'YES'),

    # Warn if a variable is clobbered by setjmp() or not initialized.
    ('GCC_WARN_UNINITIALIZED_AUTOS', 'boolean', 'YES'),

    # Warn if a pragma is used that's not know by this compiler.
    ('GCC_WARN_UNKNOWN_PRAGMAS', 'boolean', None),

    # Warn if a static function is never used.
    ('GCC_WARN_UNUSED_FUNCTION', 'boolean', 'YES'),

    # Warn if a label is declared but not used.
    ('GCC_WARN_UNUSED_LABEL', 'boolean', 'YES'),

    # Warn if a function parameter isn't used.
    ('GCC_WARN_UNUSED_PARAMETER', 'boolean', 'YES'),

    # Warn if a value isn't used.
    ('GCC_WARN_UNUSED_VALUE', 'boolean', 'YES'),

    # Warn if a variable isn't used.
    ('GCC_WARN_UNUSED_VARIABLE', 'boolean', 'YES'),

    # Merge object files into a single file (static libraries)
    ('GENERATE_MASTER_OBJECT_FILE', 'boolean', None),

    # Force generating a package information file
    ('GENERATE_PKGINFO_FILE', 'boolean', None),

    # Insert profiling code
    ('GENERATE_PROFILING_CODE', 'boolean', 'NO'),

    # List of search paths for headers
    ('HEADER_SEARCH_PATHS', 'stringarray', None),

    # Directories for recursive search
    ('INCLUDED_RECURSIVE_SEARCH_PATH_SUBDIRECTORIES', 'string', None),

    # Expand the build settings in the plist file
    ('INFOPLIST_EXPAND_BUILD_SETTINGS', 'boolean', None),

    # Name of the plist file
    ('INFOPLIST_FILE', 'string', None),

    # Preprocessor flags for the plist file
    ('INFOPLIST_OTHER_PREPROCESSOR_FLAGS', 'string', None),

    # Output file format for the plist
    ('INFOPLIST_OUTPUT_FORMAT', 'string', None),

    # Prefix header for plist
    ('INFOPLIST_PREFIX_HEADER', 'string', None),

    # Allow preprocessing of the plist file
    ('INFOPLIST_PREPROCESS', 'boolean', None),

    # Defines for the plist file
    ('INFOPLIST_PREPROCESSOR_DEFINITIONS', 'stringarray', None),

    # Initialization routine name
    ('INIT_ROUTINE', 'string', None),

    # BSD group to attach for the installed executable
    ('INSTALL_GROUP', 'string', None),

    # File mode flags for installed executable
    ('INSTALL_MODE_FLAG', 'string', None),

    # Owner account for installed executable
    ('INSTALL_OWNER', 'string', None),

    # Path for installed executable
    ('INSTALL_PATH', 'string', None),

    # Keep private externs private
    ('KEEP_PRIVATE_EXTERNS', 'boolean', None),

    # Change the interal  name of the dynamic library
    ('LD_DYLIB_INSTALL_NAME', 'string', None),

    # Generate a map file for dynamic libraries
    ('LD_GENERATE_MAP_FILE', 'boolean', None),

    # Path for the map file
    ('LD_MAP_FILE_PATH', 'string', None),

    # Flags to pass to a library using OpenMP
    ('LD_OPENMP_FLAGS', 'string', None),

    # List of paths to search for a library
    ('LD_RUNPATH_SEARCH_PATHS', 'string', None),

    # List of directories to search for libraries
    ('LIBRARY_SEARCH_PATHS', 'stringarray', None),

    # Display mangled names in linker
    ('LINKER_DISPLAYS_MANGLED_NAMES', 'boolean', None),

    # Link the standard libraries
    ('LINK_WITH_STANDARD_LIBRARIES', 'boolean', None),

    # Type of Mach-O file
    ('MACH_O_TYPE', 'string', 'mh_execute'),

    # Deployment minimum OS
    ('MACOSX_DEPLOYMENT_TARGET', 'string', '10.4'),

    # Kernel module name
    ('MODULE_NAME', 'string', None),

    # Kernel driver start function name
    ('MODULE_START', 'string', None),

    # Kernel driver stop function name
    ('MODULE_STOP', 'string', None),

    # Version number of the kernel driver
    ('MODULE_VERSION', 'string', None),

    # Root folder for intermediate files
    ('OBJROOT', 'string', 'temp'),

    # If YES, only build the active CPU for fast recompilation
    ('ONLY_ACTIVE_ARCH', 'boolean', 'NO'),

    # Path to file for order of functions to link
    ('ORDER_FILE', 'string', None),

    # Extra flags to pass to the C compiler
    ('OTHER_CFLAGS', 'string', None),

    # Extra flags to pass to the code sign tool
    ('OTHER_CODE_SIGN_FLAGS', 'string', None),

    # Extra flags to pass to the C++ compiler
    ('OTHER_CPLUSPLUSFLAGS', 'string', None),

    # Extra flags to pass to the linker
    ('OTHER_LDFLAGS', 'stringarray', None),

    # Extra flags to pass to the unit test tool
    ('OTHER_TEST_FLAGS', 'string', None),

    # Output file format for the plist file
    ('PLIST_FILE_OUTPUT_FORMAT', 'string', None),

    # Prebind the functions together
    ('PREBINDING', 'boolean', 'YES'),

    # Include headers included in precompiler header
    ('PRECOMPS_INCLUDE_HEADERS_FROM_BUILT_PRODUCTS_DIR', 'boolean', None),

    # Flags to pass for pre-linker
    ('PRELINK_FLAGS', 'string', None),

    # Libraries to use for pre-linking
    ('PRELINK_LIBS', 'string', None),

    # Don't deleate dead code initializers
    ('PRESERVE_DEAD_CODE_INITS_AND_TERMS', 'boolean', None),

    # Path to copy private headers for building
    ('PRIVATE_HEADERS_FOLDER_PATH', 'string', None),

    # Product name
    ('PRODUCT_NAME', 'string', '$(TARGET_NAME)'),

    # Path to copy public headers for building
    ('PUBLIC_HEADERS_FOLDER_PATH', 'string', None),

    # Paths to search for rez
    ('REZ_SEARCH_PATHS', 'string', None),

    # Scan source code for include files for dependency graph generation.
    ('SCAN_ALL_SOURCE_FILES_FOR_INCLUDES', 'boolean', None),

    # SDK to use to for this build
    ('SDKROOT', 'string', 'macosx10.5'),

    # Flags for the section reordering
    ('SECTORDER_FLAGS', 'string', None),

    # Strip symbols in a seperate pass
    ('SEPARATE_STRIP', 'boolean', None),

    # Edit symbols with nmedit
    ('SEPARATE_SYMBOL_EDIT', 'boolean', None),

    # Path for directory for precompiled header files
    ('SHARED_PRECOMPS_DIR', 'string', None),

    # Skip the install phase in deployment
    ('SKIP_INSTALL', 'boolean', None),

    # Type of libary for Standard C
    ('STANDARD_C_PLUS_PLUS_LIBRARY_TYPE', 'string', None),

    # Encoding for Strings file for localization
    ('STRINGS_FILE_OUTPUT_ENCODING', 'string', 'UTF-8'),

    # Flags to pass to the symbol stripper
    ('STRIPFLAGS', 'string', None),

    # Set to YES to strip symbols from installed product
    ('STRIP_INSTALLED_PRODUCT', 'boolean', None),

    # Style of symbol stripping
    ('STRIP_STYLE', 'string', None),

    # Custom label for configuration short code
    ('SUFFIX', 'string', 'osxrel'),

    # Products are placed in this folder
    ('SYMROOT', 'string', 'temp'),

    # Path to the executable that accepts unit test bundles
    ('TEST_HOST', 'string', None),

    # Path to unit test tool
    ('TEST_RIG', 'string', None),

    # Path to file with symbols to NOT export
    ('UNEXPORTED_SYMBOLS_FILE', 'string', None),

    # Paths to user headers
    ('USER_HEADER_SEARCH_PATHS', 'string', None),

    # List of allowable cpu architectures
    ('VALID_ARCHS', 'string', None),

    # Name of the executable that creates the version info.
    ('VERSIONING_SYSTEM', 'string', None),

    # User name of the invoker of the version tool
    ('VERSION_INFO_BUILDER', 'string', None),

    # Allow exporting the version information
    ('VERSION_INFO_EXPORT_DECL', 'string', None),

    # Name of the file for version information
    ('VERSION_INFO_FILE', 'string', None),

    # Version info prefix
    ('VERSION_INFO_PREFIX', 'string', None),

    # Version info suffix
    ('VERSION_INFO_SUFFIX', 'string', None),

    # List of additional warning flags to pass to the compiler.
    ('WARNING_CFLAGS', 'stringarray', None),

    # List of additional warning flags to pass to the linker.
    ('WARNING_LDFLAGS', 'stringarray', None),

    # Extension for product wrappers
    ('WRAPPER_EXTENSION', 'string', None)
)

########################################


def parse_xcodeproj_file(full_pathname):
    """
    Extract configurations from an XCode project file.

    Given a .xcodeproj directory for XCode for macOS
    locate and extract all of the build targets
    available and return the list.

    Args:
        full_pathname: Pathname to the .xcodeproj folder
    Returns:
        list of configuration strings
    See Also:
        build_xcode
    """

    # Start with an empty list

    targetlist = []
    try:
        if PY2:
            # pylint: disable=unspecified-encoding
            with open(full_pathname, "r") as filep:
                projectfile = filep.read().splitlines()
        else:
            with open(full_pathname, "r", encoding="utf-8") as filep:
                projectfile = filep.read().splitlines()

    except IOError as error:
        print(str(error), file=sys.stderr)
        return targetlist

    configurationfound = False
    for line in projectfile:
        # Look for this section. Immediately after it
        # has the targets
        if configurationfound is False:
            if 'buildConfigurations' in line:
                configurationfound = True
        else:
            # Once the end of the section is reached, end
            if ');' in line:
                break
            # Format 1DEB923608733DC60010E9CD /* Debug */,
            # The third entry is the data needed
            targetlist.append(line.rsplit()[2])

    # Exit with the results
    return targetlist

########################################




def test_parse_xcodeproj_file():
"""Check the correctness of parse_xcodeproj_file
"""
    assert 