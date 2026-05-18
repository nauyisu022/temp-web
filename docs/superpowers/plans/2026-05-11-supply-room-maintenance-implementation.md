# Supply Room Maintenance Management System Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a JeecgBoot-style supply room equipment maintenance management system from scratch, matching the provided operation manual and frontend code logic.

**Architecture:** Use a front-end/back-end separated admin system. The backend provides Spring Boot + MyBatis Plus REST APIs and MySQL persistence; the frontend uses Vue 2 + Ant Design Vue with JeecgBoot-style List/Form/Modal pages. The first release focuses on login, permissions, six CRUD modules, Excel import/export, file upload, testing, and deployment.

**Tech Stack:** Vue 2, Ant Design Vue, Vue Router, Vuex, Axios, Spring Boot, MyBatis Plus, MySQL, Swagger/Knife4j, EasyExcel or JeecgBoot Excel utilities, Nginx.

---

## File Structure Map

### Backend files

Create or modify these backend files in the JeecgBoot/Spring Boot backend project:

```text
backend/
  src/main/java/org/jeecg/modules/supply/
    controller/
      MaintenanceRecordController.java
      EquipmentArchiveController.java
      MaintenancePlanController.java
      RepairReportController.java
      SparePartController.java
      PerformanceMonitorController.java
    entity/
      MaintenanceRecord.java
      EquipmentArchive.java
      MaintenancePlan.java
      RepairReport.java
      SparePart.java
      PerformanceMonitor.java
    mapper/
      MaintenanceRecordMapper.java
      EquipmentArchiveMapper.java
      MaintenancePlanMapper.java
      RepairReportMapper.java
      SparePartMapper.java
      PerformanceMonitorMapper.java
    mapper/xml/
      MaintenanceRecordMapper.xml
      EquipmentArchiveMapper.xml
      MaintenancePlanMapper.xml
      RepairReportMapper.xml
      SparePartMapper.xml
      PerformanceMonitorMapper.xml
    service/
      IMaintenanceRecordService.java
      IEquipmentArchiveService.java
      IMaintenancePlanService.java
      IRepairReportService.java
      ISparePartService.java
      IPerformanceMonitorService.java
    service/impl/
      MaintenanceRecordServiceImpl.java
      EquipmentArchiveServiceImpl.java
      MaintenancePlanServiceImpl.java
      RepairReportServiceImpl.java
      SparePartServiceImpl.java
      PerformanceMonitorServiceImpl.java
  src/main/resources/db/migration/
    V1__create_supply_room_tables.sql
    V2__init_supply_room_dicts_and_menus.sql
  src/test/java/org/jeecg/modules/supply/
    MaintenanceRecordControllerTest.java
    EquipmentArchiveControllerTest.java
    MaintenancePlanControllerTest.java
    RepairReportControllerTest.java
    SparePartControllerTest.java
    PerformanceMonitorControllerTest.java
```

### Frontend files

Create or modify these frontend files in the Vue 2 / JeecgBoot frontend project:

```text
frontend/
  src/views/supply/
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
  src/api/supply/
    maintenanceRecord.js
    equipmentArchive.js
    maintenancePlan.js
    repairReport.js
    sparePart.js
    performanceMonitor.js
```

### Deployment files

```text
deploy/
  nginx/supply-room.conf
  systemd/supply-room-backend.service
  sql/init_supply_room.sql
```

---

## Task 1: Initialize Backend and Frontend Projects

**Files:**
- Create: `backend/`
- Create: `frontend/`
- Create: `deploy/`

- [ ] **Step 1: Create or import JeecgBoot backend project**

Use the existing JeecgBoot backend template if available. If starting from a standard Spring Boot project, include these core dependencies in `backend/pom.xml`:

```xml
<dependencies>
  <dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-web</artifactId>
  </dependency>
  <dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-validation</artifactId>
  </dependency>
  <dependency>
    <groupId>com.baomidou</groupId>
    <artifactId>mybatis-plus-boot-starter</artifactId>
    <version>3.5.5</version>
  </dependency>
  <dependency>
    <groupId>mysql</groupId>
    <artifactId>mysql-connector-java</artifactId>
    <version>8.0.33</version>
  </dependency>
  <dependency>
    <groupId>com.alibaba</groupId>
    <artifactId>easyexcel</artifactId>
    <version>3.3.4</version>
  </dependency>
  <dependency>
    <groupId>org.springdoc</groupId>
    <artifactId>springdoc-openapi-ui</artifactId>
    <version>1.7.0</version>
  </dependency>
  <dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-test</artifactId>
    <scope>test</scope>
  </dependency>
</dependencies>
```

- [ ] **Step 2: Configure backend database connection**

Create or modify `backend/src/main/resources/application.yml`:

```yaml
server:
  port: 8080

spring:
  datasource:
    driver-class-name: com.mysql.cj.jdbc.Driver
    url: jdbc:mysql://127.0.0.1:3306/supply_room?useUnicode=true&characterEncoding=utf8&serverTimezone=Asia/Shanghai
    username: root
    password: root

mybatis-plus:
  mapper-locations: classpath*:org/jeecg/modules/**/xml/*Mapper.xml
  global-config:
    db-config:
      id-type: ASSIGN_ID
      logic-delete-field: delFlag
      logic-delete-value: 1
      logic-not-delete-value: 0
```

- [ ] **Step 3: Create or import JeecgBoot Vue 2 frontend project**

Use the existing JeecgBoot Vue 2 frontend template if available. Confirm these packages exist in `frontend/package.json`:

```json
{
  "dependencies": {
    "ant-design-vue": "^1.7.8",
    "axios": "^0.19.0",
    "vue": "^2.6.10",
    "vue-router": "^3.1.3",
    "vuex": "^3.1.1"
  }
}
```

- [ ] **Step 4: Verify backend starts**

Run:

```bash
cd backend && mvn test
```

Expected: Maven test phase completes successfully.

- [ ] **Step 5: Verify frontend installs**

Run:

```bash
cd frontend && npm install
```

Expected: Dependencies install successfully.

- [ ] **Step 6: Commit initialization**

```bash
git add backend frontend deploy
git commit -m "chore: initialize supply room system projects"
```

---

## Task 2: Create Database Tables

**Files:**
- Create: `backend/src/main/resources/db/migration/V1__create_supply_room_tables.sql`
- Create: `deploy/sql/init_supply_room.sql`

- [ ] **Step 1: Write database creation SQL**

Create `backend/src/main/resources/db/migration/V1__create_supply_room_tables.sql` with:

