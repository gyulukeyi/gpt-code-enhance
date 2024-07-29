import os
import argparse
from datetime import datetime
from gpt_code_enhance.pipe import Pipe


def enhance_single_codefile(codefile: str):
    extension = os.path.splitext(codefile)[1].lstrip(".")
    pipeline = Pipe(mode=extension)  # type: ignore
    enhanced_code = pipeline.enhance_single(codefile)

    with open(codefile, "w", encoding="utf-8") as file:
        file.write(enhanced_code)


def enhance_codebase_files(base_root: str, codefile: str, extension: str):
    pipeline = Pipe(mode="codebase")
    codefiles_to_enhance = []

    if os.path.isdir(codefile):
        for file in os.listdir(codefile):
            if file.startswith("."):
                continue
            if (
                not extension
                or os.path.splitext(file)[-1].lower().lstrip(".") == extension.lower()
            ):
                codefiles_to_enhance.append(os.path.join(codefile, file))
    else:
        codefiles_to_enhance.append(codefile)

    for codefp in codefiles_to_enhance:
        enhanced_code = pipeline.enhance_codebase(base_root, codefp, extension)
        with open(codefp, "w", encoding="utf-8") as fp:
            fp.write(enhanced_code)


def execute_enhancement(args):
    print(f"{datetime.isoformat(datetime.now())} - Running enhancement...")
    if args.single:
        enhance_single_codefile(args.input)
    else:
        enhance_codebase_files(args.input, args.file_to_enhance, args.extension)
    print(f"{datetime.isoformat(datetime.now())} - Enhancement completed")


def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-s", "--single", action="store_true", help="Activate single code enhance mode."
    )
    parser.add_argument(
        "-i", "--input", required=True, type=str, help="Input path for enhancement."
    )
    parser.add_argument(
        "-e", "--extension", type=str, default="", help="File extension filter."
    )
    parser.add_argument(
        "-f",
        "--file_to_enhance",
        type=str,
        default="",
        help="Specific file or directory to enhance.",
    )

    return parser.parse_args()


if __name__ == "__main__":
    arguments = parse_arguments()
    execute_enhancement(arguments)
