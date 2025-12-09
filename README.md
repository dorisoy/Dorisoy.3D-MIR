
# Sinol.3D-MIR（口腔医学影像三维重建软件）

Sinol.3D-MIR 是一个口腔医学影像三维重建软件，基于CT(CBCT)或MRI设备采集的二维DICOM文件序列生成三维医学影像重建，支持多平台（GNU Linux、Windows和MacOS），并提供多种辅助工具。

## 主要功能

  * **DICOM 支持**：包括 (a) ACR-NEMA 版本 1 和 2；(b) DICOM 版本 3.0（包括多种 JPEG 编码 -无损和有损-、RLE）
  * 支持 Analyze 文件格式
  * 支持 BMP、PNG、JPEG 和 TIF 文件格式
  * **图像操作功能**：缩放、平移、旋转、亮度/对比度调节等
  * **基于2D切片的分割**：支持手动和自动分割
  * **预定义阈值范围**：根据组织类型提供预设阈值
  * **分水岭算法分割**：高级分割方法
  * **编辑工具**：类似画笔的2D切片编辑工具
  * **测量工具**：线性和角度测量
  * **体积重定向工具**：灵活调整体积方向
  * **三维表面创建**：从分割结果生成3D模型
  * **三维表面体积测量**：计算表面包围的体积
  * **三维表面连接工具**：修复和优化3D模型
  * **三维表面导出**：支持多种格式（二进制和ASCII STL、PLY、OBJ、VRML、Inventor）
  * **高质量体渲染投影**：逼真的三维可视化
  * **预定义体渲染预设**：多种专业渲染模板
  * **体渲染裁剪平面**：灵活的截面工具
  * **图片导出**：支持 BMP、TIFF、JPG、PostScript、POV-Ray 等格式

## 屏幕

<img src="https://github.com/dorisoy/Dorisoy.3D-MIR/blob/main/Screen/1.png?raw=true"/>
<img src="https://github.com/dorisoy/Dorisoy.3D-MIR/blob/main/Screen/2.png?raw=true"/>
<img src="https://github.com/dorisoy/Dorisoy.3D-MIR/blob/main/Screen/3.png?raw=true"/>
<img src="https://github.com/dorisoy/Dorisoy.3D-MIR/blob/main/Screen/4.png?raw=true"/>


## 系统要求

### 依赖包版本

本项目使用以下主要依赖包，请确保安装了相应版本：

#### 科学计算
- numpy==1.26.4
- scipy==1.14.0
- matplotlib==3.9.0

#### 图像处理
- Pillow==10.3.0
- imageio==2.34.2
- nibabel==5.2.1
- scikit-image==0.24.0
- python-gdcm==3.0.24
- vtk==9.3.0
- h5py==3.11.0

#### 机器学习
- torch==2.3.1

#### GUI 框架
- wxPython==4.2.2

#### 其他工具
- Cython==3.0.10
- Pypubsub==4.0.3
- psutil==6.0.0
- pyserial==3.5
- pyacvd==0.2.11
- pytest==8.3.5
- pytest-mock==3.14.0

### 安装依赖

在项目根目录执行以下命令安装所有依赖：

```powershell
# 使用 pip 安装
.\invenv\Scripts\pip.exe install -r requirements.txt

# 或者使用虚拟环境激活后安装
.\invenv\Scripts\Activate.ps1
pip install -r requirements.txt
```

## 快速开始

### 启动应用

在项目根目录执行以下命令：

```powershell
# 直接运行
.\invenv\Scripts\python.exe app.py

# 或激活虚拟环境后运行
.\invenv\Scripts\Activate.ps1
python app.py
```

### 命令行参数

```powershell
# 启用调试模式
python app.py -d

# 导入 DICOM 目录
python app.py -i <dicom_folder_path>

# 打开已有的项目文件
python app.py <project_file_path>
```

## 许可证

本项目为专有软件，未经授权禁止使用、复制或分发。

---

## 联系方式

<img src="https://github.com/dorisoy/Dorisoy.DICOM/blob/main/Screen/wx.jpg?raw=true"/>
