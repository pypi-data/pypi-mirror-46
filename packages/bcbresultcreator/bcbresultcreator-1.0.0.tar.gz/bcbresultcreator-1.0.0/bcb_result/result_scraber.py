from bcb_json import read_json, excel_handle
from pathlib import Path
import argparse

ap = argparse.ArgumentParser()
ap.add_argument("-p", "--pattern", required=True,
                help="Searching pattern in file e.g.: -p buy")
ap.add_argument("-f", "--folder", required=True,
                help="Folder name where searching for e.g.: -f .")
args = vars(ap.parse_args())


def create_result_from_jmeter(pattern=r'.+\/buy', folder="."):
    return read_json.read_mean_time(pattern, folder)


if __name__ == "__main__":
    result = []
    zam = Path(args['folder'])
    if zam.exists():
        for folder in zam.glob("*"):
            if folder.is_dir():
                res = create_result_from_jmeter(
                    f".+\/{args['pattern']}", folder)
                if res:
                    result.append(
                        [f'{folder.parts[len(folder.parts)-1]}', res])
                else:
                    print('Error was occurred during json read')
    else:
        print(f'{zam.absolute()} doesn\'t exist')

    if excel_handle.create_excel_with_text(
            text=result, folder=zam.absolute()):
        print('Result was created successfully')
