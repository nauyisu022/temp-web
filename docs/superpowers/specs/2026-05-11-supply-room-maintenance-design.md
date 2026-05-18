# 供应室设备维护管理系统开发计划设计

## 1. 设计来源

本设计基于以下两个文件中的业务逻辑整理：

- `/Users/admin/Downloads/供应室设备维护管理系统-操作手册.docx`
- `/Users/admin/Downloads/供应室设备维护管理系统-代码(1).docx`

现有文件提供了用户操作手册和部分前端 CRUD 页面代码。系统应贴近现有 JeecgBoot 风格，从零开发为一个前后端分离的后台管理系统。

## 2. 系统目标

开发一个供应室设备维护管理系统，用于统一管理供应室设备档案、维护记录、维护计划、故障报修、备品备件和设备性能监测信息。

第一版目标是完整还原现有文件中的后台管理能力：登录、首页、6 个业务模块、查询、新增、编辑、详情、删除、批量删除、导入、导出、权限控制和基础部署。

第一版不实现复杂流程引擎、物联网实时采集、移动端 App 或高级 BI 大屏。设备性能监测先按人工录入和维护的数据实现。

## 3. 技术方案

| 层级 | 技术 |
|---|---|
| 前端 | Vue 2、Ant Design Vue、Vue Router、Vuex、Axios |
| 前端风格 | JeecgBoot 风格 List/Form/Modal 三件套 |
| 后端 | Spring Boot、MyBatis Plus |
| 权限 | Spring Security + JWT，或 JeecgBoot 自带权限体系 |
| 数据库 | MySQL |
| 导入导出 | EasyExcel 或 JeecgBoot Excel 工具 |
| 接口文档 | Swagger / Knife4j |
| 部署 | Nginx + Spring Boot Jar + MySQL |

优先贴近 JeecgBoot 生态，复用用户、角色、菜单、按钮权限、字典、文件上传、Excel 导入导出等能力。

## 4. 功能模块

| 模块 | 说明 |
|---|---|
| 登录与权限管理 | 用户登录、验证码、角色权限、菜单权限、按钮权限 |
| 首页 | 系统名称、快捷入口、基础统计 |
| 设备维护管理 | 管理维护类型、维护人员、维护日期、维护结果、设备位置等维护记录 |
| 设备档案管理 | 管理设备二维码、设备图片、设备电子资料、设备模板等档案信息 |
| 维护计划制定 | 管理定期维护、紧急维护、预防性维护、制定日期、负责人等计划信息 |
| 故障报修管理 | 管理报修编号、报修人、报修日期、故障描述、处理状态等报修信息 |
| 备品备件管理 | 管理库存数量、最低库存、采购日期、采购周期等备件信息 |
| 设备性能监测 | 管理实时监测、运行状态、性能参数、潜在故障、能效评估等性能信息 |
| 系统通用能力 | 查询、重置、新增、编辑、详情、删除、批量删除、导入、导出 |

## 5. 角色权限

| 角色 | 权限 |
|---|---|
| 系统管理员 | 用户、角色、菜单、全部业务数据管理 |
| 设备管理员 | 设备档案、维护计划、维护记录、性能监测管理 |
| 维护人员 | 查看设备档案，处理维护记录和故障报修 |
| 普通用户 | 提交故障报修，查看本人相关记录 |

## 6. 数据库设计

### 6.1 通用字段

每张业务表保留通用字段：

| 字段 | 类型 | 说明 |
|---|---|---|
| `id` | varchar(36) | 主键 |
| `create_by` | varchar(50) | 创建人 |
| `create_time` | datetime | 创建时间 |
| `update_by` | varchar(50) | 更新人 |
| `update_time` | datetime | 更新时间 |
| `sys_org_code` | varchar(64) | 所属机构 |
| `del_flag` | tinyint | 逻辑删除标识 |

现有代码中存在将 `createBy`、`updateBy`、`createTime`、`updateTime`、`sysOrgCode` 当作业务字段使用的情况。从零开发时应修正字段语义，业务字段使用独立命名。

### 6.2 设备维护管理表 `supply_maintenance_record`