```sql
CREATE TABLE supply_maintenance_record (
  id varchar(36) NOT NULL COMMENT '主键',
  maintenance_type varchar(100) DEFAULT NULL COMMENT '维护类型',
  maintenance_person varchar(100) DEFAULT NULL COMMENT '维护人员',
  maintenance_date datetime DEFAULT NULL COMMENT '维护日期',
  maintenance_result varchar(500) DEFAULT NULL COMMENT '维护结果',
  equipment_location varchar(200) DEFAULT NULL COMMENT '设备位置',
  remark varchar(500) DEFAULT NULL COMMENT '备注',
  create_by varchar(50) DEFAULT NULL COMMENT '创建人',
  create_time datetime DEFAULT NULL COMMENT '创建时间',
  update_by varchar(50) DEFAULT NULL COMMENT '更新人',
  update_time datetime DEFAULT NULL COMMENT '更新时间',
  sys_org_code varchar(64) DEFAULT NULL COMMENT '所属机构',
  del_flag tinyint DEFAULT 0 COMMENT '删除标识',
  PRIMARY KEY (id),
  KEY idx_maintenance_date (maintenance_date),
  KEY idx_maintenance_type (maintenance_type)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='设备维护管理';

CREATE TABLE supply_equipment_archive (
  id varchar(36) NOT NULL COMMENT '主键',
  equipment_name varchar(100) DEFAULT NULL COMMENT '设备名称',
  equipment_code varchar(100) DEFAULT NULL COMMENT '设备编号',
  equipment_qr_code varchar(255) DEFAULT NULL COMMENT '设备二维码',
  equipment_image varchar(255) DEFAULT NULL COMMENT '设备图片',
  electronic_document varchar(255) DEFAULT NULL COMMENT '设备电子资料',
  equipment_template varchar(255) DEFAULT NULL COMMENT '设备模板',
  equipment_location varchar(200) DEFAULT NULL COMMENT '设备位置',
  running_status varchar(50) DEFAULT NULL COMMENT '运行状态',
  remark varchar(500) DEFAULT NULL COMMENT '备注',
  create_by varchar(50) DEFAULT NULL COMMENT '创建人',
  create_time datetime DEFAULT NULL COMMENT '创建时间',
  update_by varchar(50) DEFAULT NULL COMMENT '更新人',
  update_time datetime DEFAULT NULL COMMENT '更新时间',
  sys_org_code varchar(64) DEFAULT NULL COMMENT '所属机构',
  del_flag tinyint DEFAULT 0 COMMENT '删除标识',
  PRIMARY KEY (id),
  UNIQUE KEY uk_equipment_code (equipment_code),
  KEY idx_running_status (running_status)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='设备档案管理';

CREATE TABLE supply_maintenance_plan (
  id varchar(36) NOT NULL COMMENT '主键',
  plan_name varchar(100) DEFAULT NULL COMMENT '计划名称',
  regular_maintenance varchar(500) DEFAULT NULL COMMENT '定期维护',
  urgent_maintenance varchar(500) DEFAULT NULL COMMENT '紧急维护',
  preventive_maintenance varchar(500) DEFAULT NULL COMMENT '预防性维护',
  plan_date datetime DEFAULT NULL COMMENT '制定日期',
  principal varchar(100) DEFAULT NULL COMMENT '负责人',
  plan_status varchar(50) DEFAULT NULL COMMENT '计划状态',
  remark varchar(500) DEFAULT NULL COMMENT '备注',
  create_by varchar(50) DEFAULT NULL COMMENT '创建人',
  create_time datetime DEFAULT NULL COMMENT '创建时间',
  update_by varchar(50) DEFAULT NULL COMMENT '更新人',
  update_time datetime DEFAULT NULL COMMENT '更新时间',
  sys_org_code varchar(64) DEFAULT NULL COMMENT '所属机构',
  del_flag tinyint DEFAULT 0 COMMENT '删除标识',
  PRIMARY KEY (id),
  KEY idx_plan_date (plan_date),
  KEY idx_plan_status (plan_status)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='维护计划制定';

CREATE TABLE supply_repair_report (
  id varchar(36) NOT NULL COMMENT '主键',
  repair_no varchar(100) DEFAULT NULL COMMENT '报修编号',
  repair_person varchar(100) DEFAULT NULL COMMENT '报修人',
  repair_date datetime DEFAULT NULL COMMENT '报修日期',
  fault_description varchar(1000) DEFAULT NULL COMMENT '故障描述',
  process_status varchar(50) DEFAULT NULL COMMENT '处理状态',
  equipment_location varchar(200) DEFAULT NULL COMMENT '设备位置',
  handler varchar(100) DEFAULT NULL COMMENT '处理人',
  process_result varchar(500) DEFAULT NULL COMMENT '处理结果',
  remark varchar(500) DEFAULT NULL COMMENT '备注',
  create_by varchar(50) DEFAULT NULL COMMENT '创建人',
  create_time datetime DEFAULT NULL COMMENT '创建时间',
  update_by varchar(50) DEFAULT NULL COMMENT '更新人',
  update_time datetime DEFAULT NULL COMMENT '更新时间',
  sys_org_code varchar(64) DEFAULT NULL COMMENT '所属机构',
  del_flag tinyint DEFAULT 0 COMMENT '删除标识',
  PRIMARY KEY (id),
  UNIQUE KEY uk_repair_no (repair_no),
  KEY idx_process_status (process_status),
  KEY idx_repair_date (repair_date)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='故障报修管理';

CREATE TABLE supply_spare_part (
  id varchar(36) NOT NULL COMMENT '主键',
  part_name varchar(100) DEFAULT NULL COMMENT '备件名称',
  part_code varchar(100) DEFAULT NULL COMMENT '备件编号',
  stock_quantity int DEFAULT 0 COMMENT '库存数量',
  minimum_stock int DEFAULT 0 COMMENT '最低库存',
  purchase_date datetime DEFAULT NULL COMMENT '采购日期',
  purchase_cycle varchar(100) DEFAULT NULL COMMENT '采购周期',
  supplier varchar(100) DEFAULT NULL COMMENT '供应商',
  remark varchar(500) DEFAULT NULL COMMENT '备注',
  create_by varchar(50) DEFAULT NULL COMMENT '创建人',
  create_time datetime DEFAULT NULL COMMENT '创建时间',
  update_by varchar(50) DEFAULT NULL COMMENT '更新人',
  update_time datetime DEFAULT NULL COMMENT '更新时间',
  sys_org_code varchar(64) DEFAULT NULL COMMENT '所属机构',
  del_flag tinyint DEFAULT 0 COMMENT '删除标识',
  PRIMARY KEY (id),
  UNIQUE KEY uk_part_code (part_code),
  KEY idx_stock_quantity (stock_quantity)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='备品备件管理';

CREATE TABLE supply_performance_monitor (
  id varchar(36) NOT NULL COMMENT '主键',
  monitor_name varchar(100) DEFAULT NULL COMMENT '监测名称',
  real_time_monitor varchar(500) DEFAULT NULL COMMENT '实时监测',
  running_status varchar(50) DEFAULT NULL COMMENT '运行状态',
  performance_param varchar(500) DEFAULT NULL COMMENT '性能参数',
  potential_fault varchar(500) DEFAULT NULL COMMENT '潜在故障',
  energy_efficiency_eval varchar(500) DEFAULT NULL COMMENT '评估设备能效',
  monitor_time datetime DEFAULT NULL COMMENT '监测时间',
  remark varchar(500) DEFAULT NULL COMMENT '备注',
  create_by varchar(50) DEFAULT NULL COMMENT '创建人',
  create_time datetime DEFAULT NULL COMMENT '创建时间',
  update_by varchar(50) DEFAULT NULL COMMENT '更新人',
  update_time datetime DEFAULT NULL COMMENT '更新时间',
  sys_org_code varchar(64) DEFAULT NULL COMMENT '所属机构',
  del_flag tinyint DEFAULT 0 COMMENT '删除标识',
  PRIMARY KEY (id),
  KEY idx_running_status (running_status),
  KEY idx_monitor_time (monitor_time)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='设备性能监测';
```

