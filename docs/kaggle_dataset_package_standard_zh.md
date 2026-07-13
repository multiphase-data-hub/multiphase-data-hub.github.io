# 多相流 Kaggle 数据集上传文件规范

目标：下载者应能根据上传文件，用 Python 读取流场数据，并按自己的任务构造训练集、测试集或可视化结果。

本规范不强制统一数据格式，但强制要求元数据清楚、文件可读、变量含义明确。

## 一、数据格式分类

### A 类：已处理好的数组数据

适用于已经整理成机器学习友好格式的数据。

常见格式：

```text
.npy
.npz
.h5 / .hdf5
.zarr
.nc / NetCDF
```

必须说明：

- 数组名称；
- shape；
- dtype；
- 单位；
- 坐标顺序，例如 `[z, y, x]` 或 `[x, y, z]`；
- cell-centered 还是 node-centered；
- 是否做过归一化或无量纲化；
- 如果已有训练/验证/测试集，需要说明划分方式。

推荐提供：

```text
load_example.py
```

### B 类：常见 CFD 流场文件

适用于求解器或后处理软件常见输出格式。

常见格式：

```text
.dat
.vtk / .vti / .vtu / .vtr
.xdmf + .h5
EnSight Gold
OpenFOAM
Basilisk outputs
```

必须说明：

- 文件格式；
- 变量名称和物理含义；
- 单位；
- 网格类型；
- 网格尺寸；
- 网格坐标来源；
- 变量位于 cell center、node 还是 face；
- 时间步 / snapshot 与文件的对应关系；
- 文件路径规则；
- 推荐读取方式，例如 PyVista、meshio、h5py、xarray 或自定义读取代码。

如果网格不能由元数据恢复，必须上传网格、坐标或 mesh 文件。

如果是均匀直角网格，可以不上传坐标文件，但必须在 `info.json` 中写清：

```text
网格尺寸
物理范围
dx / dy / dz
坐标顺序
变量位置
```

### C 类：无扩展名或求解器特定二进制文件

适用于类似下面这种文件：

```text
Gvol.000001
V.000001
P.000001
VOF.000001
field000120
```

这类数据可以上传，但必须提供明确读取说明。

必须说明：

- 二进制格式；
- header 字节数；
- dtype；
- 大端 / 小端；
- payload shape；
- vector 分量排列方式；
- reshape 顺序；
- 文件路径规则；
- 单位；
- 网格尺寸和坐标约定。

必须提供：

```text
load_example.py
```

否则外部用户很难可靠读取数据。

## 二、必须包含的文件

每个 Kaggle 数据集至少应包含：

```text
dataset-metadata.json
info.json
data/
```

### 1. `dataset-metadata.json`

Kaggle 必需文件。

示例：

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

注意：`id` 中的用户名必须和 Kaggle 账号用户名一致。

### 2. `info.json`

核心元数据文件，必须提供。

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
- known_limitations。

`local` 至少应包含：

- snapshot / sample id；
- time，如果有；
- 每个变量对应的文件路径。

重要要求：

```text
info.json 中列出的文件必须真实存在。
如果只上传了 Gvol，就不要在 info.json 中写 V 和 P 的文件路径。
```

### 3. `data/`

存放真实数据。

推荐结构：

```text
data/Gvol/
data/V/
data/P/
data/train/
data/test/
```

具体结构可以不同，但必须在 `info.json` 中解释清楚。

## 三、强烈推荐的文件

### 1. `load_example.py`

强烈推荐所有数据集提供。

对于 C 类二进制文件，必须提供。

脚本应做到：

- 能从数据集根目录直接运行；
- 至少读取一个样本或一个 snapshot；
- 打印变量名、shape、dtype、min、max；
- 不依赖作者私有代码；
- 尽量使用常见 Python 库。

### 2. `README.md`

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

### 3. `checksums.sha256`

推荐提供，用于校验文件完整性。

生成方式：

```bash
find . -type f ! -name checksums.sha256 -print0 | sort -z | xargs -0 sha256sum > checksums.sha256
```

## 四、可选文件

按需提供：

```text
figures/
scripts/
grid/
metadata/
case files
mesh files
```

例如：

- 预览图；
- 数据转换脚本；
- 训练/验证/测试集划分文件；
- 求解器输入文件；
- 网格或坐标文件；
- ParaView / EnSight / OpenFOAM 所需 case 文件。

## 五、最小 `info.json` 示例

```json
{
  "schema_version": "0.1.0",
  "dataset_type": "multiphase_flow_simulation",
  "global": {
    "dataset_id": "kaggle-user/dataset-slug",
    "title": "Dataset title",
    "description": "Short dataset description.",
    "format": "custom binary",
    "snapshots": 1,
    "variables": ["Gvol"],
    "grid": {
      "type": "uniform_cartesian",
      "cell_dims": [256, 256, 256],
      "domain_bounds_xyz": [[-3.14159, 3.14159], [-3.14159, 3.14159], [-3.14159, 3.14159]],
      "field_location": "cell_centered",
      "coordinate_order": "x,y,z"
    },
    "physics": {
      "flow_type": "two_phase_flow",
      "configuration": "droplet breakup in homogeneous isotropic turbulence",
      "physical_parameters": {
        "density_liquid": "TBD",
        "density_gas": "TBD",
        "viscosity_liquid": "TBD",
        "viscosity_gas": "TBD",
        "surface_tension": "TBD"
      },
      "boundary_conditions": "TBD",
      "initial_conditions": "TBD"
    },
    "contributors": ["TBD"],
    "license": "TBD",
    "doi": "TBD",
    "known_limitations": []
  },
  "local": [
    {
      "id": 0,
      "snapshot_id": "000001",
      "time": {
        "value": null,
        "units": "TBD"
      },
      "files": {
        "Gvol": "./data/Gvol/Gvol.000001"
      }
    }
  ]
}
```

## 六、上传前检查清单

上传或提交前，应确认：

- `dataset-metadata.json` 存在；
- `info.json` 存在；
- `info.json` 中列出的文件都真实存在；
- 变量单位、shape、dtype 已说明；
- 网格可以根据文件或元数据恢复；
- 相位约定已说明，例如 `Gvol=1` 表示哪一相；
- 至少一个样本能用 Python 读取；
- C 类二进制文件提供了 `load_example.py`；
- license 和 citation 信息清楚。

