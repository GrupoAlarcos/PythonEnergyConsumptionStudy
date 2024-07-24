import numpy as np

def mandel(x: float, y: float, max_iters: int) -> int:
    i: int = 0
    c: complex = complex(x, y)
    z: complex = 0.0j
    for i in range(max_iters):
        z = z * z + c
        if (z.real * z.real + z.imag * z.imag) >= 4:
            return i

    return 255

def create_fractal(min_x: float, max_x: float, min_y: float, max_y: float, image: np.ndarray, iters: int) -> np.ndarray:
    height: int = image.shape[0]
    width: int = image.shape[1]

    pixel_size_x: float = (max_x - min_x) / width
    pixel_size_y: float = (max_y - min_y) / height
    for x in range(width):
        real: float = min_x + x * pixel_size_x
        for y in range(height):
            imag: float = min_y + y * pixel_size_y
            color: int = mandel(real, imag, iters)
            image[y, x] = color

    return image

image: np.ndarray = np.zeros((500 * 6, 750 * 6), dtype=np.uint8)
create_fractal(-2.0, 1.0, -1.0, 1.0, image, 20)