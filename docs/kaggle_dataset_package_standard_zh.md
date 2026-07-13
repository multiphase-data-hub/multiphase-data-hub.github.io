# 多相流 Kaggle 数据集上传文件规范

目标：下载者能够根据上传文件，用 Python 读取速度、压力、界面等流场变量，并按自己的任务构造训练集、测试集或可视化结果。

本规范不强制统一数据格式，但强制要求元数据清楚、变量含义明确、字段数据可读取。

## 一、推荐目录结构

```text
dataset_name/
  dataset-metadata.json
  info.json
  README.md
  load_example.py
  checksums.sha256

  data/
    ...

  grid/        可选
  scripts/     可选
  figures/     可选
```

其中：

```text
必须：dataset-metadata.json, info.json, data/
推荐：README.md, load_example.py, checksums.sha256
可选：grid/, scripts/, figures/
```

## 二、数据文件 `data/`

`data/` 存放真实流场数据。数据格式不强制统一，可接受以下几类。

### 1. 已处理好的数组格式

例如：

```text
.npy
.npz
.h5 / .hdf5
.zarr
.nc / NetCDF
```

这类格式较常见，不需要额外解释文件结构，但必须在 `info.json` 中说明数组名称、shape、dtype、单位、坐标顺序和变量含义。

### 2. 常见 CFD / 可视化文件格式

例如：

```text
.dat
.vtk / .vti / .vtu / .vtr
.xdmf + .h5
EnSight Gold
OpenFOAM
Basilisk outputs
```

这类格式也可以直接上传，但必须在 `info.json` 中说明变量名、文件路径、网格信息、单位和推荐读取方式。

### 3. 无扩展名或求解器特定二进制文件

例如：

```text
Gvol.000001
V.000001
P.000001
VOF.000001
field000120
```

这类文件必须额外说明读取方式。`info.json` 中应包含：

- header 字节数；
- dtype；
- 大端 / 小端；
- payload shape；
- vector 分量排列方式；
- reshape 顺序；
- 文件路径规则；
- 单位；
- 网格尺寸和坐标约定。

同时必须提供：

```text
load_example.py
```

否则外部用户很难可靠读取数据。

## 三、变量要求

对于完整两/多相流 CFD 流场数据，原则上必须包含：

```text
速度变量
压力变量
界面变量
```

常见命名示例：

```text
速度：U / V / velocity / u,v,w
压力：P / p / pressure
界面：alpha / Gvol / VOF / phi / level_set
```

其中界面变量应说明相位约定，例如：

```text
Gvol = 1 表示液相还是气相
alpha = 1 表示哪一相
phi > 0 表示哪一相
```

其他变量可选上传，例如：

```text
曲率
界面法向量
涡量
温度
组分
密度场
黏度场
诊断量
```

固定工况参数通常不应作为流场变量上传，而应写入 `info.json`，例如：

```text
rho_l, rho_g
mu_l, mu_g
surface tension
gravity
Re, We, Oh, density ratio, viscosity ratio
```

## 四、网格要求

### 均匀网格

如果坐标可以通过数学函数生成，不必上传单独的网格或几何文件。

但必须在 `info.json` 中写清：

- 网格类型；
- cell 数或 point 数；
- 物理范围；
- dx / dy / dz；
- 坐标顺序；
- 变量位于 cell center 还是 node；
- 周期边界或其他边界条件。

示例：

```json
{
  "type": "uniform_cartesian",
  "cell_dims": [256, 256, 256],
  "domain_bounds_xyz": [[-3.14159, 3.14159], [-3.14159, 3.14159], [-3.14159, 3.14159]],
  "spacing_xyz": [0.0245437, 0.0245437, 0.0245437],
  "field_location": "cell_centered"
}
```

### 非均匀网格

如果是非均匀网格、曲线网格或非结构网格，必须上传相应的网格/几何/坐标文件，例如：

```text
grid/X.dat
grid/Y.dat
grid/Z.dat
geometry
mesh.vtu
mesh.h5
```

并在 `info.json` 中说明这些文件如何与流场变量对应。

## 五、`dataset-metadata.json`

这是 Kaggle 数据集上传所需文件。

按照 BlastNet 教程，通常先执行：

```bash
kaggle datasets init -p <path/to/dataset>
```

该命令会自动生成：

```text
dataset-metadata.json
```

但生成后需要人为编辑，至少填写：

```json
{
  "title": "Dataset title",
  "id": "kaggle-user/dataset-slug",
  "licenses": [
    {
      "name": "CC-BY-4.0"
    }
  ]
}
```

注意：

- `id` 中的用户名必须和 Kaggle 账号用户名一致；
- `dataset-slug` 建议只使用小写字母、数字和连字符；
- 如果许可证尚未确定，先不要公开发布。

## 六、`info.json`

`info.json` 是最重要的元数据文件，应作为数据集的权威说明。

它应包含两部分：

```text
global：整个数据集的信息
local：每个 snapshot / case / sample 的文件路径和时间信息
```

`global` 至少应包含：

- dataset_id；
- title；
- description；
- format；
- snapshot 数量或 sample 数量；
- variables；
- grid；
- physics；
- contributors；
- license；
- DOI 或引用说明；
- known limitations。

`local` 至少应包含：

- snapshot / sample id；
- time，如果有；
- 每个变量对应的文件路径。

重要要求：

```text
info.json 中列出的文件必须真实存在。
如果只上传了 Gvol，就不要在 info.json 中写 V 和 P 的文件路径。
```

## 七、`load_example.py`

推荐所有数据集提供。

对于无扩展名或求解器特定二进制文件，必须提供。

脚本应做到：

- 能从数据集根目录直接运行；
- 至少读取一个样本或一个 snapshot；
- 打印变量名、shape、dtype、min、max；
- 不依赖作者私有代码；
- 尽量使用常见 Python 库。

## 八、`README.md`

推荐提供，但应保持简洁。

不需要重复 `info.json` 的全部内容。

建议只写：

```text
数据集名称
一句话介绍
包含哪些变量
完整元数据见 info.json
读取示例见 load_example.py
引用方式或 DOI
```

## 九、`checksums.sha256`

推荐提供，用于校验文件完整性。

生成方式：

```bash
find . -type f ! -name checksums.sha256 -print0 | sort -z | xargs -0 sha256sum > checksums.sha256
```

## 十、上传前检查清单

上传或提交前，应确认：

- `dataset-metadata.json` 存在，且 `id` 中的 Kaggle 用户名正确；
- `info.json` 存在；
- `info.json` 中列出的文件都真实存在；
- 完整流场数据包含速度、压力和界面变量；
- 变量单位、shape、dtype 已说明；
- 网格可以根据文件或元数据恢复；
- 相位约定已说明；
- 至少一个样本能用 Python 读取；
- 无扩展名或求解器特定二进制文件提供了 `load_example.py`；
- license 和 citation 信息清楚。

