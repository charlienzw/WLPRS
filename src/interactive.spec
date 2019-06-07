# -*- mode: python -*-

block_cipher = None


a = Analysis(['interactive.py'],
             pathex=['.'],
             binaries=[],
             datas=[
                 ('./inventory_data/qvBox-warehouse-data-s19-v01.txt', 'inventory_data'),
                 ('./order_lists/order_of_fifteen.txt', 'order_lists'),
                 ('./order_lists/order_of_five.txt', 'order_lists'),
                 ('./order_lists/order_of_one.txt', 'order_lists'),
                 ('./order_lists/order_of_ten.txt', 'order_lists'),
                 ('./order_lists/order_of_twenty.txt', 'order_lists'),
                 ('./order_lists/order_of_thirty.txt', 'order_lists'),
                 ('./order_lists/order_of_fifty.txt', 'order_lists'),
                 ('./order_lists/qvBox-warehouse-orders-list-part01.txt', 'order_lists'),
                 ('./data/temp.json', 'data'),
                 ('./data/shelves.txt', 'data'),
                 ('./data/Order.json', 'data'),
                 ('./data/Inventory.json', 'data'),
                 ('./data/ID2Index.json', 'data'),
                 ('./data/distances.txt', 'data')
             ],
             hiddenimports=["timeout_decorator"],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          [],
          exclude_binaries=True,
          name='interactive',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=True )
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               name='interactive')
