"""Test toolbar icon loading"""
import os
import sys
import unittest
from pathlib import Path

project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

import invesalius.inv_paths as inv_paths


class TestToolbarIcons(unittest.TestCase):
    """Test if all toolbar icons load correctly"""

    def test_icon_dir_exists(self):
        """Test if icon directory exists"""
        self.assertTrue(
            inv_paths.ICON_DIR.exists(),
            f"Icon directory does not exist: {inv_paths.ICON_DIR}"
        )

    def test_icon_dir_is_pathlib_path(self):
        """Test if ICON_DIR is a pathlib.Path object"""
        self.assertIsInstance(
            inv_paths.ICON_DIR,
            Path,
            "ICON_DIR should be a pathlib.Path object"
        )

    def test_icon_files_exist(self):
        """Test if all toolbar icon files exist"""
        icon_files = [
            "file_import_original.png",
            "file_open_original.png",
            "file_save_original.png",
            "preferences.png",
            "tool_rotate_original.png",
            "tool_translate_original.png",
            "tool_zoom_original.png",
            "tool_zoom_select_original.png",
            "tool_contrast_original.png",
            "measure_line_original.png",
            "measure_angle_original.png",
            "measure_density_ellipse32px.png",
            "measure_density_polygon32px.png",
            "slice_original.png",
            "cross_original.png",
            "layout_data_only_original.png",
            "layout_full_original.png",
            "text_inverted_original.png",
            "text_original.png",
            "ruler_original_disabled.png",
            "ruler_original_enabled.png",
            "undo_original.png",
            "redo_original.png",
        ]

        d = str(inv_paths.ICON_DIR)
        for icon_file in icon_files:
            path = os.path.join(d, icon_file)
            self.assertTrue(
                os.path.exists(path),
                f"Icon file not found: {path}"
            )

    def test_icon_dir_string_conversion(self):
        """Test if ICON_DIR converts to string correctly"""
        d = str(inv_paths.ICON_DIR)
        self.assertIsInstance(d, str)
        self.assertTrue(
            os.path.exists(d),
            f"Converted icon directory path does not exist: {d}"
        )

    def test_icon_path_joining(self):
        """Test if icon paths can be joined correctly"""
        d = str(inv_paths.ICON_DIR)
        icon_file = "file_import_original.png"
        path = os.path.join(d, icon_file)

        self.assertIsInstance(path, str)
        self.assertTrue(
            os.path.exists(path),
            f"Joined icon path does not exist: {path}"
        )


if __name__ == '__main__':
    unittest.main()
