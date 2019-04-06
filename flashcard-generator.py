import re
import argparse
import os

flashcard_pattern = r"^(.+?(?=:)):\s*([\S\s]+?(?=[^\n]+:))"

start = r"""
\documentclass[avery5371,grid,frame]{flashcards}
\cardfrontstyle[\LARGE\slshape]{headings}
\cardbackstyle{empty}
\begin{document}

"""

end = r"""\end{document}"""

def flashcard(front, back):
    card = r"\begin{{flashcard}}{{{title}}}".format(title=front) + '\n'
    card += back.replace('\n', r'\\') + '\n'
    card += r"\end{flashcard}" + '\n'
    return card

def main():
    # Parse args
    parser = argparse.ArgumentParser()
    parser.add_argument("input")
    args = parser.parse_args()

    # Open input file
    with open(args.input, 'r') as f:
        input_file = f.read()

        # Add special ending that allows regex to catch
        # the final flashcard, since matches are made up to ([\w]:)
        input_file += "\n Done:"

    # Add doc start
    document = start

    # Generate doc middle
    matches = re.finditer(flashcard_pattern, input_file, re.MULTILINE)
    for match in matches:
        front, back = match.groups()
        document += flashcard(front, back)

    # Add doc end
    document += end

    # Write output file
    base_filename = '.'.join(args.input.split('.')[:-1])
    tex_filename = base_filename + '.tex'
    with open(tex_filename, 'w') as f:
        f.write(document)

    # Convert tex to pdf
    if '/' not in base_filename:
        output_dir = '.'
    else:
        output_dir = '/'.join(base_filename.split('/')[:-1])
    os.system("pdflatex -output-directory {} {}".format(output_dir,
                                                        tex_filename))

    # Clean up intermediate files
    os.remove("{}.log".format(base_filename))
    os.remove("{}.aux".format(base_filename))
    os.remove("{}.tex".format(base_filename))


if __name__ == "__main__":
    main()
