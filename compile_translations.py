#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
将 PO 文件编译为 MO 文件的脚本
使用 polib 或是直接的方法
"""
import sys
from pathlib import Path

try:
    # 尝试使用 polib
    import polib
    USE_POLIB = True
except ImportError:
    USE_POLIB = False
    print('✓ polib 未找到，使用 gettext.Catalog')

if USE_POLIB:
    def compile_po_to_mo(po_file, mo_file):
        """using polib to compile"""
        po = polib.pofile(str(po_file))
        po.save_as_mofile(str(mo_file))
        return len(po)
else:
    # Fallback: use internal gettext catalog
    import io
    from email.utils import parsedate_to_datetime
    from collections import OrderedDict
    import struct
    
    def compile_po_to_mo(po_file, mo_file):
        """Compile PO file to MO file using internal parser"""
        
        # Parse PO file
        entries = OrderedDict()
        with open(po_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        msgid = None
        msgstr = None
        msgid_lines = []
        msgstr_lines = []
        in_msgid = False
        in_msgstr = False
        
        for line in lines:
            line = line.rstrip()
            
            if line.startswith('msgid '):
                # Save previous entry
                if msgid is not None:
                    full_msgid = ''.join(msgid_lines).strip('"')
                    full_msgstr = ''.join(msgstr_lines).strip('"')
                    
                    # Unescape
                    full_msgid = full_msgid.encode('utf-8').decode('unicode_escape')
                    full_msgstr = full_msgstr.encode('utf-8').decode('unicode_escape')
                    
                    if full_msgid:  # Skip empty msgid
                        entries[full_msgid] = full_msgstr
                
                msgid = line[6:].strip()
                msgid_lines = [msgid] if msgid != '""' else []
                msgstr = None
                msgstr_lines = []
                in_msgid = True
                in_msgstr = False
                
            elif line.startswith('msgstr '):
                in_msgid = False
                in_msgstr = True
                msgstr = line[7:].strip()
                msgstr_lines = [msgstr] if msgstr != '""' else []
                
            elif in_msgid and line.startswith('"'):
                msgid_lines.append(line.strip())
            elif in_msgstr and line.startswith('"'):
                msgstr_lines.append(line.strip())
        
        # Save last entry
        if msgid is not None:
            full_msgid = ''.join(msgid_lines).strip('"')
            full_msgstr = ''.join(msgstr_lines).strip('"')
            
            full_msgid = full_msgid.encode('utf-8').decode('unicode_escape')
            full_msgstr = full_msgstr.encode('utf-8').decode('unicode_escape')
            
            if full_msgid:
                entries[full_msgid] = full_msgstr
        
        # Generate MO file
        sorted_entries = sorted((k, entries[k]) for k in entries if k)
        num_entries = len(sorted_entries)
        
        # Calculate offsets
        id_data = b''
        str_data = b''
        id_offsets = []
        str_offsets = []
        
        for msgid, msgstr in sorted_entries:
            id_bytes = msgid.encode('utf-8')
            str_bytes = msgstr.encode('utf-8')
            
            id_offsets.append((len(id_data), len(id_bytes)))
            id_data += id_bytes + b'\x00'
            
            str_offsets.append((len(str_data), len(str_bytes)))
            str_data += str_bytes + b'\x00'
        
        # Build MO file
        keystart = 28 + 8 * num_entries
        valuestart = keystart + len(id_data)
        
        header = struct.pack(
            'Iiiiiii',
            0xde120495,  # magic
            0,           # version
            num_entries,
            28,          # master index offset
            28 + 8 * num_entries,  # translation index offset
            0,           # hash size
            0            # hash offset
        )
        
        master_index = b''
        trans_index = b''
        
        for (id_offset, id_len), (str_offset, str_len) in zip(id_offsets, str_offsets):
            master_index += struct.pack('ii', id_len, keystart + id_offset)
            trans_index += struct.pack('ii', str_len, valuestart + str_offset)
        
        # Write file
        mo_file.parent.mkdir(parents=True, exist_ok=True)
        with open(mo_file, 'wb') as f:
            f.write(header)
            f.write(master_index)
            f.write(trans_index)
            f.write(id_data)
            f.write(str_data)
        
        return num_entries

def main():
    languages = [
        'ar', 'be', 'ca', 'cs', 'de', 'el', 'en', 'es', 'fa', 'fr', 
        'it', 'ja', 'ko', 'ms', 'nl', 'pt', 'pt_BR', 'ro', 'ru', 'sr', 
        'sv', 'tr_TR', 'ur_PK', 'uz', 'zh_CN', 'zh_TW'
    ]
    
    po_dir = Path('po')
    locale_dir = Path('locale')
    
    print(f'开始编译翻译文件... (using {'polib' if USE_POLIB else 'internal parser'})\n')
    
    for lang in languages:
        po_file = po_dir / f'{lang}.po'
        if po_file.exists():
            mo_file = locale_dir / lang / 'LC_MESSAGES' / 'invesalius.mo'
            try:
                count = compile_po_to_mo(po_file, mo_file)
                print(f'✓ 已编译: {lang} ({count} 个翻译)')
            except Exception as e:
                print(f'✗ 编译失败 {lang}: {e}')
        else:
            print(f'⚠ 未找到文件: {po_file}')
    
    print('\n✓ 所有翻译文件编译完成！')

if __name__ == '__main__':
    main()
