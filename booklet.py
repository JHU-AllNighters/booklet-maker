# %%
from pathlib import Path

import click
from pdfrw import PageMerge, PdfReader, PdfWriter


# %%
def fixpage(*pages):
    valid_pages = (page for page in pages if page is not None)
    result = PageMerge() + valid_pages
    result[-1].x += result[0].w
    return result.render()


# %%
def get_outfile_name(infile):
    infile = Path(infile)
    outfile = infile.parent / ("booklet." + str(infile.name))
    return str(outfile)


# %%
@click.command()
@click.argument("infile", type=click.Path(exists=True))
def main(infile, pad_to=2):

    # Read the input and make sure we have a correct number of sides
    in_pages = PdfReader(infile).pages
    in_pages += [None] * (-len(in_pages) % pad_to)

    # Construct the booklet
    out_pages = []
    while len(in_pages) > 2:
        out_pages.append(fixpage(in_pages.pop(), in_pages.pop(0)))
        out_pages.append(fixpage(in_pages.pop(0), in_pages.pop()))

    out_pages += in_pages

    # Save the booklet
    outfile = get_outfile_name(infile)
    PdfWriter(outfile).addpages(out_pages).write()


# %%
if __name__ == "__main__":
    main()
