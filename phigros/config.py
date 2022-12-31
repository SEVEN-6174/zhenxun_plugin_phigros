from pathlib import Path

main_path: Path = Path(__file__).resolve().parent
res_path: Path = main_path / 'resources'
data_path: Path = res_path / 'data'
temp_path: Path = res_path / 'temp'
img_path: Path = res_path / 'image'
bg_path: Path = res_path / 'bg'
font_path: Path = res_path / 'font'
