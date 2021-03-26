import json
import os
import argparse
from fnmatch import fnmatch
parser = argparse.ArgumentParser(description='Generates a list of tests from locally present yaml api test files.')

parser.add_argument('-b','--baseurl', type=str, help='The base url ending with a / on which these files are hosted. http://localhost:8081 if excluded',required=False)
parser.add_argument('-d','--directory', type=str, help='Path to the yaml files. Set to ./ if this is excluded',required=False)
parser.add_argument('-o','--output', type=str, help='Path to save the json. Set to ./ if this is excluded',required=False)
parser.add_argument('-t','--trimstart', type=str, help='The beginning of each test in the tests array will have this string trimmed off. If running this script from the api_tests directory, do not include this.',required=False)
args = parser.parse_args()


directory = "./" if args.directory is None else args.directory
output = "./" if args.output is None else args.output

manifest = {}
manifest["base_url"] = 'http://localhost:8081/api_tests' if args.baseurl is None else args.baseurl
manifest["tests"] = []
tests = []

for path, subdirs, files in os.walk(directory):
    path = path if args.trimstart is None else path.replace(args.trimstart, "/")
    for name in files:
        if fnmatch(name, "*.yaml") or fnmatch(name, "*.yml"):
            pth = os.path.join(path, name)
            if manifest["base_url"].endswith("/"):
                pth = pth.replace("./", "")
            else:
                pth = pth.replace("./", "/")
            pth = pth.replace("\\", "/")
            tests.append(pth)

manifest["tests"] = tests

jsonout = json.dumps(manifest)

with open("%stest-manifest.json" % output, "w+") as fout:
    fout.writelines(jsonout)