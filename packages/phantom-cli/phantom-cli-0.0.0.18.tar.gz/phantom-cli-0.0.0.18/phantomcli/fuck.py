from phantomcli.image import PhantomMedia
import matplotlib.pyplot as plt


phantom_image = PhantomMedia.load_phantom_image("/home/jonas/Desktop/phantom/image_00009.p16", (1000, 1500))
plt.imshow(phantom_image.array, cmap="gray")
plt.show()