- [ ] **Step 2: Copy SQL to deployment init script**

Copy the same SQL into `deploy/sql/init_supply_room.sql` so deployment has a standalone initialization script.

- [ ] **Step 3: Validate SQL syntax**

Run:

```bash
mysql -uroot -proot -e "CREATE DATABASE IF NOT EXISTS supply_room DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci; USE supply_room; SOURCE backend/src/main/resources/db/migration/V1__create_supply_room_tables.sql; SHOW TABLES;"
```

Expected: output includes all six tables: `supply_maintenance_record`, `supply_equipment_archive`, `supply_maintenance_plan`, `supply_repair_report`, `supply_spare_part`, `supply_performance_monitor`.

- [ ] **Step 4: Commit database schema**

```bash
git add backend/src/main/resources/db/migration/V1__create_supply_room_tables.sql deploy/sql/init_supply_room.sql
git commit -m "feat: add supply room database schema"
```

---

## Task 3: Implement Backend Entity and Mapper Layer

**Files:**
- Create: all files under `backend/src/main/java/org/jeecg/modules/supply/entity/`
- Create: all files under `backend/src/main/java/org/jeecg/modules/supply/mapper/`
- Create: all files under `backend/src/main/java/org/jeecg/modules/supply/mapper/xml/`

- [ ] **Step 1: Create `MaintenanceRecord.java`**

```java
package org.jeecg.modules.supply.entity;

import com.baomidou.mybatisplus.annotation.IdType;
import com.baomidou.mybatisplus.annotation.TableId;
import com.baomidou.mybatisplus.annotation.TableLogic;
import com.baomidou.mybatisplus.annotation.TableName;
import java.io.Serializable;
import java.util.Date;
import lombok.Data;
import org.springframework.format.annotation.DateTimeFormat;
import com.fasterxml.jackson.annotation.JsonFormat;

@Data
@TableName("supply_maintenance_record")
public class MaintenanceRecord implements Serializable {
    @TableId(type = IdType.ASSIGN_ID)
    private String id;
    private String maintenanceType;
    private String maintenancePerson;
    @JsonFormat(timezone = "GMT+8", pattern = "yyyy-MM-dd HH:mm:ss")
    @DateTimeFormat(pattern = "yyyy-MM-dd HH:mm:ss")
    private Date maintenanceDate;
    private String maintenanceResult;
    private String equipmentLocation;
    private String remark;
    private String createBy;
    @JsonFormat(timezone = "GMT+8", pattern = "yyyy-MM-dd HH:mm:ss")
    @DateTimeFormat(pattern = "yyyy-MM-dd HH:mm:ss")
    private Date createTime;
    private String updateBy;
    @JsonFormat(timezone = "GMT+8", pattern = "yyyy-MM-dd HH:mm:ss")
    @DateTimeFormat(pattern = "yyyy-MM-dd HH:mm:ss")
    private Date updateTime;
    private String sysOrgCode;
    @TableLogic
    private Integer delFlag;
}
```

- [ ] **Step 2: Create the other five entity classes**

Use the same annotations and common fields as `MaintenanceRecord`. Define fields matching the SQL:

`EquipmentArchive.java` fields:

```java
private String id;
private String equipmentName;
private String equipmentCode;
private String equipmentQrCode;
private String equipmentImage;
private String electronicDocument;
private String equipmentTemplate;
private String equipmentLocation;
private String runningStatus;
private String remark;
private String createBy;
private Date createTime;
private String updateBy;
private Date updateTime;
private String sysOrgCode;
private Integer delFlag;
```

`MaintenancePlan.java` fields:

```java
private String id;
private String planName;
private String regularMaintenance;
private String urgentMaintenance;
private String preventiveMaintenance;
private Date planDate;
private String principal;
private String planStatus;
private String remark;
private String createBy;
private Date createTime;
private String updateBy;
private Date updateTime;
private String sysOrgCode;
private Integer delFlag;
```

`RepairReport.java` fields:

```java
private String id;
private String repairNo;
private String repairPerson;
private Date repairDate;
private String faultDescription;
private String processStatus;
private String equipmentLocation;
private String handler;
private String processResult;
private String remark;
private String createBy;
private Date createTime;
private String updateBy;
private Date updateTime;
private String sysOrgCode;
private Integer delFlag;
```

`SparePart.java` fields:

```java
private String id;
private String partName;
private String partCode;
private Integer stockQuantity;
private Integer minimumStock;
private Date purchaseDate;
private String purchaseCycle;
private String supplier;
private String remark;
private String createBy;
private Date createTime;
private String updateBy;
private Date updateTime;
private String sysOrgCode;
private Integer delFlag;
```

`PerformanceMonitor.java` fields:

```java
private String id;
private String monitorName;
private String realTimeMonitor;
private String runningStatus;
private String performanceParam;
private String potentialFault;
private String energyEfficiencyEval;
private Date monitorTime;
private String remark;
private String createBy;
private Date createTime;
private String updateBy;
private Date updateTime;
private String sysOrgCode;
private Integer delFlag;
```

- [ ] **Step 3: Create mapper interfaces**

For each entity, create a mapper. Example `MaintenanceRecordMapper.java`:

```java
package org.jeecg.modules.supply.mapper;

import com.baomidou.mybatisplus.core.mapper.BaseMapper;
import org.apache.ibatis.annotations.Mapper;
import org.jeecg.modules.supply.entity.MaintenanceRecord;

@Mapper
public interface MaintenanceRecordMapper extends BaseMapper<MaintenanceRecord> {
}
```

Repeat for `EquipmentArchiveMapper`, `MaintenancePlanMapper`, `RepairReportMapper`, `SparePartMapper`, and `PerformanceMonitorMapper`.

- [ ] **Step 4: Create mapper XML files**