| 字段 | 类型 | 说明 |
|---|---|---|
| `id` | varchar(36) | 主键 |
| `maintenance_type` | varchar(100) | 维护类型 |
| `maintenance_person` | varchar(100) | 维护人员 |
| `maintenance_date` | datetime | 维护日期 |
| `maintenance_result` | varchar(500) | 维护结果 |
| `equipment_location` | varchar(200) | 设备位置 |
| `remark` | varchar(500) | 备注 |
| 通用字段 | - | 创建人、创建时间、更新人、更新时间、机构编码、删除标识 |

### 6.3 设备档案管理表 `supply_equipment_archive`

| 字段 | 类型 | 说明 |
|---|---|---|
| `id` | varchar(36) | 主键 |
| `equipment_name` | varchar(100) | 设备名称 |
| `equipment_code` | varchar(100) | 设备编号 |
| `equipment_qr_code` | varchar(255) | 设备二维码 |
| `equipment_image` | varchar(255) | 设备图片 |
| `electronic_document` | varchar(255) | 设备电子资料 |
| `equipment_template` | varchar(255) | 设备模板 |
| `equipment_location` | varchar(200) | 设备位置 |
| `running_status` | varchar(50) | 运行状态 |
| `remark` | varchar(500) | 备注 |
| 通用字段 | - | 创建人、创建时间、更新人、更新时间、机构编码、删除标识 |

### 6.4 维护计划制定表 `supply_maintenance_plan`

| 字段 | 类型 | 说明 |
|---|---|---|
| `id` | varchar(36) | 主键 |
| `plan_name` | varchar(100) | 计划名称 |
| `regular_maintenance` | varchar(500) | 定期维护 |
| `urgent_maintenance` | varchar(500) | 紧急维护 |
| `preventive_maintenance` | varchar(500) | 预防性维护 |
| `plan_date` | datetime | 制定日期 |
| `principal` | varchar(100) | 负责人 |
| `plan_status` | varchar(50) | 计划状态 |
| `remark` | varchar(500) | 备注 |
| 通用字段 | - | 创建人、创建时间、更新人、更新时间、机构编码、删除标识 |

### 6.5 故障报修管理表 `supply_repair_report`

| 字段 | 类型 | 说明 |
|---|---|---|
| `id` | varchar(36) | 主键 |
| `repair_no` | varchar(100) | 报修编号 |
| `repair_person` | varchar(100) | 报修人 |
| `repair_date` | datetime | 报修日期 |
| `fault_description` | varchar(1000) | 故障描述 |
| `process_status` | varchar(50) | 处理状态 |
| `equipment_location` | varchar(200) | 设备位置 |
| `handler` | varchar(100) | 处理人 |
| `process_result` | varchar(500) | 处理结果 |
| `remark` | varchar(500) | 备注 |
| 通用字段 | - | 创建人、创建时间、更新人、更新时间、机构编码、删除标识 |

### 6.6 备品备件管理表 `supply_spare_part`

| 字段 | 类型 | 说明 |
|---|---|---|
| `id` | varchar(36) | 主键 |
| `part_name` | varchar(100) | 备件名称 |
| `part_code` | varchar(100) | 备件编号 |
| `stock_quantity` | int | 库存数量 |
| `minimum_stock` | int | 最低库存 |
| `purchase_date` | datetime | 采购日期 |
| `purchase_cycle` | varchar(100) | 采购周期 |
| `supplier` | varchar(100) | 供应商 |
| `remark` | varchar(500) | 备注 |
| 通用字段 | - | 创建人、创建时间、更新人、更新时间、机构编码、删除标识 |

### 6.7 设备性能监测表 `supply_performance_monitor`

| 字段 | 类型 | 说明 |
|---|---|---|
| `id` | varchar(36) | 主键 |
| `monitor_name` | varchar(100) | 监测名称 |
| `real_time_monitor` | varchar(500) | 实时监测 |
| `running_status` | varchar(50) | 运行状态 |
| `performance_param` | varchar(500) | 性能参数 |
| `potential_fault` | varchar(500) | 潜在故障 |
| `energy_efficiency_eval` | varchar(500) | 评估设备能效 |
| `monitor_time` | datetime | 监测时间 |
| `remark` | varchar(500) | 备注 |
| 通用字段 | - | 创建人、创建时间、更新人、更新时间、机构编码、删除标识 |

## 7. 接口设计

每个业务模块统一采用 JeecgBoot 风格 REST 接口。

