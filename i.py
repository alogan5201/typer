import typer
import subprocess

def main(name: str):
    command = f'mamba install {name} -c conda-forge'
    process = subprocess.Popen(command.split(), stdout=subprocess.PIPE)
    output, error = process.communicate()
    #print(f"Hello {name}")


if __name__ == "__main__":
    typer.run(main)
