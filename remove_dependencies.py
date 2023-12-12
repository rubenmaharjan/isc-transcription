import subprocess

def uninstall_package(package):
    subprocess.run(["pip", "uninstall", package, "-y"], check=True)

def read_requirements_file(filename):
    with open(filename, "r") as file:
        return [line.strip() for line in file]

def main():
    requirements = read_requirements_file("requirements.txt")
    for package in requirements:
        uninstall_package(package)

if __name__ == "__main__":
    main()