"""Print text in blocks."""

import subprocess
from math import ceil

line_length = 80

def print_text_block(pt):
  """Print the plaintext to screen in blocks."""
  s = ''.join(pt)
  for line in range(ceil(len(pt) / line_length)):
    print(s[line * line_length:line * line_length + line_length])

def clear_screen():
  subprocess.call(['/usr/bin/clear'])

def print_text_blocks(plaintext):
  """Print a tuple of two texts in blocks."""
  clear_screen()
  print_text_block(plaintext[0])
  print('-' * line_length)
  print_text_block(plaintext[1])
