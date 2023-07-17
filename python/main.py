import typer

app = typer.Typer()

# To go elsewhere little endian
def le(byte_str):
    n = 0
    for index, byte in enumerate(byte_str):
        n += (byte << (index * 8))
    return n

@app.command()
def rotate(infile: str, outfile:str):
    with open(infile, 'rb') as f:
        data = f.read()

    assert data[:2] == b'BM'
    
    offset, width, height = le(data[10:14]), le(data[18:22]), le(data[22:26])

# Iterate in the expected order for *rotated* pixels
# look up corresponding *source* pixel, and append to `tpixels`
    spixels = data[offset:]
    tpixels = [] # TODO: currently only BGR triples - what about alpha?
    for ty in range(width): # TODO what should these be for non-squares?
        for tx in range(width):
            sy = tx
            sx = width - ty- 1
            n = 3 * (sy * width + sx)
            tpixels.append(spixels[n:n+3])
    
    with open(outfile, 'wb') as f:
        f.write(data[:offset])
        f.write(b''.join(tpixels))

if __name__ == "__main__":
    app()