| 方法 | 路径 | 说明 |
|---|---|---|
| `GET` | `/list` | 分页查询 |
| `POST` | `/add` | 新增 |
| `PUT` | `/edit` | 编辑 |
| `DELETE` | `/delete?id={id}` | 删除单条 |
| `DELETE` | `/deleteBatch?ids=1,2,3` | 批量删除 |
| `GET` | `/queryById?id={id}` | 查询详情 |
| `GET` | `/exportXls` | 导出 Excel |
| `POST` | `/importExcel` | 导入 Excel |

接口前缀：

| 模块 | 接口前缀 |
|---|---|
| 设备维护管理 | `/supply/maintenanceRecord` |
| 设备档案管理 | `/supply/equipmentArchive` |
| 维护计划制定 | `/supply/maintenancePlan` |
| 故障报修管理 | `/supply/repairReport` |
| 备品备件管理 | `/supply/sparePart` |
| 设备性能监测 | `/supply/performanceMonitor` |

## 8. 前端设计

### 8.1 前端目录

```text
src/
  views/
    supply/
      maintenanceRecord/
        MaintenanceRecordList.vue
        MaintenanceRecordForm.vue
        MaintenanceRecordModal.vue
      equipmentArchive/
        EquipmentArchiveList.vue
        EquipmentArchiveForm.vue
        EquipmentArchiveModal.vue
      maintenancePlan/
        MaintenancePlanList.vue
        MaintenancePlanForm.vue
        MaintenancePlanModal.vue
      repairReport/
        RepairReportList.vue
        RepairReportForm.vue
        RepairReportModal.vue
      sparePart/
        SparePartList.vue
        SparePartForm.vue
        SparePartModal.vue
      performanceMonitor/
        PerformanceMonitorList.vue
        PerformanceMonitorForm.vue
        PerformanceMonitorModal.vue
  api/
    supply/
      maintenanceRecord.js
      equipmentArchive.js
      maintenancePlan.js
      repairReport.js
      sparePart.js
      performanceMonitor.js
```

### 8.2 页面模式

| 文件 | 作用 |
|---|---|
| `List.vue` | 查询区、操作按钮、表格列表、分页、删除、导入、导出 |
| `Form.vue` | 新增、编辑、详情表单 |
| `Modal.vue` | 弹窗容器，控制表单打开、关闭、提交回调 |

每个列表页包含查询区域、操作按钮、数据表格、行操作、分页和展开/收起查询条件。

### 8.3 页面字段

| 页面 | 查询条件 | 列表字段 | 表单字段 |
|---|---|---|---|
| 设备维护管理 | 维护类型、维护人员、维护日期、设备位置 | 维护类型、维护人员、维护日期、维护结果、设备位置 | 同列表 + 备注 |
| 设备档案管理 | 设备名称、设备编号、设备位置、运行状态 | 设备名称、设备编号、二维码、位置、运行状态 | 设备名称、编号、二维码、图片、电子资料、模板、位置、状态、备注 |
| 维护计划制定 | 计划名称、负责人、制定日期、计划状态 | 计划名称、定期维护、紧急维护、预防性维护、制定日期、负责人、状态 | 同列表 + 备注 |
| 故障报修管理 | 报修编号、报修人、处理状态、报修日期 | 报修编号、报修人、报修日期、故障描述、处理状态、处理人 | 报修编号、报修人、报修日期、故障描述、状态、处理人、处理结果、备注 |
| 备品备件管理 | 备件名称、备件编号、库存数量 | 备件名称、备件编号、库存数量、最低库存、采购日期、采购周期 | 同列表 + 供应商、备注 |
| 设备性能监测 | 监测名称、运行状态、监测时间 | 监测名称、实时监测、运行状态、性能参数、潜在故障、能效评估、监测时间 | 同列表 + 备注 |

## 9. 后端设计

### 9.1 包结构

```text
com.example.supply/
  modules/
    supply/
      controller/
      entity/
      mapper/
      service/
      service/impl/
      dto/
      vo/
```

每个业务模块对应 Controller、Entity、Mapper、Service、ServiceImpl。第一版可以贴近 JeecgBoot 代码生成器风格，直接使用 Entity + QueryWrapper + ServiceImpl，避免过度设计。

### 9.2 后端行为