Example `MaintenanceRecordMapper.xml`:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE mapper PUBLIC "-//mybatis.org//DTD Mapper 3.0//EN" "http://mybatis.org/dtd/mybatis-3-mapper.dtd">
<mapper namespace="org.jeecg.modules.supply.mapper.MaintenanceRecordMapper">
</mapper>
```

Repeat with the correct namespace for all six mapper XML files.

- [ ] **Step 5: Compile backend**

Run:

```bash
cd backend && mvn -q -DskipTests compile
```

Expected: compile succeeds.

- [ ] **Step 6: Commit entity and mapper layer**

```bash
git add backend/src/main/java/org/jeecg/modules/supply/entity backend/src/main/java/org/jeecg/modules/supply/mapper
git commit -m "feat: add supply room entity and mapper layer"
```

---

## Task 4: Implement Backend Service Layer

**Files:**
- Create: all files under `backend/src/main/java/org/jeecg/modules/supply/service/`
- Create: all files under `backend/src/main/java/org/jeecg/modules/supply/service/impl/`

- [ ] **Step 1: Create service interface**

Example `IMaintenanceRecordService.java`:

```java
package org.jeecg.modules.supply.service;

import com.baomidou.mybatisplus.extension.service.IService;
import org.jeecg.modules.supply.entity.MaintenanceRecord;

public interface IMaintenanceRecordService extends IService<MaintenanceRecord> {
}
```

Repeat for the other five entities.

- [ ] **Step 2: Create service implementation**

Example `MaintenanceRecordServiceImpl.java`:

```java
package org.jeecg.modules.supply.service.impl;

import com.baomidou.mybatisplus.extension.service.impl.ServiceImpl;
import org.jeecg.modules.supply.entity.MaintenanceRecord;
import org.jeecg.modules.supply.mapper.MaintenanceRecordMapper;
import org.jeecg.modules.supply.service.IMaintenanceRecordService;
import org.springframework.stereotype.Service;

@Service
public class MaintenanceRecordServiceImpl extends ServiceImpl<MaintenanceRecordMapper, MaintenanceRecord> implements IMaintenanceRecordService {
}
```

Repeat for `EquipmentArchiveServiceImpl`, `MaintenancePlanServiceImpl`, `RepairReportServiceImpl`, `SparePartServiceImpl`, and `PerformanceMonitorServiceImpl`.

- [ ] **Step 3: Compile backend**

Run:

```bash
cd backend && mvn -q -DskipTests compile
```

Expected: compile succeeds.

- [ ] **Step 4: Commit service layer**

```bash
git add backend/src/main/java/org/jeecg/modules/supply/service
git commit -m "feat: add supply room service layer"
```

---

## Task 5: Implement Backend Controllers

**Files:**
- Create: all files under `backend/src/main/java/org/jeecg/modules/supply/controller/`
- Test: all files under `backend/src/test/java/org/jeecg/modules/supply/`

- [ ] **Step 1: Write failing controller smoke test**

Create `backend/src/test/java/org/jeecg/modules/supply/MaintenanceRecordControllerTest.java`:

```java
package org.jeecg.modules.supply;

import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.AutoConfigureMockMvc;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.test.web.servlet.MockMvc;

import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.get;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

@SpringBootTest
@AutoConfigureMockMvc
class MaintenanceRecordControllerTest {
    @Autowired
    private MockMvc mockMvc;

    @Test
    void listEndpointExists() throws Exception {
        mockMvc.perform(get("/supply/maintenanceRecord/list").param("pageNo", "1").param("pageSize", "10"))
                .andExpect(status().isOk());
    }
}
```

- [ ] **Step 2: Run failing test**

Run:

```bash
cd backend && mvn -Dtest=MaintenanceRecordControllerTest test
```

Expected: FAIL because `/supply/maintenanceRecord/list` controller does not exist yet.

- [ ] **Step 3: Create `MaintenanceRecordController.java`**

```java
package org.jeecg.modules.supply.controller;

import com.baomidou.mybatisplus.core.conditions.query.QueryWrapper;
import com.baomidou.mybatisplus.core.metadata.IPage;
import com.baomidou.mybatisplus.extension.plugins.pagination.Page;
import java.util.Arrays;
import org.jeecg.common.api.vo.Result;
import org.jeecg.common.system.base.controller.JeecgController;
import org.jeecg.modules.supply.entity.MaintenanceRecord;
import org.jeecg.modules.supply.service.IMaintenanceRecordService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.DeleteMapping;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.PutMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/supply/maintenanceRecord")
public class MaintenanceRecordController extends JeecgController<MaintenanceRecord, IMaintenanceRecordService> {
    @Autowired
    private IMaintenanceRecordService maintenanceRecordService;

    @GetMapping("/list")
    public Result<IPage<MaintenanceRecord>> queryPageList(MaintenanceRecord maintenanceRecord,
                                                           @RequestParam(name = "pageNo", defaultValue = "1") Integer pageNo,
                                                           @RequestParam(name = "pageSize", defaultValue = "10") Integer pageSize) {
        QueryWrapper<MaintenanceRecord> queryWrapper = new QueryWrapper<>();
        queryWrapper.orderByDesc("create_time");
        Page<MaintenanceRecord> page = new Page<>(pageNo, pageSize);
        IPage<MaintenanceRecord> pageList = maintenanceRecordService.page(page, queryWrapper);
        return Result.OK(pageList);
    }

    @PostMapping("/add")
    public Result<String> add(@RequestBody MaintenanceRecord maintenanceRecord) {
        maintenanceRecordService.save(maintenanceRecord);
        return Result.OK("添加成功！");
    }

    @PutMapping("/edit")
    public Result<String> edit(@RequestBody MaintenanceRecord maintenanceRecord) {
        maintenanceRecordService.updateById(maintenanceRecord);
        return Result.OK("编辑成功!");
    }

    @DeleteMapping("/delete")
    public Result<String> delete(@RequestParam(name = "id") String id) {
        maintenanceRecordService.removeById(id);
        return Result.OK("删除成功!");
    }

    @DeleteMapping("/deleteBatch")
    public Result<String> deleteBatch(@RequestParam(name = "ids") String ids) {
        maintenanceRecordService.removeByIds(Arrays.asList(ids.split(",")));
        return Result.OK("批量删除成功!");
    }

