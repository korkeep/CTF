# recover_from_crossing_progress.py
import sys, math
from PIL import Image
import numpy as np
import hashlib
import os
from tqdm import tqdm   # ✅ 추가

def detect_pnm_header(data: bytes):
    return len(data) >= 2 and (data[:2] == b'P5' or data[:2] == b'P6')

def parse_pnm_header(data: bytes):
    s = data
    mode = s[:2].decode()
    i = 2
    tokens = []
    cur = b''
    while len(tokens) < 3 and i < len(s):
        c = s[i:i+1]; i+=1
        if c == b'#':
            while i < len(s) and s[i:i+1] != b'\n': i+=1
            continue
        if c.isspace():
            if cur:
                tokens.append(cur.decode()); cur = b''
        else:
            cur += c
    if cur and len(tokens) < 3:
        tokens.append(cur.decode())
    if len(tokens) < 3:
        raise ValueError("Can't parse PNM header")
    w = int(tokens[0]); h = int(tokens[1]); maxv = int(tokens[2])
    marker = tokens[2].encode()
    pos = s.find(marker)
    if pos == -1:
        raise ValueError("Can't find header end")
    off = pos + len(marker)
    while off < len(s) and s[off:off+1].isspace(): off += 1
    return mode, w, h, maxv, off

def image_from_crossing(path):
    with open(path, 'rb') as f:
        data = f.read()
    if detect_pnm_header(data):
        mode, w, h, maxv, off = parse_pnm_header(data)
        raw = data[off:]
        if mode == 'P5':
            img = Image.frombytes('L', (w,h), raw)
        else:
            img = Image.frombytes('RGB', (w,h), raw)
            img = img.convert('L')
        return img
    L = len(data)
    v25 = math.ceil(math.sqrt(100 * L))
    need = v25 * v25
    if L < need:
        raw = data + b'\x00'*(need - L)
    else:
        raw = data[:need]
    img = Image.frombytes('L', (v25, v25), raw)
    return img

def tile_hash(arr):
    thr = arr.mean()
    bw = (arr > thr).astype(np.uint8)
    h = hashlib.sha1(bw.tobytes()).hexdigest()
    return h, bw

def try_find_tiles(img, min_t=2, max_t=20):
    w,h = img.size
    a = np.array(img)
    for t in range(min_t, max_t+1):
        cols = w // t
        rows = h // t
        if cols == 0 or rows == 0:
            continue
        tiles = []
        # ✅ 진행률 표시 추가
        for r in tqdm(range(rows), desc=f"tile_size={t}", leave=False):
            for c in range(cols):
                y0 = r*t; x0 = c*t
                tile = a[y0:y0+t, x0:x0+t]
                if tile.shape != (t,t):
                    continue
                hsh, bw = tile_hash(tile)
                tiles.append((hsh, tile.copy(), r, c))
        uniq = {}
        for hsh, tile, r,c in tiles:
            uniq.setdefault(hsh, []).append((tile,r,c))
        if len(uniq) == 16:
            print("Found tile_size =", t, "grid", cols, "x", rows)
            return t, cols, rows, tiles, uniq
    return None

def map_tiles_and_recover(img, path_out_bytes):
    tinfo = try_find_tiles(img)
    if not tinfo:
        print("Could not find tile_size with naive method.")
        return False
    t, cols, rows, tiles, uniq = tinfo
    uniq_list = []
    for hsh, items in uniq.items():
        meanv = items[0][0].mean()
        uniq_list.append((hsh, meanv))
    uniq_list.sort(key=lambda x: x[1])
    hsh_to_nibble = {hsh: idx for idx,(hsh,_) in enumerate(uniq_list)}

    a = np.array(img)
    tile_hashes_sequence = []
    # ✅ tqdm 적용
    for r in tqdm(range(rows), desc="Building sequence"):
        for c in range(cols):
            y0 = r*t; x0 = c*t
            tile = a[y0:y0+t, x0:x0+t]
            hsh, bw = tile_hash(tile)
            tile_hashes_sequence.append(hsh)

    out_bytes = bytearray()
    num_tiles = len(tile_hashes_sequence)
    for i in tqdm(range(0, num_tiles, 2), desc="Assembling bytes"):
        if i+1 >= num_tiles: break
        h_hi = tile_hashes_sequence[i]
        h_lo = tile_hashes_sequence[i+1]
        if h_hi not in hsh_to_nibble or h_lo not in hsh_to_nibble:
            print("Unknown tile hash encountered; aborting.")
            return False
        b = (hsh_to_nibble[h_hi] << 4) | hsh_to_nibble[h_lo]
        out_bytes.append(b)

    with open(path_out_bytes, 'wb') as f:
        f.write(out_bytes)
    print("Recovered bytes written to", path_out_bytes)
    try:
        txt = out_bytes.decode('utf-8')
        print("Decoded as UTF-8:\n", txt)
    except:
        print("Recovered data is not valid UTF-8 (binary).")
    return True

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python recover_from_crossing_progress.py file.crossing")
        sys.exit(1)
    path = sys.argv[1]
    img = image_from_crossing(path)
    out = os.path.splitext(path)[0] + ".recovered.bin"
    ok = map_tiles_and_recover(img, out)
    if not ok:
        print("Automatic recovery failed; try adjusting parameters.")
