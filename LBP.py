from PIL import Image
import numpy as np
import os, sys

def writeOutPixelInfo(arr, path, filename):
    file = os.path.join(path, filename)
    N = len(arr)*len(arr[0])
    arr_flat = [ele for subarr in arr for ele in subarr]
    with open(file, 'w') as f:
        for i in range(N):
            val = f"{arr_flat[i]}".ljust(8,' ')
            pix = f"// Pixel {i + 1}  "
            row = f"Row: {i//len(arr[0]) + 1}"
            if i % len(arr[0]) == 0:
                f.write(val + pix + row + '\n')
            else:
                f.write(val + pix + '\n')

def getLBP(arr):
    Nrow = len(arr)
    Ncol = len(arr[0])
    arr_lbp = np.zeros((Nrow,Ncol))
    for row in range(1, Nrow - 1):
        for col in range(1, Ncol - 1):
            g0 = arr[row-1][col-1]
            g1 = arr[row-1][col  ]
            g2 = arr[row-1][col+1]
            g3 = arr[row  ][col-1]
            gc = arr[row  ][col  ]
            g4 = arr[row  ][col+1]
            g5 = arr[row+1][col-1]
            g6 = arr[row+1][col  ]
            g7 = arr[row+1][col+1]
            if g0 >= gc: arr_lbp[row][col] += 1
            if g1 >= gc: arr_lbp[row][col] += 2
            if g2 >= gc: arr_lbp[row][col] += 4
            if g3 >= gc: arr_lbp[row][col] += 8
            if g4 >= gc: arr_lbp[row][col] += 16
            if g5 >= gc: arr_lbp[row][col] += 32
            if g6 >= gc: arr_lbp[row][col] += 64
            if g7 >= gc: arr_lbp[row][col] += 128
    return np.uint8(arr_lbp)

def main():
    source = sys.argv[1]
    sourcename, sourcetype = source.split('.')
    current_dir = os.getcwd()

    # Create "result" directory if not
    if not os.path.exists(f"{current_dir}/result"):
        os.mkdir(f"{current_dir}/result")

    # Create a directory to save every resulting files
    result_dir = f"{current_dir}/result/{sourcename}"
    if not os.path.exists(result_dir):
        os.mkdir(result_dir)

    # Get selected image and convert into grayscale array
    file = f"{current_dir}/source/{sourcename}.{sourcetype}"
    myImage = Image.open(file)
    grayImage = myImage.convert('L')
    gray_data = np.asarray(grayImage)
    print("(Width, Height) = " + str(myImage.size))

    # Calculate and transform into lbp
    lbp_data = getLBP(gray_data)
    lbpImage = Image.fromarray(lbp_data, 'L')

    # Save all results
    grayImage.save(os.path.join(result_dir, f"{sourcename}_gray.{sourcetype}"))
    lbpImage.save(os.path.join(result_dir, f"{sourcename}_result.{sourcetype}"))
    writeOutPixelInfo(gray_data, result_dir, f"{sourcename}_gray.dat")
    writeOutPixelInfo(lbp_data, result_dir, f"{sourcename}_lbp.dat")

if __name__ == '__main__':
    main()
