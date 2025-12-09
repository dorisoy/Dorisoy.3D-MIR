#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
from pathlib import Path

import wx

try:
    import polib
except ImportError:
    polib = None


class MOFileReader:
    """Read/write gettext MO files using polib"""

    @staticmethod
    def read(mo_file_path: str) -> dict:
        """Read .mo file and return translations dict"""
        translations = {}
        if polib is None:
            return translations

        try:
            mo = polib.mofile(mo_file_path)
            for entry in mo:
                if entry.msgid:
                    translations[entry.msgid] = entry.msgstr
        except Exception as e:
            print("Failed to read: {}".format(e))

        return translations

    @staticmethod
    def write(mo_file_path: str, translations: dict) -> bool:
        """Write translations dict to .mo file"""
        if polib is None:
            return False

        try:
            mo = polib.MOFile()
            for msgid, msgstr in sorted(translations.items()):
                entry = polib.MOEntry(msgid=msgid, msgstr=msgstr)
                mo.append(entry)

            mo.save(mo_file_path)
            return True
        except Exception as e:
            print("Failed to write: {}".format(e))
            return False


class MOEditorFrame(wx.Frame):
    """MO file editor main window"""

    def __init__(self, parent=None, mo_file=None):
        wx.Frame.__init__(self, parent, title='MO Editor', size=(1000, 600))

        self.mo_file = mo_file
        self.translations = {}
        self.selected_key = None

        # Main panel
        main_panel = wx.Panel(self)
        main_sizer = wx.BoxSizer(wx.HORIZONTAL)

        # Left: List
        left_panel = wx.Panel(main_panel)
        left_sizer = wx.BoxSizer(wx.VERTICAL)

        list_style = wx.LC_REPORT | wx.LC_SINGLE_SEL
        self.list_ctrl = wx.ListCtrl(left_panel, style=list_style)
        self.list_ctrl.InsertColumn(0, 'Source (msgid)', width=200)
        self.list_ctrl.InsertColumn(1, 'Translation (msgstr)', width=200)
        self.list_ctrl.Bind(wx.EVT_LIST_ITEM_SELECTED, self.on_select_item)

        left_sizer.Add(self.list_ctrl, 1, wx.EXPAND)
        left_panel.SetSizer(left_sizer)

        # Right: Editor
        right_panel = wx.Panel(main_panel)
        right_sizer = wx.BoxSizer(wx.VERTICAL)

        # Source text
        label1 = wx.StaticText(right_panel, label='Source (msgid)')
        right_sizer.Add(label1, 0, wx.ALL, 5)
        msg_style = wx.TE_MULTILINE | wx.TE_READONLY
        self.msgid_text = wx.TextCtrl(right_panel, style=msg_style)
        right_sizer.Add(self.msgid_text, 1, wx.EXPAND | wx.ALL, 5)

        # Translation
        label2 = wx.StaticText(right_panel, label='Translation (msgstr)')
        right_sizer.Add(label2, 0, wx.ALL, 5)
        self.msgstr_text = wx.TextCtrl(right_panel, style=wx.TE_MULTILINE)
        right_sizer.Add(self.msgstr_text, 1, wx.EXPAND | wx.ALL, 5)

        # Buttons
        btn_sizer = wx.BoxSizer(wx.HORIZONTAL)
        save_item_btn = wx.Button(right_panel, label='Save Entry')
        save_item_btn.Bind(wx.EVT_BUTTON, self.on_save_item)
        btn_sizer.Add(save_item_btn, 0, wx.ALL, 5)

        open_btn = wx.Button(right_panel, label='Open File')
        open_btn.Bind(wx.EVT_BUTTON, self.on_open_file)
        btn_sizer.Add(open_btn, 0, wx.ALL, 5)

        save_file_btn = wx.Button(right_panel, label='Save File')
        save_file_btn.Bind(wx.EVT_BUTTON, self.on_save_file)
        btn_sizer.Add(save_file_btn, 0, wx.ALL, 5)

        right_sizer.Add(btn_sizer, 0, wx.EXPAND)
        right_panel.SetSizer(right_sizer)

        # Add to main panel
        main_sizer.Add(left_panel, 1, wx.EXPAND)
        main_sizer.Add(right_panel, 1, wx.EXPAND)
        main_panel.SetSizer(main_sizer)

        # Load file
        if mo_file and Path(mo_file).exists():
            self.load_file(mo_file)

    def load_file(self, file_path):
        """Load MO file"""
        self.mo_file = file_path
        self.translations = MOFileReader.read(file_path)
        self.refresh_list()
        self.SetTitle('MO Editor - {}'.format(Path(file_path).name))

    def refresh_list(self):
        """Refresh list"""
        self.list_ctrl.DeleteAllItems()
        for idx, (msgid, msgstr) in enumerate(sorted(self.translations.items())):
            self.list_ctrl.InsertItem(idx, msgid[:100])
            self.list_ctrl.SetItem(idx, 1, msgstr[:100])

    def on_select_item(self, event):
        """Select list item"""
        idx = event.GetIndex()
        items = sorted(self.translations.items())
        if 0 <= idx < len(items):
            msgid, msgstr = items[idx]
            self.selected_key = msgid
            self.msgid_text.SetValue(msgid)
            self.msgstr_text.SetValue(msgstr)

    def on_save_item(self, event):
        """Save current entry"""
        if self.selected_key:
            self.translations[self.selected_key] = self.msgstr_text.GetValue()
            self.refresh_list()
            wx.MessageBox('Entry saved to memory', 'Info')

    def on_save_file(self, event):
        """Save file"""
        if not self.mo_file:
            wx.MessageBox('Please open file first', 'Error')
            return

        if MOFileReader.write(self.mo_file, self.translations):
            wx.MessageBox('File saved: {}'.format(self.mo_file), 'Success')
        else:
            wx.MessageBox('Save failed', 'Error')

    def on_open_file(self, event):
        """Open file"""
        wildcard = 'MO files (*.mo)|*.mo|All files|*'
        dlg = wx.FileDialog(self, 'Open MO file', wildcard=wildcard,
                           defaultDir=str(Path.cwd()),
                           style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST)
        if dlg.ShowModal() == wx.ID_OK:
            self.load_file(dlg.GetPath())
        dlg.Destroy()


class MOEditorApp(wx.App):
    """Application"""

    def OnInit(self):
        mo_file = sys.argv[1] if len(sys.argv) > 1 else None
        self.frame = MOEditorFrame(None, mo_file)
        self.frame.Show()
        return True


if __name__ == '__main__':
    if polib is None:
        print("ERROR: polib not installed")
        print("Run: pip install polib")
        sys.exit(1)

    app = MOEditorApp(False)
    app.MainLoop()
