# spleeter_runner.py - Helper script to run Spleeter in subprocess
import sys
from spleeter.separator import Separator

if len(sys.argv) != 3:
    print("Usage: python spleeter_runner.py <audio_file> <output_dir>")
    sys.exit(1)

audio_file = sys.argv[1]
output_dir = sys.argv[2]

try:
    separator = Separator('spleeter:2stems')
    separator.separate_to_file(audio_file, output_dir, synchronous=True)
    print("Spleeter completed successfully")
except Exception as e:
    print(f"Spleeter error: {str(e)}", file=sys.stderr)
    sys.exit(1)