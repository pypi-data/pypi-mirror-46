#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Configuration file on how to build and clean projects in a specific folder.

This file is parsed by the cleanme, buildme, rebuildme and makeprojects
command line tools to clean, build and generate project files.
"""

from __future__ import absolute_import, print_function, unicode_literals

from makeprojects.enums import PlatformTypes, IDETypes

########################################


def rules(command, working_directory, root=True):
    """
    Main entry point for build_rules.py.

    When makeprojects, cleanme, or buildme is executed, they will call this
    function to perform the actions required for build customization.

    The parameter working_directory is required, and if it has no default
    parameter, this function will only be called with the folder that this
    file resides in. If there is a default parameter of None, it will be called with
    any folder that it is invoked on. If the default parameter is a directory, this
    function will only be called if that directory is desired.

    The optional parameter of root alerts the tool if subsequent processing of other
    build_rules.py files are needed or if set to have a default parameter of True, processing
    will end once the calls to this rules() function are completed.

    Commands are 'build', 'clean', 'prebuild', 'postbuild', 'project', 'configurations'

    Arg:
        command: Command to execute.
        working_directory: Directory for this function to clean
        root: If set to True, exit cleaning upon completion of this function
    Return:
        Zero on success, non-zero on failure, and a list for 'configurations'

    """

    # The command clean will clean the current directory of any
    # files that aren't cleaned by IDE project files.
    if command == 'clean':
        # Call functions to delete files and / or folders
        pass

        # Examples are as follows

        # Remove these directories
        # burger.clean_directories(
        #    working_directory,
        #    ('Release', 'Debug', 'temp', '*_Data', '* Data', '__pycache__'),
        #    recursive=False)

        # Recursively remove files
        # burger.clean_files(
        #    working_directory,
        #    ('.DS_Store', '*.suo', '*.user', '*.ncb', '*.err', '*.sdf', '*.layout.cbTemp',
        #     '*.VC.db', '*.pyc', '*.pyo'),
        #    recursive=True)

        # Check if the directory has a codeblocks project file and clean
        # codeblocks extra files
        # burger.clean_codeblocks(working_directory)

        # Allow purging user data in XCode project directories
        # burger.clean_xcode(working_directory)

        # Purge data for setup.py
        # burger.clean_setup_py(working_directory)

        # Return error code or zero if no errors

    elif command == 'prebuild':
        # Perform actions before building any IDE based projects
        pass

    elif command == 'build':
        # Perform actions to build
        pass

    elif command == 'postbuild':
        # Perform actions after all IDE based projects
        pass

    elif command == 'generate':
        # Perform project generation instead of the automatic system
        pass

    elif command == 'configurations':
        # Return the list of default configurations
        results = [
            'Debug',
            'Internal',
            'Release'
        ]

        #if platform == PlatformTypes.xbox360:
        #    results.extend([
        #        'Profile',
        #        'Release_LTCG',
        #        'CodeAnalysis',
        #        'Profile_FastCap'
        #    ])
        return results

    elif command == 'settings':
        # Return the settings for a specific project
        pass

    return 0

########################################

def project_rules(working_directory, configuration, platform, ide, root=True):
    """
    Return the rules to create a project file for a specific configuration.

    When the command 'makeprojects' is executed, this will generate all
    of the extra hints needed to properly generate a build file
    for popular IDEs.
    """

    result = dict()

    # Files to include
    result['files'] = ['*.c', '*.cpp', '*.h', '*.inl']

    # Files to exclude
    result['exclude'] = []

    # Extra directories for "include"
    result['include_folders'] = []

    # Extra directories for libraries
    result['library_folders'] = []

    # Debug/Release
    if configuration in ('Debug', 'Internal'):
        result['defines'] = ['_DEBUG=1']
    else:
        result['defines'] = ['NDEBUG=1']

    if configuration in ('Release', 'Internal', 'Profile'):
        result['optimization'] = 4
    else:
        result['optimization'] = 0

    if configuration in ('Profile', 'Profile_FastCap'):
        result['profile'] = True

    if configuration == 'Release_LTCG':
        result['link_time_code_generation'] = True

    # Windows specific defines
    if platform.is_windows():
        result['defines'].extend(['_WINDOWS', 'WIN32_LEAN_AND_MEAN', '_CRT_SECURE_NO_WARNINGS'])
        if platform == PlatformTypes.win64:
            result['defines'].append('WIN64')
        else:
            result['defines'].append('WIN32')
        result['UseOfMfc'] = False
        result['UseOfAtl'] = False
        result['CLRSupport'] = False
        result['CharacterSet'] = 'Unicode'

        if configuration == 'Release':
            if platform == PlatformTypes.win64:
                result['deploy_folder'] = '$(BURGER_SDKS)\\window\\bin\\x64'
            elif platform == PlatformTypes.win32:
                result['deploy_folder'] = '$(BURGER_SDKS)\\window\\bin\\x86'

    # Playstation 4
    if platform == PlatformTypes.ps4:
        result['defines'].append('__ORBIS2__')

    # Playstation Vita
    if platform == PlatformTypes.vita:
        result['defines'].append('SN_TARGET_PSP2')

    # Android targets
    if platform.is_android():
        result['defines'].append('DISABLE_IMPORTGL')

    # Xbox 360
    if platform == PlatformTypes.xbox360:
        result['defines'].extend(['_XBOX', 'XBOX'])

    # Mac Carbon
    if platform.is_macos_carbon():
        result['defines'].append('TARGET_API_MAC_CARBON=1')

    # Nintendo DSI specific defines
    if platform == PlatformTypes.dsi:
        result['defines'].extend(
            ['NN_BUILD_DEBUG',
             'NN_COMPILER_RVCT',
             'NN_COMPILER_RVCT_VERSION_MAJOR=$(CTRSDK_RVCT_VER_MAJOR)',
             'NN_PROCESSOR_ARM',
             'NN_PROCESSOR_ARM11MPCORE',
             'NN_PROCESSOR_ARM_V6',
             'NN_PROCESSOR_ARM_VFP_V2',
             'NN_HARDWARE_CTR',
             'NN_PLATFORM_CTR',
             'NN_HARDWARE_CTR_TS',
             'NN_SYSTEM_PROCESS',
             'NN_SWITCH_ENABLE_HOST_IO=1',
             'NN_BUILD_VERBOSE',
             'NN_BUILD_NOOPT',
             'NN_DEBUGGER_KMC_PARTNER'])

    # Linux platform
    if platform == PlatformTypes.linux:
        result['defines'].append('__LINUX__')
        if configuration == 'Release':
            result['deploy_folder'] = '$(BURGER_SDKS)\\linux\\bin'

    # macOS X platform
    if platform.is_macosx():
        if configuration == 'Release':
            result['deploy_folder'] = '$(BURGER_SDKS)\\macosx\\bin'
        result['frameworks'] = [
            'AppKit.framework',
            'AudioToolbox.framework',
            'AudioUnit.framework',
            'Carbon.framework',
            'Cocoa.framework',
            'CoreAudio.framework',
            'IOKit.framework',
            'OpenGL.framework',
            'QuartzCore.framework',
            'SystemConfiguration.framework'
        ]

    # iOS platform
    if platform.is_ios():
        result['frameworks'] = [
            'AVFoundation.framework',
            'CoreGraphics.framework',
            'CoreLocation.framework',
            'Foundation.framework',
            'QuartzCore.framework',
            'UIKit.framework'
        ]

    return result