    @GetMapping("/queryById")
    public Result<MaintenanceRecord> queryById(@RequestParam(name = "id") String id) {
        MaintenanceRecord maintenanceRecord = maintenanceRecordService.getById(id);
        return Result.OK(maintenanceRecord);
    }
}
```

- [ ] **Step 4: Run test again**

Run:

```bash
cd backend && mvn -Dtest=MaintenanceRecordControllerTest test
```

Expected: PASS.

- [ ] **Step 5: Create controllers for other five modules**

Create controllers using the same structure and these mappings:

```text
EquipmentArchiveController -> /supply/equipmentArchive -> IEquipmentArchiveService -> EquipmentArchive
MaintenancePlanController -> /supply/maintenancePlan -> IMaintenancePlanService -> MaintenancePlan
RepairReportController -> /supply/repairReport -> IRepairReportService -> RepairReport
SparePartController -> /supply/sparePart -> ISparePartService -> SparePart
PerformanceMonitorController -> /supply/performanceMonitor -> IPerformanceMonitorService -> PerformanceMonitor
```

Each controller must expose `/list`, `/add`, `/edit`, `/delete`, `/deleteBatch`, and `/queryById`.

- [ ] **Step 6: Add smoke tests for the other list endpoints**

Create tests equivalent to `MaintenanceRecordControllerTest` for:

```text
/supply/equipmentArchive/list
/supply/maintenancePlan/list
/supply/repairReport/list
/supply/sparePart/list
/supply/performanceMonitor/list
```

- [ ] **Step 7: Run controller tests**

Run:

```bash
cd backend && mvn -Dtest='*ControllerTest' test
```

Expected: all six controller tests pass.

- [ ] **Step 8: Commit controllers**

```bash
git add backend/src/main/java/org/jeecg/modules/supply/controller backend/src/test/java/org/jeecg/modules/supply
git commit -m "feat: add supply room CRUD controllers"
```

---

## Task 6: Add Excel Import and Export Endpoints

**Files:**
- Modify: all six controller files

- [ ] **Step 1: Add export and import methods to `MaintenanceRecordController.java`**

Add imports if using JeecgBoot utilities:

```java
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import org.springframework.web.multipart.MultipartFile;
```

Add methods:

```java
@GetMapping("/exportXls")
public void exportXls(HttpServletRequest request, HttpServletResponse response, MaintenanceRecord maintenanceRecord) {
    super.exportXls(request, response, maintenanceRecord, MaintenanceRecord.class, "设备维护管理");
}

@PostMapping("/importExcel")
public Result<?> importExcel(HttpServletRequest request, HttpServletResponse response) {
    return super.importExcel(request, response, MaintenanceRecord.class);
}
```

- [ ] **Step 2: Add export and import methods to other controllers**

Use these titles and classes:

```text
EquipmentArchive.class -> 设备档案管理
MaintenancePlan.class -> 维护计划制定
RepairReport.class -> 故障报修管理
SparePart.class -> 备品备件管理
PerformanceMonitor.class -> 设备性能监测
```

- [ ] **Step 3: Compile backend**

Run:

```bash
cd backend && mvn -q -DskipTests compile
```

Expected: compile succeeds.

- [ ] **Step 4: Commit import/export**

```bash
git add backend/src/main/java/org/jeecg/modules/supply/controller
git commit -m "feat: add supply room Excel import export endpoints"
```

---

## Task 7: Initialize Frontend API Modules

**Files:**
- Create: all files under `frontend/src/api/supply/`

- [ ] **Step 1: Create `maintenanceRecord.js`**

```javascript
import { getAction, postAction, putAction, deleteAction } from '@/api/manage'

const url = {
  list: '/supply/maintenanceRecord/list',
  add: '/supply/maintenanceRecord/add',
  edit: '/supply/maintenanceRecord/edit',
  delete: '/supply/maintenanceRecord/delete',
  deleteBatch: '/supply/maintenanceRecord/deleteBatch',
  queryById: '/supply/maintenanceRecord/queryById',
  exportXlsUrl: '/supply/maintenanceRecord/exportXls',
  importExcelUrl: '/supply/maintenanceRecord/importExcel'
}

export function listMaintenanceRecord(params) {
  return getAction(url.list, params)
}

export function addMaintenanceRecord(params) {
  return postAction(url.add, params)
}

export function editMaintenanceRecord(params) {
  return putAction(url.edit, params)
}

export function deleteMaintenanceRecord(params) {
  return deleteAction(url.delete, params)
}

export function deleteBatchMaintenanceRecord(params) {
  return deleteAction(url.deleteBatch, params)
}

export default url
```

- [ ] **Step 2: Create API files for other modules**

Create equivalent files with these names and prefixes:

```text
equipmentArchive.js -> /supply/equipmentArchive -> EquipmentArchive
maintenancePlan.js -> /supply/maintenancePlan -> MaintenancePlan
repairReport.js -> /supply/repairReport -> RepairReport
sparePart.js -> /supply/sparePart -> SparePart
performanceMonitor.js -> /supply/performanceMonitor -> PerformanceMonitor
```

Each file exports list/add/edit/delete/deleteBatch functions and default `url`.

- [ ] **Step 3: Run frontend lint or build**

Run:

```bash
cd frontend && npm run lint
```

Expected: lint succeeds. If the project has no lint script, run:

```bash
cd frontend && npm run build
```

Expected: build succeeds.

- [ ] **Step 4: Commit frontend API modules**

```bash
git add frontend/src/api/supply
git commit -m "feat: add supply room frontend API modules"
```

---

## Task 8: Implement Maintenance Record Frontend Page

**Files:**
- Create: `frontend/src/views/supply/maintenanceRecord/MaintenanceRecordList.vue`
- Create: `frontend/src/views/supply/maintenanceRecord/MaintenanceRecordForm.vue`
- Create: `frontend/src/views/supply/maintenanceRecord/MaintenanceRecordModal.vue`

- [ ] **Step 1: Create `MaintenanceRecordModal.vue`**

```vue
<template>
  <j-modal
    :title="title"
    :width="width"
    :visible="visible"
    switchFullscreen
    @ok="handleOk"
    @cancel="handleCancel"
    cancelText="关闭">
    <maintenance-record-form ref="realForm" @ok="submitCallback" :disabled="disableSubmit" />
  </j-modal>
</template>

<script>
import MaintenanceRecordForm from './MaintenanceRecordForm'