| 功能 | 规则 |
|---|---|
| 分页查询 | 支持页码、页大小、条件筛选、按创建时间倒序 |
| 新增 | 校验必填字段，写入创建人、创建时间、机构编码 |
| 编辑 | 根据 ID 更新，写入更新人、更新时间 |
| 删除 | 建议逻辑删除 |
| 批量删除 | 接收逗号分隔 IDs 或数组 |
| 详情 | 根据 ID 查询单条记录 |
| 导出 | 按当前查询条件导出 Excel |
| 导入 | 解析 Excel，校验后批量入库 |

## 10. 状态字典

| 字典 | 值 |
|---|---|
| 运行状态 | 正常、异常、停用、维修中 |
| 处理状态 | 待处理、处理中、已完成、已关闭 |
| 计划状态 | 未开始、执行中、已完成、已取消 |
| 维护类型 | 定期维护、紧急维护、预防性维护、其他 |
| 删除标识 | 正常、已删除 |

## 11. 开发阶段

| 阶段 | 工作内容 | 交付物 |
|---|---|---|
| 需求整理 | 根据操作手册和代码文档整理功能模块、字段、页面、接口 | 需求清单、模块清单 |
| 技术选型 | 确定 Vue 2 + Ant Design Vue / JeecgBoot + Spring Boot + MyBatis Plus + MySQL | 技术方案 |
| 数据库设计 | 设计 6 张业务表、通用字段、状态字典 | 建表 SQL、字典 SQL |
| 后端开发 | 实现 6 个模块的 Controller、Service、Mapper、Entity、导入导出 | 后端源码、接口文档 |
| 前端开发 | 实现 6 个模块的 List、Form、Modal 页面 | 前端源码、页面路由 |
| 权限配置 | 配置用户、角色、菜单、按钮权限 | 权限菜单、角色配置 |
| 通用能力 | 文件上传、Excel 导入导出、字典展示、表单校验 | 通用功能完成 |
| 联调测试 | 前后端接口联调、业务功能测试、权限测试 | 测试报告、问题清单 |
| 部署上线 | 后端打包、前端打包、Nginx 配置、数据库初始化 | 可访问系统 |
| 验收交付 | 按操作手册逐项验收所有功能 | 验收报告、部署说明 |

推荐开发顺序：

```text
权限登录
  ↓
数据库建表
  ↓
后端 6 个模块基础接口
  ↓
前端 6 个模块页面
  ↓
导入导出和文件上传
  ↓
权限按钮和菜单
  ↓
测试修复
  ↓
部署上线
```

## 12. 测试计划

### 12.1 登录与权限测试

| 编号 | 测试项 | 预期结果 |
|---|---|---|
| T-001 | 正确用户名、密码、验证码登录 | 登录成功，进入首页 |
| T-002 | 错误密码登录 | 提示账号或密码错误 |
| T-003 | 错误验证码登录 | 提示验证码错误 |
| T-004 | 未登录访问业务页面 | 自动跳转登录页 |
| T-005 | 普通用户访问无权限菜单 | 菜单不可见或提示无权限 |
| T-006 | 不同角色查看按钮权限 | 新增、编辑、删除按钮按权限显示 |

### 12.2 业务模块通用测试

每个业务模块执行以下测试：

| 编号 | 测试项 | 预期结果 |
|---|---|---|
| T-B-001 | 打开列表页面 | 页面正常加载，默认显示分页数据 |
| T-B-002 | 按条件查询 | 返回符合条件的数据 |
| T-B-003 | 点击重置 | 查询条件清空，列表恢复默认 |
| T-B-004 | 新增必填字段为空 | 表单提示必填 |
| T-B-005 | 新增合法数据 | 保存成功，列表出现新记录 |
| T-B-006 | 编辑已有数据 | 保存成功，数据更新 |
| T-B-007 | 查看详情 | 展示完整详情，不允许编辑 |
| T-B-008 | 删除单条数据 | 删除成功，列表刷新 |
| T-B-009 | 批量删除数据 | 选中数据被删除 |
| T-B-010 | 导出 Excel | 下载文件成功，内容与查询结果一致 |
| T-B-011 | 导入合法 Excel | 数据导入成功 |
| T-B-012 | 导入错误 Excel | 提示错误原因，不影响已有数据 |

### 12.3 模块专项测试

