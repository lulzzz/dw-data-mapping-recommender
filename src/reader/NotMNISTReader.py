import os
import numpy as np

from scipy import ndimage


class NotMNISTReader(object):

    def __init__(self):
        self.image_size = 28  # Pixel width and height.
        self.pixel_depth = 255.0  # Number of levels per pixel.

    def read(self, path):
        X = []
        y = []

        letter_folders = os.listdir(path)
        for letter_folder in letter_folders:
            letter_folder_dir = os.path.join(path, letter_folder)
            image_files = []
            # TODO: Maybe this can be refactored
            for (dirName, subdirList, fileList) in os.walk(letter_folder_dir):
                for image_file in fileList:
                    image_files.append(os.path.join(dirName, image_file))
            _X, _y = self._load_letter(image_files=image_files, min_num_images=100)
            X.extend(_X)
            y.extend(_y)
        X = np.asarray(X)
        samples, width, height = X.shape
        X = np.reshape(X, (samples, width * height))
        y = np.asarray(y)

        return X, y

    def _load_letter(self, image_files, min_num_images):
        """Load the data for a single letter label."""
        X = np.ndarray(shape=(len(image_files), self.image_size, self.image_size),
                       dtype=np.float32)
        # y = np.zeros(shape=(len(image_files), 10), dtype=np.int8)
        y = np.zeros(shape=(len(image_files)), dtype=np.int8)
        num_images = 0
        for image_file in image_files:
            try:
                image_data = (ndimage.imread(image_file).astype(float) -
                              self.pixel_depth / 2) / self.pixel_depth
                if image_data.shape != (self.image_size, self.image_size):
                    raise Exception('Unexpected image shape: %s' % str(image_data.shape))
                X[num_images, :, :] = image_data
                # FIXME: don't harccode this!!!
                # y[num_images, (ord(image_file[24]) - 65)] = 1
                y[num_images] = (ord(image_file[24]) - 65)
                num_images = num_images + 1
            except IOError as e:
                print('Could not read:', image_file, ':', e, '- it\'s ok, skipping.')

        X = X[0:num_images, :, :]
        y = y[0:num_images]
        if num_images < min_num_images:
            raise Exception('Many fewer images than expected: %d < %d' %
                            (num_images, min_num_images))

        print('Full dataset tensor:', X.shape)
        print('Mean:', np.mean(X))
        print('Standard deviation:', np.std(X))
        return X, y