export default {
  name: 'MaintenanceRecordModal',
  components: { MaintenanceRecordForm },
  data() {
    return {
      title: '',
      width: 800,
      visible: false,
      disableSubmit: false
    }
  },
  methods: {
    add() {
      this.title = '新增设备维护管理'
      this.visible = true
      this.disableSubmit = false
      this.$nextTick(() => this.$refs.realForm.add())
    },
    edit(record) {
      this.title = '编辑设备维护管理'
      this.visible = true
      this.disableSubmit = false
      this.$nextTick(() => this.$refs.realForm.edit(record))
    },
    detail(record) {
      this.title = '设备维护管理详情'
      this.visible = true
      this.disableSubmit = true
      this.$nextTick(() => this.$refs.realForm.edit(record))
    },
    close() {
      this.$emit('close')
      this.visible = false
    },
    handleOk() {
      this.$refs.realForm.submitForm()
    },
    submitCallback() {
      this.$emit('ok')
      this.visible = false
    },
    handleCancel() {
      this.close()
    }
  }
}
</script>
```

- [ ] **Step 2: Create `MaintenanceRecordForm.vue`**

```vue
<template>
  <a-spin :spinning="confirmLoading">
    <j-form-container :disabled="formDisabled">
      <a-form-model ref="form" :model="model" :rules="validatorRules" slot="detail">
        <a-row>
          <a-col :span="24">
            <a-form-model-item label="维护类型" :labelCol="labelCol" :wrapperCol="wrapperCol" prop="maintenanceType">
              <a-input v-model="model.maintenanceType" placeholder="请输入维护类型" />
            </a-form-model-item>
          </a-col>
          <a-col :span="24">
            <a-form-model-item label="维护人员" :labelCol="labelCol" :wrapperCol="wrapperCol" prop="maintenancePerson">
              <a-input v-model="model.maintenancePerson" placeholder="请输入维护人员" />
            </a-form-model-item>
          </a-col>
          <a-col :span="24">
            <a-form-model-item label="维护日期" :labelCol="labelCol" :wrapperCol="wrapperCol" prop="maintenanceDate">
              <j-date v-model="model.maintenanceDate" :show-time="true" date-format="YYYY-MM-DD HH:mm:ss" placeholder="请选择维护日期" style="width: 100%" />
            </a-form-model-item>
          </a-col>
          <a-col :span="24">
            <a-form-model-item label="维护结果" :labelCol="labelCol" :wrapperCol="wrapperCol" prop="maintenanceResult">
              <a-input v-model="model.maintenanceResult" placeholder="请输入维护结果" />
            </a-form-model-item>
          </a-col>
          <a-col :span="24">
            <a-form-model-item label="设备位置" :labelCol="labelCol" :wrapperCol="wrapperCol" prop="equipmentLocation">
              <a-input v-model="model.equipmentLocation" placeholder="请输入设备位置" />
            </a-form-model-item>
          </a-col>
          <a-col :span="24">
            <a-form-model-item label="备注" :labelCol="labelCol" :wrapperCol="wrapperCol" prop="remark">
              <a-textarea v-model="model.remark" placeholder="请输入备注" :rows="3" />
            </a-form-model-item>
          </a-col>
        </a-row>
      </a-form-model>
    </j-form-container>
  </a-spin>
</template>

<script>
import { httpAction } from '@/api/manage'
import url from '@/api/supply/maintenanceRecord'

export default {
  name: 'MaintenanceRecordForm',
  props: {
    disabled: {
      type: Boolean,
      default: false
    }
  },
  data() {
    return {
      model: {},
      labelCol: { xs: { span: 24 }, sm: { span: 5 } },
      wrapperCol: { xs: { span: 24 }, sm: { span: 16 } },
      confirmLoading: false,
      validatorRules: {
        maintenanceType: [{ required: true, message: '请输入维护类型!' }],
        maintenancePerson: [{ required: true, message: '请输入维护人员!' }],
        maintenanceDate: [{ required: true, message: '请选择维护日期!' }]
      },
      url
    }
  },
  computed: {
    formDisabled() {
      return this.disabled
    }
  },
  created() {
    this.modelDefault = JSON.parse(JSON.stringify(this.model))
  },
  methods: {
    add() {
      this.edit(this.modelDefault)
    },
    edit(record) {
      this.model = Object.assign({}, record)
    },
    submitForm() {
      this.$refs.form.validate(valid => {
        if (!valid) return
        this.confirmLoading = true
        const httpurl = this.model.id ? this.url.edit : this.url.add
        const method = this.model.id ? 'put' : 'post'
        httpAction(httpurl, this.model, method).then(res => {
          if (res.success) {
            this.$message.success(res.message)
            this.$emit('ok')
          } else {
            this.$message.warning(res.message)
          }
        }).finally(() => {
          this.confirmLoading = false
        })
      })
    }
  }
}
</script>
```

- [ ] **Step 3: Create `MaintenanceRecordList.vue`**

```vue
<template>
  <a-card :bordered="false">
    <div class="table-page-search-wrapper">
      <a-form layout="inline" @keyup.enter.native="searchQuery">
        <a-row :gutter="24">
          <a-col :xl="6" :lg="7" :md="8" :sm="24">
            <a-form-item label="维护类型">
              <a-input v-model="queryParam.maintenanceType" placeholder="请输入维护类型" />
            </a-form-item>
          </a-col>
          <a-col :xl="6" :lg="7" :md="8" :sm="24">
            <a-form-item label="维护人员">
              <a-input v-model="queryParam.maintenancePerson" placeholder="请输入维护人员" />
            </a-form-item>
          </a-col>
          <a-col :xl="6" :lg="7" :md="8" :sm="24">
            <a-form-item label="设备位置">
              <a-input v-model="queryParam.equipmentLocation" placeholder="请输入设备位置" />
            </a-form-item>
          </a-col>
          <a-col :xl="6" :lg="7" :md="8" :sm="24">
            <span class="table-page-search-submitButtons">
              <a-button type="primary" @click="searchQuery" icon="search">查询</a-button>
              <a-button type="primary" @click="searchReset" icon="reload" style="margin-left: 8px">重置</a-button>
            </span>
          </a-col>
        </a-row>
      </a-form>
    </div>

    <div class="table-operator">
      <a-button @click="handleAdd" type="primary" icon="plus">新增</a-button>
      <a-button type="primary" icon="download" @click="handleExportXls('设备维护管理')">导出</a-button>
      <a-upload name="file" :showUploadList="false" :multiple="false" :headers="tokenHeader" :action="importExcelUrl" @change="handleImportExcel">
        <a-button type="primary" icon="import">导入</a-button>
      </a-upload>
      <a-button type="danger" icon="delete" @click="batchDel" v-if="selectedRowKeys.length > 0">批量删除</a-button>
    </div>

    <a-table
      ref="table"
      size="middle"
      bordered
      rowKey="id"
      :columns="columns"
      :dataSource="dataSource"
      :pagination="ipagination"
      :loading="loading"
      :rowSelection="{ selectedRowKeys: selectedRowKeys, onChange: onSelectChange }"
      @change="handleTableChange">
      <span slot="action" slot-scope="text, record">
        <a @click="handleEdit(record)">编辑</a>
        <a-divider type="vertical" />
        <a-dropdown>
          <a class="ant-dropdown-link">更多 <a-icon type="down" /></a>
          <a-menu slot="overlay">
            <a-menu-item><a @click="handleDetail(record)">详情</a></a-menu-item>
            <a-menu-item><a-popconfirm title="确定删除吗?" @confirm="() => handleDelete(record.id)"><a>删除</a></a-popconfirm></a-menu-item>
          </a-menu>
        </a-dropdown>
      </span>
    </a-table>

    <maintenance-record-modal ref="modalForm" @ok="modalFormOk" />
  </a-card>
</template>

