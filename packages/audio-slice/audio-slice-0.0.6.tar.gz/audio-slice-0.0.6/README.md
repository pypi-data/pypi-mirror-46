# Audio Slice

## Description

This tool slices an MP3 file in to a specified number of pieces. Using this
command line tool, you can extract multiple audio files from one master file.

## Current Development Status

This tool is still in its early stages and can only be described as "quick and
dirty". You should be comfortable with everything that comes along with that
descriptor.

## Usage Dependencies

Here are the required dependencies to use this tool:

- [FFmpeg](https://www.ffmpeg.org/download.html)
- Python 2.7+

## Installation

The easiest way to install this tool is to use PIP. No other method of
installation is officially supported at this time.

- PIP ([OS/X Installation Instructions](https://ahmadawais.com/install-pip-macos-os-x-python/))

Installing Audio Slice can be achieved by running the following command once
you have PIP installed:

```bash
pip install audio-slice
```

If you're upgrading to a new version of Audio Slice, you simply use:

```bash
pip install audio-slice --upgrade
```

## Usage

### Recommended usage

If you're going to use this tool, the recommended usage is to do any file-renaming you have to do first, and then move on to the slicing.

### File renaming

You should rename all of the files BEFORE performing any slice operations.
In order to rename the files, it only works by navigating directly to the
directory containing all of the files. Once you've navigated there, then you can
type the following command:

```bash
slice . rename
```

This will rename all of the files in the directory to just their participant IDs.
During the slicing process, the tags will be added on to the end of the slices.

### Slicing

```bash
slice --piece <start_in_seconds> <end_in_seconds> --tags <tag>,<tag>,<tag> <filename>
```

Example:
```bash
slice --piece 24.3 34.1 --piece 35.3 41.2 --tags pig,book never_gonna_give_you_up.mp3
```

A few things to note about using the tool:

1. You can create as many slices of the audio as you need to; even if they overlap. You simply need to add another `--piece <start> <end>` option to the command line.
2. The tool will place the output files in the same directory as the input file.
3. You specify the start and end of a slice in seconds that can include greater precision. (_Ex: 74.3_)
4. Currently, this only works with MP3s.

## Problems

The following are known solutions to problems that have been raised:

### slice command not found

If you're having a problem executing the `slice` command at the command line,
your Python binary folder may not be in your PATH. If you need to add the
Python binary directory to your PATH, you can do the following (MacOS only):

```bash
echo 'export PATH="$PATH:~/Library/Python/2.7/bin"' >> ~/.bash_profile
```