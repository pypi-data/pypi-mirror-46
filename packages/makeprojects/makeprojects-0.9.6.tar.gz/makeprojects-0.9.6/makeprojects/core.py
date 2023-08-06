#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Module contains the core classes for makeproject.
"""

## \package makeprojects.core

from __future__ import absolute_import, print_function, unicode_literals
import os
import uuid
import operator
import burger
import makeprojects.visualstudio
import makeprojects.xcode
import makeprojects.codewarrior
import makeprojects.watcom
import makeprojects.codeblocks
import makeprojects.makefile
from makeprojects import FileTypes, ProjectTypes, \
    IDETypes, PlatformTypes, \
    SourceFile, Property
from .enums import configuration_short_code

########################################


class Configuration:
    """
    Object for containing attributes specific to a build configuration.

    This object contains all of the items needed to create a specific configuration of
    a project.

    See Also:
        Project, Solution
    """

    def __init__(self, configuration=None, platform=None, **kargs):

        if configuration is None:
            configuration = 'Debug'
        ## Name of the configuration.
        self.configuration = configuration

        ## Platform used for the configuration.
        self.platform = PlatformTypes.lookup(platform)
        if not self.platform:
            self.platform = PlatformTypes.default()

        ## Dictionary of attributes describing how to build this configuration.
        self.attributes = kargs

    def __repr__(self):
        """
        Convert the solultion record into a human readable description

        Returns:
            Human readable string or None if the solution is invalid
        """

        return 'Configuration: {}, Platform: {}, Attributes: {}'.format(
            self.configuration, str(self.platform), str(self.attributes))

    ## Allow str() to work.
    __str__ = __repr__


########################################


class Project:
    """
    Object for processing a project file.

    This object contains all of the items needed to create a project

    @note On most IDEs, this is merged into one file, but Visual Studio
    2010 and higher generates a project file for each project.
    """

    def __init__(self, name=None, project_type_name=None, suffix_enable=False):
        ## True if naming suffixes are enabled
        self.suffix_enable = suffix_enable

        ## Root directory (Default None)
        self.working_directory = os.getcwd()

        ## Type of project, tool is default ('tool', 'app', 'library')
        self.projecttype = ProjectTypes.lookup(project_type_name)
        if not self.projecttype:
            self.projecttype = ProjectTypes.default()

        ## Generic name for the project, 'project' is default
        if not name:
            name = 'project'
        self.projectname = name

        ## No parent solution yet
        self.solution = None

        ## Generate a windows project as a default
        self.platform = PlatformTypes.default()

        ## Generate the three default configurations
        self.configurations = [
            'Debug',
            'Internal',
            'Release']

        ## No special folder for the final binary
        self.deploy_folder = None

        ## Don't exclude any files
        self.exclude = []

        ## No special \#define for C/C++ code
        self.defines = []

        ## Properties used by generators
        self.properties = [
            Property(name="DEFINE", data="_DEBUG", configuration='Debug'),
            Property(name="DEFINE", data="_DEBUG", configuration='Internal'),
            Property(name="DEFINE", data="NDEBUG", configuration='Release'),
            Property(name="DEFINE", data="WIN32_LEAN_AND_MEAN", platform=PlatformTypes.windows),
            Property(name="DEFINE", data="WIN32", platform=PlatformTypes.win32),
            Property(name="DEFINE", data="WIN64", platform=PlatformTypes.win64)
        ]

        ## Scan at the current folder
        self.sourcefolders = ['.', 'source', 'src']

        ## No extra folders for include files
        self.includefolders = []

        ## Initial array of SourceFile in the solution
        self.codefiles = []

        ## Initial array of Project records that need to be built first
        self.dependentprojects = []

        ## Create default XCode object
        self.xcode = makeprojects.xcode.Defaults()

        ## Create default Codewarrior object
        self.codewarrior = makeprojects.codewarrior.Defaults()

        ## Create default Watcom object
        #self.watcom = makeprojects.watcom.Defaults()

        ## Create default Codeblocks object
        #self.codeblocks = makeprojects.codeblocks.Defaults()

        ## Create default Visual Studio object
        self.visualstudio = makeprojects.visualstudio.Defaults()

    def setconfigurations(self, configurations):
        """
        Set the names of the configurations this project will support.

        Given a string or an array of strings, replace the
        configurations with the new list.

        Args:
            self: The 'this' reference.
            configurations: String or an array of strings for the new configuration list.
        """

        # Force to a list
        self.configurations = burger.convert_to_array(configurations)

    def setplatform(self, platform):
        """
        Set the names of the configurations this project will support.

        Given a string or an array of strings, replace the
        configurations with the new list.

        Args:
            self: The 'this' reference.
            platform: Enumeration of PlatformTypes.
        """

        # Sanity check
        if not isinstance(platform, PlatformTypes):
            raise TypeError("parameter 'platform' must be of type PlatformTypes")
        self.platform = platform

    def adddependency(self, project):
        """
        Add a dependent project.
        """
        # Sanity check
        if not isinstance(project, Project):
            raise TypeError("parameter 'project' must be of type Project")
        self.dependentprojects.append(project)

    def __repr__(self):
        """
        Convert the solultion record into a human readable description

        Returns:
            Human readable string or None if the solution is invalid
        """

        return 'Project: {}, Working Directory: {}, Project Type: {}, ' \
            'Platform: {}, Configurations: {}, Deploy Folder: {}, Exclude: {}, ' \
            'Defines: {}, Properties: {}, Source Folders: {}, Include: {}, CodeFiles: {}'.format(
                str(self.projectname),
                self.working_directory, str(self.projecttype),
                str(self.platform),
                str(self.configurations),
                str(self.deploy_folder),
                str(self.exclude),
                str(self.defines),
                str(self.properties),
                str(self.sourcefolders),
                str(self.includefolders),
                str(self.codefiles))

    ## Allow str() to work.
    __str__ = __repr__


class Solution:
    """
    Object for processing a solution file.

    This object contains all of the items needed to create a solution.
    """

    def __init__(self, name=None, suffix_enable=True):
        ## Generic name for the project, 'project' is default
        if not name:
            name = 'project'
        self.name = name

        ## True if verbose output is requested (Default False)
        self.verbose = False

        ## True if naming suffixes are enabled
        self.suffix_enable = suffix_enable

        ## Root directory (Default None)
        self.working_directory = os.getcwd()

        ## Type of ide
        self.ide = IDETypes.default()

        ## Initial array of Project records for projects
        self.projects = []

        ## Create default XCode object
        self.xcode = makeprojects.xcode.Defaults()

        ## Create default Codewarrior object
        self.codewarrior = makeprojects.codewarrior.Defaults()

        ## Create default Visual Studio object
        self.visualstudio = makeprojects.visualstudio.Defaults()

    def add_project(self, project):
        """
        Add a project to the list of projects found in this solution.

        Given a new Project class instance, append it to the list of
        projects that this solution is managing.

        Args:
            self: The 'this' reference.
            project: Reference to an instance of a Project.
        """

        # Sanity check
        if not isinstance(project, Project):
            raise TypeError("parameter 'project' must be of type Project")

        project.solution = self
        self.projects.append(project)

    def generate(self, ide, platform):
        """
        Generate a project file and write it out to disk.
        """
        # Sanity check
        if not isinstance(ide, IDETypes):
            raise TypeError("parameter 'ide' must be of type IDETypes")

        self.projects[0].platform = platform

        if ide.is_windows():
            return makeprojects.visualstudio.generate(self, ide)
        return 10

    def processjson(self, myjson):
        r"""
        Given a json record process, all the sub sections.
        @details
        Given a dictionary created by a json file or manually update the solution to the new data.

        Acceptable keys
        * finalfolder = pathname to store final release binary.
        * 'kind' = 'tool', 'library', 'app'.
        * 'projectname' = Name of the project's filename (basename only)
        * 'platform' = 'windows', 'macosx', 'linux', 'ps3', 'ps4', 'vita', 'xbox',
        * 'xbox360', 'xboxone', 'shield', 'ios', 'mac', 'msdos', 'beos', 'ouya', 'wiiu', 'dsi'
        * 'configurations' = ['Debug', 'Release', 'Internal']
        * 'sourcefolders' = ['.','source']
        * 'exclude' = [] (List of files to exclude from processing)
        * 'defines' = [] (List of \#define to add to the project)
        * 'includefolders' = [] (List of folders to add for \#include )
        * 'xcode' = dir (Keys and values for special cases for xcode projects)
        * 'visualstudio' = dir (Keys and values for special cases for visual studio projects)

        Args:
            self: The 'this' reference.
            myjson: Dictionary with key value pairs.

        See Also:
            makeprojects.xcode, makeprojects.visualstudio
        """

        error = 0
        for key in myjson.keys():
            if key == 'finalfolder':
                if myjson[key] == "":
                    self.projects[0].deploy_folder = None
                else:
                    self.projects[0].deploy_folder = myjson[key]

            elif key == 'kind':
                # Convert json token to enumeration (Will assert if not enumerated)
                self.projects[0].projecttype = ProjectTypes[myjson[key]]
            elif key == 'projectname':
                self.name = myjson[key]
            elif key == 'platform':
                self.projects[0].platform = PlatformTypes[myjson[key]]

            elif key == 'configurations':
                self.projects[0].configurations = []
                for item in burger.convert_to_array(myjson[key]):
                    self.projects[0].configurations.append(item)
            elif key == 'sourcefolders':
                self.projects[0].sourcefolders = burger.convert_to_array(myjson[key])
            elif key == 'exclude':
                self.projects[0].exclude = burger.convert_to_array(myjson[key])
            elif key == 'defines':
                definelist = burger.convert_to_array(myjson[key])
                for item in definelist:
                    self.projects[0].properties.append(Property(name="DEFINE", data=item))
                self.projects[0].defines = definelist
            elif key == 'includefolders':
                self.projects[0].includefolders = burger.convert_to_array(myjson[key])

            #
            # Handle IDE specific data
            #

            elif key == 'xcode':
                error = self.xcode.loadjson(myjson[key])
            elif key == 'visualstudio':
                error = self.visualstudio.loadjson(myjson[key])
            elif key == 'codewarrior':
                error = self.codewarrior.loadjson(myjson[key])
            else:
                print('Unknown keyword "' + str(key) + '" with data "'
                      + str(myjson[key]) + '" found in json file')
                error = 1

            if error != 0:
                break

        return error

    #
    # The script is an array of objects containing solution settings
    # and a list of IDEs to output scripts
    #

    def process(self, myjson):
        error = 0
        for item in myjson:
            if isinstance(item, dict):
                error = self.processjson(item)
            elif item == 'vs2019':
                self.ide = IDETypes.vs2019
                error = makeprojects.visualstudio.generateold(self, IDETypes.vs2019)
            elif item == 'vs2017':
                self.ide = IDETypes.vs2017
                error = makeprojects.visualstudio.generateold(self, IDETypes.vs2017)
            elif item == 'vs2015':
                self.ide = IDETypes.vs2015
                error = makeprojects.visualstudio.generateold(self, IDETypes.vs2015)
            elif item == 'vs2013':
                self.ide = IDETypes.vs2013
                error = makeprojects.visualstudio.generateold(self, IDETypes.vs2013)
            elif item == 'vs2012':
                self.ide = IDETypes.vs2012
                error = makeprojects.visualstudio.generateold(self, IDETypes.vs2012)
            elif item == 'vs2010':
                self.ide = IDETypes.vs2010
                error = makeprojects.visualstudio.generateold(self, IDETypes.vs2010)
            elif item == 'vs2008':
                self.ide = IDETypes.vs2008
                error = createvs2008solution(self)
            elif item == 'vs2005':
                self.ide = IDETypes.vs2005
                error = createvs2005solution(self)
            elif item == 'xcode3':
                self.ide = IDETypes.xcode3
                error = makeprojects.xcode.generate(self)
            elif item == 'xcode4':
                self.ide = IDETypes.xcode4
                error = makeprojects.xcode.generate(self)
            elif item == 'xcode5':
                self.ide = IDETypes.xcode5
                error = makeprojects.xcode.generate(self)
            elif item == 'xcode6':
                self.ide = IDETypes.xcode6
                error = makeprojects.xcode.generate(self)
            elif item == 'xcode7':
                self.ide = IDETypes.xcode7
                error = makeprojects.xcode.generate(self)
            elif item == 'xcode8':
                self.ide = IDETypes.xcode8
                error = makeprojects.xcode.generate(self)
            elif item == 'xcode9':
                self.ide = IDETypes.xcode9
                error = makeprojects.xcode.generate(self)
            elif item == 'codewarrior9' or item == 'codewarrior50':
                self.ide = IDETypes.codewarrior50
                error = makeprojects.codewarrior.generate(self)
            elif item == 'codewarrior10' or item == 'codewarrior58':
                self.ide = IDETypes.codewarrior58
                error = makeprojects.codewarrior.generate(self)
            elif item == 'codewarrior59':
                self.ide = IDETypes.codewarrior59
                error = makeprojects.codewarrior.generate(self)
            elif item == 'codeblocks':
                self.ide = IDETypes.codeblocks
                error = makeprojects.codeblocks.generate(self)
            elif item == 'watcom':
                self.ide = IDETypes.watcom
                error = makeprojects.watcom.generate(self, perforce=True)
            elif item == 'makefile':
                self.ide = IDETypes.make
                error = makeprojects.makefile.generate(self, perforce=True)
            else:
                print('Saving ' + item + ' not implemented yet')
                error = 0
            if error:
                break
        return error

    #
    # Handle the command line case
    # by creating a phony json file and passing it
    # in for processing
    #

    def processcommandline(self, args):

        #
        # Fake json file and initialization record
        #

        dictrecord = dict()

        #
        # Use the work folder name as the project name
        #

        dictrecord['projectname'] = os.path.basename(self.working_directory)

        configurations = []
        if args.debug is True:
            configurations.append('Debug')
        if args.internal is True:
            configurations.append('Internal')
        if args.release is True:
            configurations.append('Release')
        if not configurations:
            configurations = [
                'Debug',
                'Internal',
                'Release']

        #
        # Only allow finalfolder when release builds are made
        #

        if not 'Release' in configurations:
            args.deploy_folder = False

        dictrecord['configurations'] = configurations

        #
        # Lib, app or tool?
        #

        if args.app is True:
            kind = 'app'
        elif args.library is True:
            kind = 'library'
        else:
            kind = 'tool'
        dictrecord['kind'] = kind

        #
        # Where to find the source
        #

        dictrecord['sourcefolders'] = ['.', 'source/*.*']

        #
        # Save the initializer in a fake json record
        # list
        #

        myjson = [dictrecord]

        #
        # Xcode projects assume a macosx platform
        # unless directed otherwise
        #

        if args.xcode3 is True:
            initializationrecord = dict()
            initializationrecord['platform'] = 'macosx'
            if args.deploy_folder:
                initializationrecord['finalfolder'] = makeprojects.xcode.DEFAULT_FINAL_FOLDER
            myjson.append(initializationrecord)
            myjson.append('xcode3')

        if args.xcode4 is True:
            initializationrecord = dict()
            initializationrecord['platform'] = 'macosx'
            if args.deploy_folder:
                initializationrecord['finalfolder'] = makeprojects.xcode.DEFAULT_FINAL_FOLDER
            myjson.append(initializationrecord)
            myjson.append('xcode4')

        if args.xcode5 is True:
            initializationrecord = dict()
            initializationrecord['platform'] = 'macosx'
            if args.deploy_folder:
                initializationrecord['finalfolder'] = makeprojects.xcode.DEFAULT_FINAL_FOLDER
            myjson.append(initializationrecord)
            myjson.append('xcode5')

        if args.xcode6 is True:
            initializationrecord = dict()
            initializationrecord['platform'] = 'macosx'
            if args.deploy_folder:
                initializationrecord['finalfolder'] = makeprojects.xcode.DEFAULT_FINAL_FOLDER
            myjson.append(initializationrecord)
            myjson.append('xcode6')

        if args.xcode7 is True:
            initializationrecord = dict()
            initializationrecord['platform'] = 'macosx'
            if args.deploy_folder:
                initializationrecord['finalfolder'] = makeprojects.xcode.DEFAULT_FINAL_FOLDER
            myjson.append(initializationrecord)
            myjson.append('xcode7')

        if args.xcode8 is True:
            initializationrecord = dict()
            initializationrecord['platform'] = 'macosx'
            if args.deploy_folder:
                initializationrecord['finalfolder'] = makeprojects.xcode.DEFAULT_FINAL_FOLDER
            myjson.append(initializationrecord)
            myjson.append('xcode8')

        if args.xcode9 is True:
            initializationrecord = dict()
            initializationrecord['platform'] = 'macosx'
            if args.deploy_folder:
                initializationrecord['finalfolder'] = makeprojects.xcode.DEFAULT_FINAL_FOLDER
            myjson.append(initializationrecord)
            myjson.append('xcode9')

        #
        # These are windows only
        #

        if args.vs2005 is True:
            initializationrecord = dict()
            initializationrecord['platform'] = 'windows'
            myjson.append(initializationrecord)
            myjson.append('vs2005')

        if args.vs2008 is True:
            initializationrecord = dict()
            initializationrecord['platform'] = 'windows'
            myjson.append(initializationrecord)
            myjson.append('vs2008')

        if args.vs2010 is True:
            initializationrecord = dict()
            initializationrecord['platform'] = 'windows'
            if args.deploy_folder:
                initializationrecord['finalfolder'] = makeprojects.visualstudio.DEFAULT_FINAL_FOLDER
            myjson.append(initializationrecord)
            myjson.append('vs2010')

        if args.vs2012 is True:
            initializationrecord = dict()
            initializationrecord['platform'] = 'windows'
            if args.deploy_folder:
                initializationrecord['finalfolder'] = makeprojects.visualstudio.DEFAULT_FINAL_FOLDER
            myjson.append(initializationrecord)
            myjson.append('vs2012')

        if args.vs2013 is True:
            initializationrecord = dict()
            initializationrecord['platform'] = 'windows'
            if args.deploy_folder:
                initializationrecord['finalfolder'] = makeprojects.visualstudio.DEFAULT_FINAL_FOLDER
            myjson.append(initializationrecord)
            myjson.append('vs2013')

        if args.vs2015 is True:
            initializationrecord = dict()
            initializationrecord['platform'] = 'windows'
            if args.deploy_folder:
                initializationrecord['finalfolder'] = makeprojects.visualstudio.DEFAULT_FINAL_FOLDER
            myjson.append(initializationrecord)
            myjson.append('vs2015')

        if args.vs2017 is True:
            initializationrecord = dict()
            initializationrecord['platform'] = 'windows'
            if args.deploy_folder:
                initializationrecord['finalfolder'] = makeprojects.visualstudio.DEFAULT_FINAL_FOLDER
            myjson.append(initializationrecord)
            myjson.append('vs2017')

        if args.vs2019 is True:
            initializationrecord = dict()
            initializationrecord['platform'] = 'windows'
            if args.deploy_folder:
                initializationrecord['finalfolder'] = makeprojects.visualstudio.DEFAULT_FINAL_FOLDER
            myjson.append(initializationrecord)
            myjson.append('vs2019')

        if args.codeblocks is True:
            initializationrecord = dict()
            initializationrecord['platform'] = 'windows'
            myjson.append(initializationrecord)
            myjson.append('codeblocks')

        if args.codewarrior is True:
            initializationrecord = dict()
            initializationrecord['platform'] = 'windows'
            myjson.append(initializationrecord)
            myjson.append('codewarrior50')

        if args.watcom is True:
            initializationrecord = dict()
            initializationrecord['platform'] = 'windows'
            if args.deploy_folder:
                initializationrecord['finalfolder'] = makeprojects.watcom.DEFAULT_FINAL_FOLDER
            myjson.append(initializationrecord)
            myjson.append('watcom')

        if args.linux is True:
            initializationrecord = dict()
            initializationrecord['platform'] = 'linux'
            if args.deploy_folder:
                initializationrecord['finalfolder'] = makeprojects.makefile.DEFAULT_FINAL_FOLDER
            myjson.append(initializationrecord)
            myjson.append('makefile')

        #
        # These are platform specific, and as such are
        # tied to specific IDEs that are tailored to
        # the specific platforms
        #

        if args.xbox360 is True:
            initializationrecord = dict()
            initializationrecord['platform'] = 'xbox360'
            myjson.append(initializationrecord)
            myjson.append('vs2010')

        if args.ios is True:
            initializationrecord = dict()
            initializationrecord['platform'] = 'ios'
            myjson.append(initializationrecord)
            myjson.append('xcode5')

        if args.vita is True:
            initializationrecord = dict()
            initializationrecord['platform'] = 'vita'
            myjson.append(initializationrecord)
            myjson.append('vs2010')

        if args.wiiu is True:
            initializationrecord = dict()
            initializationrecord['platform'] = 'wiiu'
            myjson.append(initializationrecord)
            myjson.append('vs2013')

        if args.dsi is True:
            initializationrecord = dict()
            initializationrecord['platform'] = 'dsi'
            myjson.append(initializationrecord)
            myjson.append('vs2015')

        if len(myjson) < 2:
            print('No default "projects.json" file found nor any project type specified')
            return 2

        return self.process(myjson)


#
# Given a base directory and a relative directory
# scan for all the files that are to be included in the project
#

    def scandirectory(self, directory, codefiles, includedirectories, recurse, acceptable):

        #
        # Root directory is a special case
        #

        if directory == '.':
            search_dir = self.working_directory
        else:
            search_dir = os.path.join(self.working_directory, directory)

        #
        # Is this a valid directory?
        #
        if os.path.isdir(search_dir):

            #
            # Scan the directory
            #

            name_list = os.listdir(search_dir)

            #
            # No files added, yet (Flag for adding directory to the search tree)
            #

            found = False

            for base_name in name_list:

                #
                # Is this file in the exclusion list?
                #

                test_name = base_name.lower()
                skip = False
                for item in self.projects[0].exclude:
                    if test_name == item.lower():
                        skip = True
                        break

                if skip is True:
                    continue

                #
                # Is it a file? (Skip links and folders)
                #

                fileName = os.path.join(search_dir, base_name)
                if os.path.isfile(fileName):

                    #
                    # Check against the extension list (Skip if not supported)
                    #

                    file_type = FileTypes.lookup(test_name)
                    if file_type is not None:

                        #
                        # Found a match, test if the type is in
                        # the acceptable list
                        #

                        if file_type in acceptable:

                            #
                            # If the directory is the root, then don't prepend a directory
                            #
                            if directory == '.':
                                newfilename = base_name
                            else:
                                newfilename = directory + os.sep + base_name

                            #
                            # Create a new entry (Using windows style slashes for consistency)
                            #

                            fileentry = SourceFile(newfilename, search_dir, file_type)
                            codefiles.append(fileentry)
                            if found is False:
                                found = True
                                includedirectories.append(directory)

                #
                # Process folders only if in recursion mode
                #

                elif recurse is True:
                    if os.path.isdir(fileName):
                        codefiles, includedirectories = self.scandirectory(
                            directory + os.sep + base_name, codefiles,
                            includedirectories, recurse, acceptable)

        return codefiles, includedirectories

#
# Obtain the list of source files
#

    def getfilelist(self, acceptable):

        #
        # Get the files that were manually parsed by the json
        # record
        #

        codefiles = list(self.projects[0].codefiles)
        includedirectories = []
        for item in self.projects[0].sourcefolders:

            #
            # Is it a recursive test?
            #

            recurse = False
            if item.endswith('/*.*'):
                # Remove the trailing /*.*
                item = item[0:len(item) - 4]
                recurse = True

            #
            # Scan the folder for files
            #

            codefiles, includedirectories = self.scandirectory(
                item, codefiles, includedirectories, recurse, acceptable)

        #
        # Since the slashes are all windows (No matter what
        # host this script is running on, the sort will yield consistent
        # results so it doesn't matter what platform generated the
        # file list, it's the same output.
        #

        codefiles = sorted(codefiles, key=operator.attrgetter('filename'))
        return codefiles, includedirectories

    def __repr__(self):
        """
        Convert the solultion record into a human readable description

        Returns:
            Human readable string or None if the solution is invalid
        """

        return 'Solution: {}, Verbose: {}, Suffix Enable: {}, Working Directory: {}, IDE: {}, ' \
            'Projects: [{}]'.format(
                self.name,
                str(self.verbose),
                str(self.suffix_enable),
                self.working_directory,
                str(self.ide),
                '],['.join([str(i) for i in self.projects]))

    ## Allow str() to work.
    __str__ = __repr__


def pickfromfilelist(codefiles, itemtype):
    """
    Prune the file list for a specific type.
    """
    filelist = []
    for item in codefiles:
        if item.type == itemtype:
            filelist.append(item)
    return filelist


###################################
#                                 #
# Visual Studio 2003-2013 support #
#                                 #
###################################

#
# Dump out a recursive tree of files to reconstruct a
# directory hiearchy for a file list
#
# Used by Visual Studio 2003, 2005 and 2008
#

def dumptreevs2005(indent, string, entry, fp, groups):
    for item in sorted(entry):
        if item != '':
            fp.write('\t' * indent + '<Filter Name="' + item + '">\n')
        if string == '':
            merged = item
        else:
            merged = string + '\\' + item
        if merged in groups:
            if item != '':
                tabs = '\t' * (indent + 1)
            else:
                tabs = '\t' * indent
            sortlist = sorted(groups[merged])
            for fileitem in sortlist:
                fp.write(tabs + '<File RelativePath="' + fileitem + '" />\n')
        key = entry[item]
        # Recurse down the tree
        if isinstance(key, dict):
            dumptreevs2005(indent + 1, merged, key, fp, groups)
        if item != '':
            fp.write('\t' * indent + '</Filter>\n')

#
# Create the solution and project file for visual studio 2005
#


def createvs2005solution(solution):
    error = makeprojects.visualstudio.generateold(solution, IDETypes.vs2005)
    if error != 0:
        return error

    #
    # Now, let's create the project file
    #

    acceptable = [FileTypes.h, FileTypes.cpp, FileTypes.rc, FileTypes.ico]
    codefiles, includedirectories = solution.getfilelist(acceptable)
    listh = pickfromfilelist(codefiles, FileTypes.h)
    listcpp = pickfromfilelist(codefiles, FileTypes.cpp)
    listwindowsresource = pickfromfilelist(codefiles, FileTypes.rc)

    platformcode = solution.projects[0].platform.get_short_code()
    solutionuuid = str(uuid.uuid3(uuid.NAMESPACE_DNS,
                                  str(solution.visualstudio.outputfilename))).upper()
    projectpathname = os.path.join(solution.working_directory,
                                   solution.visualstudio.outputfilename + '.vcproj')
    burger.perforce_edit(projectpathname)
    fp = open(projectpathname, 'w')

    #
    # Save off the xml header
    #

    fp.write('<?xml version="1.0" encoding="utf-8"?>\n')
    fp.write('<VisualStudioProject\n')
    fp.write('\tProjectType="Visual C++"\n')
    fp.write('\tVersion="8.00"\n')
    fp.write('\tName="' + solution.name + '"\n')
    fp.write('\tProjectGUID="{' + solutionuuid + '}"\n')
    fp.write('\t>\n')

    #
    # Write the project platforms
    #

    fp.write('\t<Platforms>\n')
    for vsplatform in solution.projects[0].platform.get_vs_platform():
        fp.write('\t\t<Platform Name="' + vsplatform + '" />\n')
    fp.write('\t</Platforms>\n')

    #
    # Write the project configurations
    #

    fp.write('\t<Configurations>\n')
    for target in solution.projects[0].configurations:
        for vsplatform in solution.projects[0].platform.get_vs_platform():
            token = str(target) + '|' + vsplatform
            fp.write('\t\t<Configuration\n')
            fp.write('\t\t\tName="' + token + '"\n')
            fp.write('\t\t\tOutputDirectory="bin\\"\n')
            if vsplatform == 'x64':
                platformcode2 = 'w64'
            elif vsplatform == 'Win32':
                platformcode2 = 'w32'
            else:
                platformcode2 = platformcode
            intdirectory = solution.name + solution.ide.get_short_code() + platformcode2 + \
                configuration_short_code(target)
            fp.write('\t\t\tIntermediateDirectory="temp\\' + intdirectory + '"\n')
            if solution.projects[0].projecttype == ProjectTypes.library:
                # Library
                fp.write('\t\t\tConfigurationType="4"\n')
            else:
                # Application
                fp.write('\t\t\tConfigurationType="1"\n')
            fp.write('\t\t\tUseOfMFC="0"\n')
            fp.write('\t\t\tATLMinimizesCRunTimeLibraryUsage="false"\n')
            # Unicode
            fp.write('\t\t\tCharacterSet="1"\n')
            fp.write('\t\t\t>\n')

            fp.write('\t\t\t<Tool\n')
            fp.write('\t\t\t\tName="VCCLCompilerTool"\n')
            fp.write('\t\t\t\tPreprocessorDefinitions="')
            if target == 'Release':
                fp.write('NDEBUG')
            else:
                fp.write('_DEBUG')
            if vsplatform == 'x64':
                fp.write(';WIN64;_WINDOWS')
            elif vsplatform == 'Win32':
                fp.write(';WIN32;_WINDOWS')
            for item in solution.projects[0].defines:
                fp.write(';' + item)
            fp.write('"\n')

            fp.write('\t\t\t\tStringPooling="true"\n')
            fp.write('\t\t\t\tExceptionHandling="0"\n')
            fp.write('\t\t\t\tStructMemberAlignment="4"\n')
            fp.write('\t\t\t\tEnableFunctionLevelLinking="true"\n')
            fp.write('\t\t\t\tFloatingPointModel="2"\n')
            fp.write('\t\t\t\tRuntimeTypeInfo="false"\n')
            fp.write('\t\t\t\tPrecompiledHeaderFile=""\n')
            # 8 byte alignment
            fp.write('\t\t\t\tWarningLevel="4"\n')
            fp.write('\t\t\t\tSuppressStartupBanner="true"\n')
            if solution.projects[0].projecttype == ProjectTypes.library or target != 'Release':
                fp.write('\t\t\t\tDebugInformationFormat="3"\n')
                fp.write('\t\t\t\tProgramDataBaseFileName="$(OutDir)$(TargetName).pdb"\n')
            else:
                fp.write('\t\t\t\tDebugInformationFormat="0"\n')

            fp.write('\t\t\t\tCallingConvention="1"\n')
            fp.write('\t\t\t\tCompileAs="2"\n')
            fp.write('\t\t\t\tFavorSizeOrSpeed="1"\n')
            # Disable annoying nameless struct warnings since windows headers trigger this
            fp.write('\t\t\t\tDisableSpecificWarnings="4201"\n')

            if target == 'Debug':
                fp.write('\t\t\t\tOptimization="0"\n')
            else:
                fp.write('\t\t\t\tOptimization="2"\n')
                fp.write('\t\t\t\tInlineFunctionExpansion="2"\n')
                fp.write('\t\t\t\tEnableIntrinsicFunctions="true"\n')
                fp.write('\t\t\t\tOmitFramePointers="true"\n')
            if target == 'Release':
                fp.write('\t\t\t\tBufferSecurityCheck="false"\n')
                fp.write('\t\t\t\tRuntimeLibrary="0"\n')
            else:
                fp.write('\t\t\t\tBufferSecurityCheck="true"\n')
                fp.write('\t\t\t\tRuntimeLibrary="1"\n')

            #
            # Include directories
            #
            fp.write('\t\t\t\tAdditionalIncludeDirectories="')
            addcolon = False
            included = includedirectories + solution.projects[0].includefolders
            if included:
                for item in included:
                    if addcolon is True:
                        fp.write(';')
                    fp.write(burger.convert_to_windows_slashes(item))
                    addcolon = True
            if platformcode == 'win':
                if addcolon is True:
                    fp.write(';')
                if solution.projects[0].projecttype != ProjectTypes.library or solution.name != 'burgerlib':
                    fp.write('$(BURGER_SDKS)\\windows\\burgerlib;')
                fp.write('$(BURGER_SDKS)\\windows\\directx9;$(BURGER_SDKS)\\windows\\opengl')
                addcolon = True
            fp.write('"\n')
            fp.write('\t\t\t/>\n')

            fp.write('\t\t\t<Tool\n')
            fp.write('\t\t\t\tName="VCResourceCompilerTool"\n')
            fp.write('\t\t\t\tCulture="1033"\n')
            fp.write('\t\t\t/>\n')

            if solution.projects[0].projecttype == ProjectTypes.library:
                fp.write('\t\t\t<Tool\n')
                fp.write('\t\t\t\tName="VCLibrarianTool"\n')
                fp.write('\t\t\t\tOutputFile="&quot;$(OutDir)' + intdirectory + '.lib&quot;"\n')
                fp.write('\t\t\t\tSuppressStartupBanner="true"\n')
                fp.write('\t\t\t/>\n')
                if solution.projects[0].deploy_folder is not None:
                    deploy_folder = burger.convert_to_windows_slashes(
                        solution.projects[0].deploy_folder)
                    fp.write('\t\t\t<Tool\n')
                    fp.write('\t\t\t\tName="VCPostBuildEventTool"\n')
                    fp.write(
                        '\t\t\t\tDescription="Copying $(TargetName)$(TargetExt) to '
                        + deploy_folder + '"\n')
                    fp.write('\t\t\t\tCommandLine="&quot;$(perforce)\\p4&quot; edit &quot;'
                             + deploy_folder + '$(TargetName)$(TargetExt)&quot;&#x0D;&#x0A;')
                    fp.write('&quot;$(perforce)\\p4&quot; edit &quot;' + deploy_folder
                             + '$(TargetName).pdb&quot;&#x0D;&#x0A;')
                    fp.write('copy /Y &quot;$(OutDir)$(TargetName)$(TargetExt)&quot; &quot;'
                             + deploy_folder + '$(TargetName)$(TargetExt)&quot;&#x0D;&#x0A;')
                    fp.write('copy /Y &quot;$(OutDir)$(TargetName).pdb&quot; &quot;' + deploy_folder
                             + '$(TargetName).pdb&quot;&#x0D;&#x0A;')
                    fp.write('&quot;$(perforce)\\p4&quot; revert -a &quot;' + deploy_folder
                             + '$(TargetName)$(TargetExt)&quot;&#x0D;&#x0A;')
                    fp.write('&quot;$(perforce)\\p4&quot; revert -a &quot;' + deploy_folder
                             + '$(TargetName).pdb&quot;&#x0D;&#x0A;"\n')
                    fp.write('\t\t\t/>\n')
            else:
                fp.write('\t\t\t<Tool\n')
                fp.write('\t\t\t\tName="VCLinkerTool"\n')
                fp.write('\t\t\t\tAdditionalDependencies="burgerlib' + solution.ide.get_short_code()
                         + platformcode2 + configuration_short_code(target) + '.lib"\n')
                fp.write('\t\t\t\tOutputFile="&quot;$(OutDir)' + intdirectory + '.exe&quot;"\n')
                fp.write('\t\t\t\tAdditionalLibraryDirectories="')
                addcolon = False
                for item in solution.projects[0].includefolders:
                    if addcolon is True:
                        fp.write(';')
                    fp.write(burger.convert_to_windows_slashes(item))
                    addcolon = True

                if addcolon is True:
                    fp.write(';')
                if solution.projects[0].projecttype != ProjectTypes.library:
                    fp.write('$(BURGER_SDKS)\\windows\\burgerlib;')
                fp.write('$(BURGER_SDKS)\\windows\\opengl"\n')
                if solution.projects[0].projecttype == ProjectTypes.tool:
                    # main()
                    fp.write('\t\t\t\tSubSystem="1"\n')
                else:
                    # WinMain()
                    fp.write('\t\t\t\tSubSystem="2"\n')
                fp.write('\t\t\t/>\n')
            fp.write('\t\t</Configuration>\n')

    fp.write('\t</Configurations>\n')

    #
    # Save out the filenames
    #

    alllists = listh + listcpp + listwindowsresource
    if alllists:

        #
        # Create groups first since Visual Studio uses a nested tree structure
        # for file groupings
        #

        groups = dict()
        for item in alllists:
            groupname = item.extractgroupname()
            # Put each filename in its proper group
            if groupname in groups:
                groups[groupname].append(burger.convert_to_windows_slashes(item.filename))
            else:
                # New group!
                groups[groupname] = [burger.convert_to_windows_slashes(item.filename)]

        #
        # Create a recursive tree in order to store out the file list
        #

        fp.write('\t<Files>\n')
        tree = dict()
        for group in groups:
            #
            # Get the depth of the tree needed
            #

            parts = group.split('\\')
            nexttree = tree
            #
            # Iterate over every part
            #
            for item in range(len(parts)):
                # Already declared?
                if not parts[item] in nexttree:
                    nexttree[parts[item]] = dict()
                # Step into the tree
                nexttree = nexttree[parts[item]]

        # Use this tree to play back all the data
        dumptreevs2005(2, '', tree, fp, groups)
        fp.write('\t</Files>\n')

    fp.write('</VisualStudioProject>\n')
    fp.close()

    return 0

#
# Create the solution and project file for visual studio 2008
#


def createvs2008solution(solution):
    error = makeprojects.visualstudio.generateold(solution, IDETypes.vs2008)
    if error != 0:
        return error
    #
    # Now, let's create the project file
    #

    acceptable = [FileTypes.h, FileTypes.cpp, FileTypes.rc, FileTypes.ico]
    codefiles, includedirectories = solution.getfilelist(acceptable)
    listh = pickfromfilelist(codefiles, FileTypes.h)
    listcpp = pickfromfilelist(codefiles, FileTypes.cpp)
    listwindowsresource = pickfromfilelist(codefiles, FileTypes.rc)

    platformcode = solution.projects[0].platform.get_short_code()
    solutionuuid = str(uuid.uuid3(uuid.NAMESPACE_DNS,
                                  str(solution.visualstudio.outputfilename))).upper()
    projectpathname = os.path.join(solution.working_directory,
                                   solution.visualstudio.outputfilename + '.vcproj')
    burger.perforce_edit(projectpathname)
    fp = open(projectpathname, 'w')

    #
    # Save off the xml header
    #

    fp.write('<?xml version="1.0" encoding="utf-8"?>\n')
    fp.write('<VisualStudioProject\n')
    fp.write('\tProjectType="Visual C++"\n')
    fp.write('\tVersion="9.00"\n')
    fp.write('\tName="' + solution.name + '"\n')
    fp.write('\tProjectGUID="{' + solutionuuid + '}"\n')
    fp.write('\t>\n')

    #
    # Write the project platforms
    #

    fp.write('\t<Platforms>\n')
    for vsplatform in solution.projects[0].platform.get_vs_platform():
        fp.write('\t\t<Platform Name="' + vsplatform + '" />\n')
    fp.write('\t</Platforms>\n')

    #
    # Write the project configurations
    #

    fp.write('\t<Configurations>\n')
    for target in solution.projects[0].configurations:
        for vsplatform in solution.projects[0].platform.get_vs_platform():
            token = str(target) + '|' + vsplatform
            fp.write('\t\t<Configuration\n')
            fp.write('\t\t\tName="' + token + '"\n')
            fp.write('\t\t\tOutputDirectory="bin\\"\n')
            if vsplatform == 'x64':
                platformcode2 = 'w64'
            elif vsplatform == 'Win32':
                platformcode2 = 'w32'
            else:
                platformcode2 = platformcode
            intdirectory = solution.name + solution.ide.get_short_code() + platformcode2 + \
                configuration_short_code(target)
            fp.write('\t\t\tIntermediateDirectory="temp\\' + intdirectory + '\\"\n')
            if solution.projects[0].projecttype == ProjectTypes.library:
                # Library
                fp.write('\t\t\tConfigurationType="4"\n')
            else:
                # Application
                fp.write('\t\t\tConfigurationType="1"\n')
            fp.write('\t\t\tUseOfMFC="0"\n')
            fp.write('\t\t\tATLMinimizesCRunTimeLibraryUsage="false"\n')
            # Unicode
            fp.write('\t\t\tCharacterSet="1"\n')
            fp.write('\t\t\t>\n')

            fp.write('\t\t\t<Tool\n')
            fp.write('\t\t\t\tName="VCCLCompilerTool"\n')
            fp.write('\t\t\t\tPreprocessorDefinitions="')
            if target == 'Release':
                fp.write('NDEBUG')
            else:
                fp.write('_DEBUG')
            if vsplatform == 'x64':
                fp.write(';WIN64;_WINDOWS')
            elif vsplatform == 'Win32':
                fp.write(';WIN32;_WINDOWS')
            for item in solution.projects[0].defines:
                fp.write(';' + item)
            fp.write('"\n')

            fp.write('\t\t\t\tStringPooling="true"\n')
            fp.write('\t\t\t\tExceptionHandling="0"\n')
            fp.write('\t\t\t\tStructMemberAlignment="4"\n')
            fp.write('\t\t\t\tEnableFunctionLevelLinking="true"\n')
            fp.write('\t\t\t\tFloatingPointModel="2"\n')
            fp.write('\t\t\t\tRuntimeTypeInfo="false"\n')
            fp.write('\t\t\t\tPrecompiledHeaderFile=""\n')
            # 8 byte alignment
            fp.write('\t\t\t\tWarningLevel="4"\n')
            fp.write('\t\t\t\tSuppressStartupBanner="true"\n')
            if solution.projects[0].projecttype == ProjectTypes.library or target != 'Release':
                fp.write('\t\t\t\tDebugInformationFormat="3"\n')
                fp.write('\t\t\t\tProgramDataBaseFileName="$(OutDir)$(TargetName).pdb"\n')
            else:
                fp.write('\t\t\t\tDebugInformationFormat="0"\n')

            fp.write('\t\t\t\tCallingConvention="1"\n')
            fp.write('\t\t\t\tCompileAs="2"\n')
            fp.write('\t\t\t\tFavorSizeOrSpeed="1"\n')
            # Disable annoying nameless struct warnings since windows headers trigger this
            fp.write('\t\t\t\tDisableSpecificWarnings="4201"\n')

            if target == 'Debug':
                fp.write('\t\t\t\tOptimization="0"\n')
                # Necessary to quiet Visual Studio 2008 warnings
                fp.write('\t\t\t\tEnableIntrinsicFunctions="true"\n')
            else:
                fp.write('\t\t\t\tOptimization="2"\n')
                fp.write('\t\t\t\tInlineFunctionExpansion="2"\n')
                fp.write('\t\t\t\tEnableIntrinsicFunctions="true"\n')
                fp.write('\t\t\t\tOmitFramePointers="true"\n')
            if target == 'Release':
                fp.write('\t\t\t\tBufferSecurityCheck="false"\n')
                fp.write('\t\t\t\tRuntimeLibrary="0"\n')
            else:
                fp.write('\t\t\t\tBufferSecurityCheck="true"\n')
                fp.write('\t\t\t\tRuntimeLibrary="1"\n')

            #
            # Include directories
            #
            fp.write('\t\t\t\tAdditionalIncludeDirectories="')
            addcolon = False
            included = includedirectories + solution.projects[0].includefolders
            if included:
                for item in included:
                    if addcolon is True:
                        fp.write(';')
                    fp.write(burger.convert_to_windows_slashes(item))
                    addcolon = True
            if platformcode == 'win':
                if addcolon is True:
                    fp.write(';')
                if solution.projects[0].projecttype != ProjectTypes.library or solution.name != 'burgerlib':
                    fp.write('$(BURGER_SDKS)\\windows\\burgerlib;')
                fp.write('$(BURGER_SDKS)\\windows\\directx9;$(BURGER_SDKS)\\windows\\opengl')
                addcolon = True
            fp.write('"\n')
            fp.write('\t\t\t/>\n')

            fp.write('\t\t\t<Tool\n')
            fp.write('\t\t\t\tName="VCResourceCompilerTool"\n')
            fp.write('\t\t\t\tCulture="1033"\n')
            fp.write('\t\t\t/>\n')

            if solution.projects[0].projecttype == ProjectTypes.library:
                fp.write('\t\t\t<Tool\n')
                fp.write('\t\t\t\tName="VCLibrarianTool"\n')
                fp.write('\t\t\t\tOutputFile="&quot;$(OutDir)' + intdirectory + '.lib&quot;"\n')
                fp.write('\t\t\t\tSuppressStartupBanner="true"\n')
                fp.write('\t\t\t/>\n')
                if solution.projects[0].deploy_folder is not None:
                    deploy_folder = burger.convert_to_windows_slashes(
                        solution.projects[0].deploy_folder, True)
                    fp.write('\t\t\t<Tool\n')
                    fp.write('\t\t\t\tName="VCPostBuildEventTool"\n')
                    fp.write(
                        '\t\t\t\tDescription="Copying $(TargetName)$(TargetExt) to '
                        + deploy_folder + '"\n')
                    fp.write('\t\t\t\tCommandLine="&quot;$(perforce)\\p4&quot; edit &quot;'
                             + deploy_folder + '$(TargetName)$(TargetExt)&quot;&#x0D;&#x0A;')
                    fp.write('&quot;$(perforce)\\p4&quot; edit &quot;' + deploy_folder
                             + '$(TargetName).pdb&quot;&#x0D;&#x0A;')
                    fp.write('copy /Y &quot;$(OutDir)$(TargetName)$(TargetExt)&quot; &quot;'
                             + deploy_folder + '$(TargetName)$(TargetExt)&quot;&#x0D;&#x0A;')
                    fp.write('copy /Y &quot;$(OutDir)$(TargetName).pdb&quot; &quot;' + deploy_folder
                             + '$(TargetName).pdb&quot;&#x0D;&#x0A;')
                    fp.write('&quot;$(perforce)\\p4&quot; revert -a &quot;' + deploy_folder
                             + '$(TargetName)$(TargetExt)&quot;&#x0D;&#x0A;')
                    fp.write('&quot;$(perforce)\\p4&quot; revert -a &quot;' + deploy_folder
                             + '$(TargetName).pdb&quot;&#x0D;&#x0A;"\n')
                    fp.write('\t\t\t/>\n')
            else:
                fp.write('\t\t\t<Tool\n')
                fp.write('\t\t\t\tName="VCLinkerTool"\n')
                fp.write('\t\t\t\tAdditionalDependencies="burgerlib' + solution.ide.get_short_code()
                         + platformcode2 + configuration_short_code(target) + '.lib"\n')
                fp.write('\t\t\t\tOutputFile="&quot;$(OutDir)' + intdirectory + '.exe&quot;"\n')
                fp.write('\t\t\t\tAdditionalLibraryDirectories="')
                addcolon = False
                for item in solution.projects[0].includefolders:
                    if addcolon is True:
                        fp.write(';')
                    fp.write(burger.convert_to_windows_slashes(item))
                    addcolon = True

                if addcolon is True:
                    fp.write(';')
                if solution.projects[0].projecttype != ProjectTypes.library:
                    fp.write('$(BURGER_SDKS)\\windows\\burgerlib;')
                fp.write('$(BURGER_SDKS)\\windows\\opengl"\n')
                if solution.projects[0].projecttype == ProjectTypes.tool:
                    # main()
                    fp.write('\t\t\t\tSubSystem="1"\n')
                else:
                    # WinMain()
                    fp.write('\t\t\t\tSubSystem="2"\n')
                fp.write('\t\t\t/>\n')
            fp.write('\t\t</Configuration>\n')

    fp.write('\t</Configurations>\n')

    #
    # Save out the filenames
    #

    alllists = listh + listcpp + listwindowsresource
    if alllists:

        #
        # Create groups first
        #

        groups = dict()
        for item in alllists:
            groupname = item.extractgroupname()
            # Put each filename in its proper group
            if groupname in groups:
                groups[groupname].append(burger.convert_to_windows_slashes(item.filename))
            else:
                # New group!
                groups[groupname] = [burger.convert_to_windows_slashes(item.filename)]

        #
        # Create a recursive tree in order to store out the file list
        #

        fp.write('\t<Files>\n')
        tree = dict()
        for group in groups:
            #
            # Get the depth of the tree needed
            #

            parts = group.split('\\')
            nexttree = tree
            #
            # Iterate over every part
            #
            for item in range(len(parts)):
                # Already declared?
                if not parts[item] in nexttree:
                    nexttree[parts[item]] = dict()
                # Step into the tree
                nexttree = nexttree[parts[item]]

        # Use this tree to play back all the data
        dumptreevs2005(2, '', tree, fp, groups)
        fp.write('\t</Files>\n')

    fp.write('</VisualStudioProject>\n')
    fp.close()

    return 0
