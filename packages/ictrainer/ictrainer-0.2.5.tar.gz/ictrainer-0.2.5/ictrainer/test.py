# from image_collector import ImageCollector
# import argparse

# parser = argparse.ArgumentParser(description="image download")
# parser.add_argument("-k", "--keyword", dest="keyword", help="type keyword")
# parser.add_argument("-n", "--number", dest="number", help="number of total images", default=100)
# args = parser.parse_args()

# # image keyword
# keyword = args.keyword
# number = int(args.number)

# ic = ImageCollector(keyword, number)
# ic.get_images()

# from image_resizer import ImageResizer
# import os
# import argparse

# parser = argparse.ArgumentParser(description="image download")
# parser.add_argument("-t", "--target", dest="target", help="type keyword")
# args = parser.parse_args()

# # image keyword
# target = args.target

# ir = ImageResizer()
# cwd = os.getcwd()
# ImageResizer.resize_image(cwd + '/dataset/' + target)

# from image_size_check import ImageSizeChecker

# isc = ImageSizeChecker()

# isc.check_size('test')