<script>
import { JeecgListMixin } from '@/mixins/JeecgListMixin'
import MaintenanceRecordModal from './MaintenanceRecordModal'
import url from '@/api/supply/maintenanceRecord'

export default {
  name: 'MaintenanceRecordList',
  mixins: [JeecgListMixin],
  components: { MaintenanceRecordModal },
  data() {
    return {
      description: '设备维护管理页面',
      url,
      columns: [
        { title: '#', dataIndex: '', key: 'rowIndex', width: 60, align: 'center', customRender: (t, r, index) => parseInt(index) + 1 },
        { title: '维护类型', align: 'center', dataIndex: 'maintenanceType' },
        { title: '维护人员', align: 'center', dataIndex: 'maintenancePerson' },
        { title: '维护日期', align: 'center', dataIndex: 'maintenanceDate' },
        { title: '维护结果', align: 'center', dataIndex: 'maintenanceResult' },
        { title: '设备位置', align: 'center', dataIndex: 'equipmentLocation' },
        { title: '操作', dataIndex: 'action', align: 'center', scopedSlots: { customRender: 'action' } }
      ]
    }
  },
  computed: {
    importExcelUrl() {
      return `${window._CONFIG['domianURL']}${this.url.importExcelUrl}`
    }
  }
}
</script>
```

- [ ] **Step 4: Build frontend**

Run:

```bash
cd frontend && npm run build
```

Expected: build succeeds.

- [ ] **Step 5: Commit maintenance record page**

```bash
git add frontend/src/views/supply/maintenanceRecord
git commit -m "feat: add maintenance record frontend page"
```

---

## Task 9: Implement Remaining Frontend CRUD Pages

**Files:**
- Create all remaining module page files under `frontend/src/views/supply/`

- [ ] **Step 1: Create EquipmentArchive page set**

Create `EquipmentArchiveList.vue`, `EquipmentArchiveForm.vue`, and `EquipmentArchiveModal.vue` using the Task 8 structure with these fields:

```text
equipmentName -> 设备名称 -> required
equipmentCode -> 设备编号 -> required
equipmentQrCode -> 设备二维码
equipmentImage -> 设备图片
electronicDocument -> 设备电子资料
equipmentTemplate -> 设备模板
equipmentLocation -> 设备位置
runningStatus -> 运行状态
remark -> 备注
```

The list columns are:

```javascript
[
  { title: '设备名称', align: 'center', dataIndex: 'equipmentName' },
  { title: '设备编号', align: 'center', dataIndex: 'equipmentCode' },
  { title: '设备二维码', align: 'center', dataIndex: 'equipmentQrCode' },
  { title: '设备位置', align: 'center', dataIndex: 'equipmentLocation' },
  { title: '运行状态', align: 'center', dataIndex: 'runningStatus' }
]
```

Use API module `@/api/supply/equipmentArchive` and component names `EquipmentArchiveList`, `EquipmentArchiveForm`, `EquipmentArchiveModal`.

- [ ] **Step 2: Create MaintenancePlan page set**

Fields:

```text
planName -> 计划名称 -> required
regularMaintenance -> 定期维护
urgentMaintenance -> 紧急维护
preventiveMaintenance -> 预防性维护
planDate -> 制定日期 -> required
principal -> 负责人 -> required
planStatus -> 计划状态
remark -> 备注
```

List columns:

```javascript
[
  { title: '计划名称', align: 'center', dataIndex: 'planName' },
  { title: '定期维护', align: 'center', dataIndex: 'regularMaintenance' },
  { title: '紧急维护', align: 'center', dataIndex: 'urgentMaintenance' },
  { title: '预防性维护', align: 'center', dataIndex: 'preventiveMaintenance' },
  { title: '制定日期', align: 'center', dataIndex: 'planDate' },
  { title: '负责人', align: 'center', dataIndex: 'principal' },
  { title: '计划状态', align: 'center', dataIndex: 'planStatus' }
]
```

- [ ] **Step 3: Create RepairReport page set**

Fields:

```text
repairNo -> 报修编号 -> required
repairPerson -> 报修人 -> required
repairDate -> 报修日期 -> required
faultDescription -> 故障描述 -> required
processStatus -> 处理状态
 equipmentLocation -> 设备位置
handler -> 处理人
processResult -> 处理结果
remark -> 备注
```

List columns:

```javascript
[
  { title: '报修编号', align: 'center', dataIndex: 'repairNo' },
  { title: '报修人', align: 'center', dataIndex: 'repairPerson' },
  { title: '报修日期', align: 'center', dataIndex: 'repairDate' },
  { title: '故障描述', align: 'center', dataIndex: 'faultDescription' },
  { title: '处理状态', align: 'center', dataIndex: 'processStatus' },
  { title: '处理人', align: 'center', dataIndex: 'handler' }
]
```

- [ ] **Step 4: Create SparePart page set**

Fields:

```text
partName -> 备件名称 -> required
partCode -> 备件编号 -> required
stockQuantity -> 库存数量 -> required number
minimumStock -> 最低库存 -> required number
purchaseDate -> 采购日期
purchaseCycle -> 采购周期
supplier -> 供应商
remark -> 备注
```

List columns:

```javascript
[
  { title: '备件名称', align: 'center', dataIndex: 'partName' },
  { title: '备件编号', align: 'center', dataIndex: 'partCode' },
  { title: '库存数量', align: 'center', dataIndex: 'stockQuantity' },
  { title: '最低库存', align: 'center', dataIndex: 'minimumStock' },
  { title: '采购日期', align: 'center', dataIndex: 'purchaseDate' },
  { title: '采购周期', align: 'center', dataIndex: 'purchaseCycle' }
]
```

- [ ] **Step 5: Create PerformanceMonitor page set**

Fields:

```text
monitorName -> 监测名称 -> required
realTimeMonitor -> 实时监测
runningStatus -> 运行状态 -> required
performanceParam -> 性能参数
potentialFault -> 潜在故障
energyEfficiencyEval -> 评估设备能效
monitorTime -> 监测时间
remark -> 备注
```

List columns:

```javascript
[
  { title: '监测名称', align: 'center', dataIndex: 'monitorName' },
  { title: '实时监测', align: 'center', dataIndex: 'realTimeMonitor' },
  { title: '运行状态', align: 'center', dataIndex: 'runningStatus' },
  { title: '性能参数', align: 'center', dataIndex: 'performanceParam' },
  { title: '潜在故障', align: 'center', dataIndex: 'potentialFault' },
  { title: '评估设备能效', align: 'center', dataIndex: 'energyEfficiencyEval' },
  { title: '监测时间', align: 'center', dataIndex: 'monitorTime' }
]
```

- [ ] **Step 6: Build frontend**

Run:

```bash
cd frontend && npm run build
```

Expected: build succeeds.

- [ ] **Step 7: Commit remaining pages**

```bash
git add frontend/src/views/supply
git commit -m "feat: add supply room frontend CRUD pages"
```

---

## Task 10: Configure Menus, Dictionaries, and Permissions

**Files:**
- Create: `backend/src/main/resources/db/migration/V2__init_supply_room_dicts_and_menus.sql`

- [ ] **Step 1: Create dictionary initialization SQL**

Create `V2__init_supply_room_dicts_and_menus.sql` with dictionary values. If using JeecgBoot dictionary tables, adapt table names to the project. Required dictionaries:

```sql
-- 运行状态: normal=正常, abnormal=异常, disabled=停用, repairing=维修中
-- 处理状态: pending=待处理, processing=处理中, completed=已完成, closed=已关闭
-- 计划状态: not_started=未开始, running=执行中, completed=已完成, cancelled=已取消
-- 维护类型: regular=定期维护, urgent=紧急维护, preventive=预防性维护, other=其他
```

- [ ] **Step 2: Create menu initialization SQL**

Add menus for:

```text
供应室设备维护管理
  设备维护管理 -> /supply/maintenanceRecord/MaintenanceRecordList
  设备档案管理 -> /supply/equipmentArchive/EquipmentArchiveList
  维护计划制定 -> /supply/maintenancePlan/MaintenancePlanList
  故障报修管理 -> /supply/repairReport/RepairReportList
  备品备件管理 -> /supply/sparePart/SparePartList
  设备性能监测 -> /supply/performanceMonitor/PerformanceMonitorList
