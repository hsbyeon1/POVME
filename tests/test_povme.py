import glob
import os
import shutil

from povme.config import PocketVolumeConfig
from povme.pocket.volume import PocketVolume


def test_4nss(path_4nss_config, path_4nss_output):
    dir_output = os.path.dirname(path_4nss_output)
    if os.path.exists(dir_output):
        shutil.rmtree(dir_output)

    config = PocketVolumeConfig()
    config.from_yaml(path_4nss_config)
    volume_calc = PocketVolume(config)
    results = volume_calc.run(
        "./tests/files/4nss/4nss.pdb", output_prefix=path_4nss_output, chunk_size=1
    )

    expected_vols = set([1673.0, 1493.0, 1711.0, 1854.0, 2023.0])
    actual_vols = set(results.values())
    assert actual_vols == expected_vols
    num_output_files = len(glob.glob(dir_output + "/*"))
    # Was 12, but we currently do not write a log file.
    if num_output_files != 11:
        raise Exception("Expected 11 output files, but got " + str(num_output_files))


def test_rogfp2_traj(path_rogfp2_traj_config, path_rogfp2_traj_output):
    dir_output = os.path.dirname(path_rogfp2_traj_output)
    if os.path.exists(dir_output):
        shutil.rmtree(dir_output)

    config = PocketVolumeConfig()
    config.from_yaml(path_rogfp2_traj_config)
    volume_calc = PocketVolume(config)
    results = volume_calc.run(
        "./tests/files/rogfp2/rogfp2-traj.pdb",
        output_prefix=path_rogfp2_traj_output,
        chunk_size=1,
    )

    expected_vols = set([169.0, 143.0])
    actual_vols = set(results.values())
    assert actual_vols == expected_vols
    num_output_files = len(glob.glob(dir_output + "/*"))
    # Was 12, but we currently do not write a log file.
    if num_output_files != 3:
        raise Exception("Expected 11 output files, but got " + str(num_output_files))


# For profiling
# For example (while in repo root): scalene --profile-all ./tests/test_povme.py
if __name__ == "__main__":
    test_4nss("tests/files/4nss/povme.yml", "tests/tmp/4nss/")