| 模块 | 测试重点 |
|---|---|
| 设备维护管理 | 日期格式、维护结果长度、维护类型字典 |
| 设备档案管理 | 图片上传、电子资料上传、设备编号唯一性 |
| 维护计划制定 | 计划状态、负责人、制定日期 |
| 故障报修管理 | 报修编号唯一性、处理状态流转 |
| 备品备件管理 | 库存数量不能小于 0、最低库存预警 |
| 设备性能监测 | 运行状态字典、性能参数录入、潜在故障描述 |

## 13. 部署方案

### 13.1 环境要求

| 类型 | 建议版本 |
|---|---|
| 操作系统 | Linux CentOS / Ubuntu |
| JDK | JDK 8 或 JDK 11，取决于 JeecgBoot 版本 |
| Node.js | Node 12 / 14，适配 Vue 2 工程 |
| MySQL | MySQL 5.7 / 8.0 |
| Nginx | 1.18+ |
| Maven | 3.6+ |
| Redis | 可选，若权限框架或验证码使用缓存则启用 |

### 13.2 部署结构

```text
用户浏览器
  ↓
Nginx
  ├── 前端 dist 静态资源
  └── /jeecg-boot 或 /api 反向代理
        ↓
     Spring Boot 后端服务
        ↓
     MySQL 数据库
```

### 13.3 部署步骤

| 步骤 | 内容 |
|---|---|
| 1 | 安装 JDK、MySQL、Nginx、Node.js、Maven |
| 2 | 创建数据库并执行初始化 SQL |
| 3 | 修改后端数据库连接、文件上传路径、JWT 配置 |
| 4 | 后端使用 Maven 打包生成 `.jar` |
| 5 | 使用 `java -jar` 或 systemd 启动后端 |
| 6 | 前端配置接口地址并执行打包 |
| 7 | 将前端 `dist/` 放入 Nginx 静态目录 |
| 8 | 配置 Nginx 代理后端接口 |
| 9 | 启动 Nginx 并访问系统 |
| 10 | 执行上线验收测试 |

## 14. 优先级

| 优先级 | 内容 |
|---|---|
| P0 | 登录、权限、菜单、6 个模块基础 CRUD |
| P1 | 查询、详情、批量删除、导入导出 |
| P2 | 文件上传、字典、表单校验、权限按钮 |
| P3 | 首页统计、库存预警、状态颜色、体验优化 |

## 15. 验收标准

系统满足以下条件即可进行第一版验收：

1. 用户可以登录系统并按角色看到对应菜单。
2. 首页可以正常访问，展示系统名称和基础入口。
3. 6 个业务模块均可执行查询、新增、编辑、详情、删除、批量删除。
4. 6 个业务模块均支持 Excel 导入和导出。
5. 设备档案模块支持设备图片和电子资料上传。
6. 状态字段通过字典展示，表单具备必要校验。
7. 后端接口文档可访问，接口返回格式统一。
8. 系统可以通过 Nginx + Spring Boot + MySQL 部署访问。
9. 按操作手册逐项测试通过。

## 16. 设计取舍

| 问题 | 决策 |
|---|---|
| 是否完全沿用原字段名 | 不完全沿用 |
| 原因 | 原代码存在系统字段承载业务含义的问题，从零开发应修正字段语义 |
| 是否保留原页面逻辑 | 保留 |
| 是否保留原接口风格 | 保留 JeecgBoot 风格，但接口路径改为语义化路径 |
| 是否做模块强关联 | 第一版只做弱关联，通过设备编号、设备位置等字段关联 |
| 是否做真实实时监测 | 第一版不接传感器，先做人工维护数据 |

## 17. 总结

本系统以现有操作手册和前端代码文档为蓝本，采用 JeecgBoot 风格前后端分离架构，开发一个包含登录权限、首页、设备维护管理、设备档案管理、维护计划制定、故障报修管理、备品备件管理、设备性能监测的供应室设备维护管理系统。

第一版重点还原现有文件中的 CRUD、查询、导入、导出、详情、删除等功能。数据库字段在保留业务含义的基础上修正原代码中系统字段误用的问题。后端提供统一 REST 接口，前端采用 List/Form/Modal 三件套页面结构，最终完成权限测试、接口测试、前端功能测试和部署验收。
