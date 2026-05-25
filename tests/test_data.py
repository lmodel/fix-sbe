"""Data test."""
import os
import glob
import pytest
from pathlib import Path

import fix_simple_binary_encoding.datamodel.fix_simple_binary_encoding
from linkml_runtime.loaders import yaml_loader

DATA_DIR_VALID = Path(__file__).parent / "data" / "valid"
DATA_DIR_INVALID = Path(__file__).parent / "data" / "invalid"
DATA_DIR_CONFORMANCE = Path(__file__).parent / "data" / "third-party" / "fix-sbe-conformance"

VALID_EXAMPLE_FILES = glob.glob(os.path.join(DATA_DIR_VALID, '*.yaml'))
INVALID_EXAMPLE_FILES = glob.glob(os.path.join(DATA_DIR_INVALID, '*.yaml'))
CONFORMANCE_YAML_FILES = glob.glob(os.path.join(DATA_DIR_CONFORMANCE, '*.yaml'))


@pytest.mark.parametrize("filepath", VALID_EXAMPLE_FILES)
def test_valid_data_files(filepath):
    """Test loading of all valid data files."""
    target_class_name = Path(filepath).stem.split("-")[0]
    tgt_class = getattr(
        fix_simple_binary_encoding.datamodel.fix_simple_binary_encoding,
        target_class_name,
    )
    obj = yaml_loader.load(filepath, target_class=tgt_class)
    assert obj


@pytest.mark.parametrize("filepath", CONFORMANCE_YAML_FILES)
def test_conformance_yaml_files(filepath):
    """Test loading of conformance YAML fixtures derived from fix-sbe-conformance."""
    target_class_name = Path(filepath).stem.split("-")[0]
    tgt_class = getattr(
        fix_simple_binary_encoding.datamodel.fix_simple_binary_encoding,
        target_class_name,
    )
    obj = yaml_loader.load(filepath, target_class=tgt_class)
    assert obj