```

Button permissions for each module:

```text
add, edit, delete, deleteBatch, importExcel, exportXls, queryById
```

- [ ] **Step 3: Apply SQL in local database**

Run:

```bash
mysql -uroot -proot supply_room < backend/src/main/resources/db/migration/V2__init_supply_room_dicts_and_menus.sql
```

Expected: SQL runs without errors.

- [ ] **Step 4: Verify menu access in browser**

Start backend and frontend, log in as admin, and confirm left menu shows all six modules.

- [ ] **Step 5: Commit dictionaries and menus**

```bash
git add backend/src/main/resources/db/migration/V2__init_supply_room_dicts_and_menus.sql
git commit -m "feat: initialize supply room menus and dictionaries"
```

---

## Task 11: End-to-End Manual Verification

**Files:**
- No source changes required unless defects are found.

- [ ] **Step 1: Start backend**

Run:

```bash
cd backend && mvn spring-boot:run
```

Expected: backend starts on port `8080`.

- [ ] **Step 2: Start frontend**

Run:

```bash
cd frontend && npm run serve
```

Expected: frontend dev server starts and displays a local URL.

- [ ] **Step 3: Verify login and menu**

Open the frontend URL in Chrome or Edge. Log in as admin. Confirm the menu contains:

```text
设备维护管理
设备档案管理
维护计划制定
故障报修管理
备品备件管理
设备性能监测
```

- [ ] **Step 4: Verify each module's golden path**

For each of the six modules:

```text
Open list page
Click 新增
Fill required fields
Click 确定
Confirm success message
Search by one field
Click 编辑
Change one field
Click 确定
Click 详情
Click 删除
Confirm record disappears
```

- [ ] **Step 5: Verify import/export**

For each module:

```text
Click 导出
Confirm Excel downloads
Use exported Excel as template
Add one row
Click 导入
Confirm row appears in list
```

- [ ] **Step 6: Verify permissions**

Log in with a non-admin role and confirm restricted modules or buttons are hidden according to assigned permissions.

- [ ] **Step 7: Commit fixes if needed**

If manual testing required fixes:

```bash
git add backend frontend
git commit -m "fix: resolve supply room verification issues"
```

---

## Task 12: Deployment Configuration

**Files:**
- Create: `deploy/nginx/supply-room.conf`
- Create: `deploy/systemd/supply-room-backend.service`

- [ ] **Step 1: Create Nginx config**

Create `deploy/nginx/supply-room.conf`:

```nginx
server {
    listen 80;
    server_name supply-room.local;

    root /opt/supply-room/frontend/dist;
    index index.html;

    location / {
        try_files $uri $uri/ /index.html;
    }

    location /jeecg-boot/ {
        proxy_pass http://127.0.0.1:8080/jeecg-boot/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }

    location /supply/ {
        proxy_pass http://127.0.0.1:8080/supply/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }
}
```

- [ ] **Step 2: Create systemd service**

Create `deploy/systemd/supply-room-backend.service`:

```ini
[Unit]
Description=Supply Room Backend Service
After=network.target mysql.service

[Service]
Type=simple
User=www-data
WorkingDirectory=/opt/supply-room/backend
ExecStart=/usr/bin/java -jar /opt/supply-room/backend/supply-room-backend.jar
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
```

- [ ] **Step 3: Build backend jar**

Run:

```bash
cd backend && mvn clean package -DskipTests
```

Expected: jar is generated under `backend/target/`.

- [ ] **Step 4: Build frontend dist**

Run:

```bash
cd frontend && npm run build
```

Expected: `frontend/dist/` is generated.

- [ ] **Step 5: Commit deployment files**

```bash
git add deploy
git commit -m "chore: add supply room deployment configuration"
```

---

## Task 13: Final Quality Gates

**Files:**
- Review all files changed in previous tasks.

- [ ] **Step 1: Run backend tests**

```bash
cd backend && mvn test
```

Expected: all tests pass.

- [ ] **Step 2: Run backend package**

```bash
cd backend && mvn clean package
```

Expected: package succeeds.

- [ ] **Step 3: Run frontend build**

```bash
cd frontend && npm run build
```

Expected: build succeeds.

- [ ] **Step 4: Review git diff**

```bash
git status --short
git diff --stat
```

Expected: only intended files are modified or untracked.

- [ ] **Step 5: Commit final verification fixes if any**

```bash
git add backend frontend deploy
git commit -m "fix: finalize supply room system verification"
```

Skip this commit if there are no changes after verification.

---

## Self-Review

- Spec coverage: login, permissions, homepage/menu, six CRUD modules, Excel import/export, file upload placeholders through Jeecg file fields, testing, and deployment are covered.
- Scope: this is a large but single coherent admin system; tasks are split by database, backend layers, frontend APIs/pages, menu permissions, verification, and deployment.
- No unresolved `TBD` or `TODO` placeholders are intentionally left in the execution steps.
- Naming consistency: database columns use snake_case, Java/Vue fields use camelCase, and API prefixes match the design document.

## Execution Options

Plan complete and saved to `docs/superpowers/plans/2026-05-11-supply-room-maintenance-implementation.md`.

Two execution options:

1. **Subagent-Driven (recommended)** - Dispatch a fresh subagent per task, review between tasks, fast iteration.
2. **Inline Execution** - Execute tasks in this session using executing-plans, batch execution with checkpoints.

Which approach?
