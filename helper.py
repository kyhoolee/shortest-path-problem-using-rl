"""
print gif file
"""
import numpy as np
import scipy.misc
import datetime

def make_gif(images, fname, duration=100, true_image=False):
  import moviepy.editor as mpy

  def make_frame(t):
    try:
      x = images[int((len(images))/duration*t)]
    except:
      x = images[-1]

    if true_image:
      return x.astype(np.uint8)
    else:
      return ((x+1)/2*255).astype(np.uint8)

  clip = mpy.VideoClip(make_frame, duration=duration)
  clip.write_gif(fname, fps = len(images) / duration)

def print_gif(name, max_stack, num_stack, saved_state):
    big_images = []
    for k in range(len(saved_state)):
        _newstate = -1 * saved_state[k]
        big_images.append(scipy.misc.imresize(_newstate, [max_stack * 30, num_stack * 30], interp='nearest'))
    big_images = np.array(big_images)
    make_gif(big_images, './' + str(name) + '.gif', duration=len(big_images), true_image=True)




